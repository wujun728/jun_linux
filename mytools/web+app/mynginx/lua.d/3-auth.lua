--if ngx.var.arg_user == "foo" then
--    return
--else
--    Ngx.exit(ngx.HTTP_FORBIDDEN)
--end

--[[
    认证通过之后分配的ctoken与使用者的IP 关联；
    渠道和个人用户都可以使用；
--]]


--支撑head或者cookie 获取参数;
--java 对渠道参数配置进行管理，并且将数据同步到redis


ip_bind_time = 300 --封禁IP时间,300秒
ip_time_out = 60 --指定ip访问频率时间段,60秒
connect_count = 100 --指定ip访问频率计数最大值,100次/分钟


--验证渠道与ip 地址是否一致
local myIp = ngx.req.get_headers()["X-Real-IP"]
if isempty(myIp) then
    myIp = ngx.req.get_headers()["x_forwarded_for"]
end
if isempty(myIp) then
    myIp = ngx.var.remote_addr
end

if isempty(myIp) then
    ngx.log(ngx.DEBUG, "没有获取到ip 地址")

    returnjson(-2, "没有获取到ip地址")
    ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);
end

myIp = string.sub(myIp, string.find(myIp, "%d+%.%d+%.%d+"))


--如果已经动态分配ctoken,token 与IP 地址绑定；验证token 的有效性；则不进行认证,直接进行能力管控
local ctoken = ngx.req.get_headers()["ctoken"]
if isempty(ctoken) then
    ctoken = ngx.var.cookie_ctoken
end


local channel_code = ngx.req.get_headers()["ChannelCode"]
if isempty(channel_code) then
    channel_code = ngx.var.cookie_ChannelCode
end
if isempty(channel_code) then
    ngx.log(ngx.DEBUG, "传递的参数不全，或者名称不对")
    returnjson(-4, "请仔细检查传递的参数")
    ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);
end


--参数通过上下文传递到后面的程序使用
ngx.ctx.ctoken = ctoken;
ngx.ctx.myip = myIp;
ngx.ctx.channel_code = channel_code;

--进行认证
if isempty(ctoken) then


    local myconfig = ngx.shared.myconfig
    local redis_host = myconfig:get("redis-host")
    local redis_port = myconfig:get("redis-port")

    ngx.log(ngx.DEBUG, ">>>redis链接," .. redis_host .. ":" .. redis_port)
    local cache1 = redis.new()
    cache1:set_timeout(1000) --1分钟
    local ok, err = cache1:connect(redis_host, redis_port)


    --如果连接失败，跳转到脚本结尾
    if not ok then
        ngx.log(ngx.DEBUG, ">>>redis链接失败")
        ngx.say(">>>redis链接失败")

        close_redis(cache1)
        ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE)
    end


    channel_secretkey = ngx.req.get_headers()["ChannelSecretkey"]
    if isempty(channel_secretkey) then
        channel_secretkey = ngx.var.cookie_ChannelSecretkey
    end

    if isempty(channel_secretkey) then

        ngx.log(ngx.DEBUG, "传递的参数不全，或者名称不对")
        returnjson(-4, "请仔细检查传递的参数")

        close_redis(cache1)
        ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);
    end


    --- telnet 192.168.99.101 6379/monitor/keys */set 1234ip_bind_time 300/set 1234ip_time_out 60 /set 1234connect_count 100
    --- set 1234pwd 111111/set 1234iplist 192.168.59.3/set 1234token_expire 1/
    -- 设置渠道的封禁时间，访问频率和统计时间段
    -- 注意数字和字符串类型
    if not isempty(channel_code) then
        --渠道带宽控制


        cache1:init_pipeline()

        cache1:hget("hash_" .. channel_code, "ip_bind_time")
        cache1:hget("hash_" .. channel_code, "ip_time_out")
        cache1:hget("hash_" .. channel_code, "connect_count")

        cache1:hget("hash_" .. channel_code, "pwd") --秘钥盐渍
        cache1:hget("hash_" .. channel_code, "iplist") --渠道ip 地址
        cache1:hget("hash_" .. channel_code, "token_expire") --渠道有效期

        local respTable, err = cache1:commit_pipeline()

        --得到的数据为空处理
        if respTable == ngx.null then
            respTable = {} --比如默认值

            returnjson(-99, "请仔细检查配置文件")

            ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);
        end


        ----------------------------------------------------------
        -- 调用获取数据接口；
        -- 获取渠道的代理接口地址save_url与key;
        ----------------------------------------------------------


        if isempty(respTable[1]) or isempty(respTable[2]) or isempty(respTable[3])
                or isempty(respTable[4]) or isempty(respTable[5]) or isempty(respTable[6]) then

            ngx.log(ngx.DEBUG, "渠道号没有生效")
            returnjson(-6, "渠道号没有生效")

            ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);

        end

        local channel_ip_bind_time = respTable[1]
        local channel_ip_time_out = respTable[2]
        local channel_connect_count = respTable[3]

        local channel_pwd = respTable[4]
        local channel_iplist = respTable[5]
        local channel_token_expire = respTable[6]

        ip_bind_time = channel_ip_bind_time
        ip_time_out = channel_ip_time_out
        connect_count = channel_connect_count


        _, q = string.find(channel_iplist, myIp)
        if isempty(q) then

            ngx.log(ngx.DEBUG, "实际ip地址与渠道设置的ip地址不匹配")

            returnjson(-7, "实际ip地址与渠道设置的ip地址不匹配")

            ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);
        end

        --验证秘钥 是否有效
        local server_secretkey = ngx.md5(channel_code .. myIp .. channel_pwd)
        ngx.log(ngx.DEBUG, "server秘钥" .. server_secretkey)

        if channel_secretkey ~= server_secretkey then

            ngx.log(ngx.DEBUG, "秘钥不匹配")

            returnjson(-8, "秘钥不匹配")

            ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);
        end

        --1天的秒数
        local daysec = 60 * 60 * 24

        --给渠道返回一个token,有效期
        --    local ctoken = ngx.md5( channel_code .. myIp .. channel_pwd .. os.time())
        local ctoken = ngx.md5(channel_code .. myIp .. server_secretkey)
        res, err = cache1:set(channel_code .. ctoken, myIp)

        --设置生存时间 天数转换为秒
        res, err = cache1:expire(channel_code .. ctoken, channel_token_expire * daysec)

        ngx.log(ngx.DEBUG, "新的令牌" .. ctoken .. "，有效期：" .. channel_token_expire * daysec)

        --tokenvalue = "{status:200,desc:"ok",ctoken:"..ctoken..",expire:" .. channel_token_expire*daysec .. "}"

        --ngx.say(tokenvalue);
        close_redis(cache1)



        local data = {}
        data.desc = "ok";
        data.status = 200;
        data.ctoken = ctoken;
        data.expire = channel_token_expire * daysec;
        --data.attachment={}

        local jsonvalue = cjson.encode(data);
        ngx.say(jsonvalue);
        ngx.exit(ngx.HTTP_OK);
    end

    close_redis(cache1)
end
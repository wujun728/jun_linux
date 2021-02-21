--[[
    认证通过之后分配的ctoken与使用者的IP 关联；
    渠道和个人用户都可以使用；
--]]


local common = require "common"


--支撑head或者cookie 获取参数;
--java 对渠道参数配置进行管理，并且将数据同步到redis

--环境初始化
--默认全局封禁时间，每秒访问次数，统计时间段；从redis 取渠道设置的阀值

ip_bind_time = 300 --封禁IP时间,300秒
ip_time_out = 60 --指定ip访问频率时间段,60秒
connect_count = 100 --指定ip访问频率计数最大值,100次/分钟


local cache = common.getConfigRedisCache()


local myIp = common.getIp()
if common.isempty(myIp) then

    ngx.log(ngx.DEBUG, "没有获取到ip 地址")

    common.returnjson(-2, "没有获取到ip地址")
    ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);

    return common.close_redis(cache)
end




--:::::::::::::::::::::begin
--所有的操作都进行并发控制；
--查询ip是否在封禁段内，若在则返回403错误代码
--因封禁时间会大于ip记录时间，故此处不对ip时间key和计数key做处理
is_bind, err = cache:get("bind_" .. ngx.var.remote_addr)
if is_bind == '1' then
    ngx.log(ngx.DEBUG, ">>>redis封禁......")
    common.returnjson(-3, "ip地址已经被封禁")
    ngx.exit(403)
    return common.close_redis(cache)
end


--封杀计数
start_time, err = cache:get("time_" .. ngx.var.remote_addr)
ip_count, err = cache:get("count_" .. ngx.var.remote_addr)

--如果ip记录时间大于指定时间间隔或者记录时间或者不存在ip时间key则重置时间key和计数key
--如果ip时间key小于时间间隔，则ip计数+1，且如果ip计数大于ip频率计数，则设置ip的封禁key为1
--同时设置封禁key的过期时间为封禁ip的时间

if start_time == ngx.null or os.time() - start_time > ip_time_out then

    ngx.log(ngx.DEBUG, ">>>设置初始值" .. ngx.var.remote_addr)

    res, err = cache:set("time_" .. ngx.var.remote_addr, os.time())
    res, err = cache:set("count_" .. ngx.var.remote_addr, 1)
else

    ip_count = ip_count + 1

    ngx.log(ngx.DEBUG, ">>>计数" .. ip_count)

    res, err = cache:incr("count_" .. ngx.var.remote_addr)

    if ip_count >= connect_count then

        ngx.log(ngx.DEBUG, ">>>设置为封禁" .. ngx.var.remote_addr)

        res, err = cache:set("bind_" .. ngx.var.remote_addr, 1)
        --设置生存时间 300 秒
        res, err = cache:expire("bind_" .. ngx.var.remote_addr, ip_bind_time)
    end
end
--:::::::::::::::::::::end







--设置ctoken 数据
--redis-cli 192.168.99.101 6379/monitor/keys */set testf97a93b6e5e08843a7c825a53bdae246 192.168.59.3/get aa6f21ec0fcf008aa5250904985a817b
--curl -v -b "ChannelCode=test;ctoken=testf97a93b6e5e08843a7c825a53bdae246" http://192.168.99.101/api?key=one
--curl -v -b "ChannelCode=test;ctoken=testf97a93b6e5e08843a7c825a53bdae246" http://127.0.0.1:8888/api?key=one

--curl -v -b "ChannelCode=test;ctoken=testf97a93b6e5e08843a7c825a53bdae246" http://192.168.99.101/api?key=one&type=hash
--ab -n 5000 -c 200  -C ctoken=testf97a93b6e5e08843a7c825a53bdae246 http://192.168.99.101/api
--如果已经动态分配ctoken,token 与IP 地址绑定；验证token 的有效性；则不进行认证,直接进行能力管控
ctoken = common.getHeadCookie("ctoken")

--验证ctoken 在有效期内，跳过认证流程;不在有效期，继续认证流程；
if not common.isempty(ctoken) then
    ctokenok, err = cache:get(ctoken)

    ngx.log(ngx.DEBUG, myIp)

    if ctokenok == myIp then

        ngx.log(ngx.DEBUG, ">>>ctoken 有效，不再进行渠道认证......")

        ----------------------------------------------------------
        -- 调用获取数据接口；
        -- 获取渠道的代理接口地址save_url与key;
        ----------------------------------------------------------
        local channelCode1 = common.getHeadCookie("ChannelCode")
        ngx.log(ngx.DEBUG, ">>>channel_code:" .. channelCode1)

        local channelSaveHost, err1 = cache:hget("hash_" .. channelCode1, "save_host")
        local channelSavePort, err2 = cache:hget("hash_" .. channelCode1, "save_port")


        if common.isempty(channelSaveHost) or common.isempty(channelSavePort) or common.isempty(channelCode1) then

            ngx.log(ngx.DEBUG, "传递的参数不全channel_code，或者host or port不对")

            common.returnjson(-4, "请仔细检查传递的参数")
            ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);
            return common.close_redis(cache)
        end

        local channelCache = common.getRedisCache(channelSaveHost,channelSavePort)

        --如果连接失败，跳转到脚本结尾
        if not ok then
            ngx.log(ngx.DEBUG, ">>>redis链接失败")

            common.close_redis(channelCache)
            common.close_redis(cache)
            return
        end

        --hgetall 获得所有字段的数据
        local getkey = ngx.var.arg_key
        --local getkey = ngx.req.get_uri_args["key"]

        ngx.log(ngx.DEBUG, getkey .. "数据......")

        local result, err3 = channelCache:hgetall(getkey);

        if common.isempty(result) then

            ngx.log(ngx.DEBUG, key + "数据为空......" .. getkey)

            common.returnjson(-1, "失败原因，数据为空，请仔细检查传递的key" .. getkey)
            ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);

            common.close_redis(channelCache)
            common.close_redis(cache)
            return
        end

        ngx.log(ngx.DEBUG, "数据......" .. result)

        --redis hash 转换为标准map格式，用于转换json
        local result2 = {};
        for i = 1, #result / 2 do
            result2[result[i * 2 - 1]] = result[i * 2]
        end

        --转换为json格式输出
        common.returnjson(200, "ok", result2)
        ngx.exit(ngx.HTTP_OK);

        common.close_redis(channelCache)
        common.close_redis(cache)
        return

    else

        common.returnjson(-5, "无效的令牌")
        ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);
    end
end





--进行认证

--获取从head 或者cookie 中渠道编码code/渠道秘钥-动态生成  ab -C 会更改cookie 的名称
--curl -v -b "ChannelCode=test;ChannelSecretkey=a8152b13f4ef9daca84cf981eb5a7907"  http://192.168.99.101/api
--mysql2redis.sh 同步数据
--ab -n 5000 -c 200 -H "Cookie:ChannelCode=test;ChannelSecretkey=a8152b13f4ef9daca84cf981eb5a7907"   http://192.168.99.101/api
channel_code = common.getHeadCookie("ChannelCode")
channel_secretkey = common.getHeadCookie("ChannelSecretkey")
if common.isempty(channel_code) or common.isempty(channel_secretkey) then

    ngx.log(ngx.DEBUG, "传递的参数不全，或者名称不对")
    --ngx.header.content_type = "application/json; charset=UTF-8";
    common.returnjson(-4, "请仔细检查传递的参数")
    ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);
    return common.close_redis(cache)
end


--- telnet 192.168.99.101 6379/monitor/keys */set 1234ip_bind_time 300/set 1234ip_time_out 60 /set 1234connect_count 100
--- set 1234pwd 111111/set 1234iplist 192.168.59.3/set 1234token_expire 1/
-- 设置渠道的封禁时间，访问频率和统计时间段
-- 注意数字和字符串类型
if not common.isempty(channel_code) then
    --渠道带宽控制

    local channel_ip_bind_time, err = cache:hget("hash_" .. channel_code, "ip_bind_time")
    local channel_ip_time_out, err = cache:hget("hash_" .. channel_code, "ip_time_out")
    local channel_connect_count, err = cache:hget("hash_" .. channel_code, "connect_count")

    local channel_pwd, err = cache:hget("hash_" .. channel_code, "pwd") --秘钥盐渍
    local channel_iplist, err = cache:hget("hash_" .. channel_code, "iplist") --渠道ip 地址
    local channel_token, err = cache:hget("hash_" .. channel_code, "token") --渠道令牌
    local channel_token_expire, err = cache:hget("hash_" .. channel_code, "token_expire") --渠道有效期


    ngx.log(ngx.DEBUG, channel_connect_count)

    if common.isempty(channel_ip_bind_time) or common.isempty(channel_ip_time_out) or common.isempty(channel_connect_count)
            or common.isempty(channel_pwd) or common.isempty(channel_iplist) or common.isempty(channel_token) or common.isempty(channel_token_expire) then

        ngx.log(ngx.DEBUG, "渠道号没有生效")

        common.returnjson(-6, "渠道号没有生效")
        ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);

    else
        ip_bind_time = channel_ip_bind_time
        ip_time_out = channel_ip_time_out
        connect_count = channel_connect_count
    end

    _, q = string.find(channel_iplist, myIp)
    if common.isempty(q) then

        ngx.log(ngx.DEBUG, "实际ip地址与渠道设置的ip地址不匹配")

        common.returnjson(-7, "实际ip地址与渠道设置的ip地址不匹配")
        ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);
        return common.close_redis(cache)
    end

    --验证秘钥 是否有效
    local server_secretkey = ngx.md5(channel_code .. myIp .. channel_pwd)
    ngx.log(ngx.DEBUG, "server秘钥" .. server_secretkey)

    if channel_secretkey ~= server_secretkey then

        ngx.log(ngx.DEBUG, "秘钥不匹配")

        common.returnjson(-8, "秘钥不匹配")
        ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);
        return common.close_redis(cache)
    end



    --1天的秒数
    local daysec = 60 * 60 * 24

    --给渠道返回一个token,有效期
    --    local ctoken = ngx.md5( channel_code .. myIp .. channel_pwd .. os.time())
    local ctoken = ngx.md5(channel_code .. myIp .. server_secretkey)
    res, err = cache:set(channel_code .. ctoken, myIp)

    --设置生存时间 天数转换为秒
    res, err = cache:expire(channel_code .. ctoken, channel_token_expire * daysec)

    ngx.log(ngx.DEBUG, "新的令牌" .. ctoken .. "，有效期：" .. channel_token_expire * daysec)

    local cjson = require "cjson"
    local data = {}
    data.desc = "ok";
    data.status = 200;
    data.ctoken = ctoken;
    data.expire = channel_token_expire * daysec;
    --data.attachment={}

    local jsonvalue = cjson.encode(data);
    ngx.say(jsonvalue);

    ngx.exit(ngx.HTTP_OK);

    return common.close_redis(cache)
end

common.close_redis(channelCache)
return common.close_redis(cache)
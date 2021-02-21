--[[
    认证通过之后分配的ctoken与使用者的IP 关联；
    渠道和个人用户都可以使用；
--]]

--支撑head或者cookie 获取参数;
--java 对渠道参数配置进行管理，并且将数据同步到redis


--验证渠道与ip 地址是否一致
--local myIp = ngx.req.get_headers()["X-Real-IP"]
--if isempty(myIp) then
--    myIp = ngx.req.get_headers()["x_forwarded_for"]
--end
--if isempty(myIp) then
--    myIp = ngx.var.remote_addr
--end
--
--if isempty(myIp) then
--    ngx.log(ngx.DEBUG, "没有获取到ip 地址")
--
--    returnjson(-2, "没有获取到ip地址")
--    ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);
--end
--
--myIp = string.sub(myIp, string.find(myIp, "%d+%.%d+%.%d+"))
--
--
----如果已经动态分配ctoken,token 与IP 地址绑定；验证token 的有效性；则不进行认证,直接进行能力管控
--ctoken = ngx.req.get_headers()["ctoken"]
--if isempty(ctoken) then
--    ctoken = ngx.var.cookie_ctoken
--end


--ngx.log(ngx.ERR, ngx.ctx.ctoken)
--ngx.log(ngx.ERR, ngx.ctx.myip)
--ngx.log(ngx.ERR, ngx.ctx.channel_code)

local ctoken = ngx.ctx.ctoken
local myIp = ngx.ctx.myip
local channel_code1 = ngx.ctx.channel_code


--验证ctoken 在有效期内，跳过认证流程;不在有效期，继续认证流程；
if not isempty(ctoken) then


    local myconfig = ngx.shared.myconfig
    local redis_host = myconfig:get("redis-host")
    local redis_port = myconfig:get("redis-port")

    ngx.log(ngx.DEBUG, ">>>redis链接," .. redis_host .. ":" .. redis_port)

    --连接redis
    --local redis = require "resty.redis"
    local cache = redis.new()
    cache:set_timeout(1000) --1分钟
    local ok, err = cache:connect(redis_host, redis_port)
    --local ok, err = cache:connect("192.168.152.6", 6380)


    --如果连接失败，跳转到脚本结尾
    if not ok then
        ngx.log(ngx.DEBUG, ">>>redis链接失败")

        close_redis(cache)

        ngx.say(">>>redis链接失败")

        ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE)
    end


    --    local channel_code1 = ngx.req.get_headers()["ChannelCode"]
    --    if isempty(channel_code1) then
    --        channel_code1 = ngx.var.cookie_ChannelCode
    --    end

    cache:init_pipeline()

    cache:get(ctoken)
    cache:hget("hash_" .. channel_code1, "save_host")
    cache:hget("hash_" .. channel_code1, "save_port")

    local respTable, err = cache:commit_pipeline()

    --得到的数据为空处理
    if respTable == ngx.null then
        respTable = {} --比如默认值

        returnjson(-99, "请仔细检查配置文件")

        ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);
    end

    --结果是按照执行顺序返回的一个table
    --[[
    for i, v in ipairs(respTable) do
        ngx.say("msg : ",i..v, "<br/>")
    end
    --]]

    --ngx.say("msg : ",respTable[1]..respTable[3]..respTable[3], "<br/>")


    --ctokenok, err = cache:get(ctoken)
    close_redis(cache)

    ----------------------------------------------------------
    -- 调用获取数据接口；
    -- 获取渠道的代理接口地址save_url与key;
    ----------------------------------------------------------

    ctokenok = respTable[1]
    local channel_save_host = respTable[2]
    local channel_save_port = respTable[3]

    if ctokenok == myIp then

        --ngx.log(ngx.DEBUG,">>>ctoken 有效，不再进行渠道认证......")

        --连接redis
        --local channel_redis = require "resty.redis"
        local channel_cache = redis.new()
        channel_cache:set_timeout(1000) --1分钟
        --local ok, err = channel_cache:connect("192.168.152.5", 19001)
        local ok, err = channel_cache:connect(channel_save_host, channel_save_port)


        --如果连接失败，跳转到脚本结尾
        if not ok then
            ngx.log(ngx.DEBUG, ">>>redis链接失败")

            ngx.say(">>>redis链接失败")

            close_redis(channel_cache)

            ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);
        end

        --hgetall 获得所有字段的数据
        local getkey = ngx.var.arg_key
        --local getkey = ngx.req.get_uri_args["key"]

        --ngx.log(ngx.DEBUG,"数据......"..getkey)

        local result, err3 = channel_cache:hgetall(getkey);

        if isempty(result) then

            --ngx.log(ngx.DEBUG,key+"数据为空......"..getkey)

            returnjson(-1, "失败原因，数据为空，请仔细检查传递的key" .. getkey)

            close_redis(channel_cache)
            ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);
        end

        --ngx.log(ngx.ERR,"数据......"..result)

        --redis hash 转换为标准map格式，用于转换json
        local result2 = {};
        for i = 1, #result / 2 do
            result2[result[i * 2 - 1]] = result[i * 2]
        end


        --转换为json格式输出

        local resultend = returnjsonnew(200, "ok", result2)
        --日志传输流转到下一个阶段
        --ngx.log(ngx.ERR, channel_code1.."|"..resultend)
        ngx.ctx.logcontent = channel_code1 .. "|" .. resultend

        ngx.say(resultend);

        close_redis(channel_cache)

        ngx.exit(ngx.HTTP_OK);

    else

        returnjson(-5, "无效的令牌")

        ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);
    end


end


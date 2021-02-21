--[[
    使用渠道与密钥进行认证，内部网络不对IP 地址进行绑定验证；
    根据chanel_code与secretkey 参数自动转换到es 的链接；
    合作商接入时候，首先进行index 的分配与创建，并且创建合作商的index 的ttl 为1d;
--]]

--判断字符串是否为空
local function isempty(s)
    return s == nil or s == '' or s == ngx.null
end

local function close_redis(red)
    if not red then
        return
    end
    --释放连接(连接池实现)
    local pool_max_idle_time = 10000 --毫秒
    local pool_size = 10000 --连接池大小
    local ok, err = red:set_keepalive(pool_max_idle_time, pool_size)
    if not ok then
        ngx.say("set keepalive error : ", err)
    end
end

--local function getUrlParam(param1)
--    local result = ngx.req.get_uri_args[param1]
--
--    ngx.log(ngx.DEBUG,param1.."="..result)
--
--    return result
--end

--从head or cookie 获取参数值
--local function getHeadCookie(param1)
--    local result = ngx.req.get_headers()[param1]
--
--    if isempty(result) then
--
--        --收集cookie 的值
--        local t = {}
--
--        if ngx.var.http_cookie then
--
--            local s = ngx.var.http_cookie
--
--            for k, v in string.gmatch(s, "(%w+)=([%w%/%.=_-]+)") do
--
--                t[k] = v
--
--            end
--
--        end
--        result = t[param1]
--
--        --result = ngx.req.get_uri_args[param1]
--
--    end
--
--    ngx.log(ngx.DEBUG,param1.."="..result)
--
--    return result
--end





--支撑head或者cookie 获取参数;
--1.获取code and 秘钥进行验证，参数放入head or cookie ；chanelcode key
--curl -v -b "ChannelCode=test;ChannelSecretkey=2fb4f6d2ec30fc45da6d5e81cfdf5d1d"  -XPOST http://127.0.0.1:8891/esjson?key=a3 -d '{
--    "user": "kimchy",
--    "post_date": "2009-11-15T14:12:12",
--    "message": "You know, for Search"
--}'
--{"_index":"test","_type":"test","_id":"a2","found":false}

--curl -v -b "ChannelCode=test;ChannelSecretkey=2fb4f6d2ec30fc45da6d5e81cfdf5d1d"  -XPUT http://127.0.0.1:8891/esjson?key=a3 -d '{
--    "user": "kimchy",
--    "post_date": "2009-11-15T14:12:12",
--    "message": "You know, for Search"
--}'

--ab  -p "test.json" -H "Cookie:ChannelCode=test;ChannelSecretkey=2fb4f6d2ec30fc45da6d5e81cfdf5d1d"  http://127.0.0.1:8891/esjson?key=a3


--直接访问
--curl -v -b "ChannelCode=test;ChannelSecretkey=2fb4f6d2ec30fc45da6d5e81cfdf5d1d"  -XPUT http://127.0.0.1:8891/test/test/a1 -d '{
--    "user": "kimchy",
--    "post_date": "2009-11-15T14:12:12",
--    "message": "You know, for Search"
--}'

--{"_index":"test","_type":"test","_id":"a1","_version":23,"created":false}


--获取参数
local paramkey = ngx.var.arg_key

if isempty(paramkey) then
    --ngx.log(ngx.DEBUG, "没有获取到 key")
    ngx.say("请检查从url的参数传递，key 不允许为空");
    ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);
    return
end


local chanelcode = ngx.req.get_headers()["ChannelCode"]
local chanelsecretkey = ngx.req.get_headers()["ChannelSecretkey"]


if isempty(chanelcode) then
    chanelcode = ngx.var.cookie_ChannelCode
end

if isempty(chanelsecretkey) then
    chanelsecretkey = ngx.var.cookie_ChannelSecretkey
end


if isempty(chanelcode) or isempty(chanelsecretkey) then
    --ngx.log(ngx.DEBUG, "没有获取到chanelcode or chanelsecretkey")
    ngx.say("请检查从head or cookie 的参数传递，chanelcode or chanelsecretkey");
    ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);
    return
end





--获取密钥，进行认证
local myconfig = ngx.shared.myconfig
local redis_host = myconfig:get("redis-host")
local redis_port = myconfig:get("redis-port")

--ngx.log(ngx.DEBUG, ">>>redis链接," .. redis_host .. ":" .. redis_port)

--连接redis
local redis = require "resty.redis"
local cache = redis.new()
--local ok , err = cache:connect(cache,redis_host,redis_port)
local ok, err = cache:connect(redis_host, redis_port)

cache:set_timeout(1000) --1分钟

--如果连接失败，跳转到脚本结尾
if not ok then
    ngx.log(ngx.DEBUG, ">>>redis链接失败")

    return close_redis(cache)
end


--验证秘钥 是否有效
local channel_pwd, err = cache:hget("hash_" .. chanelcode, "pwd") --秘钥盐渍
local channel_iplist, err = cache:hget("hash_" .. chanelcode, "iplist") --渠道ip 地址

local server_secretkey = ngx.md5(chanelcode .. channel_iplist .. channel_pwd)


if chanelsecretkey ~= server_secretkey then

    ngx.log(ngx.DEBUG, chanelsecretkey .. "秘钥不匹配" .. server_secretkey)

    ngx.say("秘钥不匹配");
    ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);

    return close_redis(cache)
end
--关闭链接池
close_redis(cache)




--2.调用子请求，存入数据,post application-json；

local requestmethod = ngx.var.request_method

local json = require("cjson")



ngx.req.read_body()
local data = ngx.req.get_body_data()

local res;
if isempty(data) then
    res = ngx.location.capture("/es/" .. chanelcode .. "/" .. chanelcode .. "/" .. paramkey,
        {
            share_all_vars = true
        })

    --形成错误日志内容，可以进行采集
    ngx.log(ngx.ERR, chanelcode .. "|" .. res.body)

else
    res = ngx.location.capture("/es/" .. chanelcode .. "/" .. chanelcode .. "/" .. paramkey,
        {
            method = ngx.HTTP_POST,
            --body = ngx.req.read_body(),
            ngx.req.read_body(),
            share_all_vars = true
            --copy_all_vars = true
        })
end

ngx.log(ngx.DEBUG, "POST子请求返回值......" .. res.body)
ngx.log(ngx.DEBUG, "POST子请求返回状态......" .. res.status)
ngx.say(res.body);
ngx.exit(ngx.HTTP_OK);
return


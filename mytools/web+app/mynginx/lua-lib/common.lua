local common = {}             -- Public namespace

--判断字符串是否为空
function common.isempty(s)
    return s == nil or s == ''  or  s == ngx.null
end

--拼接返回json字符串
function common.returnjson(status,desc,result)
    local cjson = require "cjson"
    local data = {}
    data.status=status;
    data.desc= desc;
    data.data = result;
    local jsonvalue=cjson.encode(data);
    ngx.say(jsonvalue);
end

function common.close_redis(red)
    if not red then
        return
    end
    --释放连接(连接池实现)
    local pool_max_idle_time = 10000 --毫秒
    local pool_size = 1000 --连接池大小
    local ok, err = red:set_keepalive(pool_max_idle_time, pool_size)
    if not ok then
        ngx.say("set keepalive error : ", err)
    end
end

--从head or cookie 获取参数值  测试 ok
function common.getHeadCookie(param1)
    local result = ngx.req.get_headers()[param1]

    if common.isempty(result) then

        --收集cookie 的值
        local t = {}

        if ngx.var.http_cookie then
            local s = ngx.var.http_cookie
            for k, v in string.gmatch(s, "(%w+)=([%w%/%.=_-]+)") do
                t[k] = v
            end
        end
        result = t[param1]

        if common.isempty(result) then return end
        --result = ngx.req.get_uri_args[param1]
        ngx.log(ngx.DEBUG,param1.."="..result)

    end

    return result
end

--ngx.log(ngx.ERR,"***********************"..getHeadCookie("ChannelCode"))

--获取uri参数
function common.getUrlParam(param1)
    ngx.req.read_body()
    local args = ngx.req.get_uri_args()
    for key, val in pairs(args) do
        if key == param1 then
            if type(val) == "table" then
                return table.concat(val, ", ")
            else
                return val
            end
        end
    end

    return

end

--ngx.log(ngx.ERR,"++++++++++++++++++++++"..getUrlParam("one"))


function common.getIp()
    --验证渠道与ip 地址是否一致
    local myIp = ngx.req.get_headers()["X-Real-IP"]
    if common.isempty(myIp) then
        myIp = ngx.req.get_headers()["x_forwarded_for"]
    end

    if common.isempty(myIp) then
        myIp=ngx.var.remote_addr
    end
    return myIp
end


function common.getConfigRedisCache()

    local myconfig = ngx.shared.myconfig
    local redis_host=myconfig:get("redis-host")
    local redis_port=myconfig:get("redis-port")

    ngx.log(ngx.ERR,">>>redis链接,"..redis_host..":"..redis_port)

    --连接redis
    local redis = require "resty.redis"
    local cache = redis.new()
    local ok , err = cache:connect(redis_host,redis_port)

    --如果连接失败，跳转到脚本结尾
    if not ok then
        ngx.log(ngx.ERR,">>>redis链接失败")

        return common.close_redis(cache)
    end

    cache:set_timeout(1000) --1分钟

    return cache
end

function common.getRedisCache(redis_host,redis_port)

    ngx.log(ngx.ERR,">>>redis链接,"..redis_host..":"..redis_port)

    --连接redis
    local redis = require "resty.redis"
    local cache = redis.new()
    local ok , err = cache:connect(redis_host,redis_port)

    --如果连接失败，跳转到脚本结尾
    if not ok then
        ngx.log(ngx.ERR,">>>redis链接失败")
        return common.close_redis(cache)
    end

    cache:set_timeout(1000) --1分钟

    return cache
end

return common
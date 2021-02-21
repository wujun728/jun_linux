--curl -v -b "ChannelCode=test;ChannelSecretkey=2fb4f6d2ec30fc45da6d5e81cfdf5d1d"  "http://192.168.99.101/api3?datatype=db1&datakey="
--无datatype or datakey 参数直接返回鉴权成功的信息

local channel_code = ngx.req.get_headers()["ChannelCode"]
if isempty(channel_code) then
    channel_code = ngx.var.cookie_ChannelCode
end
if isempty(channel_code) then
    ngx.log(ngx.DEBUG, "传递的参数不全，或者名称不对")
    returnjson(-4, "请仔细检查传递的参数")
    ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);
end


local channel_secretkey = ngx.req.get_headers()["ChannelSecretkey"]
if isempty(channel_secretkey) then
    channel_secretkey = ngx.var.cookie_ChannelSecretkey
end

if isempty(channel_secretkey) then

    ngx.log(ngx.DEBUG, "传递的参数不全，或者名称不对")
    returnjson(-4, "请仔细检查传递的参数")

    close_redis(cache1)
    ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);
end

ngx.log(ngx.DEBUG, ">>>redis链接,start...")


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

--开始查询
local result, err3 = cache1:get(channel_secretkey);

ngx.log(ngx.DEBUG, isempty(result))


local h=ngx.req.get_headers()
ngx.log(ngx.DEBUG, print_table(h))
ngx.log(ngx.DEBUG, format_table(_G))


if isempty(result) then

    returnjson(-1, "失败原因，鉴权失败，请仔细检查传递的key" .. channel_secretkey)

    close_redis(cache1)
    ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);
end

ngx.log(ngx.DEBUG, " 鉴权通过 ......")

--保持链接池
close_redis(cache1)


local datatype = ngx.var.arg_datatype
local datakey = ngx.var.arg_datakey

if isempty(datatype) or isempty(datakey) then


    returnjson(200, "认证通过", "ture")

    ngx.exit(ngx.HTTP_OK);

end

--参数通过上下文传递到后面的程序使用
ngx.ctx.channel_code = channel_code
ngx.ctx.channel_secretkey = channel_secretkey

ngx.ctx.datatype = datatype
ngx.ctx.datakey = datakey
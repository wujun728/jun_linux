--curl -v -b "ChannelCode=test;ChannelSecretkey=2fb4f6d2ec30fc45da6d5e81cfdf5d1d"  "http://192.168.99.101/api3?datatype=db1&datakey=aaa"
--set 2fb4f6d2ec30fc45da6d5e81cfdf5d1d 1
--hset aaa a1 123;hset aaa a2 123;hgetall aaa;hget aaa a1;

ngx.log(ngx.DEBUG, "app3 start ......")

local channel_code = ngx.ctx.channel_code
local channel_secretkey = ngx.ctx.channel_secretkey

local datatype = ngx.ctx.datatype
local datakey = ngx.ctx.datakey

--根据渠道code,获取渠道的db-list;
--判断db-list 是否存在datatype;
--如果存在,调用 datakey 从datatye 获取数据;
--配置datatype 与 redis 对应关系;
--加载配置文件


--local fileDbAcl = io.open("/usr/local/nginx/conf/lua.d/0-config-db-acl.json", "r");
--
--local contentDbAcl = cjson.decode(fileDbAcl:read("*all"));
--fileDbAcl: close();
local myconfig = ngx.shared.myconfig;
local contentDbAcl = cjson.decode(myconfig:get("cfgDbAcl"))

if isempty(contentDbAcl.data[channel_code]) then
    return
end

if isempty(contentDbAcl.data[channel_code][datatype]) then
    return
end

ngx.log(ngx.DEBUG, "**********有数据集获取权限*********")
ngx.log(ngx.DEBUG, contentDbAcl.data[channel_code][datatype])



ngx.log(ngx.DEBUG, "**********获取数据*********")

--local fileDbCodis = io.open("/usr/local/nginx/conf/lua.d/0-config-db-codis.json", "r");
--
--local contentDbCodis = cjson.decode(fileDbCodis:read("*all"));
--fileDbCodis: close();

local cfgDbCodis =  cjson.decode(myconfig:get("cfgDbCodis"))

local dbhost = cfgDbCodis.data[datatype]["host"];
local dbport = cfgDbCodis.data[datatype]["port"];

ngx.log(ngx.DEBUG, dbhost)
ngx.log(ngx.DEBUG, dbport)


local cache1 = redis.new()
cache1:set_timeout(1000) --1分钟
local ok, err = cache1:connect(dbhost,dbport)


--如果连接失败，跳转到脚本结尾
if not ok then
    ngx.log(ngx.DEBUG, ">>>redis链接失败")
    ngx.say(">>>redis链接失败")

    close_redis(cache1)
    ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE)
end

--开始查询
--local result, err3 = cache1:get(datakey);
local result, err3 = cache1:hgetall(datakey);


local h=ngx.req.get_headers()
ngx.log(ngx.DEBUG, print_table(h))
ngx.log(ngx.DEBUG, format_table(_G))


if isempty(result) then

    returnjson(-1, "失败原因，数据不存在，请仔细检查传递的key" .. datakey)

    close_redis(cache1)
    ngx.exit(ngx.HTTP_SERVICE_UNAVAILABLE);
end

ngx.log(ngx.DEBUG, " 获取数据 ......" .. cjson.encode(result))

--redis hash 转换为标准map格式，用于转换json
local result2 = {};
for i = 1, #result / 2 do
    result2[result[i * 2 - 1]] = result[i * 2]
end


--保持链接池
close_redis(cache1)

--传递日志信息,记录日志
ngx.ctx.logcontent = channel_code .. "|" .. datatype .. "|" .. datakey .. cjson.encode(result2)

returnjson(200, "认证成功,返回数据...", result2)

ngx.exit(ngx.HTTP_OK);
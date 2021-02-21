local myconfig = ngx.shared.myconfig;
--es 检索引擎地址配置
local cfgDbQuery = cjson.decode(myconfig:get("cfgDbQuery"))

local request = ngx.var.request_uri;

ngx.log(ngx.DEBUG,request)

local pathproxy = string.match(request, "(/[%w_]+/[%w_]+/)")
local requrl = string.sub(request,#pathproxy+1)

ngx.log(ngx.DEBUG,requrl)
--
--    local valuepath = string.match(request, "([%w_]+)")
--    local valuepath1 = string.match(request, "([%w_]+)", #valuepath + 2)
--    local valuekey = string.match(request, "([%w_]+)",#valuepath1+ #valuepath + 4)
--    ngx.log(ngx.DEBUG,valuekey)

ngx.log(ngx.DEBUG,cfgDbQuery.urlrest..requrl)


return cfgDbQuery.urlrest..requrl
--return "http://172.16.71.56:9006/form/rest/"
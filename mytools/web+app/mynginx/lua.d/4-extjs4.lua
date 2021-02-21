--1.crud + filter
--2.filter turn to es-query
ngx.log(ngx.DEBUG, "首先由elasticsearch 对需要查询的数据表建立自动索引[es-query] ......")
ngx.log(ngx.DEBUG, "extjs 的crud 增加代理，遇到filter 方法启动es 查询，将查询结果idList 返回，再由spring-data 执行实际数据查询 ......")


--总记录数 利用全局变量的特性记录


local request_method = ngx.var.request_method
local args = nil
--获取参数的值
if "GET" == request_method then
    args = ngx.req.get_uri_args()
elseif "POST" == request_method then
    ngx.req.read_body()
    args = ngx.req.get_post_args()
end

local filterparam = ngx.var.arg_filter
--ngx.say(filterparam)
if isempty(filterparam) then
    returnjson(-1, "没有filter参数", args)
    return
end
--ngx.exit(ngx.HTTP_OK);


--通过form-route 引擎调用es-query,在es-query 中配置extjs-filter 的查询语句
--local esUrl = 'http://192.168.99.101/formroutequery?html=route-json&query=q6'
--local esUrl = 'http://192.168.99.101/formroutequery'
--args["html"] = 'route-json'
--args["query"] = 'q6'


local myconfig = ngx.shared.myconfig;
--es 检索引擎地址配置
local cfgDbQuery = cjson.decode(myconfig:get("cfgDbQuery"))

args["html"] = cfgDbQuery.es.htmles
args["query"] = cfgDbQuery.es.esquery

local http = require "resty.http"
local httpc = http.new()
local res, err = httpc:request_uri(cfgDbQuery.url, {
    method = "GET",
    query = args,
    headers = {
        ["Content-Type"] = "application/x-www-form-urlencoded",
    }
})

--没有查询到数据情况的处理
--提取实体id
local jsonvalue = cjson.decode(res.body)
local restargstmp = {}

if (#jsonvalue[args["query"]].hits.hits==0) then
    returnjson(-1, "没有检索到数据", {'检索path',cfgDbQuery.es.url,'检索条件',args})
    ngx.exit(ngx.HTTP_OK);
end
--确定只有一个查询语句
for key, values in pairs(jsonvalue[args["query"]].hits.hits) do
    if type(values) ~= "table" then
        values = {values}
    end
    restargstmp[key]=values._source[cfgDbQuery.es.entrykey]
end
local restargs={}
restargs[cfgDbQuery.es.entrykey]=restargstmp

--spring rest and id list query
--es-query 对不存在数据的情况进行了处理，不存在无数据的情况
restargs["html"] = cfgDbQuery.es.htmlrest
restargs["query"] = cfgDbQuery.es.restquery
res, err = httpc:request_uri(cfgDbQuery.url, {
    method = "GET",
    query = restargs,
    headers = {
        ["Content-Type"] = "application/x-www-form-urlencoded",
    }
})


--ngx.say(fgDbQuery.url..'\n')
--ngx.say(res.body)
ngx.say(res.body)

--ngx.exit(ngx.HTTP_OK);

--- 查询设置查询变量


--else
--
--    res, err = httpc:request_uri(url, {
--        method = "POST",
--        body = cjson.encode(args),
--        headers = {
--            ["Content-Type"] = "application/x-www-form-urlencoded",
--        }
--    })
--end



--local url = "http://172.16.73.20:9006/form/rest/"..uri
--ngx.req.seturi(url)
--proxy_pass http://backendjava/myweb;

-- es-query 数据格式转换
--1.es-query查询；2.组装spring-rest idList 查询；3.返回查询结果；
--只是需要修改uri,其他不变


------按规则获取data-path = channel_auth
---- lua 是自己实现的专有正则 string.mathc string.find
--local url = ngx.var.uri
------local uri = ngx.re.sub(ngx.var.uri, "^(/[a-z\-]*/)(.*)", "$2", "o")
----local uri = ngx.re.sub(ngx.var.uri, "^(/[a-z\-]*/)(.*)", "$2", "o")
----local uri1 = ngx.re.sub(uri, "\w*", "$3", "o")
----ngx.print(url..'\r')
----ngx.print(uri1)
--local valuepath=string.match(url,"([%w_]+)")
--local valuekey=string.match(url,"([%w_]+)",#valuepath+2)
--
----ngx.print(valuekey)
--ngx.ctx.domain=valuekey
--
---- spring-rest 数据格式转换
--ngx.log(ngx.DEBUG,isempty(res.body))
--if not isempty(res.body) then
--
--    local result = {};
--
--    local jsonvalue = cjson.decode(res.body);
--
--    --更新总记录数
--    if (not isempty(jsonvalue.page)) then
--        totalElements = jsonvalue.page.totalElements
--    end
--
--    if (isempty(jsonvalue._embedded[ngx.ctx.domain])) then
--        --单条记录数据
--        result["DATA"] = jsonvalue
--    else
--        --多条记录数据
--        result["DATA"] = jsonvalue._embedded[ngx.ctx.domain]
--    end
--
--        --无page 数据情况处理
--    if (isempty(jsonvalue.page)) then
--        result["PAGE"] = cjson.decode('{ "page": { "totalElements": ' .. totalElements .. ' } }')
--    else
--        result["PAGE"] = jsonvalue.page
--    end
--
--    ngx.say(cjson.encode(result));
--end




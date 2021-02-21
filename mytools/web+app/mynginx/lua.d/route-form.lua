--常用函数
local function isempty(s)
    return s == nil or s == '' or s == ngx.null
end


--获取es查询参数 query=q4&XXX=电路&PId=dllx0000
--获取es查询参数 http://192.168.99.101/formroutequery?html=route-form&query=q5&namevalue=test&codevalue=test&start=1&size=10
--给属性赋值json 替换参数  key 要求单个语句全局唯一
function setattr(values, params)
    for i, v in pairs(values) do
        --ngx.say(type(v))
        --ngx.exit(ngx.HTTP_OK);

        if (type(v) == 'string') then
            --参数值存在，赋值
            --ngx.say(cjson.encode(v))

            if ( params[v]) then
                values[i] = params[v]
            end
        else
            --递归调用table
            if ( type(v) == 'table') then
                setattr(v, params)
            end
        end
    end
end

function split(szFullString, szSeparator)
    local nFindStartIndex = 1
    local nSplitIndex = 1
    local nSplitArray = {}
    while true do
        local nFindLastIndex = string.find(szFullString, szSeparator, nFindStartIndex)
        if not nFindLastIndex then
            nSplitArray[nSplitIndex] = string.sub(szFullString, nFindStartIndex, string.len(szFullString)) break
        end
        nSplitArray[nSplitIndex] = string.sub(szFullString, nFindStartIndex, nFindLastIndex - 1) nFindStartIndex = nFindLastIndex + string.len(szSeparator)
        nSplitIndex = nSplitIndex + 1
    end
    return nSplitArray
end

--转换sort 查询参数为es 能够识别的查询json
function sorttojson(sortKey)

    if (not isempty(sortKey)) then
        local sortKeys = {}

        if (type(sortKey) == 'string') then
            --ngx.say("query 查询id参数必须赋值,必须是数组.自动转换为数组");
            sortKeys['1'] = sortKey
        else
            sortKeys = sortKey
        end

        local sortjson='{'
        for key, val in pairs(sortKeys) do
            local sortvalue=split(val,",")

            local sortline= '"'..sortvalue[1]..'": { "order":"'..sortvalue[2]..'"}'
            if  (#sortjson == 1 ) then
                sortjson=sortjson..sortline
            else
                sortjson=sortjson..','..sortline
            end
        end
        sortjson=sortjson..'}'
        return sortjson
    end
    return ""
end


--获取模板名称
local htmlname = ngx.var.arg_html
if isempty(htmlname) then
    ngx.say("html 模板引擎参数必须赋值");
    ngx.exit(ngx.HTTP_OK);
end

--获取参数
local args = ngx.req.get_uri_args()
--local args = ngx.req.get_post_args()
--local myargs = ''
--
--- -获取所有的参数
-- for key, val in pairs(args) do
-- if isempty(myargs) then
--
-- else
-- myargs=myargs.."&"
-- end
-- myargs=myargs..key.."="..val;
-- end


--获取查询参数 query=q1&query=q2&query=q4&PK=abc&BK=123&XXX=电路&PId=dllx0000
local myconfig = ngx.shared.myconfig;
local cfgDbQuery = cjson.decode(myconfig:get("cfgDbQuery"))



--查询id q1,q2,q3
local queryKey = ngx.req.get_uri_args()["query"]
--ngx.say(queryKey)

if (isempty(queryKey)) then
    ngx.say("query 查询id参数必须赋值");
    ngx.exit(ngx.HTTP_OK);
end

--查询语句key列表
local queryKeys = {}
--构造查询语句
local queryList = {}
--参数
local params = {}
--方法
local mtds = {}

if (type(queryKey) == 'string') then
    --ngx.say("query 查询id参数必须赋值,必须是数组.自动转换为数组");
    queryKeys['1'] = queryKey
else
    queryKeys = queryKey
end

--特殊参数处理
--sort
local sortKey = ngx.req.get_uri_args()["sort"]
local sortjson = sorttojson(sortKey)
--ngx.say(cjson.encode(sortjson))
--ngx.exit(ngx.HTTP_OK);

--filter
local filtervalue = ngx.req.get_uri_args()["filter"]
local filterjson=""
if (not(isempty(filtervalue))) then
    local filterjsontmp = cjson.decode(filtervalue)
    filterjson="["

    for key, val in pairs(filterjsontmp) do
        local line =  '{"term": { "'..val.field..'": "'..val.value..'" }}'
        if (#(filterjson) == 1 ) then
            filterjson = filterjson .. line
        else
            filterjson = filterjson ..','.. line
        end
    end
    filterjson=filterjson .. ']'
end
--ngx.say(cjson.encode(filterjson))
--ngx.exit(ngx.HTTP_OK);

local dcKey = ngx.req.get_uri_args()["_dc"]

--逐个处理查询语句的参数
for key, val in pairs(queryKeys) do

    query = cfgDbQuery["list"][val]
    local url = query["url"]
    local mtd = query["method"]

    mtds[val] = mtd
    --待处理的参数
    local argsp = query["param"]
    if (mtd == 'GET') then
        --构造参数字符串
        local myargsp = ''
        --查询参数组合,获取参数值并且注入
        for keyp, valp in pairs(argsp) do
            --兼容参数是数组
            local line=""
            if type(args[valp]) == 'table' then
                local c = 1
                for _, valpp in pairs(args[valp]) do
                    if c > 1 then
                        line = line .."&"..keyp .. "=" .. valpp;
                    else
                        line = line .. keyp .. "=" .. valpp;

                    end
                    c = c+1
                end
               -- ngx.say(line)
            else
                line = keyp .. "=" .. args[valp];
            end

            if isempty(myargsp) then
                myargsp = myargsp .. line

            else
                myargsp = myargsp .. "&" ..line
            end


        end
        params[val] = myargsp
        queryList[val] = url .. "?" .. myargsp;

    elseif (isempty(dcKey)) then
        -- method = POST 主要是支持es查询
        setattr(argsp, args)

        ngx.say(cjson.encode(argsp))

        --ngx.exit(ngx.HTTP_OK);
        params[val] = argsp
        queryList[val] = url
    else
        -- extjs for es-query
        -- 替换filter sort 字符串

        --ngx.say(filterjson)
        --ngx.say(sortjson)

        local argsptext=string.gsub(cjson.encode(argsp),'"filterkey"',filterjson)
        argsptext=string.gsub(argsptext,'"sortkey"',sortjson)

        --ngx.say(argsptext)

        argsp=cjson.decode(argsptext)

        -- method = POST 主要是支持es查询
        setattr(argsp, args)

        --ngx.say(cjson.encode(argsp))
        --ngx.exit(ngx.HTTP_OK);

        params[val] = argsp
        queryList[val] = url
    end
end

--ngx.say(queryList)
--进行查询,构造查询结果数据与参数数据
local result = {}
--所有参数值
result["paramsText"] = cjson.encode(args);
result["params"] = args;
--查询语句与参数
result["methodsValue"] = cjson.encode(mtds);
result["querylistText"] = cjson.encode(queryList)
result["paramsValue"] = cjson.encode(params);


result["methods"] = mtds;
result["querylist"] = queryList
result["queryParam"] = params;


--- 查询设置查询变量
local http = require "resty.http"
local httpc = http.new()
for keyq, valq in pairs(queryList) do



    local res, err
    if (mtds[keyq] == 'GET') then
        res, err = httpc:request_uri(valq, {
            method = "GET",
            headers = {
                ["Content-Type"] = "application/x-www-form-urlencoded",
            }
        })
    else

        res, err = httpc:request_uri(valq, {
            method = "POST",
            body = cjson.encode(params[keyq]),
            headers = {
                ["Content-Type"] = "application/x-www-form-urlencoded",
            }
        })
    end


--    ngx.say(valq);
--    ngx.say(mtds[keyq]);
--    ngx.say(params[keyq]);
--    ngx.say(err);
--    ngx.say(res.body);
--
--    ngx.exit(ngx.HTTP_OK);

    local jsonvalue = cjson.decode(res.body);
    result[keyq] = jsonvalue
end

--
--- -模板引擎渲染,设置模板,设置变量
local template = require "resty.template"
template.render("/" .. htmlname .. ".html", {
    formvalue = result
})
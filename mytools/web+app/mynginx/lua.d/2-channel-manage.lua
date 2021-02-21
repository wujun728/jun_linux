local args = ngx.req.get_uri_args()
--local args = ngx.req.get_post_args()
local myargs = ''

local function isempty(s)
    return s == nil or s == ''  or  s == ngx.null
end

for key, val in pairs(args) do
--    if type(val) == "table" then
--        ngx.say(key, ": ", table.concat(val, ", "))
--    else
--        ngx.say(key, ": ", val)
--    end
    if isempty(myargs) then

    else
        myargs=myargs.."&"
    end
    myargs=myargs..key.."="..val;

end

--    ngx.say(myargs);

local http = require "resty.http"

local httpc = http.new()
local res, err = httpc:request_uri("http://127.0.0.1/springboot/channel_auth/filter?"..myargs, {
--local res, err = httpc:request_uri("http://172.17.0.239:8080/channel_auth/filter?"..myargs, {
    method = "GET",
    body = myargs,
    headers = {
        ["Content-Type"] = "application/x-www-form-urlencoded",
    }
})

if not res then
    ngx.say("failed to request: ", err)
    return
end

-- In this simple form, there is no manual connection step, so the body is read
-- all in one go, including any trailers, and the connection closed or keptalive
-- for you.

ngx.status = res.status

for k,v in pairs(res.headers) do
    --
end

--ngx.say(res.body);

local jsonvalue=cjson.decode(res.body);
--
--ngx.say("================");
--
--for name, value in pairs(jsonvalue._embedded.channel_auth[1]) do
--    ngx.say(name);
--    ngx.say(cjson.encode(value));
----    for name, value in pairs(value) do
----        ngx.say(name);
----    end
--end



local template = require "resty.template"

#url?temp=channel-list.html
local templatefile = ngx.var.arg_temp
template.render(templatefile, {
#template.render("channel-list.html", {
    channels = jsonvalue._embedded.channel_auth ,
    page = jsonvalue.page
})

--模板嵌套的例子
--id/name/code/pwd/token/token_expire/iplist/ip_bind_time/ip_time_out/connect_count/limit_bandwidth/status/
--template.render("channel-list-test.html", { channels = {
--    {id=1,name = "Jane", code = "1001" ,pwd="asdfkjs;dlkfjqwer",token_expire="10",
--        iplist="192.168.59.3",
--        ip_bind_time=60,ip_time_out=60,connect_count=300,limit_bandwidth="10M",status=1},
--    {id=1,name = "Jane", code = "1001" ,pwd="asdfkjs;dlkfjqwer",token_expire="10",
--        iplist="192.168.59.3",
--        ip_bind_time=60,ip_time_out=60,connect_count=300,limit_bandwidth="10M",status=1},
--    {id=1,name = "Jane", code = "1001" ,pwd="asdfkjs;dlkfjqwer",token_expire="10",
--        iplist="192.168.59.3",
--        ip_bind_time=60,ip_time_out=60,connect_count=300,limit_bandwidth="10M",status=1},
--    {id=1,name = "Jane", code = "1001" ,pwd="asdfkjs;dlkfjqwer",token_expire="10",
--        iplist="192.168.59.3",
--        ip_bind_time=60,ip_time_out=60,connect_count=300,limit_bandwidth="10M",status=1},
--    {id=1,name = "Jane", code = "1001" ,pwd="asdfkjs;dlkfjqwer",token_expire="10",
--        iplist="192.168.59.3",
--        ip_bind_time=60,ip_time_out=60,connect_count=300,limit_bandwidth="10M",status=1}
--}})


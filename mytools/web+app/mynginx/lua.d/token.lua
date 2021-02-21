--获取ip 地址，进行token验证
--require("redis-ip")

local function isempty(s)
  return s == nil or s == ''
end

local myIp = ngx.req.get_headers()["X-Real-IP"]

if isempty(myIp) then
    myIp = ngx.req.get_headers()["x_forwarded_for"]
end

if isempty(myIp) then
    myIp=ngx.var.remote_addr
end

if isempty(myIp) then
    myIp = '没有获取到ip 地址'
end

ngx.log(ngx.ERR,">>>ip:" .. myIp)

--if myIp == "公司出口IP" then
--    ngx.exec("@client")
--else
--    ngx.exec("@client_test")
--end


local secretkey='1234567890abcdefghi'

local expiretime = ngx.time()
expiretime = expiretime+86400
expiretime = ngx.cookie_time(expiretime)


if ngx.var.cookie_uid == nil or ngx.var.cookie_nickname == nil or ngx.var.cookie_token == nil then
    ngx.log(ngx.ERR,">>>222")
    ngx.req.set_header("Check-Login", "NULL")
    ngx.req.set_header("Foo", {"a", "abc"})

    ngx.header["Set-Cookie"] = {"Check-Login=NULL" .. "; expires=" .. expiretime ..";path=/" }

    return
end

local ctoken = ngx.md5('uid:' .. ngx.var.cookie_uid .. '&nickname:' .. ngx.var.cookie_nickname .. '&secretkey:' .. secretkey)

ngx.log(ngx.ERR,">>>333")

if ctoken == ngx.var.cookie_token then
    ngx.req.set_header("Check-Login", "Yes")

    ngx.header["Set-Cookie"] = {"Check-Login=Yes" .. "; expires=" .. expiretime ..";path=/" }

    ngx.log(ngx.ERR,">>>444")
 else
    ngx.req.set_header("Check-Login", "No")

    ngx.header["Set-Cookie"] = {"Check-Login=No" .. "; expires=" .. expiretime ..";path=/" }

    ngx.log(ngx.ERR,">>>555")

end

return

--curl -v "http://192.168.99.101/hello1"
--token 错误测试
--curl -v -b "uid=12345;nickname=soga;token=aa6f21ec0fcf008aa5250904985a817b" "http://192.168.99.101/hello1"
--token 正确测试
--curl -v -b "uid=1234;nickname=soga;token=aa6f21ec0fcf008aa5250904985a817b"  "http://192.168.99.101/hello1"



--1、获取全局共享内存变量
local shared_data = ngx.shared.shared_data
--2、获取字典值
local i = shared_data:get("i")
if not i then
  i = 1
  --3、惰性赋值
  shared_data:set("i", i)
  ngx.say("lazy set i ", i, "<br/>")
end
--递增
i = shared_data:incr("i", 1)
ngx.say("i=", i, "<br/>")
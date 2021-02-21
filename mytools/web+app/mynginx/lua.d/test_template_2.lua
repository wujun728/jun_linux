local template = require("resty.template")
--是否缓存解析后的模板，默认true
template.caching(false)
--渲染模板需要的上下文(数据)
local context = {title = "世界，你好！<br>"}
--渲染模板
template.render("t2.html", context)
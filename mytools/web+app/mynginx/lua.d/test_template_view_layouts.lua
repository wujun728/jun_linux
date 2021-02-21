local template = require "resty.template"
local view     = template.new("viewlayout.html", "layout.html")
view.title     = "Testing lua-resty-template"
view.message   = "Hello, World!"
view:render()
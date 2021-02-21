local template = require "resty.template"

-- Using template.new
local view = template.new "view.html"
view.message = "Hello, World!"
view:render()

-- Using template.render
template.render("view.html", { message = "Hello, World!" })

ngx.log(ngx.ERR,3)

--模板嵌套的例子
template.render("include.html", { users = {
    { name = "Jane", age = 29 },
    { name = "John", age = 25 }
}})


--判断字符串是否为空
function isempty(s)
    return s == nil or s == ''
end

function average(a,...)
    result = 0
    local arg={... }
    print(#arg)
    for i,v in ipairs(arg) do
        result = result + v
    end
    return result/#arg
end

print("The average is",average("a",10,5,3,4,5,6))

--可变参数,返回多级child 的 json 结果的值
function getValue(val,...)
    local arg={... }
    --print(#arg)
    --如果key 为空则返回空字符串
    for i,v in ipairs(arg) do
        if (isempty(val[v])) then
            return "";
        else
            val = val[v]
        end
    end
    return val;
end


local v1 = {}
local v2 = {}
local v3 = {}

v1["c"] = 'xxx'
v2["b"] = v1
v3["a"] = v2

print(v3["a"]["b"]["c"])

print("getvalue is:",getValue(v3,'a','b','c'));

--递归json 数据处理
function setattr (values,params)
    for i,v in ipairs(values) do
        if (type(v) == 'string') then
            v = params[v]
        else
            setattr(v,params)
        end
    end
end

local params = {}

params['xxx']='abc'

setattr(v3,params)

print(v3.a.b.c)

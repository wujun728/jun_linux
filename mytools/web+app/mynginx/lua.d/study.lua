--单行注释
--[[
    多行注释
--]]
--变量和程序流程控制
num = 42 --所有的数值都是双精度的
-- 别吓一跳，64位的双精度需要52位
s = 'walternate' --字符串常量
t = "也可以使用双引号"
u = [[在开始和解释使用
      标识多行字符串
    ]]
t = nil
while num < 50 do
    num = num +1
end

if num > 40 then
    print ('over 40')
elseif s ~= 'walternate' then
    io.write('not over 40\n')
else
    thisGlobal = 5

local line = io.read()
    print ('Winter is coming,' .. line)
end



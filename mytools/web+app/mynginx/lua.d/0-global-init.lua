cjson = require "cjson";
redis = require "resty.redis"
--lrucache = require "resty.lrucache"
--
--c = lrucache.new(200)  -- allow up to 200 items in the cache
--if not c then
--    return error("failed to create the cache: " .. (err or "unknown"))
--end

local myconfig = ngx.shared.myconfig;
myconfig: set("Tom", 56)


--加载配置文件
local file = io.open("/usr/local/nginx/conf/lua.d/0-config.json", "r");

local content = cjson.decode(file:read("*all"));
file: close();

for name, value in pairs(content) do
  myconfig: set(name, value);
end


--lua_shared_dict myconfig 10m;
--lua_shared_dict cfgDbAcl 10m;
--lua_shared_dict cfgDbCodis 10m;

local fileDbCodis = io.open("/usr/local/nginx/conf/lua.d/0-config-db-codis.json", "r");
local contentDbCodis = fileDbCodis:read("*all");
fileDbCodis: close();

myconfig: set("cfgDbCodis", contentDbCodis);

local fileDbAcl = io.open("/usr/local/nginx/conf/lua.d/0-config-db-acl.json", "r");
local contentDbAcl = fileDbAcl:read("*all");
fileDbAcl: close();

myconfig: set("cfgDbAcl", contentDbAcl);


local fileDbQuery = io.open("/usr/local/nginx/conf/lua.d/0-config-db-query.json", "r");
local contentDbQuery = fileDbQuery:read("*all");
fileDbQuery: close();

myconfig: set("cfgDbQuery", contentDbQuery);



--判断字符串是否为空
function isempty(s)
  return s == nil or s == '' or s == ngx.null
end

--可变参数,返回多级child 的 json 结果的值
function getValue(value, ...)

    local result = ""
    --如果key 为空则返回空字符串
    for i,v in ipairs(arg) do
        --printResult = printResult .. tostring(v) .. "\t"
        if (isempty(value[v])) then
            return "";
        else
            result = value[v]
        end
    end
    return result;
end

--local cjson = require "cjson"

--拼接返回json字符串
function returnjson(status, desc, result)
  local data = {}
  data.status = status;
  data.desc = desc;
  data.data = result;
  local jsonvalue = cjson.encode(data);
  ngx.say(jsonvalue);
end

function returnjsonnew(status, desc, result)
  local data = {}
  data.status = status;
  data.desc = desc;
  data.data = result;
  local jsonvalue = cjson.encode(data);
  return jsonvalue;
end


function close_redis(red)
  if not red then
    return
  end
  --释放连接(连接池实现)
  local pool_max_idle_time = 10000 --毫秒
  local pool_size = 100 --连接池大小
  local ok, err = red:set_keepalive(pool_max_idle_time, pool_size)

  if not ok then
    ngx.say("set keepalive error : ", err)
  end
end

----config-db-acl
--function have_acldb(dbacl,dbtype)
--
--    local str = '0'
--    for key, val in pairs(dbacl) do
--        -- 获取授权的 DB数组
--        if key == "data" then
--            ngx.log(ngx.DEBUG, "@@@@@@@@@@")
--
--            for _,v in pairs(val) do
--
--
--                ngx.log(ngx.DEBUG, v)
--
--                if v == dbtype then
--                    return '1';
--                end
--            end
--        end
--    end
--
--    return str
--end


function print_table(t)
  local function parse_array(key,tab)
      local str = ''
      for _,v in pairs(tab) do
        str = str .. key .. ' ' .. v .. '\r\n'
      end

    return str
  end

  local str = ''
  for key, val in pairs(t) do
        if type(val) == "table" then
            str = str .. parse_array(key,val)
        else
            str = str .. key .. ' ' .. val  .. '\r\n'
        end
  end
  return str

end


function format_table(t)

  local str = ''
  for key, val in pairs(t) do
      --str = str .. key .. ' ' .. type(val) .. '\r\n'
      str = str .. key .. ' ' .. '\r\n'
  end

  return str

end

function get_from_cache(key)
    local cache_ngx = ngx.shared.myconfig
    local value = cache_ngx:get(key)
    return value
end

function set_to_cache(key, value, exptime)
    if not exptime then
        exptime = 0
    end

    local cache_ngx = ngx.shared.myconfig
    local succ, err, forcible = cache_ngx:set(key, value, exptime)
    return succ
end



--local h=ngx.req.get_headers()
--ngx.log(ngx.DEBUG, print_table(h))
--ngx.log(ngx.DEBUG, format_table(getmetatable(_G).__index))
--ngx.log(ngx.DEBUG, format_table(getmetatable(_G)))
--ngx.log(ngx.DEBUG, format_table(_G)))

dofile("/usr/local/nginx/conf/waf.d/init.lua")
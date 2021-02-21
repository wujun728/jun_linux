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


local fileDimQuery = io.open("/usr/local/nginx/conf/lua.d/config-dim-query.json", "r");
local contentDimQuery = fileDimQuery:read("*all");
fileDimQuery: close();
myconfig: set("cfgDimQuery", contentDimQuery);

--获取码表名称
function getDimName(code)
	if isempty(code) then
		return '';
	end
	local cfgDimQuery =  cjson.decode(myconfig:get("cfgDimQuery"));
	local dimName = cfgDimQuery[code];
	if isempty(dimName) then
		return '';
	else
		return dimName;
	end
end

--常用函数判断是否为空值
function isempty(s)
	if s == nil then
		return true;
	end
	if s == ngx.null then 
		return true;
	end
	if type(s) == nil then 
		return true;
	end
	if type(s) == 'string' and s == '' then 
		return true;
	end
	if type(s) == 'table' and not next(s) then
		return true;
	end
	return false;
end

--常用函数判断长路径是否为空防止异常
function tf(ob,s)
	if type(s) == 'string' and s ~= '' then
		local ise = true;
		local list = {};
		for match in (s.."@"):gmatch("(.-)".."@") do
			table.insert(list,match);
		end
		local obj = ob;
		for i = 1, #list do
			local pn = tonumber(list[i]);
			if type(obj) == "table" and pn then
				obj = obj[tonumber(list[i])];
			else
				obj = obj[list[i]];
			end
			if isempty(obj) then
				ise = false;
				break;
			end
		end
		return ise;
	else
	return false;
	end
end

function fm(ob,s)
	if type(s) == 'string' and s ~= '' then
		local list = {};
		for match in (s.."@"):gmatch("(.-)".."@") do
			table.insert(list,match);
		end
		local obj = ob;
		for i = 1, #list do
			local pn = tonumber(list[i]);
			if type(obj) == "table" and pn then
				obj = obj[tonumber(list[i])];
			else
				obj = obj[list[i]];
			end
			if isempty(obj) then
				return '';
			end
		end
		return obj;
	else
	return '';
	end
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

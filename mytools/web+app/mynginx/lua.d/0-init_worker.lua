--心跳监测
local count = 0
local delayInSeconds = 120
local heartbeatCheck = nil


heartbeatCheck = function(args)
  count = count + 1
  ngx.log(ngx.DEBUG, "do check ", count)
  local ok, err = ngx.timer.at(delayInSeconds, heartbeatCheck)
  if not ok then
    ngx.log(ngx.DEBUG, "failed to startup heartbeart worker...", err)
  end
end


heartbeatCheck()
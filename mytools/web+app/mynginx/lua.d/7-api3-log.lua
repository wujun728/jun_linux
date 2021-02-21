if ngx.ctx.logcontent  then
    ngx.log(ngx.ERR, ngx.ctx.logcontent)
end

--慢速日志记录
--if tonumber(ngx.var.upstream_response_time) >= 1 then
--       ngx.log(ngx.WARN, "[SLOW] Ngx upstream response time: " .. ngx.var.upstream_response_time .. "s from " .. ngx.var.upstream_addr);
--end
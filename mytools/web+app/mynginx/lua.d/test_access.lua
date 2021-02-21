if ngx.req.get_uri_args()["token"] ~= "123" then
   return ngx.exit(403)
end
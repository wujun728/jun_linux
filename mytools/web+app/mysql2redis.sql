SELECT CONCAT(
    '*22\r\n',
    '$', LENGTH(redis_cmd),'\r\n',
    CAST(redis_cmd AS CHAR),'\r\n',
    '$', LENGTH(redis_key),'\r\n',
    CAST(redis_key AS CHAR),'\r\n',
    '$', LENGTH(hkey1), '\r\n',hkey1, '\r\n','$', LENGTH(hval1), '\r\n', hval1, '\r\n',
    '$', LENGTH(hkey2), '\r\n',hkey2, '\r\n','$', LENGTH(hval2), '\r\n', hval2, '\r\n',
    '$', LENGTH(hkey3), '\r\n',hkey3, '\r\n','$', LENGTH(hval3), '\r\n', hval3, '\r\n',
    '$', LENGTH(hkey4), '\r\n',hkey4, '\r\n','$', LENGTH(hval4), '\r\n', hval4, '\r\n',
    '$', LENGTH(hkey5), '\r\n',hkey5, '\r\n','$', LENGTH(hval5), '\r\n', hval5, '\r\n',
    '$', LENGTH(hkey6), '\r\n',hkey6, '\r\n','$', LENGTH(hval6), '\r\n', hval6, '\r\n',
    '$', LENGTH(hkey7), '\r\n',hkey7, '\r\n','$', LENGTH(hval7), '\r\n', hval7, '\r\n',
    '$', LENGTH(hkey8), '\r\n',hkey8, '\r\n','$', LENGTH(hval8), '\r\n', hval8, '\r\n',
    '$', LENGTH(hkey9), '\r\n',hkey9, '\r\n','$', LENGTH(hval9), '\r\n', hval9, '\r\n',
    '$', LENGTH(hkey10), '\r\n',hkey10, '\r\n','$', LENGTH(hval10), '\r\n', hval10, '\r')

FROM (SELECT
        "HMSET"                       AS redis_cmd,
        concat("hash_",code)          AS redis_key,
        concat("ip_bind_time")        AS hkey1,
        ip_bind_time                  AS hval1,
        concat("ip_time_out")         AS hkey2,
        ip_time_out                   AS hval2,
        concat("connect_count")       AS hkey3,
        connect_count                 AS hval3,
        concat("pwd")                 AS hkey4,
        pwd                           AS hval4,
        concat("iplist")              AS hkey5,
        iplist                        AS hval5,
        concat("token")               AS hkey6,
        token                         AS hval6,
        concat("token_expire")        AS hkey7,
        token_expire                  AS hval7,
        concat("limit_bandwidth")     AS hkey8,
        limit_bandwidth               AS hval8,
        concat("save_host")           AS hkey9,
        save_host                     AS hval9,
        concat("save_port")           AS hkey10,
        save_port                     AS hval10

      FROM channel_auth
      WHERE status=1)
  AS t
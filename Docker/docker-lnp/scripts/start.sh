#!/bin/bash

## 检测是否有自定义的 SERVER_NAME 环境变量, 存在则替换
if [ -n "$SERVER_NAME" ]; then
	sed -i "s/server_name .*/server_name $SERVER_NAME;/" /etc/nginx/conf.d/www.conf
fi

## 检测是否有自定义的 DOCUMENT_ROOT 环境变量, 存在则替换
if [ -n "$DOCUMENT_ROOT" ]; then
	sed -i "s#root .*#root $DOCUMENT_ROOT;#" /etc/nginx/conf.d/www.conf
fi

/usr/bin/supervisord -c /etc/supervisor/supervisord.conf

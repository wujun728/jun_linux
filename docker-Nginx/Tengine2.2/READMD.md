挂载参数：
1. `/etc/nginx/nginx.conf`：全局nginx配置。由于默认的配置`include /etc/nginx/conf.d/*.conf`，**因此不建议挂载该参数**。
2. `/etc/nginx/conf.d/`：nginx配置文件夹，挂载后，nginx可以加载该文件夹下所有的配置。**推荐**。
3. `/usr/share/nginx/html/`：html文件夹。**推荐**

例子：



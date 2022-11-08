**docker安装 dubbo**

2022-08-14 05:55:10

# 查看dubbo-admin镜像

![在这里插入图片描述](https://img-blog.csdnimg.cn/6a1ff69f31e445e986b20cd02d379968.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5oq56aaZ6bK45LmL5rW3,size_16,color_FFFFFF,t_70,g_se,x_16)

# 执行拉取指令，默认选择latest版本

```
 docker pull chenchuxin/dubbo-admin
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/c0ff7b010d1c417db8bf2ec8da2cd46b.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5oq56aaZ6bK45LmL5rW3,size_16,color_FFFFFF,t_70,g_se,x_16)

# 查看下载的镜像

```
docker images
```

# 启动容器

```
docker run -d 
--name dubbo-admin 
-v /home/keyan/dubbo/dubbo-admin:/data 
-p 8180:8080 
-e DUBBO_REGISTRY="zookeeper://192.168.8.145:2181" 
-e DUBBO_ROOT_PASSWORD=root 
-e DUBBO_GUEST_PASSWORD=guest 
--restart=always 
chenchuxin/dubbo-admin


# 注意 -e DUBBO_REGISTRY=zookeeper://ip:port  填写自己的zookeeper ip和端口号
# -e DUBBO_ROOT_PASSWORD 配置控制台root账号 密码
# -e DUBBO_GUEST_PASSWORD 配置控制台guest账号 密码
#-v 是宿主机与容器的挂载目录
#-p 是访问的端口号
```

# 访问

![在这里插入图片描述](https://img-blog.csdnimg.cn/e73218171f1549a6983dc60ff4d5d047.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5oq56aaZ6bK45LmL5rW3,size_16,color_FFFFFF,t_70,g_se,x_16)
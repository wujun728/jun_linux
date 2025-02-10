1. 创建镜像
  执行  `docker build -t bw/tomcat .` 命令
1. 进入容器：
  执行 `docker run -i -t -p 18080:8080 bw/tomcat` 
1. 启动tomcat:   
  1. `./usr/local/apache-tomcat-8.5.6/bin/startup.sh`
  1. 启动完后可以通过宿主机的18080端口访问，或通过Container的8080端口访问 
1. 也可以使用-v进行共享宿主机目录启动：
  1. `docker run -i -t -p 18080:8080 -v /home/ubuntu/docker:/opt/data bw/tomcat`
  1. 把主机的/usr/local/dockerData挂载到Container的/usr/local/docker目录上用于共享数据

1. 对容器进行修改后可以保存镜像用于以后继续使用

  `docker commit containerID bw/tomcat3` 把容器containerID保存为镜像

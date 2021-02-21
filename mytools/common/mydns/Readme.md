#shell 定制启动脚本；fig 启动脚本的名称与父目录相关,不能指定

#启动dns服务器，指定域名 aabb
docker run --name dns -v /var/run/docker.sock:/docker.sock phensley/docker-dns \
    --domain aabb.com
docker logs -f dns
#启动容器的时候指定DNS服务器，可选 使用--no-recursion 禁止外网访问
docker run -it --dns $(docker inspect -f '{{.NetworkSettings.IPAddress}}' dns) \
    --dns-search aabb.com debian:wheezy bash
    >cat /etc/resolv.conf
     nameserver 172.17.0.22
     search aabb.com
    >ping trusting_jang.aabb.com
     PING trusting_jang.aabb.com (172.17.0.23): 48 data bytes
     56 bytes from 172.17.0.23: icmp_seq=0 ttl=64 time=0.074 ms

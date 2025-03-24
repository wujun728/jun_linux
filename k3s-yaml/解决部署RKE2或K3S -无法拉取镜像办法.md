一、根因

        1、默认的仓库在docker你懂的。

二、修改拉取的仓库前缀

        1、创建文件

/etc/rancher/k3s/registries.yaml

k10-01:~ # cat /etc/rancher/k3s/registries.yaml
mirrors:
  docker.io:
    endpoint:
      - "https://m.daocloud.io"
        *填充上即可。 
————————————————

                            版权声明：本文为博主原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接和本声明。

原文链接：https://blog.csdn.net/weixin_46510209/article/details/143695739
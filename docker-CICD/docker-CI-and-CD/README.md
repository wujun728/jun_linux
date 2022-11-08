#CI and CD
## How to use ?
### master的部署:
    docker-compose -f docker-compose-jenkins.yml up -d 

### slave的部署:
    1. 在master节点上创建slave节点：
            系统管理---管理节点---新建节点---启动方法(Launch agent via Java Web Start)---save---获取步骤2使用的secret和slave name;
![jenkins-slave-1.png](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73191&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FD4%2FPaAvDFiFyoeAf_mlAAC7HTS9qi8984.png%3Ftoken%3D13c9eccd40fe50720de41b3327068606%26ts%3D1485163090%26attname%3Djenkins-slave-1.png)

    2. 执行jenkins-slave.sh脚本:
        ./jenkins-slave.sh <http://master-ip:port> <secret> <slave-name>
    
### 邮件通知的配置
#### 1. 配置发送者：
![jenkins-email-step-1.png](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73071&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FD2%2FPaAvDFiB0vGAAbzUAAAkX6EqgN4060.png%3Ftoken%3De4131802f2a3e69382e37fcda408923d%26ts%3D1484903142%26attname%3Djenkins-email-step-1.png)

#### 2. 配置SMTP相关信息：
![jenkins-email-step-2.png](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73072&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FD2%2FPaAvDFiB0vyATmbMAABQboaH9UQ129.png%3Ftoken%3Df8e44ac89aa61a939276dba8b19958a9%26ts%3D1484903414%26attname%3Djenkins-email-step-2.png)

#### 3. 测试效果：
![jenkins-email-step-3.png](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73073&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FD2%2FPaAvDFiB0waAJ9dwAAAOPx7Mx7U574.png%3Ftoken%3Da02506bf2a58ef80c2a09403c18ae8a8%26ts%3D1484903414%26attname%3Djenkins-email-step-3.png)

![jenkins-email-step-4.png](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73074&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FD2%2FPaAvDFiB0xiALt3AAAA1H_D2TUM915.png%3Ftoken%3Dbfd2f2ebcec3caacc2ded4bcff5f11be%26ts%3D1484903414%26attname%3Djenkins-email-step-4.png)

#### 4. Job配置：
![jenkins-email-step-5.png](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73167&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FD3%2FPaAvDFiFa4aAVHUBAAAzFGgUvu8686.png%3Ftoken%3Dc78b527a82007ed1001a621ed3334441%26ts%3D1485138784%26attname%3Djenkins-email-step-5.png)

注： 126邮箱收到的邮件，有可能被放入了垃圾邮件列表里面，所以要手动设置一下白名单！



# Gerrit and jekins 集成
## 启动并配置gerrit
### 1. 进入gerrit目录并执行gerrit.sh脚本:
		cd gerrit && ./gerrit.sh http://gerrit-ip:8080 (例如 ./gerrit.sh  http://9.186.91.71:8080)

### 2. 查看gerrit容器日志,出现如下日志记录表示gerrit启动成功:

![gerrit-start-ok.png](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73610&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDA%2FPaAvDFiagiWAVQ2gAAAjLW-32jM562.png%3Ftoken%3Da2465022c9f96be5f5d8e551d4b5d36c%26ts%3D1486520904%26attname%3Dgerrit-start-ok.png)

### 3. 配置gerrit与jenkins集成的相关配置:

#### 1. gerrit的初始配置：
![gerrit-init-config-1](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73620&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFiarS-AcBibAAAv0Qspsbo689.png%3Ftoken%3D8b1e784e7e007a3c3e455469e0de924a%26ts%3D1486531937%26attname%3Dgerrit-init-config-1.png)

![gerrit-init-config-2](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73621&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFiarTeAE9joAAB2wZcU2uw713.png%3Ftoken%3D8aba0996694b65223b82f172492fbeff%26ts%3D1486531937%26attname%3Dgerrit-init-config-2.png)

![gerrit-init-config-3](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73622&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFiarUOAZwOeAABQzfho_Q8220.png%3Ftoken%3D21237e383fd549481c378a3e495b0227%26ts%3D1486531937%26attname%3Dgerrit-init-config-3.png)

![gerrit-init-config-4](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73623&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFiarUyAVEO2AABbbs1opQ0012.png%3Ftoken%3D2c632c6a2582c691f7b135640f16088b%26ts%3D1486531937%26attname%3Dgerrit-init-config-4.png)

![gerrit-init-config-5](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73624&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFiarViAc4HIAABTeCO6yZQ958.png%3Ftoken%3Db9c18dbe2cf00839c817b0dab6ac3312%26ts%3D1486531937%26attname%3Dgerrit-init-config-5.png)

![gerrit-init-config-6](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73625&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFiarWGAOtaCAABDOZ4-RBM599.png%3Ftoken%3Dd1d540df06cf2afcc9e0865d76a548de%26ts%3D1486531937%26attname%3Dgerrit-init-config-6.png)

![gerrit-init-config-7](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73626&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFiarXaAVOv_AAB16vyZmGs999.png%3Ftoken%3D9c8c85bdfcaeeb8d3b6c1215a17a8e58%26ts%3D1486531937%26attname%3Dgerrit-init-config-7.png)
![gerrit-init-config-7-1](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73627&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFiarYCAMMB-AABHlcVRQYA494.png%3Ftoken%3D0b529a8596abf2e7d0ea99d7eafb6cca%26ts%3D1486531937%26attname%3Dgerrit-init-config-7-1.png)
![gerrit-init-config-7-2](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73628&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFiarYmAO8TFAAA1bBuF6v8019.png%3Ftoken%3Dcf8a06bc8bfcc1df8d25276c97555e39%26ts%3D1486532148%26attname%3Dgerrit-init-config-7-2.png)

![gerrit-init-config-8](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73629&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFiarZOAB2BRAABBkWmEIsI763.png%3Ftoken%3Dc3107a3065f17dc7c43ddb6ca2c56dfc%26ts%3D1486532148%26attname%3Dgerrit-init-config-8.png)
![gerrit-init-config-8-1](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73630&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFiarZ2ASAsgAAA7UiuGMpk715.png%3Ftoken%3De0bcb536213ee3bea6396edf9e7599d8%26ts%3D1486532148%26attname%3Dgerrit-init-config-8-1.png)

#### 2. 在gerrit中,添加Label Verified(此标签在jenkins用的上)： 

![gerrit-init-config-9](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73648&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3IWANdeqAABQucg6GF4864.png%3Ftoken%3D31dd06ebe90a2230d9d64db32f054245%26ts%3D1486544475%26attname%3Dgerrit-init-config-9.png)
![gerrit-init-config-9-1](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73649&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3I-AfXflAAA-neTv9tU047.png%3Ftoken%3Da14cdd8bc76efc6c0c8575675c2e0d99%26ts%3D1486544475%26attname%3Dgerrit-init-config-9-1.png)
![gerrit-init-config-9-2](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73650&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3JmAEFydAACoYNFx2KU925.png%3Ftoken%3Dd914cba4135eefd7f0e768400b9ee7ad%26ts%3D1486544475%26attname%3Dgerrit-init-config-9-2.png)
![gerrit-init-config-9-3](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73651&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3KSAXNDjAABrUHDU8fk987.png%3Ftoken%3Dee2da158e98f6ddb414ec57d50d0024e%26ts%3D1486544475%26attname%3Dgerrit-init-config-9-3.png)
![gerrit-init-config-9-4](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73652&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3LGAKPduAAB04tk-pZk691.png%3Ftoken%3D0b5b0ca16b6142a85e5c80ed9665a29c%26ts%3D1486544475%26attname%3Dgerrit-init-config-9-4.png)
![gerrit-init-config-9-5](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73653&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3L-AQqj4AAB0gQTSqlY862.png%3Ftoken%3Dae43766c33ef202d5227e49e2cd40599%26ts%3D1486544475%26attname%3Dgerrit-init-config-9-5.png)
![gerrit-init-config-9-6](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73654&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3M6ACoYaAAB1e66e4wI626.png%3Ftoken%3D826ff81f4012909e89d40e7273478221%26ts%3D1486544475%26attname%3Dgerrit-init-config-9-6.png)
![gerrit-init-config-9-7](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73655&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3NqAIZs3AABvbu_o1UY008.png%3Ftoken%3D0b5f4d85ff364bf6e758cce087e66477%26ts%3D1486544475%26attname%3Dgerrit-init-config-9-7.png)

#### 3. 配置gerrit中，与jenkins相关的权限配置:

![gerrit-init-config-10](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73656&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3OeAQBQ2AABqMizP7VU562.png%3Ftoken%3D16902aa8dae642b0fdc66897eb8f058e%26ts%3D1486544475%26attname%3Dgerrit-init-config-10.png)
![gerrit-init-config-10-1](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73657&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3PKAbp2zAAGdPDBsc1M990.png%3Ftoken%3D8a8a05af2624c92081e75b924286a3ea%26ts%3D1486544475%26attname%3Dgerrit-init-config-10-1.png)
![gerrit-init-config-10-2](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73658&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3P-Aa8mdAABSVp9cqXI784.png%3Ftoken%3D2bde07353bec17ca94e20c1c68c8fa5f%26ts%3D1486544475%26attname%3Dgerrit-init-config-10-2.png)
![gerrit-init-config-10-3](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73659&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3QuANpjZAABRvX8itlA388.png%3Ftoken%3D826372ce238c039cd7faafc4aa7bb275%26ts%3D1486544475%26attname%3Dgerrit-init-config-10-3.png)
![gerrit-init-config-10-4](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73660&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3RaAQRmLAABcTsjEePw631.png%3Ftoken%3D10250018f3ab87e5ac61f486d4811f8e%26ts%3D1486544475%26attname%3Dgerrit-init-config-10-4.png)
![gerrit-init-config-10-5](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73661&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3SGAHQL1AABl0Oz2yT8944.png%3Ftoken%3D1a04410ce3ddf0307a6f93029d356435%26ts%3D1486544475%26attname%3Dgerrit-init-config-10-5.png)
#### 4. 在jenkins中，配置gerrit Trigger：
![gerrit-init-config-11](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73662&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3TeATGSAAAKwNCfLuqE478.png%3Ftoken%3D12e69bd8679926669bfd5abf1f42c64f%26ts%3D1486544475%26attname%3Dgerrit-init-config-11.png)
![gerrit-init-config-11-1](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73663&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3UWAS4cFAABtYV8Cq1M668.png%3Ftoken%3D8cc312dddc06364790626458f2b5c07f%26ts%3D1486544475%26attname%3Dgerrit-init-config-11-1.png)
![gerrit-init-config-11-2](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73664&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3VGADV_YAAEoIdD6LIE000.png%3Ftoken%3D73e4a6a2ef6445e55bc624403d315970%26ts%3D1486544475%26attname%3Dgerrit-init-config-11-2.png)
![gerrit-init-config-11-3](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73665&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3WyANwEUAACrAWQqD9E222.png%3Ftoken%3Dab32acd395f2d101decdff5877996e57%26ts%3D1486545248%26attname%3Dgerrit-init-config-11-3.png)
![gerrit-init-config-11-4](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73666&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3XyAHEsMAACaQHpPMNw533.png%3Ftoken%3D40f39f355db6c7df00ba5a367e24a2b0%26ts%3D1486545248%26attname%3Dgerrit-init-config-11-4.png)
![gerrit-init-config-11-5](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73667&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3YiAG22WAAEWPf0hB_8117.png%3Ftoken%3D795fad7e78ebd48582223d393d21f2e6%26ts%3D1486545248%26attname%3Dgerrit-init-config-11-5.png)
![gerrit-init-config-11-6](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73668&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3ZGAIAktAAC7W6oVCec249.png%3Ftoken%3D67f4c6f5d9fdff769518b2c2bbe1f045%26ts%3D1486545248%26attname%3Dgerrit-init-config-11-6.png)

#### 5. 在gerrit中，创建要审查的项目：

![gerrit-init-config-12](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73669&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3Z-AXND8AABUqOIUPTw579.png%3Ftoken%3Db68965cd4bebdab446e1e24718a50463%26ts%3D1486545248%26attname%3Dgerrit-init-config-12.png)
![gerrit-init-config-12-1](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73670&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3auAK5uKAAA5-CyaeBM445.png%3Ftoken%3D333c3d3c074ef875b5396eecf0dba885%26ts%3D1486545248%26attname%3Dgerrit-init-config-12-1.png)
![gerrit-init-config-12-2](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73671&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3b-AANHBAABXeTp_YdA894.png%3Ftoken%3D5f80d62cd6529fc31bc35b36311941cf%26ts%3D1486545248%26attname%3Dgerrit-init-config-12-2.png)
![gerrit-init-config-12-3](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73672&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3cqAMtjvAAEkBuX1eOc959.png%3Ftoken%3Daac2a348cb1619f3f0610041f0d8d924%26ts%3D1486545248%26attname%3Dgerrit-init-config-12-3.png)
![gerrit-init-config-12-4](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73673&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3dOASAgiAAAvT8x0P7Y826.png%3Ftoken%3Df008b5f9b500b17902cf321cb9bdb85e%26ts%3D1486545248%26attname%3Dgerrit-init-config-12-4.png)
![gerrit-init-config-12-5](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73674&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3eCABiXiAADGMLQ9fNY419.png%3Ftoken%3D951521718cbdcd07c270a8e6061f7365%26ts%3D1486545248%26attname%3Dgerrit-init-config-12-5.png)

#### 6. 在jenkins中，配置gerrit Trigger需要调用的Job：

![gerrit-init-config-13](https://gitee.com/yonchin/CI-and-CD/attach_files/download?i=73675&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F00%2FDB%2FPaAvDFia3e2AWRn4AAHBL2sZ1do532.png%3Ftoken%3De97efe1a7180a9ed1698216c0763cc32%26ts%3D1486545248%26attname%3Dgerrit-init-config-13.png)
	

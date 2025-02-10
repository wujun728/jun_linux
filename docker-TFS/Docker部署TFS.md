# 使用TFS玩转Docker自动化部署

简介本文将介绍如何通过微软的Team Foundation Server平台，结合Docker完成程序的持续集成、持续部署。这里小编以.NET Core为例向大家分享整个DevOps流水线的搭建过程以及思路，其他语言平台均适用。 ![img](https://mmbiz.qpic.cn/mmbiz_jpg/3MRbgjUiaA2W5Vlfia3KcvdjH2TdxYTbCL5FWy26Wn1TNGSKMPib6jIVoOQCSB3YhMWtaJyyyOrKGLcgWmNM5KyQA/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1) *作者：周文洋**LEANSOFT研发总监，认证 Scrum Master，曾为多家客户提供微软Team Foundation Server实施咨询、二次开发、报表定制等服务，包括：中国农业银行，\*博时基金，\*斯伦贝谢，**京东商城，国电南自等，现负责公司核心产品的开发工作。****流水线概述\***开发人员编写代码，并提交代码到TFS配置库(Git TFVC), 触发持续集成。构建代理服务器拉取最新代码到服务器，**通过Docker容器完成应用的编译、测试工作**，并生成镜像推送到镜像仓库，最后**更新 docker-compose.yml镜像版本**并回传到TFS Build Artifact, 触发持续部署。构建代理服务器根据目标环境，**替换docker-compose.yml内的环境变量**，并复制docker-compose.yml文件到目标环境，运行应用。 ***流水线拓扑图\***![img](https://mmbiz.qpic.cn/mmbiz_png/3MRbgjUiaA2W5Vlfia3KcvdjH2TdxYTbCLpibf4s6cpvmGiahict2us0B2JWQhbWHlLXrtmc7eAHLP2xLuYbW7QfRIA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)***项目配置\***
在配置TFS持续集成之前，需要先在项目根目录下添加如下几个文件，每个文件独立分工，各负其责，以便我们完成后面的持续集成，持续部署。大家可以根据自己的实际需求来增减。![img](https://mmbiz.qpic.cn/mmbiz_png/3MRbgjUiaA2W5Vlfia3KcvdjH2TdxYTbCLMtM66XA7jRFTuMOKYVZWU9zr62PICtSjKial30xAOicmLzdmBb89Ve4Q/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)接下来分别看下几个文件的职责、说明以及具体实现方式。程序编译发布（容器内）：文件：docker-compose-ci.build.yml
说明：通过微软官方提供的aspnetcore-build镜像，完成.net core程序的编译以及发布。不需要自己安装编译环境，一旦编译完成，容器销毁。`version: '3'  services: labs-ci-build: image: devopslabs.azurecr.io/aspnetcore-build:1.0-1.1 volumes: - .:/src working_dir: /src command: /bin/bash -c "dotnet restore ./devopslabs/devopslabs.csproj &&  dotnet publish ./devopslabs/devopslabs.csproj  -c Release -o ./obj/Docker/publish"` ***代码说明：
***• 使用微软官方提供的aspnetcore-build:1.0-1.1 镜像，这里我们的镜像存储在微软的Azure Container Registry，大家也可以使用Harbor搭建企业内部的私有镜像仓库。
• 将当前目录（即程序根目录）映射到容器内的”/src”目录
• 工作目录设置为 “/src”目录执行dotnet restore以及dotnet publish命令，完成应用程序的编译以及发布。单元测试（容器内）：文件：docker-compose-test.yml
说明：通过微软官方提供的aspnetcore-build镜像，完成.net core程序的单元测试，并生成测试结果。`version: '3'  services: devopslabs-ci-test: image: devopslabs.azurecr.io/aspnetcore-build:1.0-1.1 volumes: - .:/src working_dir: /src/DevopslabsTest command: /bin/bash -c "dotnet restore ./DevopslabsTest.csproj  && dotnet test --logger "trx;logfilename=TEST.xml""`*
**代码说明：
***• 执行dotnet restore以及dotnet test命令，完成单元测试，并发布测试结果。镜像制作：文件：Dockerfile
说明：使用微软官方镜像aspnetcore，运行编译后的ASP.NET Core程序。`FROM devopslabs.azurecr.io/aspnetcore:1.1 ARG source WORKDIR /app EXPOSE 80 COPY ${source:-obj/Docker/publish} . ENTRYPOINT ["dotnet", "devopslabs.dll"]`***
代码说明：***
• 基础镜像为aspnetcore:1.1
• 声明变量source
• 设置RUN、CMD、ENTRYPOINT指令的工作路径为“/app”
• 容器对外暴漏80端口
• 如果环境变量source为空则复制”obj/Docker/publish”目录到容器的”/app”目录容器启动时执行”dotnet devopslabs.dll”命令部署编排：文件：docker-compose-template.yml
说明：编排模版文件，通过替换编排文件内的镜像标签版本，以及环境变量完成版本更新以及多环境不同配置的部署。`version: '2'  services: devopslabs: image: devopslabs.azurecr.io/devopslab:***%{Build.BuildId}%
***environment: - ASPNETCORE_ENVIRONMENT=***#{ASPNETCORE_ENVIRONMENT}#*** restart: always ports: - "81:80"  devopslabs_db: image: microsoft/mssql-server-linux environment: - ACCEPT_EULA=Y - SA_PASSWORD=******** - TZ=Asia/Shanghai restart: always volumes: - ~/sqlserverdata:/var/opt/mssql/ ports: - "1433:1433"`***
代码说明：\***
• 包含应用层，以及数据层服务
• 应用层的镜像标签为构建编号变量，在执行持续集成的时候被动态替换环境变量为占位符，需要在执行持续部署的时候，根据目标环境更新实际参数（Test、UAT、Production）***持续集成搭建\***
基础文件准备完成后，就可以配置TFS的持续集成了。
这里用到了两个插件并提供了插件市场的地址，大家可以自己下载安装：Docker Integration（微软提供的Docker集成工具）Replace Token （变量替换工具）创建构建定义，添加构建步骤：
![img](https://mmbiz.qpic.cn/mmbiz_gif/3MRbgjUiaA2W5Vlfia3KcvdjH2TdxYTbCLW1CWKWT9JCRpSqQN5RHAa2vgnzthkPzZVolKNg1anjRl8ZVv03CJeg/640?wx_fmt=gif&tp=webp&wxfrom=5&wx_lazy=1)

Step1：执行docker-compose-ci.build.yml文件，完成程序的编译，发布。
Step2：执行docker-compose-test.yml文件，完成程序的单元测试工作。
Step3：执行Dockerfile文件，完成镜像的构建。
Step4：推送镜像到私有镜像仓库。
Step5：更新docker-compose-template.yml的镜像版本 。
Step6：发布测试结果到TFS。
Step7：发布docker-compose-template.yml文件。
 *测试结果页面如下：
**![img](https://mmbiz.qpic.cn/mmbiz_png/3MRbgjUiaA2W5Vlfia3KcvdjH2TdxYTbCLyZNP7icgMmp3JOhastZgSBnjc7nicjGNLTvIVK3zq0L1853aWWxVM1hQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)* **Build Artifact：**![img](https://mmbiz.qpic.cn/mmbiz_png/3MRbgjUiaA2W5Vlfia3KcvdjH2TdxYTbCLeQnhUQXXV6BaMqwuUAHiayPAJicLudQWeibZlGe71vkjh5NzFA3DcpoTA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1) **注意**：这里的Build Artifact是带有最新镜像版本的编排文件，但是环境变量并没有替换，因为当前状态只是镜像版本确定了，具体是要部署的***目标环境暂时不清楚\***，所以暂时不做替换。***持续发布配置\***
说明：持续集成已经完成了镜像的生成以及推送，并生成了最新版本的docker-compose编排文件。接下来的工作就是在目标环境执行最新版本的docker-compose.yml完成应用的部署。创建发布环境- 测试环境：![img](https://mmbiz.qpic.cn/mmbiz_png/3MRbgjUiaA2W5Vlfia3KcvdjH2TdxYTbCLfJe6Mia32Csyfb9dicga5wh4FCBwnRXMnJAcRvFCv9omVQ1zUneIxdkg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)***设置环境变量：***
由于不同的部署环境往往需要使用不同的配置文件，这里就通过环境变量来决定需要使用哪个配置文件，添加环境变量ASPNETCORE_ENVIRONMENT，并设置对应值，如下图所示：***注意：这里小编只是Demo环境变量的使用方式，实际应用不建议将配置文件打包到容器。
******![img](https://mmbiz.qpic.cn/mmbiz_png/3MRbgjUiaA2W5Vlfia3KcvdjH2TdxYTbCLgkInTa7fxxKydz7NGvVUt473MBWX5ohiaicVibsGyMibicRRjkBMAlZuW1A/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)******发布步骤：***![img](https://mmbiz.qpic.cn/mmbiz_gif/3MRbgjUiaA2W5Vlfia3KcvdjH2TdxYTbCLxB31TrWWxESgZeicqVKdEjlicYAhhdkbFcl5kAFjeegJ58iaGSTeQyibTw/640?wx_fmt=gif&tp=webp&wxfrom=5&wx_lazy=1)*Step1*：替换环境变量
*Step2*：复制docker-compose.yml文件到目标环境
*Step3*：启动新版本容器，具体命令如下：`docker stop labs_devopslabs_1 *#停止容器
*docker rm labs_devopslabs_1 *#移除容器
*docker login devopslabs.azurecr.io -u devopslabs -p $(ACR_PASSWORD) *#登录镜像仓库，密码设置为环境变量，避免明文显示
*docker-compose -p labs -f docker-compose-template.yml up -d *#启动容器*`这样我们就完成了测试环境自动化发布的配置。

创建发布环境 – 生产环境：![img](https://mmbiz.qpic.cn/mmbiz_png/3MRbgjUiaA2W5Vlfia3KcvdjH2TdxYTbCLusj2thu6U5DlH7DSUtPofzRIS5x2k5DibUVSgBHv5o1AJrurPeVqouw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)部署步骤与测试环境一致，只需要调整部署目标环境以及修改相关环境变量。***仪表盘配置\***
可以在仪表盘上配置近期代码迁入，持续集成、持续部署情况、以及失败原因。![img](https://mmbiz.qpic.cn/mmbiz_png/3MRbgjUiaA2W5Vlfia3KcvdjH2TdxYTbCLCMIxH0EkvWtU4VoD6IrJvcIHWhIuxGjy9wG6Fj1QicNicD1yz86EiciaXw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)在TFS Wiki首页，配置当前项目下所有服务的构建状态以及部署状态。
![img](https://mmbiz.qpic.cn/mmbiz_png/3MRbgjUiaA2W5Vlfia3KcvdjH2TdxYTbCLlzUxLhicy0zjmBKF41b8uacA4GaaHdD1tfszxwSibw7NmibiaehgWDZJuA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)当前项目下所有服务的持续集成、持续部署状态。![img](https://mmbiz.qpic.cn/mmbiz_png/3MRbgjUiaA2W5Vlfia3KcvdjH2TdxYTbCLIYBKdJ2u89CA5FUWj7Dpr5tfic0xr6tXfiapDWt6GkUdtoBtGRia25ySQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)总结：DevOps流水线的搭建大大提高了我们产品的部署频率，测试环境每日可以达到几十次甚至上百次的部署频率。测试人员可以提早的介入测试，发现并反馈问题。容器化编译，让编译服务器更干净，稳定，有效预防了编译服务器软件之间的冲突。一台服务器可以支持多种语言环境的编译工作，大大降低了服务器成本，开发运维无须手工搭建环境，避免了环境不一致等问题。容器化部署，消除了环境差异问题，保证了环境的一致性，这一点我们特别有感触。我们服务器期间做过多次迁移，很难想象如果没有使用容器，这些复杂的服务部署能不能把我们累死。TFS强大的仪表盘，可以实时的看到当前项目下各个服务的状态，以及服务的发布频率，团队成员可以快速了解当前各个服务的健康状态，及早的发现并解决问题。
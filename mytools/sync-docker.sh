#!/usr/bin/env bash
# 通用工具构造
# 分拆到不同的项目，自动同步到版本库；进行自动镜像构建
rsync -avz  common/mydebian/*  /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-debian/
rsync -avz  common/myjava7/*  /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-jdk/
rsync -avz  common/myjre7/*  /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-jre/
rsync -avz  common/mysolr/*  /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-solr/

rsync -avz  common/mykafka/*  /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-kafka/
rsync -avz  common/myrabbitmq/*  /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-rabbitmq-base/
rsync -avz  common/myrabbitmq/rabbitmq/*  /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-rabbitmq/

rsync -avz  common/myflume/*  /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-myflume/
rsync -avz  common/mytwemproxy/*  /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-mytwemproxy/
rsync -avz  common/myredis/*  /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-myredis/
rsync -avz  common/mysql/*  /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-mysql/

rsync -avz  common/mystorm/storm/*  /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-storm/
rsync -avz  common/mystorm/storm-nimbus/*  /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-storm-nimbus/
rsync -avz  common/mystorm/storm-supervisor/*  /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-storm-supervisor/
rsync -avz  common/mystorm/storm-ui/*  /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-storm-ui/

rsync -avz  mymongodb/base/* /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-mongodb/

rsync -avz  web+app/mynginx/* /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-mynginx/
rsync -avz  web+app/mytomcat/*  /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-mytomcat/

# 同步到网上数据库


cd    /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-debian/
sh /Users/moyong/project/env-myopensource/3-tools/docker/mygit.sh  更新项目名称
cd   /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-jdk/
sh /Users/moyong/project/env-myopensource/3-tools/docker/mygit.sh  更新项目名称
cd   /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-jre/
sh /Users/moyong/project/env-myopensource/3-tools/docker/mygit.sh  更新项目名称
cd   /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-solr/
sh /Users/moyong/project/env-myopensource/3-tools/docker/mygit.sh  更新项目名称

cd   /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-kafka/
sh /Users/moyong/project/env-myopensource/3-tools/docker/mygit.sh  更新项目名称
cd   /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-rabbitmq-base/
sh /Users/moyong/project/env-myopensource/3-tools/docker/mygit.sh  更新项目名称
cd   /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-rabbitmq/
sh /Users/moyong/project/env-myopensource/3-tools/docker/mygit.sh  更新项目名称

cd   /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-myflume/
sh /Users/moyong/project/env-myopensource/3-tools/docker/mygit.sh  更新项目名称
cd   /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-mytwemproxy/
sh /Users/moyong/project/env-myopensource/3-tools/docker/mygit.sh  更新项目名称
cd   /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-myredis/
sh /Users/moyong/project/env-myopensource/3-tools/docker/mygit.sh  更新项目名称
cd   /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-mysql/
sh /Users/moyong/project/env-myopensource/3-tools/docker/mygit.sh  更新项目名称

cd   /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-storm/
sh /Users/moyong/project/env-myopensource/3-tools/docker/mygit.sh  更新项目名称
cd   /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-storm-nimbus/
sh /Users/moyong/project/env-myopensource/3-tools/docker/mygit.sh  更新项目名称
cd   /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-storm-supervisor/
sh /Users/moyong/project/env-myopensource/3-tools/docker/mygit.sh  更新项目名称
cd   /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-storm-ui/
sh /Users/moyong/project/env-myopensource/3-tools/docker/mygit.sh  更新项目名称

cd   /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-mongodb/
sh /Users/moyong/project/env-myopensource/3-tools/docker/mygit.sh  更新项目名称

cd   /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-mynginx/
sh /Users/moyong/project/env-myopensource/3-tools/docker/mygit.sh  更新项目名称
cd  /Users/moyong/project/env-myopensource/3-tools/docker/apps/docker-mytomcat/
sh /Users/moyong/project/env-myopensource/3-tools/docker/mygit.sh  更新项目名称

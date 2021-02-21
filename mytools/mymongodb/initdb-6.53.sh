#所有的服务器要通过IP地址进行通讯
#mac sed修改强制要求备份
#  rsync -avz -e ssh root@192.168.6.53:/file/mymongodb/initdbi*.js .
#初始化复制集1
cat initdbi-1.js
mongo  192.168.6.53:27018/test --quiet initdbi-1.js
sleep 3

#初始化复制集2
cat initdbi-2.js
mongo  192.168.6.53:27019/test --quiet initdbi-2.js
sleep 3

## 初始化Shard
cat initdbi.js
mongo  192.168.6.53:27017/admin --quiet initdbi.js

##
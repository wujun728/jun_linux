docker run -d elasticsearch

docker run -d supermy/elasticsearch:latest elasticsearch -Des.node.name="TestNode"


docker run -d -v "$PWD/config":/usr/share/elasticsearch/config elasticsearch

docker run -d -v "$PWD/esdata":/usr/share/elasticsearch/data elasticsearch



curl -XPUT http://192.168.59.103:9200/supermy/test/123 -d '{
    "name" : "史密斯"
}'

//索引
$ curl -XPUT http://192.168.59.103:9200/twitter/user/kimchy -d '{
    "name" : "Shay Banon"
}'

//索引，多个field
$ curl -XPUT http://192.168.59.103:9200/twitter/tweet/1 -d '{
    "user": "kimchy",
    "post_date": "2009-11-15T13:12:00",
    "message": "Trying out elasticsearch, so far so good?"
}'

//索引，注意url里面的id是不一样的哦
$ curl -XPUT http://192.168.59.103:9200/twitter/tweet/2 -d '{
    "user": "kimchy",
    "post_date": "2009-11-15T14:12:12",
    "message": "You know, for Search"
}'


//创建索引
curl -XPUT http://192.168.59.103:9200/twitter

//创建Mapping
curl -XPUT http://192.168.59.103:9200/twitter/user/_mapping -d '{
    "properties" : {
        "name" : { "type" : "string" }
    }
}'


//索引
curl -XPUT http://192.168.59.103:9200/twitter/tweet/2 -d '{
    "user": "kimchy",
    "post_date": "2009-11-15T14:12:12",
    "message": "You know, for Search"
}'

//获取
curl -XGET http://192.168.59.103:9200/twitter/tweet/2

-------------
//索引
curl -XPUT http://192.168.59.103:9200/twitter/tweet/2 -d '{
    "user": "kimchy",
    "post_date": "2009-11-15T14:12:12",
    "message": "You know, for Search"
}'

//lucene语法方式的查询
curl -XGET http://192.168.59.103:9200/twitter/tweet/_search?q=user:kimchy

//query DSL方式查询
curl -XGET http://192.168.59.103:9200/twitter/tweet/_search -d '{
    "query" : {
        "term" : { "user": "kimchy" }
    }
}'

//query DSL方式查询
curl -XGET http://192.168.59.103:9200/twitter/_search?pretty=true -d '{
    "query" : {
        "range" : {
            "post_date" : {
                "from" : "2009-11-15T13:00:00",
                "to" : "2009-11-15T14:30:00"
            }
        }
    }
}'

中文分词
https://github.com/supermy/elasticsearch-analysis-ik
http://my.oschina.net/u/579033/blog/394845#OSC_h4_18


http://www.elasticsearch.cn/guide/reference/setup/installation.html
分布式集群
http://my.oschina.net/u/579033/blog/394845
docker exec elasticsearch_fulltext_1  cat /etc/elasticsearch/elasticsearch.yml


http://www.learnes.net/distributed_cluster/README.html

http://tanjianna.diandian.com/post/2013-07-24/elasticsearch-aboutme

ElasticSearch的一些概念:
集群 (cluster)
在一个分布式系统里面,可以通过多个elasticsearch运行实例组成一个集群,这个集群里面有一个节点叫做主节点(master),elasticsearch是去中心化的,所以这里的主节点是动态选举出来的,不存在单点故障。
在同一个子网内，只需要在每个节点上设置相同的集群名,elasticsearch就会自动的把这些集群名相同的节点组成一个集群。节点和节点之间通讯以及节点之间的数据分配和平衡全部由elasticsearch自动管理。
在外部看来elasticsearch就是一个整体。
节点(node)
每一个运行实例称为一个节点,每一个运行实例既可以在同一机器上,也可以在不同的机器上.所谓运行实例,就是一个服务器进程.在测试环境内,可以在一台服务器上运行多个服务器进程,在生产环境建议每台服务器运行一个服务器进程
索引(index)
这里的索引是名词不是动词,在elasticsearch里面支持多个索引。类似于关系数据库里面每一个服务器可以支持多个数据库一样。在每一索引下面又支持多种类型，类似于关系数据库里面的一个数据库可以有多张表。但是本质上和关系数据库有很大的区别。这里暂时可以这么理解
 
分片(shards)
把一个索引分解为多个小的索引，每一个小的索引叫做分片。分片后就可以把各个分片分配到不同的节点中
 
副本(replicas)
每一个分片可以有0到多个副本，每个副本都是分片的完整拷贝，可以用来增加速度，同时也可以提高系统的容错性，一旦某个节点数据损坏，其他节点可以代替他.

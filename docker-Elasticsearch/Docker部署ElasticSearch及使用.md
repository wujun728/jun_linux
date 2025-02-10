.1 聊聊ElasticSearch的简介
​ Elaticsearch，简称为es， es是一个开源的高扩展的分布式全文检索引擎，它可以近乎实时的存储、检索数据；本身扩展性很好，可以扩展到上百台服务器，处理PB级别（大数据时代）的数据。es也使用Java开发并使用Lucene作为其核心来实现所有索引和搜索的功能，但是它的目的是通过简单的RESTful API来隐藏Lucene的复杂性，从而让全文搜索变得简单。

 据国际权威的数据库产品评测机构DB Engines的统计，在2016年1月，ElasticSearch已超过Solr等，成为排名第一的搜索引擎类应用。

ElasticSearch的小故事

 多年前，一个叫做Shay Banon的刚结婚不久的失业开发者，由于妻子要去伦敦学习厨师，他便跟着也去了。在他找工作的过程中，为了给妻子构建一个食谱的搜索引擎，他开始构建一个早期版本的Lucene。直接基于Lucene工作会比较困难，所以Shay开始抽象Lucene代码以便Java程序员可以在应用中添加搜 索功能。他发布了他的第一个开源项目，叫做“Compass”。

 后来Shay找到一份工作，这份工作处在高性能和内存数据网格的分布式环境中，因此高性能的、实时 的、分布式的搜索引擎也是理所当然需要的。然后他决定重写Compass库使其成为一个独立的服务叫做Elasticsearch。第一个公开版本出现在2010年2月，在那之后Elasticsearch已经成为Github上最受欢迎的项目之一，代 码贡献者超过300人。一家主营Elasticsearch的公司就此成立，他们一边提供商业支持一边开发新功能，不过Elasticsearch将永远开源且对所有人可用。

 Shay的妻子依旧等待着她的食谱搜索……

1.2 使用场景
1、维基百科，类似百度百科，全文检索，高亮，搜索推荐/2 （权重，百度！）

2、The Guardian（国外新闻网站），类似搜狐新闻，用户行为日志（点击，浏览，收藏，评论）+社交网络数据（对某某新闻的相关看法），数据分析，给到每篇新闻文章的作者，让他知道他的文章的公众 反馈（好，坏，热门，垃圾，鄙视，崇拜）

3、Stack Overﬂow（国外的程序异常讨论论坛），IT问题，程序的报错，提交上去，有人会跟你讨论和回答，全文检索，搜索相关问题和答案，程序报错了，就会将报错信息粘贴到里面去，搜索有没有对应的答案

4、GitHub（开源代码管理），搜索上千亿行代码

5、电商网站，检索商品

6、日志数据分析，logstash采集日志，ES进行复杂的数据分析，ELK技术， elasticsearch+logstash+kibana

7、商品价格监控网站，用户设定某商品的价格阈值，当低于该阈值的时候，发送通知消息给用户，比如 说订阅牙膏的监控，如果高露洁牙膏的家庭套装低于50块钱，就通知我，我就去买。

8、BI系统，商业智能，Business Intelligence。比如说有个大型商场集团，BI，分析一下某某区域最近3年的用户消费金额的趋势以及用户群体的组成构成，产出相关的数张报表，**区，最近3年，每年消费 金额呈现100%的增长，而且用户群体85%是高级白领，开一个新商场。ES执行数据分析和挖掘， Kibana进行数据可视化

9、国内：站内搜索（电商，招聘，门户，等等），IT系统搜索（OA，CRM，ERP，等等），数据分析（ES热门的一个使用场景）

1.3 ES的核心概念
​ ES是如何去存储数据，数据结构是什么，又是如何实现搜索的呢？我们先来聊聊ElasticSearch的相关概念吧！集群，节点，索引，类型，文档，分片，映射是什么？

1.31 与关系型数据库对比
Relational DB Elasticsearch
数据库(database) 索引 index
表(tables) 类型 types
行(rows) 文档 documents
字段(columns) ﬁelds
​ 综上所示，elasticsearch(集群)中可以包含多个索引(数据库)，每个索引中可以包含多个类型(表)，每个类型下又包 含多个文档(行)，每个文档中又包含多个字段(列)。

物理设计：

elasticsearch 在后台把每个索引划分成多个分片，每分分片可以在集群中的不同服务器间迁移一个人就是一个集群！默认的集群名称就是 elaticsearh

逻辑设计

一个索引类型中，包含多个文档，比如说文档1，文档2。 当我们索引一篇文档时，可以通过这样的一各顺序找到 它: **索引 ▷ 类型 ▷ 文档ID **，通过这个组合我们就能索引到某个具体的文档。 注意:ID不必是整数，实际上它是个字符串。就是我们的一条条数据。

1.32 文档
之前说elasticsearch是面向文档的，那么就意味着索引和搜索数据的最小单位是文档，elasticsearch中，文档有几个重要属性 :

自我包含，一篇文档同时包含字段和对应的值，也就是同时包含 key:value！
可以是层次型的，一个文档中包含自文档，复杂的逻辑实体就是这么来的！ {就是一个json对象！ fastjson进行自动转换！}
灵活的结构，文档不依赖预先定义的模式，我们知道关系型数据库中，要提前定义字段才能使用，在elasticsearch中，对于字段是非常灵活的，有时候，我们可以忽略该字段，或者动态的添加一个 新的字段。
尽管我们可以随意的新增或者忽略某个字段，但是，每个字段的类型非常重要，比如一个年龄字段类型，可以是字符 串也可以是整形。因为elasticsearch会保存字段和类型之间的映射及其他的设置。这种映射具体到每个映射的每种类型，这也是为什么在elasticsearch中，类型有时候也称为映射类型。

1.33 类型
​ 类型是文档的逻辑容器，就像关系型数据库一样，表格是行的容器。 类型中对于字段的定义称为映射， 比如 name 映 射为字符串类型。 我们说文档是无模式的，它们不需要拥有映射中所定义的所有字段， 比如新增一个字段，那么elasticsearch是怎么做的呢?elasticsearch会自动的将新字段加入映射，但是这 个字段的不确定它是什么类型，elasticsearch就开始猜，如果这个值是18，那么elasticsearch会认为它 是整形。 但是elasticsearch也可能猜不对， 所以最安全的方式就是提前定义好所需要的映射，这点跟关系型数据库殊途同归了，先定义好字段，然后再使用，别 整什么幺蛾子。

1.34 索引
​ 索引是映射类型的容器，elasticsearch中的索引是一个非常大的文档集合。索引存储了映射类型的字段 和其他设置。 然后它们被存储到了各个分片上了。 我们来研究下分片是如何工作的。

2.1 安装ElasticSearch
2.11 Windows安装
声明：JDK1.8 ，最低要求！ ElasticSearch 客户端，界面工具！官网：https://www.elastic.co/

下载地址：https://www.elastic.co/cn/downloads/elasticsearch 官网下载巨慢，FQ，网盘中下载即可！

1.下载完解压就可以使用了！

2.目录结构

3.启动，访问9200；

kibana启动同上述操作一样，不在赘述。
2.12 Docker安装
1.下载镜像
`docker pull elasticsearch:7.6.2`
2.创建挂载的目录
`mkdir -p /mydata/elasticsearch/config mkdir -p /mydata/elasticsearch/data echo "http.host: 0.0.0.0" >> /mydata/elasticsearch/config/elasticsearch.yml`
3.创建容器并启动
`docker run --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e ES_JAVA_OPTS="-Xms64m -Xmx128m" -v /mydata/elasticsearch/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml -v /mydata/elasticsearch/data:/usr/share/elasticsearch/data -v /mydata/elasticsearch/plugins:/usr/share/elasticsearch/plugins -d elasticsearch:7.6.2

其中elasticsearch.yml是挂载的配置文件，data是挂载的数据，plugins是es的插件，如ik，而数据挂载需要权限，需要设置data文件的权限为可读可写,需要下边的指令。
chmod -R 777 要修改的路径

-e "discovery.type=single-node" 设置为单节点
特别注意：
-e ES_JAVA_OPTS="-Xms256m -Xmx256m" \ 测试环境下，设置ES的初始内存和最大内存，否则导致过大启动不了ES

`
4.Kibana启动

`docker pull kibana:7.6.2
docker run --name kibana -e ELASTICSEARCH_HOSTS=http://自己的IP地址:9200 -p 5601:5601 -d kibana:7.6.2
//docker run --name kibana -e ELASTICSEARCH_URL=http://自己的IP地址:9200 -p 5601:5601 -d kibana:7.6.2

进入容器修改相应内容
server.port: 5601
server.host: 0.0.0.0
elasticsearch.hosts: [ "[http://自己的IP地址:9200](http://xn--ip-im8ckc388bqo2btxq:9200/)" ]
i18n.locale: "Zh-CN"

然后访问页面
[http://自己的IP地址:5601/app/kibana](http://xn--ip-im8ckc388bqo2btxq:5601/app/kibana)

`
2.2 kibana操作ElasticSearch
2.21 文档操作

1. _cat

`GET /_cat/node 查看所有节点 GET /_cat/health 查看es健康状况 GET /_cat/master 查看主节点 GET /_cat/indices 查看所有索引`
\2. 保存文档
保存一个数据，保存在那个索引的那个类型下，指定用唯一的标识，customer为索引,external为类型,1为标识。其中PUT和POST都可以，POST新增。如果不指定ID，会自动生成ID，指定ID就会修改这个数据，并新增版本号。PUT可以新增可以修改，PUT必须指定ID，一般都用来修改操作，不指定ID会报错

`PUT customer/external/1
{
"name":"张三"
}

返回结果
{
"_index" : "customer",
"_type" : "external",
"_id" : "1",
"_version" : 3,
"result" : "updated",
"_shards" : {
"total" : 2,
"successful" : 1,
"failed" : 0
},
"_seq_no" : 1001,
"_primary_term" : 2
}

`3. 查询文档`GET customer/external/1

结果:
{
"_index" : "customer", //在那个索引
"_type" : "external", //在那个类型
"_id" : "1", //记录ID
"_version" : 1, //版本号
"_seq_no" : 0, //并发控制字段，每次更新就+1，可用于乐观锁
"_primary_term" : 1, //主分片重新分配，如重启，就会变化
"found" : true, //true就是找到数据了
"_source" : { //数据
"name" : "张三"
}
}

`
\4. 更新文档

`POST操作带_update会对比原来的数据，如果是一样的那就不会更新了
POST customer/external/1/_update
{
"doc":{
"name":"你好"
}
}
POST操作不带_update会直接更新操作
POST customer/external/1
{
"name":"你好"
}

`5. 删除文档`DELETE customer/external/1`6. bulk批量API`需要加_bulk，然后请求体中的index是id，下边的是要保存的内容
POST customer/external/_bulk
{"index":{"_id":1}}
{"name":"榨干"}
{"index":{"_id":2}}
{"name":"你瞅啥"}

`7.查询操作 先导入批量的数据，在进行查询操作。`1.一种是通过REST request URI 发送搜索的参数，其中_search是固定写法，q=*是查询所有，sort=balance排序是按照balance排序的，asc是升序排序
GET customer/_search?q=*&sort=balance:asc

结果集，took是花费时间，timed_out没有超时，hits是命中的记录

2.另一种是通过REST request body 来发送，query代表查询条件，match_all是查询所有，sort代表排序条件
GET customer/_search
{
"query": {
"match_all": {}
},
"sort": [
{
"balance": "asc"
}
]
}

3.分页操作，from是从第几条数据开始，size是一页多少个，默认是十条数据
4.按需返回参数为，_source
GET customer/_search
{
"query": {
"match_all": {}
},
"sort": [
{
"balance": "asc"
}
],
"from": 11,
"size": 2,
"_source": ["account_number","balance"]
}

5.全文检索，使用match操作，查询的结果是按照评分从高到低排序的
GET customer/_search
{
"query": {
"match": {
"age": 20
}
}
}

6.match_phrase的精确匹配，
GET customer/_search
{
"query": {
"match_phrase": {
"age": 20
}
}
}

7.多字段匹配，multi_match
GET customer/_search
{
"query": {
"multi_match": {
"query": "mill",
"fields": ["address","email"]
}
}
}

8.复合查询bool，其中must是必须满足，must_not是必须不满足，should是应该满足，不过不满足的也能查出来，就是得分低，range是区间查询
GET customer/_search
{
"query": {
"bool": {
"must": [
{"match": {
"gender": "F"
}},
{"match": {
"address": "Mill"
}}
],
"must_not": [
{"match": {
"age": "38"
}}
],
"should": [
{"match": {
"lastname": "Long"
}}
]
}
}
}

9.filter过滤，区间查询操作，而且filter不会计算相关性得分
GET customer/_search
{
"query": {
"bool": {
"filter": [
{"range": {
"age": {
"gte": 10,
"lte": 30
}
}}
]
}
}
}

10.team查询，一些精确字段的推荐使用team，而一些全文检索的推荐使用match
GET customer/_search
{
"query": {
"term": {
"age": "28"
}
}
}

11.keyword的作用：当有keyword的时候，就会精确查找，而没有keyword的时候，这个值会当成一个关键字
GET customer/_search
{
"query": {"match": {
"address.keyword": "789 Madison"
}}
}

GET customer/_search
{
"query": {"match_phrase": {
"address": "789 Madison"
}}
}

`2.22 es分析功能（聚合函数）`搜索address中包含mill的所有人的年龄分布以及平均年龄，但不显示这些人的详情
其中，aggs代表使用聚合函数，terms为结果种类求和，avg为平均值，size为0则不显示详细信息
GET customer/_search
{
"query": {
"match": {
"address": "mill"
}
},
"aggs": {
"ageagg": {
"terms": {
"field": "age",
"size": 10
}
},
"ageavg":{
"avg": {
"field": "age"
}
}
},
"size": 0
}

聚合中还可以有子聚合
GET customer/_search
{
"query": {
"match_all": {}
},
"aggs": {
"ageagg": {
"terms": {
"field": "age",
"size": 10
},
"aggs": {
"ageAvg": {
"avg": {
"field": "balance"
}
}
}
}
},
"size": 0
}

`

3.1 rest-high-level-client整合ElasticSearch
1.导入依赖
`

<java.version>1.8</java.version>
<elasticsearch.version>7.6.2</elasticsearch.version>



```
    <!-- elasticsearch-rest-high-level-client -->
    <dependency>
        <groupId>org.elasticsearch.client</groupId>
        <artifactId>elasticsearch-rest-high-level-client</artifactId>
        <version>7.6.2</version>
    </dependency>
    
    <dependency>
        <groupId>com.alibaba</groupId>
        <artifactId>fastjson</artifactId>
        <version>1.2.68</version>
    </dependency>
```

`2.编写配置类`@Configuration
public class ElasticSearchClientConfig {
@Bean
public RestHighLevelClient restHighLevelClient(){
RestHighLevelClient client = new RestHighLevelClient(
RestClient.builder(
new HttpHost("自己的IP地址", 9200, "http")
)
);
return client;
}
}

`3进行es的索引操作`@Autowired
@Qualifier("restHighLevelClient")
private RestHighLevelClient client;
//index名字，静态一般都是放在另一个类中的
public static final String ES_INDEX="han_index";



```
//创建索引
@Test
public void createIndex() throws IOException {
    //1. 创建索引
    CreateIndexRequest index = new CreateIndexRequest(ES_INDEX);
    //2. 客户端执行请求,请求后获得相应
    CreateIndexResponse response = client.indices().create(index, RequestOptions.DEFAULT);
    //3.打印结果
    System.out.println(response.toString());
}
//测试索引是否存在
@Test
public void exitIndex() throws IOException{
    //1.
    GetIndexRequest request = new GetIndexRequest(ES_INDEX);
    boolean exists = client.indices().exists(request, RequestOptions.DEFAULT);
    System.out.println("是否存在"+exists);
}
//删除索引
@Test
public void deleteIndex() throws IOException{
    DeleteIndexRequest request = new DeleteIndexRequest(ES_INDEX);
    AcknowledgedResponse response = client.indices().delete(request, RequestOptions.DEFAULT);
    System.out.println("是否删除"+response);
}
```

`

4.es的文档操作

` @Autowired
@Qualifier("restHighLevelClient")
private RestHighLevelClient client;



```
public static final String ES_INDEX="han_index";

//创建文档
@Test
public void createDocument() throws IOException {
    //创建对象
    UserInfo userInfo = new UserInfo("张三",12);
    //创建请求
    IndexRequest request = new IndexRequest(ES_INDEX);
    //规则
    request.id("1").timeout(TimeValue.timeValueSeconds(1));
    //将数据放到请求中
    request.source(JSON.toJSONString(userInfo), XContentType.JSON);
    //客户端发送请求，获取相应的结果
    IndexResponse response = client.index(request, RequestOptions.DEFAULT);
    //打印一下
    System.out.println(response.toString());
    System.out.println(response.status());
}

//判断是否存在
@Test
public void exitDocument() throws IOException {
    GetRequest request = new GetRequest(ES_INDEX, "1");
    //不获取返回的_source 的上下文
    request.fetchSourceContext(new FetchSourceContext(false));
    request.storedFields("_none");

    boolean exists = client.exists(request, RequestOptions.DEFAULT);
    System.out.println(exists);
}

//获取文档信息
@Test
public void getDocument() throws IOException {
    GetRequest request = new GetRequest(ES_INDEX, "1");
    GetResponse response = client.get(request, RequestOptions.DEFAULT);
    System.out.println("获取到的结果"+response.getSourceAsString());
}

//更新文档
@Test
public void updateDocument() throws IOException {
    //创建对象
    UserInfo userInfo = new UserInfo("李四",12);

    UpdateRequest request = new UpdateRequest(ES_INDEX, "1");
    request.timeout("1s");

    request.doc(JSON.toJSONString(userInfo),XContentType.JSON);
    UpdateResponse response = client.update(request, RequestOptions.DEFAULT);
    System.out.println(response.status());
}

//删除文档
@Test
public void deleteDocument() throws IOException{
    DeleteRequest request = new DeleteRequest(ES_INDEX, "1");
    request.timeout("1s");

    DeleteResponse response = client.delete(request, RequestOptions.DEFAULT);
    System.out.println(response.status());
}

//批量添加
@Test
public void bulkDocument() throws IOException{
    BulkRequest request = new BulkRequest();
    request.timeout("10s");

    ArrayList<UserInfo> userInfos = new ArrayList<>();
    userInfos.add(new UserInfo("李四",1));
    userInfos.add(new UserInfo("李四",2));
    userInfos.add(new UserInfo("李四",3));
    userInfos.add(new UserInfo("李四",4));
    userInfos.add(new UserInfo("李四",5));
    userInfos.add(new UserInfo("李四",6));
    userInfos.add(new UserInfo("李四",7));

    //进行批处理请求
    for (int i = 0; i <userInfos.size() ; i++) {
        request.add(
                new IndexRequest(ES_INDEX)
                .id(""+(i+1))
                .source(JSON.toJSONString(userInfos.get(i)),XContentType.JSON));
    }

    BulkResponse response = client.bulk(request, RequestOptions.DEFAULT);
    System.out.println(response.hasFailures());
}

//查询
@Test
public void SearchDocument() throws IOException{
    SearchRequest request = new SearchRequest(ES_INDEX);
    //构建搜索条件
    SearchSourceBuilder builder = new SearchSourceBuilder();

    //查询条件使用QueryBuilders工具来实现
    //QueryBuilders.termQuery 精准查询
    //QueryBuilders.matchAllQuery() 匹配全部
    MatchQueryBuilder matchQuery = QueryBuilders.matchQuery("name", "李四");
    builder.query(matchQuery);
    builder.timeout(new TimeValue(60, TimeUnit.SECONDS));

    request.source(builder);

    SearchResponse response = client.search(request, RequestOptions.DEFAULT);
    System.out.println("查询出的结果"+JSON.toJSONString(response.getHits()));
}
```
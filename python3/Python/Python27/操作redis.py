# -*- coding:UTF-8 -*-
import redis
import time


class TestRedis:
    def __init__(self):
        self.dbconn = None

    def openRedis(self):
        # 连接redis，加上decode_responses=True，写入的键值对中的value为str类型，不加这个参数写入的则为字节类型。
        # r = redis.Redis(host=u'127.0.0.1', port=6379, db=0)
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, decode_responses=True)  # 使用连接池
        self.dbconn = redis.Redis(connection_pool=pool)

    def addKey(self, Key, Value):
        self.dbconn.set(Key, Value)

    def getKey(self, Key):
        return self.dbconn.get(Key)

    def setObj(self, name, value, ex=None, px=None, nx=False, xx=False):
        #   ex，过期时间（秒）
        #   px，过期时间（毫秒）
        #   nx，如果设置为True，则只有name不存在时，当前set操作才执行
        #   xx，如果设置为True，则只有name存在时，当前set操作才执行
        self.dbconn.set(name, value, ex=ex, px=px, nx=nx, xx=xx)
        pass

    def exAndpxDemo(self):
        # 演示过期时间, ex :秒 , px : 毫秒
        self.setObj("apple", "一个", ex=2)
        print self.getKey("apple")
        time.sleep(3)
        print self.getKey("apple")
        print "======================"
        self.setObj("banana", "two", px=2)
        print self.getKey("banana")
        time.sleep(0.3)
        print self.getKey("banana")

    def nxAandxxDemo(self):
        #   nx，如果设置为True，则只有name不存在时，当前set操作才执行 （新建）
        #   xx，如果设置为True，则只有name存在时，当前set操作才执行 （修改）
        self.addKey('grape', 'zhangsan')
        self.setObj("grape", "一个", nx=True)
        self.setObj("grape2", "一个2", nx=True)
        print self.getKey("grape")  # 此时是 zhangsan 并没有改为 一个
        print self.getKey("grape2")  # 此时是 一个2
        print "========================"
        self.setObj("grape2", "修改了", xx=True)  # grape2已经存在
        print self.getKey("grape2")  # 此时是 修改了
        self.setObj("grape3", "修改了", xx=True)  # grape3不存在 不会创建
        print self.getKey("grape3")  # None

    def listGet(self):
        # 将目前redis缓存中的键对应的值批量取出来
        print(self.dbconn.mget("grape", 'grape2'))
        print(self.dbconn.mget(['grape', 'grape2']))

    def getset(self):
        # 设置新值并获取原来的值
        print(self.dbconn.getset("grape", "aaa"))
        print(self.dbconn.getset("grape", "bbb"))

    def listSet(self):
        self.dbconn.mget({'k1': 'v1', 'k2': 'v2'})
        self.dbconn.mset(k1="v1", k2="v2")  # 这里k1 和k2 不能带引号 一次设置对个键值对

        opt = {
            "one": "aaa",
            "two": "bbb",
            "three": "ccc",
            4: 4
        }
        self.dbconn.mset(opt)

        print(self.dbconn.mget("k1", "k2"))  # 一次取出多个键对应的值
        print(self.dbconn.mget("one", "two", "three", 4))

    def addClick(self):
        self.dbconn.set("foo", 123)
        print(self.dbconn.mget("foo", "foo1", "foo2", "k1", "k2"))
        self.dbconn.incr("foo")  # 124
        self.dbconn.incr("foo")  # 125
        self.dbconn.decr("foo")  # 自减 124

        print(self.dbconn.mget("foo", "foo1", "foo2", "k1", "k2"))
        self.dbconn.set("foo1", "123.0")

        # 浮点型
        self.dbconn.set("foo1", "123.0")
        self.dbconn.set("foo2", "221.0")
        print(self.dbconn.mget("foo1", "foo2"))
        self.dbconn.incrbyfloat("foo1", amount=2.0)
        self.dbconn.incrbyfloat("foo2", amount=3.0)
        print(self.dbconn.mget("foo1", "foo2"))

    def hash(self):
        opt = {
            "sasa": {
                "v1": "1a",
                "v2": "2a"
            }
        }
        opts = {
            "v1": "1a",
            "v2": "2a"
        }

        self.dbconn.hset("hash1", "k2", "v2")
        self.dbconn.hmset("hash1", opt)
        self.dbconn.hmset("hash1", opts)

        # print(self.dbconn.hkeys("hash1"))                 # 取hash中所有的key
        # print(self.dbconn.hget("hash1", "k1"))            # 单个取hash的key对应的值
        # print(self.dbconn.hmget("hash1", "k1", "v3"))     # 多个取hash的key对应的值

        self.dbconn.hsetnx("hash1", "k3", "v3")    # 只能新建
        # print(self.dbconn.hkeys("hash1"))         # 取hash中所有的key

        print(self.dbconn.hget("hash1","k2"))            # 单个取出"hash2"的key-k2对应的value
        print(self.dbconn.hmget("hash1", "k2", "k3"))   # 批量取出"hash2"的key-k2 k3对应的value --方式1
        print(self.dbconn.hmget("hash1", ["k2", "k3"])) # 批量取出"hash2"的key-k2 k3对应的value --方式2

        print(self.dbconn.hgetall("hash1"))  #   获取name对应hash的所有键值
        print(self.dbconn.hlen("hash1"))     #   获取name对应的hash中键值对的个数
        print(self.dbconn.hkeys("hash1"))    #   获取name对应的hash中所有的key的值
        print(self.dbconn.hvals("hash1"))    #   获取name对应的hash中所有的value的值

        #检查name对应的hash是否存在当前传入的key
        print(self.dbconn.hexists("hash1", "k4"))  # False 不存在
        print(self.dbconn.hexists("hash1", "k1"))  # True 存在

        #删除键值对
        print(self.dbconn.hgetall("hash1"))
        self.dbconn.hset("hash1", "k1","v222")  # 修改已有的key k2
        self.dbconn.hset("hash1", "k11", "v1")  # 新增键值对 k11
        self.dbconn.hdel("hash1", "k11")         # 删除一个键值对
        print(self.dbconn.hgetall("hash1"))

        # 自增自减整数(将key对应的value - -整数
        # 自增1或者2，或者别的整数
        # 负数就是自减)
        # hincrby(name, key, amount=1)
        # 自增name对应的hash中的指定key的值，不存在则创建key = amount
        # 参数：
        # name，redis中的name
        # key， hash对应的key
        # amount，自增数（整数）

        self.dbconn.hset("hash1", "k3", 123)
        self.dbconn.hincrby("hash1", "k3", amount=-1)
        # print(self.dbconn.hgetall("hash1"))
        print(self.dbconn.hget("hash1", "k3"))  # 单个取出"hash2"的key-k3对应的value
        self.dbconn.hincrby("hash1", "k4", amount=1)  # 不存在的话，value默认就是1 print(r.hgetall("hash1"))
        print(self.dbconn.hget("hash1", "k4"))  # 单个取出"hash2"的key-k3对应的value

        #浮点数
        self.dbconn.hset("hash1", "k5", "1.0")
        self.dbconn.hincrbyfloat("hash1", "k5",amount=-1.0)  # 已经存在，递减-1.0
        self.dbconn.hincrbyfloat("hash1", "k6", amount=-1.0) # 不存在，value初始值是-1.0 每次递减1.0

        # 取值查看 - -分片读取
        # hscan(name, cursor=0, match=None, count=None)
        # 增量式迭代获取，对于数据大的数据非常有用，hscan可以实现分片的获取数据，并非一次性将数据全部获取完，从而放置内存被撑爆
        # 参数：
        # name，redis的name
        # cursor，游标（基于游标分批取获取数据）
        # match，匹配指定key，默认None
        # 表示所有的key
        # count，每次分片最少获取个数，默认None表示采用Redis的默认分片个数
        # 如：
        # 第一次：cursor1, data1 = r.hscan('xx', cursor=0, match=None, count=None)
        # 第二次：cursor2, data1 = r.hscan('xx', cursor=cursor1, match=None, count=None)
        # 直到返回值cursor的值为0时，表示数据已经通过分片获取完毕
        print(self.dbconn.hscan("hash1"))

        # hscan_iter(name, match=None, count=None)
        # 利用yield封装hscan创建生成器，实现分批去redis中获取数据
        # 参数：
        # match，匹配指定key，默认None
        # 表示所有的key
        # count，每次分片最少获取个数，默认None表示采用Redis的默认分片个数
        # 如：

        for item in self.dbconn.hscan_iter('hash1',match=None, count=None):
            print(item)

        print(self.dbconn.hscan_iter("hash1"))  # 生成器内存地址

    def redisList(self):
        # self.dbconn.lpush("list1", 44, 55, 66)    # 表示从左向右操作
        # print(self.dbconn.lrange('list1', 0, -1)) #切片取出值，范围是索引号0到-1(最后一个元素)

        # self.dbconn.rpush("list2", 44, 55, 66)  # 表示从右向左操作
        # print(self.dbconn.llen("list2"))  # 列表长度
        print(self.dbconn.lrange("list2", 0, -1))  # 切片取出值，范围是索引号0-3

        # 往已经有的name的列表的左边添加元素，没有的话无法创建
        # lpushx(name, value)
        # 在name对应的list中添加元素，只有name已经存在时，值添加到列表的最左边




    def main(self):
        r = self.openRedis()
        # self.dbconn.append("name", "haha")  # 在name对应的值junxi后面追加字符串haha
        # print(self.dbconn.mget("name"))

        self.addKey('grape', 'zhangsans')    # 添加
        # print self.getKey('grape')           # 获取
        # self.exAndpxDemo()
        # self.nxAandxxDemo()
        # self.listGet()
        # self.getset()                      #设置新值并获取原来的值
        # self.listSet()                      #批量设置值
        # self.addClick()                       #自增自减

        # redis基本命令 hash
        # self.hash()

        #redis基本命令 list
        self.redisList()

# 将目前redis缓存中的键对应的值批量取出来

if __name__ == '__main__':
    # r = redis.Redis(host='127.0.0.1', port=6379)
    # r.flushdb()
    # print r.dbsize()
    # r.set('foo', 'Bar')manager
    # print r.get('foo')https://gitee.com/DanBrown/Ordermeal.git

    testredis = TestRedis()
    testredis.main()

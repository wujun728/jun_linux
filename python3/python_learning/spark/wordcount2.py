from pyspark import SparkConf
from pyspark import SparkContext

def show(x):
    print(x)

if __name__ == '__main__':
    conf = SparkConf()
    conf.setAppName("wordcount")
    conf.setMaster("local")
    sc = SparkContext(conf=conf)
    lines = sc.textFile("./words", 2)
    print (lines.getNumPartitions())
    words = lines.flatMap(lambda line:line.split(" "), True)
    pairWords = words.map(lambda word : (word,1),True)
    result = pairWords.reduceByKey(lambda v1,v2:v1+v2, 3)
    print (result.getNumPartitions())
    result.foreach(lambda t :show(t))
    #将结果保存到文件
    result.saveAsTextFile("../../data/wc-result")

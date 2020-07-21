from pyspark import SparkContext
from pyspark.conf import SparkConf

def showResult(one):
    print(one);

if __name__=="__main__":
    conf = SparkConf();
    conf.setMaster("local");
    conf.setAppName("test");

    # 创建SparkContext对象
    sc = SparkContext(conf=conf);

    lines = sc.textFile("./words.txt");

    words = lines.flatMap(lambda lines: lines.split(" "));
    pairWords = words.map(lambda word:(word, 1))
    reduceResult = pairWords.reduceByKey(lambda v1, v2 : v1 + v2);
    reduceResult.foreach(lambda one : showResult(one))


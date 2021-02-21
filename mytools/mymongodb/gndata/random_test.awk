BEGIN {
# 设置AWK程序输出时各列的分隔符
OFS = "|";
srand();
#COUNT = 100000000;
COUNT = 10000000;
for (i=1; i<COUNT; i++) {
    print random_int(10, 100), random_float(3, 2), random_string("upper", 10), random_time("2009 06 01 12 30 30", "2011 07 15 23 59 59", "%Y-%m-%d %H:%M:%S");
}
}

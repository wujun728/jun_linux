Performance (Benchmark)
Intel(R) Core(TM) i7-4770 CPU @ 3.40GHz

MemTotal: 16376596 kB

Twemproxy:
redis-benchmark -p 22121 -c 500 -n 5000000 -P 100 -r 10000 -t get,set

Codis:
redis-benchmark -p 19000 -c 500 -n 5000000 -P 100 -r 10000 -t get,set

For Java users who want to support HA
[Jodis (HA Codis Connection Pool based on Jedis)] (https://github.com/wandoulabs/codis/tree/master/extern/jodis)

https://github.com/xetorthio/jedis

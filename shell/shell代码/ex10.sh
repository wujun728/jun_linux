#!/bin/sh
# select var in [params] do ... done
select var in "java" "c++" "php" "linux" "python" "ruby" "c#" 
do 
    break
done
echo "you selected $var"

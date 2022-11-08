#!/bin/bash

mysql -p$1 <<EOF
STOP SLAVE IO_THREAD;
STOP SLAVE;
RESET SLAVE;
change master to master_host='$2',master_port=$3,master_log_file='$4',master_log_pos=$5;
START SLAVE;
EOF
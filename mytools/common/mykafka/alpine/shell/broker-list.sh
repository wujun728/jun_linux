#!/usr/bin/env bash
BROKERS=$(for CONTAINER in $CONTAINERS; do docker port $CONTAINER 9092 | sed -e "s/0.0.0.0:/$HOST_IP:/g"; done)
echo $BROKERS | sed -e 's/ /,/g'
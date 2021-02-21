#!/bin/bash
#sysctl vm.overcommit_memory=1

set -e

if [ "$1" = 'redis-server' ]; then
	chown -R redis .
	exec gosu redis "$@"
fi

exec "$@"
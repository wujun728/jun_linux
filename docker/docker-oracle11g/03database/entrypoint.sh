#!/usr/bin/env bash

set -e

source /assets/colorecho

chmod 777 /u01/app/dpdump
chown -R oracle:oinstall /u01/app/dpdump

mkdir -p /u01/app/oradata/orcl/${USERNAME}
chown -R oracle:oinstall /u01/app/oradata/orcl/${USERNAME}

su oracle -c "/assets/entrypoint_oracle.sh"

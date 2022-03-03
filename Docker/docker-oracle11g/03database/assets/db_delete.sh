#!/usr/bin/env bash

set -e

source /assets/colorecho

trap "echo_red '******* ERROR: Something went wrong.'; exit 1" SIGTERM
trap "echo_red '******* Caught SIGINT signal. Stopping...'; exit 2" SIGINT

echo_yellow ""
echo_yellow "Delete Database Instance Start"
su oracle -c "/u01/app/oracle/product/11.2.0/dbhome_1/bin/dbca -silent -responseFile /assets/resp/db_delete.rsp"

echo_yellow ""
echo_yellow "Delete Database Instance End"

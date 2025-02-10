#!/usr/bin/env bash

set -e

source /assets/colorecho

trap "echo_red '******* ERROR: Something went wrong.'; exit 1" SIGTERM
trap "echo_red '******* Caught SIGINT signal. Stopping...'; exit 2" SIGINT

echo_yellow ""
echo_yellow "Modify /u01/app/oracle/product/11.2.0/dbhome_1/sysman/lib/ins_emagent.mk"
echo_yellow "在makefile中添加链接libnnz11库的参数,修改/u01/app/oracle/product/11.2.0/dbhome_1/sysman/lib/ins_emagent.mk"
echo_yellow "将\$(MK_EMAGENT_NMECTL)修改为:\$(MK_EMAGENT_NMECTL)-lnnz11"
su oracle -c "cp /u01/app/oracle/product/11.2.0/dbhome_1/sysman/lib/ins_emagent.mk /u01/app/oracle/product/11.2.0/dbhome_1/sysman/lib/ins_emagent.mk.bak"
su oracle -c "sed -i 's/\$(MK_EMAGENT_NMECTL)/\$(MK_EMAGENT_NMECTL)-lnnz11/g' /u01/app/oracle/product/11.2.0/dbhome_1/sysman/lib/ins_emagent.mk"

echo_yellow ""
echo_yellow "Create Database Instance Start"
su oracle -c "/u01/app/oracle/product/11.2.0/dbhome_1/bin/dbca -silent -responseFile /assets/resp/db_create.rsp"

echo_yellow ""
echo_yellow "Create Database Instance End"

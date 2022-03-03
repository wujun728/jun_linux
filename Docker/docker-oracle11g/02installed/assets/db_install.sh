#!/usr/bin/env bash

set -e

source /assets/colorecho

trap "echo_red '******* ERROR: Something went wrong.'; exit 1" SIGTERM
trap "echo_red '******* Caught SIGINT signal. Stopping...'; exit 2" SIGINT

echo_yellow ""
echo_yellow "Download Oracle Database 11g Install Package"
echo_yellow "Downloading ${INSTALL_ZIP1}"
wget -q -O /home/oracle/oracle_database_112040_Linux-x86-64_1.zip ${INSTALL_ZIP1}
echo_yellow "Downloading ${INSTALL_ZIP2}"
wget -q -O /home/oracle/oracle_database_112040_Linux-x86-64_2.zip ${INSTALL_ZIP2}

echo_yellow ""
echo_yellow "Unzip Oracle Database 11g Install Package"
unzip -q /home/oracle/oracle_database_112040_Linux-x86-64_1.zip -d /home/oracle
unzip -q /home/oracle/oracle_database_112040_Linux-x86-64_2.zip -d /home/oracle
echo_yellow ""
echo_yellow "Remove Oracle Database 11g Install Package"
rm -rf /home/oracle/oracle_database_*.zip

echo_yellow ""
echo_yellow "Installing Oracle Database 11g Software Start"
su oracle -c "/home/oracle/database/runInstaller -ignorePrereq -ignoreSysPrereqs -waitforcompletion -silent -responseFile /assets/resp/db_install.rsp 2>&1"
rm -rf /home/oracle/database

echo_yellow ""
echo_yellow "run /u01/app/oraInventory/orainstRoot.sh"
/u01/app/oraInventory/orainstRoot.sh

echo_yellow ""
echo_yellow "run /u01/app/oracle/product/11.2.0/dbhome_1/root.sh"
/u01/app/oracle/product/11.2.0/dbhome_1/root.sh

echo_yellow ""
echo_yellow "Installing Oracle Database 11g Software End"

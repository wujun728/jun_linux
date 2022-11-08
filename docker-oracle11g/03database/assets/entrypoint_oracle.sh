#!/usr/bin/env bash

set -e
source /assets/colorecho
source ~/.bashrc

alert_log="$ORACLE_BASE/diag/rdbms/orcl/$ORACLE_SID/trace/alert_$ORACLE_SID.log"
listener_log="$ORACLE_BASE/diag/tnslsnr/$HOSTNAME/listener/trace/listener.log"
pfile=$ORACLE_HOME/dbs/init$ORACLE_SID.ora

# monitor $logfile
monitor() {
    tail -F -n 0 $1 | while read line; do echo -e "$2: $line"; done
}

trap_db() {
    trap "echo_red 'Caught SIGTERM signal, shutting down...'; stop_db" SIGTERM;
    trap "echo_red 'Caught SIGINT signal, shutting down...'; stop_db" SIGINT;
}

# Check shared memory
check_shm() {
    echo_yellow ""
    echo_yellow "Checking shared memory..."
    df -h | grep "Mounted on" && df -h | egrep --color "^.*/dev/shm" || echo "Shared memory is not mounted."
}

# Reconfig listener
reconfig_lsnr() {
    echo_yellow ""
    echo_yellow "Reconfig listener for hostname : [$HOSTNAME]..."
    sed -i "s/(HOST.*)(/(HOST = $HOSTNAME)(/g" /u01/app/oracle/product/11.2.0/dbhome_1/network/admin/tnsnames.ora
    sed -i "s/(HOST.*)(/(HOST = $HOSTNAME)(/g" /u01/app/oracle/product/11.2.0/dbhome_1/network/admin/listener.ora
    echo_yellow "Show tnsnames.ora..."
    cat /u01/app/oracle/product/11.2.0/dbhome_1/network/admin/tnsnames.ora
    echo_yellow "Show listener.ora..."
    cat /u01/app/oracle/product/11.2.0/dbhome_1/network/admin/listener.ora
}

# Start listener
start_lsnr() {
    echo_yellow ""
    echo_yellow "Starting listener..."
    monitor $listener_log listener &
    lsnrctl start | while read line; do echo -e "lsnrctl: $line"; done
    MON_LSNR_PID=$!
}

# Start database
start_db() {
    echo_yellow ""
    echo_yellow "Starting database..."
    trap_db
    monitor $alert_log alertlog &
    MON_ALERT_PID=$!
    sqlplus / as sysdba <<-EOF |
        pro Starting with pfile='$pfile' ...
        startup;
        alter system register;
        exit 0
EOF
    while read line; do echo -e "sqlplus: $line"; done
    change_dpdump_dir
    change_default_file_dest
    change_profile_default_limit
    init_user_info
    import_script
    if [ $ENABLE_EM == "true" ]; then
        enable_em;
    fi
    wait $MON_ALERT_PID
}

# Stop database
stop_db() {
    trap '' SIGINT SIGTERM
    shut_immediate
    echo_yellow "Shutting down listener..."
    lsnrctl stop | while read line; do echo -e "lsnrctl: $line"; done
    kill $MON_ALERT_PID $MON_LSNR_PID
    exit 0
}

shut_immediate() {
    ps -ef | grep ora_pmon | grep -v grep > /dev/null && \
    echo_yellow "Shutting down the database..." && \
    sqlplus / as sysdba <<-EOF |
        set echo on
        shutdown immediate;
        exit 0
EOF
    while read line; do echo -e "sqlplus: $line"; done
}

# change_dpdump_dir
change_dpdump_dir () {
    echo_green ""
    echo_green "Changing dpdump dir to /u01/app/dpdump"
    sqlplus / as sysdba <<-EOF |
        create or replace directory data_pump_dir as '/u01/app/dpdump';
        commit;
        exit 0
EOF
    while read line; do echo -e "sqlplus: $line"; done
}

# change default file dest
change_default_file_dest() {
    echo_green ""
    echo_green "Changing default file dest as /u01/app/oradata"
    sqlplus / as sysdba <<-EOF |
        alter system set db_create_file_dest = '/u01/app/oradata';
        commit;
        exit 0
EOF
    while read line; do echo -e "sqlplus: $line"; done
}

# change profile default limit
change_profile_default_limit() {
    echo_green ""
    echo_green "Changing profile default limit : password_life_time/failed_login_attempts"
    sqlplus / as sysdba <<-EOF |
        alter profile default limit password_life_time unlimited;
        alter profile default limit failed_login_attempts unlimited;
        commit;
        exit 0
EOF
    while read line; do echo -e "sqlplus: $line"; done
}

# init user info
init_user_info() {
    echo_green ""
    echo_green "Initialise user info"
    sqlplus / as sysdba <<-EOF |
        @/assets/sql/init-user.sql "${USERNAME}" "${PASSWORD}" "orcl";
        commit;
        exit 0
EOF
    while read line; do echo -e "sqlplus: $line"; done
}

# import script
import_script() {
    echo_green ""
    echo_green "Importing Scripts from '/entrypoint-initdb.d':"
    for f in /entrypoint-initdb.d/*; do
        echo_green "found file $f"
        case "$f" in
            *.sh)     echo "[IMPORT] $0: running $f"; . "$f" ;;
            *.sql)    echo "[IMPORT] $0: running $f"; echo "exit" | su oracle -c "NLS_LANG=.$CHARACTER_SET $ORACLE_HOME/bin/sqlplus -S / as sysdba @$f"; echo ;;
            # *.dmp)    echo "[IMPORT] $0: running $f"; impdp $f ;;
            *)        echo "[IMPORT] $0: ignoring $f" ;;
        esac
        echo_green ""
    done
    echo_green "Import finished"
}

# enable em
enable_em() {
    echo_green ""
    echo_green "Enable Oracle Enterprise Manager..."
    sqlplus / as sysdba <<-EOF |
        alter user dbsnmp identified by "oracle";
        alter user sysman identified by "oracle";
        alter user dbsnmp account unlock;
        alter user sysman account unlock;
        commit;
        exit 0
EOF
    while read line; do echo -e "sqlplus: $line"; done
    /u01/app/oracle/product/11.2.0/dbhome_1/bin/emca -deconfig dbcontrol db -repos drop -silent -respfile /assets/resp/em_create.rsp
    /u01/app/oracle/product/11.2.0/dbhome_1/bin/emca -config dbcontrol db -repos create -silent -respfile /assets/resp/em_create.rsp
}

# Check shared memory
check_shm

# Reconfig listener
reconfig_lsnr

# Start listener
start_lsnr

# Start database
start_db

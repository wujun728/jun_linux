#!/bin/bash
# 在CentOS-6上使用yum -y install tomcat,生成 /etc/init.d/tomcat,内容如下
#
# chkconfig: - 80 20

# Source LSB function library.
if [ -r /lib/lsb/init-functions ]; then
    . /lib/lsb/init-functions
else
    exit 1
fi

DISTRIB_ID=`lsb_release -i -s 2>/dev/null`

NAME="$(basename $0)"
unset ISBOOT
if [ "${NAME:0:1}" = "S" -o "${NAME:0:1}" = "K" ]; then
    NAME="${NAME:3}"
    ISBOOT="1"
fi

# For SELinux we need to use 'runuser' not 'su'
if [ -x "/sbin/runuser" ]; then
    SU="/sbin/runuser -s /bin/sh"
else
    SU="/bin/su -s /bin/sh"
fi

# Get the tomcat config (use this for environment specific settings)
TOMCAT_CFG="/etc/tomcat/tomcat.conf"
if [ -r "$TOMCAT_CFG" ]; then
    . $TOMCAT_CFG
fi

# Get instance specific config file
if [ -r "/etc/sysconfig/${NAME}" ]; then
    . /etc/sysconfig/${NAME}
fi

# Define which connector port to use
CONNECTOR_PORT="${CONNECTOR_PORT:-8080}"

# Path to the tomcat launch script
TOMCAT_SCRIPT="${TOMCAT_SCRIPT:-/usr/sbin/tomcat}"

# Tomcat program name
TOMCAT_PROG="${NAME}"

# Define the tomcat username
TOMCAT_USER="${TOMCAT_USER:-tomcat}"

# Define the tomcat group
TOMCAT_GROUP="${TOMCAT_GROUP:-`id -gn $TOMCAT_USER`}"

# Define the tomcat log file
TOMCAT_LOG="${TOMCAT_LOG:-${CATALINA_HOME}/logs/${NAME}-initd.log}"

# Define the tomcat pid file
CATALINA_PID="${CATALINA_PID:-/var/run/${NAME}.pid}"

RETVAL="0"

# Look for open ports, as the function name might imply
function findFreePorts() {
    local isSet1="false"
    local isSet2="false"
    local isSet3="false"
    local lower="8000"
    randomPort1="0"
    randomPort2="0"
    randomPort3="0"
    local -a listeners="( $(
                        netstat -ntl | \
                        awk '/^tcp/ {gsub("(.)*:", "", $4); print $4}'
                    ) )"
    while [ "$isSet1" = "false" ] || \
          [ "$isSet2" = "false" ] || \
          [ "$isSet3" = "false" ]; do
        let port="${lower}+${RANDOM:0:4}"
        if [ -z `expr " ${listeners[*]} " : ".*\( $port \).*"` ]; then
            if [ "$isSet1" = "false" ]; then
                export randomPort1="$port"
                isSet1="true"
            elif [ "$isSet2" = "false" ]; then
                export randomPort2="$port"
                isSet2="true"
            elif [ "$isSet3" = "false" ]; then
                export randomPort3="$port"
                isSet3="true"
            fi
        fi
    done
}

function makeHomeDir() {
    if [ ! -d "$CATALINA_HOME" ]; then
        echo "$CATALINA_HOME does not exist, creating"
        if [ ! -d "/usr/share/${NAME}" ]; then
            mkdir /usr/share/${NAME}
            cp -pLR /usr/share/tomcat/* /usr/share/${NAME}
        fi
        mkdir -p /var/log/${NAME} \
                 /var/cache/${NAME} \
                 /var/tmp/${NAME}
        ln -fs /var/cache/${NAME} ${CATALINA_HOME}/work
        ln -fs /var/tmp/${NAME} ${CATALINA_HOME}/temp
        cp -pLR /usr/share/${NAME}/bin $CATALINA_HOME
        cp -pLR /usr/share/${NAME}/conf $CATALINA_HOME
        ln -fs /usr/share/java/tomcat ${CATALINA_HOME}/lib
        ln -fs /usr/share/tomcat/webapps ${CATALINA_HOME}/webapps
        install -o ${TOMCAT_USER} -g ${TOMCAT_GROUP} -d -m 0770 /var/log/${NAME}
    fi
}

function parseOptions() {
    options=""
    options="$options $(
                 awk '!/^#/ && !/^$/ { ORS=" "; print "export ", $0, ";" }' \
                 $TOMCAT_CFG
             )"
    if [ -r "/etc/sysconfig/${NAME}" ]; then
        options="$options $(
                     awk '!/^#/ && !/^$/ { ORS=" ";
                                           print "export ", $0, ";" }' \
                     /etc/sysconfig/${NAME}
                 )"
    fi
    TOMCAT_SCRIPT="$options ${TOMCAT_SCRIPT}"
}

# See how we were called.
function start() {

   echo -n "Starting ${TOMCAT_PROG}: "
   if [ "$RETVAL" != "0" ]; then
        start   
        ;;      
    condrestart|try-restart)
        if [ -s "$CATALINA_PID" ]; then 
            stop    
            start   
        fi      
        ;;      
    reload) 
        RETVAL="3"
        ;;      
    force-reload)
        if [ -s "$CATALINA_PID" ]; then 
            stop    
            start   
        fi      
        ;;      
    status) 
        if [ -s "$CATALINA_PID" ]; then 
            read kpid < $CATALINA_PID
            if [ -d "/proc/${kpid}" ]; then 
                log_success_msg "${NAME} (pid ${kpid}) is running..."
                RETVAL="0"
            else    
# The pid file exists but the process is not running 
               log_warning_msg "PID file exists, but process is not running"
               RETVAL="1"
            fi      
        else    
            pid="$(/usr/bin/pgrep -d , -u ${TOMCAT_USER} -G ${TOMCAT_USER} -f "catalina\.base=${CATALINA_BASE}[ $]")"
            if [ -z "$pid" ]; then 
#               status ${NAME} 
#               RETVAL="$?"
                log_success_msg "${NAME} is stopped"
                RETVAL="3"
            else    
                log_success_msg "${NAME} (pid $pid) is running..."
                RETVAL="0"
            fi      
        fi      
         if [ -f /var/lock/subsys/${NAME} ]; then 
            pid="$(/usr/bin/pgrep -d , -u ${TOMCAT_USER} -G ${TOMCAT_USER} -f "catalina\.base=${CATALINA_BASE}[ $]")"
# The lockfile exists but the process is not running 
            if [ -z "$pid" ]; then 
               log_failure_msg "${NAME} lockfile exists but process is not running"
               RETVAL="2"
            fi      
         fi      
        ;;      
    version)
        ${TOMCAT_SCRIPT} version 
        ;;      
    *)
      usage   
      ;;      
esac

exit $RETVAL
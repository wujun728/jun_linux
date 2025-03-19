#!/bin/sh
#chkconfig:35 80 20
#description:jetty.sh
ulimit -n 102400
ulimit -u 102400
#使用系统的JAVA_HOME变量
JAVA_HOME=$JAVA_HOME
JAVA_OPTIONS="-Xmn1024M -Xms2048M -Xmx2048M -XX:MaxPermSize=512M -Xconcurrentio -XX:SurvivorRatio=5 -XX:TargetSurvivorRatio=90 -XX:MaxTenuringThreshold=31 -XX:CMSInitiatingOccupancyFraction=90 -XX:MaxDirectMemorySize=256M -XX:+UseParNewGC -XX:+CMSParallelRemarkEnabled -XX:+UseConcMarkSweepGC -Djava.nio.channels.spi.SelectorProvider=sun.nio.ch.EPollSelectorProvider -Dsun.net.inetaddr.ttl=60 -Dorg.mortbay.jetty.Request.maxFormContentSize=-1"
JETTY_HOME=
JETTY_RUN=$JETTY_HOME/run

START_STOP_DAEMON=1

usage()
{
    echo "Usage: $0 {start|stop|run|restart|check|supervise} [ CONFIGS ... ] "
    exit 1
}

[ $# -gt 0 ] || usage


##################################################
# Some utility functions
##################################################

#获取程序的安装目录
PRG="$0"
while [ -h "$PRG" ] ; do
  ls=`ls -ld "$PRG"`
  link=`expr "$ls" : '.*-> \(.*\)$'`
  if expr "$link" : '/.*' > /dev/null; then
    PRG="$link"
  else
    PRG=`dirname "$PRG"`/"$link"
  fi
done

#如果JETTY_HOME的值是空字符串设置JETTY_HOME值
JETTY_HOME=${JETTY_HOME:-`dirname $PRG`}

findDirectory()
{
    OP=$1
    shift
    for L in $* ; do
        [ $OP $L ] || continue
        echo $L
        break
    done
}

running()
{
    [ -f $1 ] || return 1
    PID=$(cat $1)
    ps -p $PID >/dev/null 2>/dev/null || return 1
    return 0
}







##################################################
# Get the action & configs
##################################################

ACTION=$1
shift
ARGS="$*"
CONFIGS=""
NO_START=0

##################################################
# See if there's a default configuration file
##################################################
if [ -f /etc/default/jetty6 ] ; then
  . /etc/default/jetty6
elif [ -f /etc/default/jetty ] ; then
  . /etc/default/jetty
fi


##################################################
# See if there's a user-specific configuration file
##################################################
if [ -f $HOME/.jettyrc ] ; then
  . $HOME/.jettyrc
fi

##################################################
# Set tmp if not already set.
##################################################

if [ -z "$TMP" ]
then
  TMP=/tmp
fi

##################################################
# Jetty's hallmark
##################################################
JETTY_INSTALL_TRACE_FILE="etc/jetty.xml"
TMPJ=$TMP/j$$


##################################################
# Try to determine JETTY_HOME if not set
##################################################
if [ -z "$JETTY_HOME" ]
then
  JETTY_HOME_1=`dirname "$0"`
  JETTY_HOME_1=`dirname "$JETTY_HOME_1"`
  if [ -f "${JETTY_HOME_1}/${JETTY_INSTALL_TRACE_FILE}" ] ;
  then
     JETTY_HOME=${JETTY_HOME_1}
  fi
fi


##################################################
# if no JETTY_HOME, search likely locations.
##################################################
if [ "$JETTY_HOME" = "" ] ; then
  STANDARD_LOCATIONS="           \
        /usr/share               \
        /usr/share/java          \
        $HOME                    \
        $HOME/src                \
        ${HOME}/opt/             \
        /opt                     \
        /java                    \
        /usr/local               \
        /usr/local/share         \
        /usr/local/share/java    \
        /home                    \
        "
  JETTY_DIR_NAMES="              \
        jetty-6                  \
        jetty6                   \
        jetty-6.*                \
        jetty                    \
        Jetty-6                  \
        Jetty6                   \
        Jetty-6.*                \
        Jetty                    \
        "

  JETTY_HOME=
  for L in $STANDARD_LOCATIONS
  do
     for N in $JETTY_DIR_NAMES
     do
         if [ -d $L/$N ] && [ -f "$L/${N}/${JETTY_INSTALL_TRACE_FILE}" ] ;
         then
            JETTY_HOME="$L/$N"
         fi
     done
     [ ! -z "$JETTY_HOME" ] && break
  done
fi


##################################################
# No JETTY_HOME yet? We're out of luck!
##################################################
if [ -z "$JETTY_HOME" ] ; then
    echo "** ERROR: JETTY_HOME not set, you need to set it or install in a standard location"
    exit 1
fi

cd $JETTY_HOME
JETTY_HOME=`pwd`

#####################################################
# Check that jetty is where we think it is
#####################################################
if [ ! -r $JETTY_HOME/$JETTY_INSTALL_TRACE_FILE ]
then
   echo "** ERROR: Oops! Jetty doesn't appear to be installed in $JETTY_HOME"
   echo "** ERROR:  $JETTY_HOME/$JETTY_INSTALL_TRACE_FILE is not readable!"
   exit 1
fi


###########################################################
# Get the list of config.xml files from the command line.
###########################################################
if [ ! -z "$ARGS" ]
then
  for A in $ARGS
  do
    if [ -f $A ]
    then
       CONF="$A"
    elif [ -f $JETTY_HOME/etc/$A ]
    then
       CONF="$JETTY_HOME/etc/$A"
    elif [ -f ${A}.xml ]
    then
       CONF="${A}.xml"
    elif [ -f $JETTY_HOME/etc/${A}.xml ]
    then
       CONF="$JETTY_HOME/etc/${A}.xml"
    else
       echo "** ERROR: Cannot find configuration '$A' specified in the command line."
       exit 1
    fi
    if [ ! -r $CONF ]
    then
       echo "** ERROR: Cannot read configuration '$A' specified in the command line."
       exit 1
    fi
    CONFIGS="$CONFIGS $CONF"
  done
fi


##################################################
# Try to find this script's configuration file,
# but only if no configurations were given on the
# command line.
##################################################
if [ -z "$JETTY_CONF" ]
then
  if [ -f /etc/jetty.conf ]
  then
     JETTY_CONF=/etc/jetty.conf
  elif [ -f "${JETTY_HOME}/etc/jetty.conf" ]
  then
     JETTY_CONF="${JETTY_HOME}/etc/jetty.conf"
  fi
fi

##################################################
# Read the configuration file if one exists
##################################################
CONFIG_LINES=
if [ -z "$CONFIGS" ] && [ -f "$JETTY_CONF" ] && [ -r "$JETTY_CONF" ]
then
  CONFIG_LINES=`cat $JETTY_CONF | grep -v "^[:space:]*#" | tr "\n" " "`
fi

##################################################
# Get the list of config.xml files from jetty.conf
##################################################
if [ ! -z "${CONFIG_LINES}" ]
then
  for CONF in ${CONFIG_LINES}
  do
    if [ ! -r "$CONF" ]
    then
      echo "** WARNING: Cannot read '$CONF' specified in '$JETTY_CONF'"
    elif [ -f "$CONF" ]
    then
      # assume it's a configure.xml file
      CONFIGS="$CONFIGS $CONF"
    elif [ -d "$CONF" ]
    then
      # assume it's a directory with configure.xml files
      # for example: /etc/jetty.d/
      # sort the files before adding them to the list of CONFIGS
      XML_FILES=`ls ${CONF}/*.xml | sort | tr "\n" " "`
      for FILE in ${XML_FILES}
      do
         if [ -r "$FILE" ] && [ -f "$FILE" ]
         then
            CONFIGS="$CONFIGS $FILE"
         else
           echo "** WARNING: Cannot read '$FILE' specified in '$JETTY_CONF'"
         fi
      done
    else
      echo "** WARNING: Don''t know what to do with '$CONF' specified in '$JETTY_CONF'"
    fi
  done
fi

#####################################################
# Run the standard server if there's nothing else to run
#####################################################
if [ -z "$CONFIGS" ]
then
    CONFIGS="${JETTY_HOME}/etc/jetty-logging.xml ${JETTY_HOME}/etc/jetty.xml"
fi


#####################################################
# Find a location for the pid file
#####################################################
if [  -z "$JETTY_RUN" ]
then
  JETTY_RUN=`findDirectory -w /var/run /usr/var/run /tmp`
fi

#####################################################
# Find a PID for the pid file
#####################################################
if [  -z "$JETTY_PID" ]
then
  JETTY_PID="$JETTY_RUN/jetty.pid"
fi


##################################################
# Check for JAVA_HOME
##################################################
if [ -z "$JAVA_HOME" ]
then
    # If a java runtime is not defined, search the following
    # directories for a JVM and sort by version. Use the highest
    # version number.

    # Java search path
    JAVA_LOCATIONS="\
        /usr/java \
        /usr/bin \
        /usr/local/bin \
        /usr/local/java \
        /usr/local/jdk \
        /usr/local/jre \
	/usr/lib/jvm \
        /opt/java \
        /opt/jdk \
        /opt/jre \
    "
    JAVA_NAMES="java jdk jre"
    for N in $JAVA_NAMES ; do
        for L in $JAVA_LOCATIONS ; do
            [ -d $L ] || continue
            find $L -name "$N" ! -type d | grep -v threads | while read J ; do
                [ -x $J ] || continue
                VERSION=`eval $J -version 2>&1`
                [ $? = 0 ] || continue
                VERSION=`expr "$VERSION" : '.*"\(1.[0-9\.]*\)["_]'`
                [ "$VERSION" = "" ] && continue
                expr $VERSION \< 1.2 >/dev/null && continue
                echo $VERSION:$J
            done
        done
    done | sort | tail -1 > $TMPJ
    JAVA=`cat $TMPJ | cut -d: -f2`
    JVERSION=`cat $TMPJ | cut -d: -f1`

    JAVA_HOME=`dirname $JAVA`
    while [ ! -z "$JAVA_HOME" -a "$JAVA_HOME" != "/" -a ! -f "$JAVA_HOME/lib/tools.jar" ] ; do
        JAVA_HOME=`dirname $JAVA_HOME`
    done
    [ "$JAVA_HOME" = "" ] && JAVA_HOME=

    echo "Found JAVA=$JAVA in JAVA_HOME=$JAVA_HOME"
fi


##################################################
# Determine which JVM of version >1.2
# Try to use JAVA_HOME
##################################################
if [ "$JAVA" = "" -a "$JAVA_HOME" != "" ]
then
  if [ ! -z "$JAVACMD" ]
  then
     JAVA="$JAVACMD"
  else
    [ -x $JAVA_HOME/bin/jre -a ! -d $JAVA_HOME/bin/jre ] && JAVA=$JAVA_HOME/bin/jre
    [ -x $JAVA_HOME/bin/java -a ! -d $JAVA_HOME/bin/java ] && JAVA=$JAVA_HOME/bin/java
  fi
fi

if [ "$JAVA" = "" ]
then
    echo "Cannot find a JRE or JDK. Please set JAVA_HOME to a >=1.2 JRE" 2>&2
    exit 1
fi

JAVA_VERSION=`expr "$($JAVA -version 2>&1 | head -1)" : '.*1\.\([0-9]\)'`

#####################################################
# See if JETTY_PORT is defined
#####################################################
if [ "$JETTY_PORT" != "" ]
then
  JAVA_OPTIONS="$JAVA_OPTIONS -Djetty.port=$JETTY_PORT"
fi

#####################################################
# See if JETTY_LOGS is defined
#####################################################
if [ "$JETTY_LOGS" != "" ]
then
  JAVA_OPTIONS="$JAVA_OPTIONS -Djetty.logs=$JETTY_LOGS"
fi

#####################################################
# Are we running on Windows? Could be, with Cygwin/NT.
#####################################################
case "`uname`" in
CYGWIN*) PATH_SEPARATOR=";";;
*) PATH_SEPARATOR=":";;
esac


#####################################################
# Add jetty properties to Java VM options.
#####################################################
JAVA_OPTIONS="$JAVA_OPTIONS -Djetty.home=$JETTY_HOME -Djava.io.tmpdir=$TMP"

[ -f $JETTY_HOME/etc/start.config ] && JAVA_OPTIONS="-DSTART=$JETTY_HOME/etc/start.config $JAVA_OPTIONS"

#####################################################
# This is how the Jetty server will be started
#####################################################

JETTY_START=$JETTY_HOME/start.jar
[ ! -f $JETTY_START ] && JETTY_START=$JETTY_HOME/lib/start.jar

RUN_ARGS="$JAVA_OPTIONS -jar $JETTY_START $JETTY_ARGS $CONFIGS"
RUN_CMD="$JAVA $RUN_ARGS"

#####################################################
# Comment these out after you're happy with what
# the script is doing.
#####################################################
#echo "JETTY_HOME     =  $JETTY_HOME"
#echo "JETTY_CONF     =  $JETTY_CONF"
#echo "JETTY_RUN      =  $JETTY_RUN"
#echo "JETTY_PID      =  $JETTY_PID"
#echo "JETTY_ARGS     =  $JETTY_ARGS"
#echo "CONFIGS        =  $CONFIGS"
#echo "JAVA_OPTIONS   =  $JAVA_OPTIONS"
#echo "JAVA           =  $JAVA"


##################################################
# Do the action
##################################################
case "$ACTION" in
  start)
        echo -n "Starting Jetty: "

        if [ "$NO_START" = "1" ]; then
	  echo "Not starting jetty - NO_START=1 in /etc/default/jetty6";
          exit 0;
	fi


	if [ "$START_STOP_DAEMON" = "1" ] && type start-stop-daemon > /dev/null 2>&1
	then
          [ x$JETTY_USER = x ] && JETTY_USER=$(whoami)
	  [ $UID = 0 ] && CH_USER="-c $JETTY_USER"
	  if start-stop-daemon -S -p$JETTY_PID $CH_USER -d $JETTY_HOME -b -m -a $JAVA -- $RUN_ARGS
	  then
	      sleep 1
	      if running $JETTY_PID
	      then
                  echo OK
              else
                  echo FAILED
              fi
	  fi

	else

          if [ -f $JETTY_PID ]
          then
            if running $JETTY_PID
            then
              echo "Already Running!!"
              exit 1
            else
              # dead pid file - remove
              rm -f $JETTY_PID
            fi
          fi

          if [ x$JETTY_USER != x ]
          then
              touch $JETTY_PID
              chown $JETTY_USER $JETTY_PID
              su - $JETTY_USER -c "
                $RUN_CMD &
                PID=\$!
                disown \$PID
                echo \$PID > $JETTY_PID"
          else
              $RUN_CMD &
              PID=$!
              disown $PID
              echo $PID > $JETTY_PID
          fi

          echo "STARTED Jetty `date`"
        fi

        ;;

  stop)
        echo -n "Stopping Jetty: "
	if [ "$START_STOP_DAEMON" = "1" ] && type start-stop-daemon > /dev/null 2>&1; then
	  start-stop-daemon -K -p $JETTY_PID -d $JETTY_HOME -a $JAVA -s HUP
	  sleep 1
	  if running $JETTY_PID
	  then
	      sleep 3
	      if running $JETTY_PID
	      then
		  sleep 30
	          if running $JETTY_PID
	          then
	             start-stop-daemon -K -p $JETTY_PID -d $JETTY_HOME -a $JAVA -s KILL
		  fi
              fi
	  fi

	  rm -f $JETTY_PID
          echo OK
	else
	  PID=`cat $JETTY_PID 2>/dev/null`
          TIMEOUT=30
          while running $JETTY_PID && [ $TIMEOUT -gt 0 ]
          do
            kill $PID 2>/dev/null
            sleep 1
            let TIMEOUT=$TIMEOUT-1
          done

          [ $TIMEOUT -gt 0 ] || kill -9 $PID 2>/dev/null

	  rm -f $JETTY_PID
          echo OK
	fi
        ;;

  restart)
        JETTY_SH=$0
        if [ ! -f $JETTY_SH ]; then
          if [ ! -f $JETTY_HOME/bin/jetty.sh ]; then
            echo "$JETTY_HOME/bin/jetty.sh does not exist."
            exit 1
          fi
          JETTY_SH=$JETTY_HOME/bin/jetty.sh
        fi
        $JETTY_SH stop $*
        sleep 5
        $JETTY_SH start $*
        ;;

  supervise)
       #
       # Under control of daemontools supervise monitor which
       # handles restarts and shutdowns via the svc program.
       #
         exec $RUN_CMD
         ;;

  run|demo)
        echo "Running Jetty: "

        if [ -f $JETTY_PID ]
        then
            if running $JETTY_PID
            then
              echo "Already Running!!"
              exit 1
            else
              # dead pid file - remove
              rm -f $JETTY_PID
            fi
        fi

        exec $RUN_CMD
        ;;

  check)
        echo "Checking arguments to Jetty: "
        echo "JETTY_HOME     =  $JETTY_HOME"
        echo "JETTY_CONF     =  $JETTY_CONF"
        echo "JETTY_RUN      =  $JETTY_RUN"
        echo "JETTY_PID      =  $JETTY_PID"
        echo "JETTY_PORT     =  $JETTY_PORT"
        echo "JETTY_LOGS     =  $JETTY_LOGS"
        echo "CONFIGS        =  $CONFIGS"
        echo "JAVA_OPTIONS   =  $JAVA_OPTIONS"
        echo "JAVA           =  $JAVA"
        echo "CLASSPATH      =  $CLASSPATH"
        echo "RUN_CMD        =  $RUN_CMD"
        echo

        if [ -f $JETTY_RUN/jetty.pid ]
        then
            echo "Jetty running pid="`cat $JETTY_RUN/jetty.pid`
            exit 0
        fi
        exit 1
        ;;

*)
        usage
	;;
esac

exit 0
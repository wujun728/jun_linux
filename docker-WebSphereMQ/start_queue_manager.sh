export MYTEMPQM=TESTQM
export MYPORT=1414

source /opt/mqm/bin/setmqenv -s
crtmqm -u SYSTEM.DEAD.LETTER.QUEUE $MYTEMPQM
strmqm $MYTEMPQM
runmqsc $MYTEMPQM << EOF
  define listener(TCP.LISTENER) trptype(tcp) control(qmgr) port($MYPORT)
  start listener(TCP.LISTENER)
  define channel(SYSTEM.ADMIN.SVRCONN) chltype(SVRCONN) REPLACE
  set CHLAUTH(*) TYPE(BLOCKUSER) USERLIST('nobody','*MQADMIN')
  set CHLAUTH(SYSTEM.ADMIN.*) TYPE(BLOCKUSER) USERLIST('nobody')
EOF


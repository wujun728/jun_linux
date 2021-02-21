2016-03-22
    flume for alpine ok
    
gosu 启动方式不能正常运行

docker run --name flume-hdfs -e FLUME_AGENT_NAME=agent -d avastsoftware/flume-hdfs
docker run --name flume-hdfs -e FLUME_AGENT_NAME=agent-v /path/to/conf/dir:/opt/lib/flume/conf -d avastsoftware/flume-hdfs

Environment variable	Meaning	Default
FLUME_AGENT_NAME	Agent name. Agent specified in the configuration file needs to match this name.	No default (required setting)
FLUME_CONF_DIR	Flume configuration directory. This is where the configuration file is expected to be located.	/opt/lib/flume/conf
FLUME_CONF_FILE	Name of the Flume configuration file.	/opt/lib/flume/conf/flume-conf.properties

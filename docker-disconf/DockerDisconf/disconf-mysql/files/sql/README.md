MySQL启动后将依次执行本目录中的SQL以初始化

From official [MySQL Docker image doc](https://hub.docker.com/_/mysql/):

When a container is started for the first time, a new database mysql will be initialized with the provided configuration variables. Furthermore, it will execute files with extensions .sh and .sql that are found in /docker-entrypoint-initdb.d.
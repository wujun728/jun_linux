#基于debian-jre8

#build
```
docker build -t zub-server-610:dreamlu .
```

#run 进程守护
```
docker run -d -p 15555:15555 zub-server-610:dreamlu
```
## 说明oracle server-jre8u51

基于`buildpack-deps:jessie-curl`

已替换了lib\security目录下覆盖原来的文件，用于微信消息加解密

[Java Cryptography Extension (JCE) Unlimited Strength Jurisdiction Policy Files 8](http://www.oracle.com/technetwork/java/javase/downloads/jce8-download-2133166.html)

## build
```
docker build -t dreamlu/debian-jre8u51-weixin:latest .
```

## 直接从dockerhub pull
```
docker pull dreamlu/debian-jre8u51-weixin
```
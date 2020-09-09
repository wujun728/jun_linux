# 参考：https://github.com/gnulife/dphp/blob/master/alpine/build.sh制作。感谢！
FROM alpine
MAINTAINER Alpine Docker Maintainers "zhijiantianya@gmail.com"

RUN \
    # 阿里云镜像
    echo 'http://mirrors.aliyun.com/alpine/latest-stable/main' > /etc/apk/repositories \
    && echo '@community http://mirrors.aliyun.com/alpine/latest-stable/community' >> /etc/apk/repositories \
    && echo '@testing http://mirrors.aliyun.com/alpine/edge/testing' >> /etc/apk/repositories \
    && apk update \
    # 时区
    && TIMEZONE="Asia/Shanghai" \
    && apk add tzdata \
    && ln -snf /usr/share/zoneinfo/$TIMEZONE /etc/localtime \
    && echo $TIMEZONE > /etc/timezone

# 容器命令执行
CMD ["sh"]

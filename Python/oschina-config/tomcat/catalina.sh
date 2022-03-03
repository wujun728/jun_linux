# 在 catalina.sh 中加入以下两行

CATALINA_OPTS="-Djava.awt.headless=true -Djava.net.preferIPv4Stack=true"
JAVA_OPTS="-server -Xms4096m -Xmx4096m"

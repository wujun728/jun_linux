""" 欢迎关注 "码农架构" 微信公众号，热爱开源，拥抱开源。一个IT民工的技术之路经验分享。
    - 问题咨询 / 建议
    1.关注微信公众号 "码农架构" 后私信
    2.可发送邮件: li.shangzhi@aliyun.com
"""
import sys

# 日志告警这里有三个参数 %{type} %{path} %{message}
if len(sys.argv) == 4:
    print(sys.argv[0])  # 自身
    print("项目名：{type}, 日志路径 {path}，详细信息 {message}".format(type=sys.argv[1], path=sys.argv[2], message=sys.argv[3]))


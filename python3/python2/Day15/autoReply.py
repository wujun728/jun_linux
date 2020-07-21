""" 欢迎关注 "码农架构" 微信公众号，热爱开源，拥抱开源。一个IT民工的技术之路经验分享。
    - 问题咨询 / 建议
    1.关注微信公众号 "码农架构" 后私信
    2.可发送邮件: li.shangzhi@aliyun.com
"""
# 收到某个人的消息之后，自动回复，并播放声音提示
from wxpy import *
import winsound

bot = Bot()
my_friend = bot.friends().search("iByte")[0]


@bot.register(my_friend)
def reply_my_friend(msg):
    print(11)
    print(msg.text, msg.sender)
    winsound.MessageBeep(winsound.MB_ICONHAND)


bot.join()





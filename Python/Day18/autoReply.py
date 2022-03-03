# 收到某个人的消息之后，自动回复，并播放声音提示
from wxpy import *
import winsound

bot = Bot()
tuling = Tuling(api_key='77aa5b955fcab122b096f2c2dd8434c8')
my_friend = bot.groups().search("爪哇笔记")[0]


@bot.register(my_friend)
def reply_my_friend(msg):
    print(11)
    tuling.do_reply(msg)
    print(msg.text, msg.sender)
    print(tuling.reply_text(msg))
    winsound.MessageBeep(winsound.MB_ICONHAND)


bot.join()





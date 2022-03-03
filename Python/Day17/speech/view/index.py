import os
import time
import codecs
from aip import AipSpeech
from django.shortcuts import render
from django.http import HttpResponse


'''
pip install --upgrade pip
pip install baidu-aip
'''


def main(request):
    return render(request, 'index.html')


def m_main(request):
    return render(request, 'm_index.html')


def convert(request):
    message = request.POST.get("message")
    switch = request.POST.get("switch")
    mp3 = du_say(message, switch)
    return HttpResponse(mp3)


def du_say(message, switch):
    write_txt(message)
    app_id = '*****'
    api_key = 'sYi4GIqdPrzC4K80IFvA29pD'
    secret_key = 'rhF5SHsEuUAz3cs3TgTpj4jllTn11gFG'
    client = AipSpeech(app_id, api_key, secret_key)
    if switch == "true":
        switch = 3
    else:
        switch = 4
    result = client.synthesis(message, 'zh', 1, {
        'vol': 5, 'per': switch,
    })
    t = time.time()
    now_time = lambda: int(round(t * 1000))
    path = os.getcwd() + os.path.sep + "static" + os.path.sep + "audio"+os.path.sep
    audio = path+str(now_time())+'.mp3'
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open(audio, 'wb') as f:
            f.write(result)
    return str(now_time())+'.mp3'


def write_txt(message):
    t = time.time()
    now_time = lambda: int(round(t * 1000))
    path = os.getcwd() + os.path.sep + "static" + os.path.sep + "text"+os.path.sep
    text = path+str(now_time())+'.txt'
    with codecs.open(text, 'a', encoding='utf8')as f:
        f.write(message)


if __name__ == '__main__':
    du_say("哈哈哈哈", "true")


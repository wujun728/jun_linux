from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from utils.qr_code import decode_qr_code


def main(request):
    print(os.path.join(settings.BASE_DIR, 'image'))
    return render(request, 'index.html')


@csrf_exempt
def upload(request):
    # 元组类型，这里上传一张图片，取第一个元素即可
    img = request.FILES.get('img'),
    name = img[0].name
    f = open(os.path.join('static\\images', name), 'wb')
    for chunk in img[0].chunks():
        f.write(chunk)
    f.close()
    results = decode_qr_code(os.path.join('static\\images', name))
    if len(results):
        context = {'context': results[0].data.decode("utf-8")}
    else:
        context = {'context': "兄弟，请你传一个正常的二维码"}
    return render(request, 'show.html', context)

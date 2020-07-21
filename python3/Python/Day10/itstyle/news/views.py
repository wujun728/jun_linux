from django.shortcuts import render
from django.http.response import HttpResponse
from news.models import News


def index(request):
    return render(request, 'index.html')


def get_new(request):
    result = News.objects.get(title="面试官视角看面试")
    # print(result.id)
    # print(result.title)
    # print(result.content)
    context = {'news': result}
    return render(request, 'news.html', context)


def get_news(request, news_id):
    result = News.objects.get(id=news_id)
    context = {'news': result}
    return render(request, 'news.html', context)


# 接收POST请求数据
def search_post(request):
    print(request.POST['content'])
    context = request.POST['content']
    return HttpResponse(context, content_type="application/json")


def page_not_found(request):
    return render(request, '404.html')


def page_error(request):
    return render(request, '500.html')


def permission_denied(request):
    return render(request, '403.html')



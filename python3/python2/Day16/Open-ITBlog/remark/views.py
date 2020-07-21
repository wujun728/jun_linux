from django.shortcuts import render
from .models import Remark,ArticleReply
from article.models import ArticlePost
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def remark(request,id):
    if request.method == 'POST':
        n_remark = Remark()
        name = request.user
        text = request.POST.get('text','')
        aid = id

        n_remark.name = name
        n_remark.text = text
        n_remark.aid = aid

        n_remark.save()

        return HttpResponseRedirect(
            reverse('remark:remark',args=(id,))
        )
    else:

        r_remark = Remark.objects.filter(aid=id)
        article = ArticlePost.objects.get(id=id)

        articleReply = ArticleReply.objects.all()
        context = {
            'remark': r_remark,
            'article': article,
            'articleReply': articleReply,
        }
        return render(request,'article/detail.html',context)

def reply(request,id,aid):
    if request.user.is_authenticated:
        reply = 1
        cid =id
        r_remark = Remark.objects.filter(aid=aid)
        article = ArticlePost.objects.get(id=aid)
        articleReply = ArticleReply.objects.all()

        context = {
            'remark': r_remark,
            'article': article,
            'reply': reply,
            'articleReply': articleReply,
            'cid': cid,
             }
        return render(request,'article/detail.html',context)
    else:
        return HttpResponseRedirect('/userprofile/login')


def commit(requeset,id,aid):
    if requeset.method == 'GET':
        article = ArticlePost.objects.get(id=aid)
        remark = Remark.objects.all()
        articleReply = ArticleReply.objects.all()
        context = {
            'article': article,
            'remark': remark,
            'articleReply': articleReply,
        }

        return render(requeset,'article/detail.html',context)

    else:
        ar_commit = ArticleReply()

        ar_commit.name = requeset.user
        ar_commit.text = requeset.POST.get('text','')
        ar_commit.modelsid = id
        ar_commit.save()

        return HttpResponseRedirect(
            reverse('remark:commit',args=(id,aid))
        )
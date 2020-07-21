from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import *
# Create your views here.
from .models import *
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.views.generic.edit import FormView
from remark.models import Remark,ArticleReply
import markdown

def article_list(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        #articles = ArticlePost.objects.filter(author_id=user_id)
        articles = ArticlePost.objects.all()
        context = { 'articles':articles }
        return  render(request,'article/list.html',context)
    else:
        articles = ArticlePost.objects.all()
        context = { 'articles':articles }
        return render(request,'article/list.html',context)

#login_required(login_url='/userprofile/login/')
def article_detail(request,id):
    article = ArticlePost.objects.get(id = id)
    remark = Remark.objects.filter(aid=id)
    article.body = markdown.markdown(article.body,
                                     extensions = [
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                         'markdown.extensions.toc',
                                     ])

    remark = Remark.objects.all()
    articleReply = ArticleReply.objects.all()
    context = {
        'article': article,
        'remark': remark,
        'articleReply': articleReply,
    }
    return  render(request,'article/detail.html',context)



@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            print(request.POST)
            new_article = article_post_form.save(commit=False)
            user_id = request.user.id
            new_article.author = User.objects.get(id=user_id)
            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form = ArticlePostForm()
        context = { 'article_post_form':article_post_form }
        return render(request,'article/create.html',context)

@login_required(login_url='/userprofile/login/')
def article_delete(request,id):
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect("article:article_list")

@login_required(login_url='/userprofile/login/')
def article_update(request,id):
    article = ArticlePost.objects.get(id=id)
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)

        if article_post_form .is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()

            return redirect("article:article_detail",id = id)
        else:
            return HttpResponse("表单内容有误，请重新填写")

    else:
        article_post_form = ArticlePostForm()
        context = {'article':article,'article_post_form':article_post_form}
        return render(request,'article/update.html',context)

def remark(request):
    if request.method == "POST":
        form = RemarkForm(request.POST)
        if form.is_valid():
            myremark = Remark()
            myremark.subject = form.cleaned_data['subject']
            myremark.mail = form.cleaned_data['mail']
            myremark.topic = form.cleaned_data['topic']
            myremark.message = form.cleaned_data['message']
            myremark.cc_myself = form.cleaned_data['cc_myself']
            myremark.save()
    else:
        form = RemarkForm()

    ctx = {
        'form':form,
        'ties':Remark.objects.all()
    }

    return render(request,'article/message.html',)

def article_own(request):
    articles = ArticlePost.objects.filter(author_id=request.user.id)


    # articles.body = markdown.markdown(articles.body,
    #                                  extensions = [
    #                                      'markdown.extensions.extra',
    #                                      'markdown.extensions.codehilite',
    #                                      'markdown.extensions.toc',
    #                                  ])
    context = {'articles': articles}
    return  render(request,'article/own.html',context)


def searchtag(request,category):
    tag = category
    articles = ArticlePost.objects.filter(category=category)

    context = {
        'articles':articles,
    }
    return render(request,'article/tag.html',context)
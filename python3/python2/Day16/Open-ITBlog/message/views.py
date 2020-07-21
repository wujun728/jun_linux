from django.shortcuts import render
from .models import Message,Commit
from django.http import HttpResponseRedirect
from django.db import models
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse

# Create your views here.
def get_message(request):
    return render(request,'msg.html')

def get_content(request):
    if request.method == 'POST':
        if request.POST['name'] == '' and  request.POST['message'] == '':
            return HttpResponse("<h2>表单填写有误</h2>")
        else:
            name = request.POST.get('name','')
            email = request.POST.get('email','')
            message = request.POST.get('message','')

            Q_message = Message()
            Q_message.name = name
            Q_message.email = email
            Q_message.text = message

            Q_message.save()
            return HttpResponseRedirect('/message/message-list/')
    else:
        return render(request,'msg.html')

def message_list(request):
    objs = Message.objects.all()
    comObjs = Commit.objects.all()
    context = {
        'comObjs': comObjs,
        'objs': objs,
    }
    return render(request, 'message-list.html', context)


def reply(request,id):
    if request.user.is_authenticated:
        uid=id
        relay = 1
        comObjs = Commit.objects.all()
        objs = Message.objects.all()
        context = {
            'comObjs': comObjs,
            'relay':relay,
            'objs': objs,
            'uid':uid,
            }

        return render(request,'message-list.html',context)
    else:
        return HttpResponseRedirect('/userprofile/login')

def commit(request,id):
    if request.method == 'GET':

        cuid=id
        objs = Message.objects.all()
        comObjs = Commit.objects.all()
        print(cuid)
        context = {
            'comObjs':comObjs,
            'cuid': cuid,
            'objs': objs,
        }
        return render(request,'message-list.html',context)
    else:
        st_commit = Commit()
        name=request.user
        text=request.POST.get('text','')
        st_commit.name = name
        st_commit.text = text
        st_commit.mid = id
        st_commit.save()

        return HttpResponseRedirect(
            reverse('message:commit',args=(id,))
        )


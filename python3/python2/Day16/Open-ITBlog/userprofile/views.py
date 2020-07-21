from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .forms import UserLoginForm,UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'],password=data['password'])

            if user:
                login(request,user)
                return redirect("article:article_list")
            else:
                return HttpResponse("账号或密码输入不合法,请重新输入")
        else:
            return HttpResponse("账号或密码输入不合法")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = { 'form':user_login_form }
        return render(request,'userprofile/login.html',context)
    else:
        return HttpResponse("请使用GET或者POST请求数据")

def user_logout(request):
    logout(request)
    return redirect("userprofile:login")

def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()

            login(request,new_user)
            return redirect("article:article_list")
        else:
            return HttpResponse("注册表单输入有误")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = { 'form': user_register_form }
        return render(request,'userprofile/register.html',context)
    else:
        return HttpResponse("请使用GET或者POST请求")


@login_required(login_url='/userprofile/login/')
def user_delete(request,id):
    user = User.objects.get(id=id)
    if request.user == user:
        logout(request)
        user.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("你没有删除的权限")

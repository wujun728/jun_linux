from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect

from django.utils.deprecation import MiddlewareMixin


class SimpleMiddleware(MiddlewareMixin):

    # Ajax 请求无法获取
    def process_request(self, request):
        print(request.method)
        print(request.path)
        if request.path != '/login/' and request.path != '/':
            if request.session.get('user', None):
                pass
            else:
                return HttpResponseRedirect('/')

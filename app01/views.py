import json
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from app01 import models
from app01.forms import User
from django.utils.decorators import method_decorator


# Create your views here.

def auth(func):
    def inner(request, *args, **kwargs):
        if request.session.get('username'):
            return func(request, *args, **kwargs)
        else:
            return redirect('/user/login/')
    return inner


class Index(View):
    def get(self, request, **kwargs):
        news_type_list = models.NewType.objects.all()
        if kwargs.get('type'):
            news_id = int(kwargs.get('type'))
            news_list = models.News.objects.filter(newscategory=news_id)
            # print(news_list)
        else:
            news_list = models.News.objects.all()
            # print(news_list)
        return render(request, 'index.html', locals())


class UserLogin(View):
    ret_code = {'status': True, 'err_msg': {}}

    def post(self, request):

        form = User(data=request.POST)

        if form.is_valid():

            mb = form.cleaned_data['mobile']
            mbp = form.cleaned_data['mbpwd']

            obj = models.UserInfo.objects.filter(mobile=mb, mbpwd=mbp)

            if obj:
                request.session['username'] = mb
                self.ret_code['status'] = True
            else:
                self.ret_code['status'] = False
                self.ret_code['err_msg'] = {'mobile': '用户名或密码不正确'}
        else:
            self.ret_code['status'] = False
            self.ret_code['err_msg'] = form.errors

        return HttpResponse(json.dumps(self.ret_code))


class DelUser(View):
    def get(self, request):
        request.session.clear()

        return redirect('/index/')


class LikeNews(View):

    ret_code ={'status':True}

    def post(self, request):
        newsid = request.POST.get('nid', None)
        user_obj = models.UserInfo.objects.filter(mobile=request.session.get('username')).first()

        if newsid:
            news_obj = models.News.objects.filter(nid = newsid).first()
            if user_obj in news_obj.like.all():
                self.ret_code = False
            else:
                self.ret_code = True
                news_obj.like.add(user_obj.uid)

        return HttpResponse(json.dumps(self.ret_code))

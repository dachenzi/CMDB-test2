import json

from django.shortcuts import render, HttpResponse, redirect
from django.views import View

from app01 import models
from app01.forms import  User


# Create your views here.








class Index(View):
    def get(self, request, **kwargs):
        news_type_list = models.NewType.objects.all()
        if kwargs.get('type'):
            news_id = int(kwargs.get('type'))
            news_list = models.News.objects.filter(newscategory=news_id)
            print(news_list)
        else:
            news_list = models.News.objects.all()
            print(news_list)
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

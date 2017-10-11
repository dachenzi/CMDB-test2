import json
import os
import time

import requests
from bs4 import BeautifulSoup
from django.db import transaction
from django.db.models import F
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from app01 import models
from app01.forms import User,UrlCheck
from utils.response import  BaseResponse


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
    ret_code = BaseResponse()  # 自定义返回对象

    # ret_code ={'status':True}

    def post(self, request):
        # 获取新闻ID
        newsid = request.POST.get('nid', None)

        # 获取新闻对象
        # news_obj = models.News.objects.filter(nid=newsid).first()
        # 获取当前点赞用户对象
        # user_obj = models.UserInfo.objects.filter(mobile=request.session['username']).first()
        # 获取文章所有点赞对象列表
        # count =  news_obj.like.all()
        # 判断用户是否存在列表中，如果存在表示点过赞，如果不存在表示没点过，执行添加操作
        # if user_obj in count:
        #     pass
        # 但是这种方法，如果点赞数量很多，个人觉得很低效，因为每个人点都要去数据库里获取全量点赞数据

        # 下面是利用唯一索引的方法
        # 获取用户ID
        userid = models.UserInfo.objects.filter(mobile=request.session.get('username', None)).first().uid

        # 写入第三章关系表中，如果存在会报异常（违反联合唯一索引）

        # 同时更新关系表Like，和 news 表中的like_count字段
        try:
            with transaction.atomic():  # 启动事务检查
                models.Like.objects.create(nid_id=int(newsid), uid_id=userid)
                models.News.objects.filter(nid=newsid).update(like_count=F('like_count') + 1)
        except Exception as e:  # 异常就表示违反了联合唯一索引，表示该用户已经点过赞了， 这里就进行取消点赞。
            models.Like.objects.filter(nid_id=int(newsid), uid_id=userid).delete()
            models.News.objects.filter(nid=newsid).update(like_count=F('like_count') - 1)
            self.ret_code.status = False
        else:
            self.ret_code.status = True
        return HttpResponse(json.dumps(self.ret_code.get_dic()))


class GetUrl(View):
    ret_code = BaseResponse()

    def post(self, request):

        url_obj = UrlCheck(data=request.POST)

        if url_obj.is_valid():

            try:
                response = requests.get(url_obj.cleaned_data['url'])
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.find('title').text
                description = soup.find('meta', attrs={'name': 'description'}).get('content')

                self.ret_code.status = True
                self.ret_code.data = {'title': title, 'description': description}
            except Exception as e:
                self.ret_code.status = False
                self.ret_code.err_msg = {'url': '您输入的URL不正确'}

        else:
            self.ret_code.status = False
            self.ret_code.err_msg = url_obj.errors
            print(self.ret_code.err_msg)

        return HttpResponse(json.dumps(self.ret_code.get_dic()))


class PublishMsg(View):
    ret_code = BaseResponse()

    def post(self, request):
        newscategory_id = request.POST.get('newscategory_id')
        title = request.POST.get('title')
        com_form = request.POST.get('com_form')
        description = request.POST.get('description')
        user = models.UserInfo.objects.filter(mobile=request.session.get('username')).first()
        ctime = time.strftime('%Y-%m-%d %H:%M')
        models.News.objects.create(title=title, summary=description, com_form=com_form, user=user,
                                   newscategory_id=newscategory_id, ctime=ctime)

        self.ret_code.status = True
        return HttpResponse(json.dumps(self.ret_code.get_dic()))


class UploadImg(View):
    ret_code = BaseResponse()

    def post(self, request):
        file_obj = request.FILES.get('uploadimg')

        img_path = os.path.join('static', 'img', file_obj.name)

        with open(img_path, mode='wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        self.ret_code.status = True
        self.ret_code.data = img_path

        return HttpResponse(json.dumps(self.ret_code.get_dic()))


class ShowData(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ShowData, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        return HttpResponse('OK')


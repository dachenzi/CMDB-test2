from django.shortcuts import render,HttpResponse,redirect
from django.views import View

# Create your views here.


class Index(View):

    def get(self,request):

        return render(request,'index.html')
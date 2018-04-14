from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def index(request):
    return HttpResponse(u"欢迎光临!")


def reprot(request):
    return render(request, 'C:\\Finalworkspace\\FinalTestPlatform\\UITest\\report\\20180414\\存一封邮件至草稿箱_20180414004120.html')

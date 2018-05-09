import datetime
import os
import unittest

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from UITest.src.test.test_emailcase import SHUMail
from UITest.src.utils.TestRunnerHTML import HTMLTestRunner
from testPlatform.models import TestCase


def index(request):
    return HttpResponse(u"欢迎光临!")


def reprot(request):
    DIR = os.path.dirname(os.path.realpath(__file__)).replace('\\testPlatform', '\\UITest\\report\\')
    all_items = os.listdir(DIR)
    all_items.sort(key=lambda f: os.path.getmtime(DIR + "\\" + f))
    file_new = os.path.join(DIR, all_items[-1])
    DIR = file_new
    all_items = os.listdir(DIR)
    items = [item for item in all_items if '运行所有测试用例' in item]
    items.sort(key=lambda f: os.path.getmtime(DIR + "\\" + f))
    try:
        file_new = os.path.join(DIR, items[-1])
    except:
        file_new = os.path.join(DIR, all_items[-1])
    return render(request, file_new)


def run_all_test(request):
    report_title = '运行所有测试用例'
    ntime = datetime.datetime.now().strftime("%Y%m%d")
    nowtime = datetime.datetime.now().strftime("_%Y%m%d%H%M%S")
    report_path = os.path.dirname(os.path.realpath(__file__)).replace('\\testPlatform', '\\UITest\\report\\') + ntime
    if not os.path.exists(report_path):
        os.makedirs(report_path)
    report_file = report_path + '\\' + report_title + nowtime + '.html'
    testsuite = unittest.TestSuite()
    testsuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SHUMail))
    print(testsuite)
    with open(report_file, 'wb') as report:
        runner = HTMLTestRunner(stream=report, title=report_title, description='desc')
        runner.run(testsuite)
    return render(request, report_file)


def show_cases(request):
    case_list = TestCase.objects.all()
    return render(request, {'case_list': case_list})


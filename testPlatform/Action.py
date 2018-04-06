# @Time    : 2018/4/6 13:19
# @Author  : Eggsy
# @File    : Action.py
# @Software: PyCharm
import os

from django.template.response import TemplateResponse
from selenium import webdriver

from UITest.src.test.test_sendmail import SendMail
from xadmin.plugins.actions import BaseActionView
from UITest.src.utils.common import htmlrunner


class OpenReport(BaseActionView):

    action_name = '打开测试报告'
    description = '打开测试报告'
    model_perm = 'change'

    @staticmethod
    def get_test_report(template_name):
        return (
            "%s/%s" % (os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\UITest\\report', template_name),
            "%s" % template_name,
        )

    def do_action(self, queryset):
        for obj in queryset:
            return TemplateResponse(self.request, self.get_test_report(obj.test_report))


class RunTest(BaseActionView):

    action_name = '执行测试用例'
    description = '执行测试用例'
    model_perm = 'change'

    def do_action(self, queryset):
        for obj in queryset:
            default_path = 'UITest.src.test.'
            case = default_path + obj.test_file + '.' + obj.class_name + '.' + obj.test_method + '_' + obj.case_id + '_' + obj.case_name
            htmlrunner(obj.case_name, case)


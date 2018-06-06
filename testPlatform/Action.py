# @Time    : 2018/4/6 13:19
# @Author  : Eggsy
# @File    : Action.py
# @Software: PyCharm
import os

import pymysql
from django.template.response import TemplateResponse

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
            default_path = 'UITest.src.test.test_emailcase.SHUMail.test_emailcase_'
            case = default_path + str(obj.id) + '_' + obj.case_name + str(obj.id)
            htmlrunner(obj.case_name, case, [], 0)


class RunDataDrivenTest(BaseActionView):

    action_name = '执行测试用例'
    description = '执行测试用例'
    model_perm = 'change'

    def getTestDataId(self, case_id):
        db = pymysql.connect(host="localhost", user="root", password="1234", db="django_platform", port=3306, charset="utf8")
        cur = db.cursor()
        sql = "SELECT `datadriven_id` FROM testplatform_testcasefordatadriven_data WHERE testcasefordatadriven_id = '%s';" % case_id
        cur.execute(sql)
        results = cur.fetchall()
        db.commit()
        cur.close()
        db.close()
        return results

    def do_action(self, queryset):
        cases = []
        for obj in queryset:
            default_path = 'UITest.src.test.test_datadriven.DataDriven.test_datadriven_'
            datas = self.getTestDataId(obj.id)
            for data in datas:
                print(data[0])
                case = default_path + str(data[0]) + '_' + str(obj.id) + obj.case_name + str(data[0])
                cases.append(case)
            htmlrunner(obj.case_name, '', cases, 1)
            # print(cases)

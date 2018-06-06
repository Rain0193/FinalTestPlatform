# @Time    : 2018/4/4 17:20
# @Author  : Eggsy

import xadmin
from basicData.models import Element, Steps, StepsForCases
from testPlatform.Action import OpenReport, RunTest, RunDataDrivenTest
from xadmin import views
from .models import TestCase, TestCaseForDataDriven


class MainDashboard(object):
    widgets = [
        [
            {"type": "html", "title": "Test Widget",
             "content": "<h3> Welcome to Xadmin! </h3><p>Join Online Group: <br/>QQ Qun : 282936295</p>"},
            {"type": "chart", "model": "basicData.stepsforcases", "chart": "execution_order",
             "params": {"_p_date__gte": "2013-01-08", "p": 1, "_p_date__lt": "2013-01-29"}},
            {"type": "list", "model": "basicData.element", "params": {"o": "-guarantee_date"}},
        ],
        [
            {"type": "qbutton", "title": "Quick Start",
             "btns": [{"model": Element}, {"model": Steps}, {"title": "Google", "url": "http://www.google.com"}]},
            {"type": "addform", "model": TestCase},
        ]
    ]


class TestCaseAdmin(object):
    list_display = ['id', 'case_name', 'test_report', 'test_result']
    search_fields = ['case_name', 'test_result']
    list_filter = ['case_name', 'test_result']
    actions = [OpenReport, RunTest]
    readonly_fields = ['test_report', 'test_result']
    list_editable = ['case_name']
    filter_horizontal = ['steps']
    style_fields = {'steps': 'm2m_transfer'}


class TestCaseForDataDrivenAdmin(object):
    list_display = ['id', 'case_name', 'test_report', 'test_result','data']
    search_fields = ['case_name', 'test_result', 'data']
    list_filter = ['case_name', 'test_result', 'data']
    actions = [OpenReport, RunDataDrivenTest]
    readonly_fields = ['test_report', 'test_result']
    list_editable = ['case_name']
    filter_horizontal = ['steps', 'data']
    style_fields = {'steps': 'm2m_transfer', 'data': 'm2m_transfer'}


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = "测试用例管理系统"
    site_footer = "Copyright 2018 Eggsy"
    global_models_icon = {
        Element: "fa fa-laptop", Steps: "fa fa-cloud", TestCase: "fa fa-rocket", StepsForCases: "fa fa-coffee"
    }
    # menu_style = "accordion"


xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(views.IndexView, MainDashboard)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(TestCase, TestCaseAdmin)
xadmin.site.register(TestCaseForDataDriven, TestCaseForDataDrivenAdmin)

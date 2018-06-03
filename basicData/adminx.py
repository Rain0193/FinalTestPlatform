# @Time    : 2018/4/4 17:20
# @Author  : Eggsy

import xadmin
from .models import Element, Steps, StepsForCases, DataDriven


class ElementAdmin(object):
    list_display = ['id', 'element_name', "access_method", 'access_path', 'frame_name']
    search_fields = ['element_name', "access_method", 'access_path', 'frame_name']
    list_filter = ['element_name', "access_method", 'access_path', 'frame_name']
    # actions = [OpenReport, RunTest]


class StepsAdmin(object):
    list_display = ['id', 'step_des', 'element_name', 'actions', 'parameter', 'wait_time']
    search_fields = ['step_des', 'actions', 'parameter',]
    list_filter = ['step_des', 'actions', 'parameter',]


class StepsForCasesAdmin(object):
    list_display = ['case_name', 'step_name', 'execution_order']
    list_filter = ['case_name']


class DataDrivenAdmin(object):
    list_display = ['case_name', 'data']
    list_filter = ['case_name', 'data']

xadmin.site.register(Element, ElementAdmin)
xadmin.site.register(Steps, StepsAdmin)
xadmin.site.register(StepsForCases, StepsForCasesAdmin)
xadmin.site.register(DataDriven, DataDrivenAdmin)


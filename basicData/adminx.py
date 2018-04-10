# @Time    : 2018/4/4 17:20
# @Author  : Eggsy

import xadmin
from .models import Element, Steps


class ElementAdmin(object):
    list_display = ['element_name', "access_method", 'access_path', 'frame_name']
    search_fields = ['element_name', "access_method", 'access_path', 'frame_name']
    list_filter = ['element_name', "access_method", 'access_path', 'frame_name']
    # actions = [OpenReport, RunTest]


class StepsAdmin(object):
    list_display = ['step_des', 'element_name', 'actions', 'parameter', 'wait_time']
    search_fields = ['step_des', 'actions', 'parameter',]
    list_filter = ['step_des', 'actions', 'parameter',]

xadmin.site.register(Element, ElementAdmin)
xadmin.site.register(Steps, StepsAdmin)


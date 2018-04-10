# @Time    : 2018/4/4 17:20
# @Author  : Eggsy

import xadmin
from .models import Element


class ElementAdmin(object):
    list_display = ['element_name', "access_method", 'access_path', 'frame_name']
    search_fields = ['element_name', "access_method", 'access_path', 'frame_name']
    list_filter = ['element_name', "access_method", 'access_path', 'frame_name']
    # actions = [OpenReport, RunTest]

xadmin.site.register(Element, ElementAdmin)

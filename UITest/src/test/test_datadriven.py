# @Time    : 2018/6/6 9:12
# @Author  : Eggsy
# @File    : test_datadriven.py
# @Software: PyCharm
import unittest

import pymysql
from ddt import ddt, data, unpack
from UITest.src.utils.webuitest import WebUITest
from UITest.src.utils.getElement import GetElement


def getCaseName():
    # 查询数据库的方法
    db = pymysql.connect(host="localhost", user="root", password="1234", db="django_platform", port=3306, charset="utf8")
    cur = db.cursor()
    sql = "SELECT a.id, `case_name` ,`datadriven_id` FROM testplatform_testcasefordatadriven AS a, testplatform_testcasefordatadriven_data as b WHERE a.id = b.testcasefordatadriven_id;"
    cur.execute(sql)
    results = cur.fetchall()
    db.commit()
    cur.close()
    db.close()
    return results


@ddt
class DataDriven(WebUITest):
    @data(*getCaseName())
    @unpack
    def test_datadriven(self, case_id, case_name, data_id):
        pass
        driver = GetElement(self.driver)
        GetElement.CaseName = self._testMethodName
        driver.ui_engine(case_id, case_name, data_id)

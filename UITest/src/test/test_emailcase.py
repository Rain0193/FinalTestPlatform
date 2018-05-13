# @Time    : 2018/4/15 16:16
# @Author  : Eggsy
# @File    : test_emailcase.py
# @Software: PyCharm

import pymysql
from ddt import ddt, data, unpack
from UITest.src.utils.webuitest import WebUITest
from UITest.src.utils.getElement import GetElement


def getCaseName():
    # 查询数据库的方法
    db = pymysql.connect(host="localhost", user="root", password="1234", db="django_platform", port=3306, charset="utf8")
    cur = db.cursor()
    sql = "SELECT `case_name`, `id` FROM testplatform_testcase;"
    cur.execute(sql)
    results = cur.fetchall()
    db.commit()
    cur.close()
    db.close()
    return results


@ddt
class SHUMail(WebUITest):
    @data(*getCaseName())
    @unpack
    def test_emailcase(self, case_name, case_id):
        driver = GetElement(self.driver)
        GetElement.CaseName = self._testMethodName
        driver.ui_engine(case_name, case_id)

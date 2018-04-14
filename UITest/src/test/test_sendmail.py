# @Time    : 2018/4/1 20:35
# @Author  : Eggsy
# @File    : test_sendmail.py
# @Software: PyCharm

import pymysql
from ddt import ddt, data, unpack
from UITest.src.utils.common import htmlrunner
from UITest.src.utils.webuitest import WebUITest
from UITest.src.utils.getElement import GetElement


def getCaseName():
    # 查询数据库的方法
    db = pymysql.connect(host="localhost", user="root", password="1234", db="mysql", port=3306, charset="utf8")
    cur = db.cursor()
    sql = "SELECT `case_name` FROM testplatform_testcase WHERE id = 1;"
    cur.execute(sql)
    results = cur.fetchall()
    db.commit()
    cur.close()
    db.close()
    return results


@ddt
class SendMail(WebUITest):
    @data(*getCaseName())
    @unpack
    def test_sendMail(self, data):
        driver = GetElement(self.driver)
        GetElement.CaseName = self._testMethodName
        driver.ui_engine(data)

if __name__ == "__main__":
    htmlrunner('测试报告——发件箱', 'UITest.src.test.test_sendmail.SendMail.test_sendMail_'+'00001'+'_存一封邮件至草稿箱')

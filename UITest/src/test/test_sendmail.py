# @Time    : 2018/4/1 20:35
# @Author  : Eggsy
# @File    : test_sendmail.py
# @Software: PyCharm

from ddt import ddt, file_data
from UITest.src.utils.common import htmlrunner
from UITest.src.utils.webuitest import WebUITest
from UITest.src.utils.getElement import GetElement



@ddt
class SendMail(WebUITest):
    @file_data("sendmail.json")
    def test_sendMail(self, data):
        driver = GetElement(self.driver)
        GetElement.CaseName = self._testMethodName
        driver.ui_engine(data)

if __name__ == "__main__":
    htmlrunner('测试报告——发件箱', 'UITest.src.test.test_sendmail.SendMail.test_sendMail_'+'00001'+'_存一封邮件至草稿箱')

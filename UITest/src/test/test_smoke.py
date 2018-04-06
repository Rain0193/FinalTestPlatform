# @Time    : 2018/3/27 23:17
# @Author  : Eggsy
# @File    : test_smoke.py
# @Software: PyCharm

from ddt import ddt, file_data
from UITest.src.utils.common import htmlrunner
from UITest.src.utils.webuitest import WebUITest

from UITest.src.utils.getElement import GetElement


@ddt
class UISmokeTest(WebUITest):

    @file_data("smoke.json")
    def test_smoke(self, data):
        driver = GetElement(self.driver)
        GetElement.CaseName = self._testMethodName
        driver.ui_engine(data)

if __name__ == "__main__":
    htmlrunner('冒烟测试', 'SmokeTest', UISmokeTest)

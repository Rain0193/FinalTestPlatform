# @Time    : 2018/3/27 21:46
# @Author  : Eggsy
# @File    : webuitest.py
# @Software: PyCharm

import datetime
import time
import unittest

from selenium import webdriver
from UITest.src.utils.common import getconfig
from UITest.src.utils.getElement import GetElement

from UITest.src.utils.common import logger

username = getconfig("webui", "username")
password = getconfig("webui", "password")
url = getconfig("webui", "url")


def login(driver, username, password):
        # 登录操作
        logger('INFO', "start to login browser")
        driver.get(url)
        time.sleep(3)
        element_username = driver.find_element_by_id("uid")
        element_password = driver.find_element_by_id("password")
        element_username.clear()
        element_username.send_keys(username)
        element_password.clear()
        element_password.send_keys(password)
        driver.find_element_by_xpath("//*[@type='button']").click()
        time.sleep(3)
        logger('INFO', "login browser success")


class WebUITest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # 初始化浏览器
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        login(self.driver, username, password)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()
        logger('INFO', "login out browser")

    def setUp(self):
        GetElement.username = username
        GetElement.password = password
        GetElement.casetime = datetime.datetime.now().strftime("_%Y%m%d%H%M%S")




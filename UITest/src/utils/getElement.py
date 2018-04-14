# @Time    : 2018/3/27 23:21
# @Author  : Eggsy
# @File    : getElement.py
# @Software: PyCharm
import datetime
import json
import os
import time
import unittest

import re

import pymysql
from selenium.webdriver.support.select import Select
from UITest.src.utils.common import getconfig
from UITest.src.utils.common import get_img

from UITest.src.utils.common import logger

url = getconfig("webui", "url")
wait_time = int(getconfig("webui", "wait_time"))


class GetElement(unittest.TestCase):

    current_frame = ""
    nowtime = datetime.datetime.now().strftime("%Y%m%d")
    CaseName = "default_name"
    casetime = None
    username = getconfig("webui", "username")
    password = getconfig("webui", "password")

    def __init__(self, selenium_driver):
        self.driver = selenium_driver
        self.element_text = ''

    def find_element(self, *loc):
        return self.driver.find_element(*loc)

    def getCaseStepIDs(self, case_name):
        db = pymysql.connect(host="localhost", user="root", password="1234", db="mysql", port=3306, charset="utf8")
        cur = db.cursor()
        sql = "SELECT `steps` FROM testplatform_testcase WHERE case_name = '%s';" % case_name
        cur.execute(sql)
        results = cur.fetchall()[0][0]
        db.commit()
        cur.close()
        db.close()
        return results

    def getCaseStep(self, id):
        db = pymysql.connect(host="localhost", user="root", password="1234", db="mysql", port=3306, charset="utf8")
        cur = db.cursor()
        sql = "SELECT `actions`, `parameter`, `element_name_id`, `wait_time`, `step_des` FROM basicdata_steps WHERE id = '%s';" % id
        cur.execute(sql)
        results = cur.fetchall()[0]
        db.commit()
        cur.close()
        db.close()
        return results

    def ui_engine(self, case_name):
        step_ids = self.getCaseStepIDs(case_name)
        for step_id in step_ids.split(","):
            result = self.getCaseStep(step_id)
            action = result[0]
            element = result[1], result[2], result[3]
            logger("INFO", "CaseStep is %s" % result[4])
            # 点击操作
            if action == "点击":
                self.handle_click(element)
            # 输入操作
            elif action == "填写":
                self.handle_fill(element)
            # 检查操作
            elif action == "检查":
                self.check_value(element)
            # 选择操作
            elif action == "选择":
                self.handle_choose(element)
            # 上传操作
            elif action == "上传":
                self.handle_fill(element)
            # 切换操作
            elif action == "切换":
                self.handle_switch(element)
            else:
                logger("ERROR", "Sync Error, %s action is not correct!" % action)
                assert False, "Sync Error, %s action is not correct!" % action

    # 处理点击操作
    def handle_click(self, element):
        element_name_id = element[1]
        wait_time = element[2]
        self.click_button(element_name_id)
        time.sleep(wait_time)

    # 处理填写操作
    def handle_fill(self, element):
        parameter = element[0]
        element_name_id = element[1]
        wait_time = element[2]
        self.fill_input_box(element_name_id, parameter)
        time.sleep(wait_time)

    # 处理检查操作
    def check_value(self, element):
        parameter = element[0]
        wait_time = element[2]
        if parameter.find(u"不存在") != -1:
            val = parameter.split(u"不存在:")
            for v in val[1].split(","):
                result = self.get_tab_element(v)
                time.sleep(wait_time)
                get_img(self.driver, self.nowtime, self.CaseName)
                if result:
                    logger("INFO", "check failed")
                    self.assertTrue(False, msg="%s is exist" % v)
                else:
                    logger("INFO", "check successfully")
                    self.assertTrue(True)
        elif parameter.find(u"存在") != -1:
            val = parameter.split(u"存在:")
            for v in val[1].split(","):
                result = self.get_tab_element(v)
                time.sleep(wait_time)
                get_img(self.driver, self.nowtime, self.CaseName)
                if result:
                    logger("INFO", "check successfully")
                    self.assertTrue(True)
                else:
                    logger("INFO", "check failed")
                    self.assertTrue(False, msg="%s is not exist" % v)

    # 处理选择操作
    def handle_choose(self, element):
        parameter = element[0]
        element_name_id = element[1]
        wait_time = element[2]
        self.select_element(element_name_id, parameter)
        time.sleep(wait_time)

    # 处理循环等待操作
    def handle_wait(self, element):
        pass

    # 处理切换操作
    def handle_switch(self, element):
        parameter = element[0]
        wait_time = element[2]
        if parameter.find('default') != -1:
            self.driver.switch_to.default_content()
            self.current_frame = "default"
            logger("INFO", "Now switch to default frame")
        else:
            for frame in parameter.split('/'):
                self.driver.switch_to.frame(frame)
                self.current_frame = frame
                logger("INFO", "Now switch to frame " + frame)
        time.sleep(wait_time)

    def fill_input_box(self, label, content):
        result = self.get_allelement(label, "fill", content)
        if result is None:
            get_img(self.driver, self.nowtime, self.CaseName)
            logger("ERROR", "Element %s is not found!" % label)
            assert False, "Element %s is not found!" % label

    def select_element(self, label, content):
        result = self.get_allelement(label, "select", content)
        if result is None:
            get_img(self.driver, self.nowtime, self.CaseName)
            logger("ERROR", "Element %s is not found!" % label)
            assert False, "Element %s is not found!" % label

    # 点击元素
    def click_button(self, element_name_id):
        result = self.get_allelement(element_name_id, optype="click")
        if result is None:
            get_img(self.driver, self.nowtime, self.CaseName)
            logger("ERROR", "Element %s is not found!" % element_name_id)
            assert False, "Element %s is not found!" % element_name_id

    def get_element(self, id):
        db = pymysql.connect(host="localhost", user="root", password="1234", db="mysql", port=3306, charset="utf8")
        cur = db.cursor()
        sql = "SELECT `element_name`, `access_method`, `access_path`, `frame_name` FROM basicdata_element WHERE id = '%s';" % id
        cur.execute(sql)
        results = cur.fetchall()[0]
        db.commit()
        cur.close()
        db.close()
        return results

    # 从数据库中取元素
    def get_allelement(self, element_name_id, optype=None, content=None):
        logger("INFO", "Star to find element %s from database" % element_name_id)
        result = self.get_element(element_name_id)
        element_name = result[0]
        access_method = result[1]
        access_path = result[2]
        frame_name = result[3]
        logger("INFO", "element path is " + access_method + ':' + access_path)
        if frame_name.find('default') != -1:
            self.driver.switch_to.default_content()
            self.current_frame = "default"
            logger("INFO", "Now switch to default frame")
        else:
            for frame in frame_name.split('/'):
                if self.current_frame == frame:
                    pass
                else:
                    try:
                        self.driver.switch_to.frame(frame)
                        self.current_frame = frame
                        logger("INFO", "Now switch to frame " + frame)
                    except:
                        self.driver.switch_to.default_content()
                        self.driver.switch_to.frame(frame)
                        self.current_frame = frame
                        logger("INFO", "Now switch to frame " + frame)
        for i in range(wait_time):
            logger("DEBUG", "consume %d seconds already" % i)
            time.sleep(1)
            try:
                element = self.driver.find_element_by_link_text(element_name)
                self.handle_element(element, optype, content)
                return element
            except:
                if access_method == "id":
                    element = self.driver.find_element_by_id(access_path)
                    self.handle_element(element, optype, content)
                    return element
                if access_method == "xpath":
                    element = self.driver.find_element_by_xpath(access_path)
                    self.handle_element(element, optype, content)
                    return element
            logger("WARN", "failed to find element in page")
            return None

    # 检查页面上元素是否存在
    def get_tab_element(self, tab_name):
        element = None
        a = self.driver.find_elements_by_tag_name("a")
        tds = self.driver.find_elements_by_tag_name("td")
        elemlist = a + tds
        for i in elemlist:
            if re.search(re.compile(tab_name), i.text):
                element = i
                logger("DEBUG", "find element successfully ")
                break
        if element:
            return element.is_displayed()
        return element

    # 集中处理元素
    def handle_element(self, element, optype, content):
        if optype == "click":
            element.click()
        if optype == "fill":
            element.clear()
            element.send_keys(content)
        if optype == "select":
            Select(element).select_by_visible_text(content)
        logger("INFO", "find element successfully in page")

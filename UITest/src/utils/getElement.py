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
from selenium.webdriver.support.select import Select
from UITest.src.utils.common import getconfig
from UITest.src.utils.common import get_img

from UITest.src.utils.common import logger

url = getconfig("webui", "url")
wait_time = int(getconfig("webui", "wait_time"))


class GetElement(unittest.TestCase):

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

    def ui_engine(self, steps, start_index=None, end_index=None):

        # 开始执行步骤
        if start_index is None:
            start_index = 1
        if end_index is None:
            end_index = len(steps)
        for i in range(start_index - 1, end_index):
            step = steps[i]
            logger("INFO", "CaseStep is %s" % step)
            # 如果为已经封装好的步骤，则跳转至common.json
            path = os.path.dirname(os.path.realpath(__file__)).replace('\\src\\utils', '') + '\\data'
            data_file = open(os.path.join(path, "common.json"), encoding="utf-8")
            data_dict = json.load(data_file)
            data_file.close()
            for key in data_dict:
                if step == key:
                    key_steps = data_dict[key]
                    other_steps = []
                    for j in range(i + 1, end_index):
                        other_step = steps[j]
                        other_steps.append(other_step)
                    new_step = key_steps + other_steps
                    return GetElement.ui_engine(self, new_step)
            action = step[:2]
            element = step[2:]
            # 点击操作
            if action == "点击":
                self.handle_click(element)
            # 等待操作
            elif action == "等待":
                self.handle_sleep(element)
            # 输入操作
            elif action == "填写":
                self.handle_fill(element)
            # 检查操作
            elif action == "检查":
                self.check_value(element)
            # 选择操作
            elif action == "选择":
                self.handle_choose(element)
            # 循环操作
            elif action == "循环":
                self.handle_wait(element)
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
        for item in element.split("->"):
            self.click_button(item)

    # 处理等待操作
    def handle_sleep(self, element):
        seconds = float(element[:-1])
        time.sleep(seconds)

    # 处理输入操作
    def handle_fill(self, element):
        fillcontent = element.split(",")
        for i in fillcontent:
            con = i.split("为")
            label = con[0]
            content = con[1]
            self.fill_input_box(label, content)

    # 处理检查操作
    def check_value(self, element):
        if element.find(u"不存在") != -1:
            val = element.split(u"不存在")
            result = self.get_tab_element(val[1])
            get_img(self.driver, self.nowtime, self.CaseName)
            if result:
                logger("INFO", "check failed")
                self.assertTrue(False, msg="%s is exist" % val[1])
            else:
                logger("INFO", "check successfully")
                self.assertTrue(True)
        elif element.find(u"存在") != -1:
            val = element.split(u"存在")
            result = self.get_tab_element(val[1])
            get_img(self.driver, self.nowtime, self.CaseName)
            if result:
                logger("INFO", "check successfully")
                self.assertTrue(True)
            else:
                logger("INFO", "check failed")
                self.assertTrue(False, msg="%s is not exist" % val[1])

    # 处理选择操作
    def handle_choose(self, element):
        choosecontent = element.split(",")
        for i in choosecontent:
            con = i.split("为")
            label = con[0]
            content = con[1]
            self.select_element(label, content)

    # 处理循环等待操作
    def handle_wait(self, element):
        pass

    # 处理切换操作
    def handle_switch(self, element):
        content = element.split("至")[1]
        if content.find('默认') != -1:
            self.driver.switch_to.default_content()
        elif content.find('层') != -1:
            num = int(content.split('层')[0].split('上')[1])
            for i in range(num):
                self.driver.switch_to.parent_frame()
        else:
            frames = content.split("界面")[0]
            for frame in frames.split('/'):
                self.driver.switch_to.frame(frame)

    def fill_input_box(self, label, content):
        result = self.get_allelement(label, "fill", content)
        if result is None:
            get_img(self.driver, self.nowtime, self.CaseName)
            logger("ERROR", "%s Element is not found!" % label)
            assert False, "%s Element is not found!" % label

    def select_element(self, label, content):
        result = self.get_allelement(label, "select", content)
        if result is None:
            get_img(self.driver, self.nowtime, self.CaseName)
            logger("ERROR", "%s Element is not found!" % label)
            assert False, "%s Element is not found!" % label

    # 点击元素
    def click_button(self, button_name):
        result = self.get_allelement(button_name, optype="click")
        if result is None:
            get_img(self.driver, self.nowtime, self.CaseName)
            logger("ERROR", "%s Element is not found!" % button_name)
            assert False, "%s Element is not found!" % button_name

    # 从字典中取元素
    def get_allelement(self, element_name, optype=None, content=None):
        logger("INFO", "Star to find element %s from json dictionary" % element_name)
        element_dict = {}
        path = os.path.dirname(os.path.realpath(__file__)).replace('\\src\\utils', '') + '\\data'
        id_file = open(os.path.join(path, "element_id.json"), encoding='utf-8')
        id_dict = json.load(id_file)
        xpath_file = open(os.path.join(path, "element_xpath.json"), encoding='utf-8')
        xpath_dict = json.load(xpath_file)
        id_file.close()
        xpath_file.close()
        if element_name in id_dict.keys():
            element_dict["id"] = id_dict[element_name]
        if element_name in xpath_dict.keys():
            element_dict["xpath"] = xpath_dict[element_name]
        logger("INFO", "element dict is " + str(element_dict))
        for i in range(wait_time):
            logger("DEBUG", "consume %d seconds already" % i)
            time.sleep(1)
            try:
                element = self.driver.find_element_by_link_text(element_name)
                self.handle_element(element, optype, content)
                return element
            except:
                for key, value in element_dict.items():
                    if key == "id":
                        element = self.driver.find_element_by_id(value)
                        self.handle_element(element, optype, content)
                        return element
                    if key == "xpath":
                        element = self.driver.find_element_by_xpath(value)
                        self.handle_element(element, optype, content)
                        return element
            logger("WARN", "failed to find element in page")
            return None

    # 检查页面上元素是否存在
    def get_tab_element(self, tab_name):
        element = self.get_allelement(tab_name)
        if element is None:
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

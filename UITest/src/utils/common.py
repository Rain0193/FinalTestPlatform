# @Time    : 2018/3/27 22:12
# @Author  : Eggsy
# @File    : webuitest.py
# @Software: PyCharm

import configparser
import os
import datetime
import time
import sys
import unittest

from UITest.src.utils.TestRunnerHTML import HTMLTestRunner


# 获取配置文件
def getconfig(section, key):
    config = configparser.ConfigParser()
    path = os.path.dirname(os.path.realpath(__file__)).replace('\\src\\utils', '') + '\\config\\config.ini'
    config.read(path)
    return config.get(section, key)


# 通过HTMLRunner执行用例
def htmlrunner(report_title, case_method):
    ntime = datetime.datetime.now().strftime("%Y%m%d")
    nowtime = datetime.datetime.now().strftime("_%Y%m%d%H%M%S")
    report_path = os.path.dirname(os.path.realpath(__file__)).replace('\\src\\utils', '\\report\\') + ntime
    if not os.path.exists(report_path):
        os.makedirs(report_path)
    report_file = report_path + '\\' + report_title + nowtime + '.html'
    testsuite = unittest.TestSuite()
    testsuite.addTest(unittest.defaultTestLoader.loadTestsFromName(case_method))
    print(testsuite)
    with open(report_file, 'wb') as report:
        runner = HTMLTestRunner(stream=report, title=report_title, description='desc')
        runner.run(testsuite)


# 获取截图
def get_img(driver, nowtime, filename):
    logger("INFO", "screenshot start")
    base_dir = os.path.dirname(os.path.realpath(__file__))
    ntime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filedir = base_dir.replace('src\\utils', '') + 'screenshots\\' + nowtime
    if os.path.isdir(filedir):
        pass
    else:
        os.makedirs(filedir)
    file_path = filedir + "\\" + filename + "-" + ntime + '.png'
    logger("INFO", file_path)
    driver.get_screenshot_as_file(file_path)
    logger("INFO", "screenshot end")


# 写日志
def logger(level, log_info):
    l_type_lst = ["ERROR", "WARN", "DEBUG", "INFO"]
    # 将日志写入log文件里
    ntime = datetime.datetime.now().strftime("%Y%m%d")
    log_path = os.path.dirname(os.path.realpath(__file__)).replace('\\src\\utils', '') + '\\log\\'
    log_level = getconfig("log", "LOG_LEVEL")
    log_enable = getconfig("log", "LOG_ENABLE")
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_file = os.path.join(log_path, ntime + '.log')
    # log的等级
    lvl = l_type_lst.index(level)
    # 写入log
    log_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    log_pid = os.getpid()
    log_script = sys._getframe().f_back.f_code.co_filename.split('/')[-1]
    log_method = sys._getframe().f_back.f_code.co_name
    log_line = sys._getframe().f_back.f_lineno
    with open(log_file, "a") as log:
        if lvl <= int(log_level) and bool(log_enable):
            log.write("%s %s %s %s:%s:%s %s\
\n" % (log_time, log_pid, level, log_script, log_method, log_line, log_info))

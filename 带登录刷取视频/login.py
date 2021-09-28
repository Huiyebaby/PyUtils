#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:HarryDong
# datetime:2021-07-23 20:57
# software: PyCharm
import json
import time

from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('lang=zh_CN.UTF-8')
options.add_argument("--mute-audio")  # 静音
driver = webdriver.Chrome(chrome_options=options)
print('=====================首次登录已启动============================')


def is_login():
    loginStatus = False
    while not loginStatus:
        try:
            erro = driver.find_element_by_id('tab-student')
            print(erro.text)
        except:
            print("检测是否登录")
            checkNum = 0
            while checkNum < 10:
                try:
                    cookie = driver.get_cookie("sessionid")
                    if cookie:
                        print('登录成功', cookie)
                        loginStatus = True
                        break
                    else:
                        print('检测中', checkNum)
                        checkNum = checkNum + 1
                        time.sleep(1)
                except:
                    print('检测中', checkNum)
                    checkNum = checkNum + 1
                    time.sleep(1)


def login_ykt():
    driver.get(url='https://www.yuketang.cn/web/?next=/v2/web/index')
    driver.maximize_window()
    is_login()
    time.sleep(5)
    ykt_ck = driver.get_cookies()
    write_ck(ykt_ck)
    driver.close()

def write_ck(ykt_ck):
    with open('cookie.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(ykt_ck))


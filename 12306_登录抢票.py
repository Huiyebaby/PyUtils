# -*- coding:utf-8 -*-
import json
import requests
import time
from captcha import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
 
 
 
 
# 定义一系列code来确保每一步执行成功再进入下一步
global logincode, hkcode, yzcode, xpcode, cpcode, gmcode, code
 
 
# 初始化
def init_program():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
 
    return browser
 
 
# 登录12306
def login(browser):
    global logincode
    logincode = 0
    password = ''  # 登录12306的秘密
    username = ''  # 登录12306的账号
    login_url = 'https://kyfw.12306.cn/otn/resources/login.html'
    # ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
    try:
        browser.get(login_url)
        time.sleep(0.5)
        wait.WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-hd-code'))).click()
        input_name = browser.find_element_by_id('J-userName')
        input_pd = browser.find_element_by_id('J-password')
        input_name.send_keys(username)
        input_pd.send_keys(password)
        login = browser.find_element_by_id('J-login')
        login.click()
        logincode = 1
    except Exception as e:
        logincode = 0
        print(e)
 
     
 
 
# 拉动滑块验证
def huakuai(browser):
    global hkcode
    hkcode = 0
    try:
        browser.implicitly_wait(5)
        print('=====开始处理滑动验证码=====')
        track = [300, 400, 500]
        for i in track:
            try:
                btn = browser.find_element_by_xpath('//*[@id="nc_1__scale_text"]/span')
                ActionChains(browser).drag_and_drop_by_offset(btn, i, 0).perform()
                hkcode = 1
            except:
                time.sleep(2)
    except Exception as e:
        hkcode = 0
        print(e)
     
 
# 疫情特殊要求
def yiqingyaoqiu(browser):
    global yzcode
    yzcode = 0
    try:
        browser.implicitly_wait(5)
        try:
            browser.find_element_by_xpath('/html/body/div[4]/div[2]/div[3]/a').click()
            yzcode = 1
        except:
            try:
                browser.find_element_by_xpath('/html/body/div[2]/div[7]/div[2]/div[3]/a').click()
                yzcode = 1
            except:
                yzcode = 0
        finally:
            time.sleep(2)
    except Exception as e:
        yzcode = 0
        print(e)
     
 
 
# 进入买票页面
def enterbuy(browser):
    global xpcode
    xpcode = 0
    try:
        browser.find_element_by_xpath('//*[@id="J-chepiao"]/a').click()
        browser.find_element_by_xpath('//*[@id="megamenu-3"]/div[1]/ul/li[1]/a').click()
        browser.find_element_by_xpath('//*[@id="qd_closeDefaultWarningWindowDialog_id"]').click()
        xpcode = 1
    except Exception as e:
        print(e)
        xpcode = 0
     
 
 
# 将出发地、目的地、出发日期填进去
def input_info(browser):
    global cpcode
    cpcode = 0
 
    date = '2022-01-24'  # 填写购票日期
    start_station = ''  # 购票出发站，例如南京南
    end_station = ''  # 购票目的站
    try:
        print('=====开始买票=====')
        from_station = browser.find_element_by_xpath('//*[@id="fromStationText"]')
        from_station.send_keys(Keys.ENTER)
        from_station.send_keys(Keys.CONTROL, 'a')
        from_station.send_keys(start_station, Keys.ENTER)
        browser.implicitly_wait(5)
        to_station = browser.find_element_by_xpath('//*[@id="toStationText"]')
        to_station.send_keys(Keys.ENTER)
        to_station.send_keys(Keys.CONTROL, 'a')
        to_station.send_keys(end_station, Keys.ENTER)
        browser.implicitly_wait(5)
        start_date = browser.find_element_by_xpath('//*[@id="train_date"]')
        start_date.send_keys(Keys.ENTER)
        start_date.send_keys(Keys.CONTROL, 'a')
        start_date.send_keys(Keys.CONTROL, 'x')
        start_date.send_keys(date, Keys.ENTER)
        browser.implicitly_wait(5)
        wait.WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.ID, 'query_ticket'))).click()
        cpcode = 1
    except Exception as e:
        print(e)
        cpcode = 0
 
 
 
 
# 依次查找trains中的车次是否有票，有的话点击购买
def buy(browser):
    global gmcode, code
    gmcode = 0
    code = 0
    purpose = 'ADULT'  # 购买成人票，如果是学生票，需调整代码
    names = ['']  # 填写购票人姓名，需要在你的乘车人管理里有的
    trains = []  # 你想买的班次，例如'D666',  'G666'
    browser.implicitly_wait(5)
    try:
        trList = browser.find_elements_by_xpath(".//tbody[@id='queryLeftTable']/tr[not(@datatran)]")
        for tr in trList:
            trainNum = tr.find_element_by_class_name("number").text
            if trainNum in trains:
                leftTicket = tr.find_element_by_xpath(".//td[4]").text
                print('leftTicket', leftTicket)
                if leftTicket == '有' or leftTicket.isdigit():
                    orderBtn = tr.find_element_by_class_name("btn72")
                    orderBtn.click()
                    browser.implicitly_wait(5)
                    passengerLabels = browser.find_elements_by_xpath(".//ul[@id='normal_passenger_id']/li/label")
                    for passengerLabel in passengerLabels:
                        name = passengerLabel.text
                        if name in names:
                            passengerLabel.click()
                    browser.implicitly_wait(20)
                    # 获取提交按钮
                    submitBtn = browser.find_element_by_id("submitOrder_id")
                    submitBtn.click()
                    browser.implicitly_wait(20)
                    confirmBtn = browser.find_element_by_id("qr_submit_id")
                    confirmBtn.click()
                    time.sleep(2)
                    browser.implicitly_wait(20)
                    confirmBtn = browser.find_element_by_id("qr_submit_id")
                    confirmBtn.click()
                    code = 1
                    gmcode = 1
                    break
 
    except Exception as e:
        print(e)
        gmcode = 0
     
 
 
def tuisong():
    api = "https://sctapi.ftqq.com/*****.send" #*****替换成你的微信server酱的key，可以实现购票成功推送，然后你就自己去12306付款
 
    title = '购买成功'
 
    data = {
        "text": title
    }
    req = requests.post(api, data=data)
 
 
if __name__ == "__main__":
    global logincode, yzcode, hkcode, xpcode, cpcode, gmcode, code
    code = 0
    logincode = 0
    yzcode = 0
    hkcode = 0
    xpcode = 0
    cpcode = 0
    gmcode = 0
    browser = init_program()
    while code == 0:
        while logincode == 0:
            login(browser)
            print('logincode:', logincode)
 
        while hkcode == 0:
            huakuai(browser)
            print('hkcode:', hkcode)
 
        while yzcode == 0:
            yiqingyaoqiu(browser)
            print('yzcode:', yzcode)
 
        while xpcode == 0:
            enterbuy(browser)
            print('xpcode:', xpcode)
 
        while cpcode == 0:
            input_info(browser)
            input_info(browser)#经测试，一次有可能不成功，我直接两次提交
            print('cpcode:', cpcode)
 
        while gmcode == 0:
            buy(browser)
            print('gmcode:', gmcode)
            print('code:', code)
            if gmcode == 0:
                browser.refresh()
                time.sleep(2)
                browser.find_element_by_xpath('//*[@id="qd_closeDefaultWarningWindowDialog_id"]').click()
                input_info(browser)
                input_info(browser)
            else:
                try:
                    print('tijiao')
                    confirmBtn = browser.find_element_by_id("qr_submit_id")
                    browser.implicitly_wait(20)
                    time.sleep(3)
                    confirmBtn.click()
                except:pass
 
 
 
        if code == 1:
            tuisong()
            break
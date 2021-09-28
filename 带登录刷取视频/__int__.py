#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:HarryDong
# datetime:2021-07-20 20:03
# software: PyCharm


import json
import os
import re
import sys
import time

from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('lang=zh_CN.UTF-8')
options.add_argument("--mute-audio")  # 静音
options.add_argument("--no-sandbox")  # 非模拟环境
prefs = {
    'profile.default_content_setting_values': {
        'images': 2
    }
}
options.add_argument("--window-size=4000,8000")
options.add_argument('--headless')  # 不显示窗口

'''不显示图片'''
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(chrome_options=options)
if not os.path.exists('./log'):
    os.mkdir('./log')  # 输出截屏和日志的文件夹
print('=====================静音模式已启动============================')


def mian():
    # is_login()
    driver.get(url='https://www.yuketang.cn/web/?next=/v2/web/index')
    driver.maximize_window()
    if os.path.exists('cookie.txt'):
        listCookies = get_cookie()
        if listCookies:
            for i_ck in listCookies:
                driver.add_cookie(i_ck)
                print(i_ck)
            driver.refresh()
            time.sleep(5)
            driver.get(url='https://www.yuketang.cn/web/?next=/v2/web/index')
            driver.maximize_window()
            driver.switch_to.window(driver.window_handles[-1])
        else:
            import login
            login.login_ykt()  # 启动登录网页，目前没有针对cookie 过期做出解释
    else:
        import login
        login.login_ykt()  # 启动登录网页，目前没有针对cookie 过期做出解释

    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(5)
    driver.find_element_by_id('tab-student').click()
    shuake_mian(0)


def shuake_mian(itm):
    print('========================开始刷课================================')
    # print(driver.find_elements_by_xpath('//*[@id="el-popover-2384"]/div[1]')[0].text())
    time.sleep(5)
    lesson = driver.find_elements_by_xpath('//div/h1')
    lesson[itm].click()
    access_course()
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    # print(cur_list)
    # cursorpoint = info.xpath('//li/div[1]/div/span')
    # curdata = info.xpath('// li/div[4]/span[1]/text()')
    # print(cursorpoint,curdata)


def get_cookie():
    # 读取cookie，从同目录的cookie.txt
    with open('cookie.txt', 'r', encoding='utf-8') as f:
        listCookies = json.loads(f.read())
    return listCookies


def is_login():
    # 判断登录，从sessionid
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


def shuake(text, course_name):
    # print(text)
    time.sleep(10)
    driver.switch_to.window(driver.window_handles[-1])
    driver.find_element_by_xpath('//*[@id="tab-student_school_report"]/span').click()
    driver.save_screenshot("./log/log8.png")
    url = driver.find_element_by_xpath(
        f'//*[@id="pane-student_school_report"]/div/div[2]/section[2]/div[2]/ul/li[' + str(text) + ']/div[1]/span')
    '''
    报错位置
    '''
    try:
        url.click()
        driver.save_screenshot("./log/log4.png")
    except Exception as e:
        print(e.args)
        driver.refresh()
        driver.save_screenshot("./log/log6.png")
        time.sleep(5)
        url.click()
    print(f'进入课程->>>>>>>>>>>>第{text}个课程，课程名字叫', course_name)
    # driver.switch_to.window(driver.window_handles[-1])
    # action = ActionChains(driver)
    # action.move_to_element(driver.find_element_by_class_name('xt_video_player_big_play_layer pause_show'))
    # print('已经移动过去')
    # driver.find_element_by_xpath('//ul/li[1]').click()
    # print('2倍速开启')
    while True:
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(10)
        # rata = driver.execute_script('return document.querySelectorAll("span.text")[1].innerHTML')
        # element = WebDriverWait(driver, 10).until(driver.find_elements_by_xpath('//*[@class="text"]'))
        try:
            driver.save_screenshot("./log/log2.png")
            rata = driver.find_elements_by_xpath('//*[@class="text"]')
            if rata:
                current_time_1 = re.search(r'\d+', rata[0].text).group(0)
                # print(rata.text, current_time_1)
                # document.querySelector("video").currentTime
                # document.querySelector("video").duration
                time.sleep(5)
                currentTime = driver.execute_script('return document.querySelector("video").currentTime')
                duration = driver.execute_script('return document.querySelector("video").duration')
                print('rate of progress:', currentTime / duration)
                if (current_time_1 == '100') or (currentTime / duration == 1):
                    print('已经完成', rata[0].text)
                    # print((current_time_1 == '100'), (currentTime / duration == 1))
                    driver.save_screenshot("./log/log3.png")
                    driver.close()
                    print('==========关闭视频窗口==========')
                    driver.switch_to.window(driver.window_handles[0])
                    driver.find_element_by_xpath('//*[@id="tab-student_school_report"]/span').click()
                    driver.save_screenshot("./log/log9.png")
                    print('==========进入目录界面==========')
                    driver.refresh()
                    break

                    pass
                else:
                    print('正在刷课------------>>>>>>>>>>>>>>>>>>>>>', rata[0].text)
                time.sleep(2)
        except AttributeError:
            print('对象没有这个属性')
        except RuntimeError:
            print('	一般的运行时错误')

        # driver.switch_to.window(driver.window_handles[-1])
        # driver.refresh()
        # print('刷新了一下')
        # time.sleep(2)
        # driver.execute_script('document.querySelector("#video-box > div > xt-wrap > xt-bigbutton > button").click')


def access_course():
    time.sleep(5)
    # print(driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/ul/li[4]'))
    driver.find_element_by_class_name('new').click()
    time.sleep(5)
    driver.save_screenshot("./log/log.png")
    info_list = driver.find_elements_by_xpath(
        '//*[@id="pane-student_school_report"]/div/div[2]/section[2]/div[2]/ul/li')
    time.sleep(5)
    cur_list = []  # 小节list
    count = 0
    to_do_lsit = []  # 未刷的list
    for info in info_list:
        count += 1
        # print(info.text)
        info = info.text
        cur_list.append(info.split('\n'))
        # print(len(info.split('\n')))
        if len(info.split('\n')) > 3:
            course_name = info.split('\n')[0]
            video_duration = info.split('\n')[3]
            video_duration_1 = video_duration.split('/')[0]
            # print(course_name, video_duration, video_duration_1)
            if float(video_duration_1) < 1.176:
                # print(count, course_name, video_duration, video_duration_1)
                to_do_lsit.append([count, course_name, video_duration, video_duration_1])
    print(to_do_lsit)
    print('===============================================================')
    if to_do_lsit:
        for c in to_do_lsit:
            time.sleep(5)
            shuake(str(c[0]), c[1])
    else:
        driver.get(url='https://www.yuketang.cn/v2/web/index')
        driver.switch_to.window(driver.window_handles[0])
        driver.refresh()
        shuake_mian(1)
        print('刷课已经完成了2门')


if __name__ == '__main__':
    mian()
    log_print = open('./log/Defalust.log', 'w')
    sys.stdout = log_print
    sys.stderr = log_print
# pyinstaller __int__.py  -F --icon="123.ico"

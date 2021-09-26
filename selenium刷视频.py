
from datetime import datetime
import requests
from selenium import webdriver
import time
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 全局超时时间
TIME_OUT = 100
# 防止503等待时间
WAIT_TIME = 2

# 具体可添加QQ 1141549077 交流

print('参数列表:', str(sys.argv))
# 根据参数动态获得配置文件,以及浏览器的用户配置
# 第一个参数是文件名 , 第二个参数是参数
courseCode = ""
if len(sys.argv) > 1:
    courseCode = sys.argv[1]
    print("参数为:"+ courseCode)

startTime = datetime.now()
print("************************开始刷视频啦 "+ str(startTime)+"*******************************")
cookies = []
userName = ""
password = ""
with open("user.txt","r",encoding="UTF-8") as configFile:
    for line in configFile:
        # 去除换行符
        lineSplit = line.strip().split(":")
        userName = lineSplit[0]
        password = lineSplit[1]
print("用户名:"+userName+" 密码:"+password)
print("step1 登录")
option = webdriver.ChromeOptions()
# 隐藏窗口
option.add_argument('headless')
option.add_experimental_option("excludeSwitches", ['enable-automation','enable-logging'])
driver = webdriver.Chrome(chrome_options=option)
# 模拟登陆
driver.get("http://student.ouchn.cn/")
WebDriverWait(driver, TIME_OUT).until(EC.presence_of_element_located((By.ID, "username")))
userNameInput = driver.find_element_by_id("username")
pwdInput = driver.find_element_by_id("password")
userNameInput.send_keys(userName)
pwdInput.send_keys(password)
driver.find_element_by_name("button").click()
WebDriverWait(driver, TIME_OUT).until(EC.presence_of_element_located((By.XPATH, "//button[text()='进入学习']")))

allCourse = driver.find_elements_by_xpath("//button[text()='进入学习']")
#http://ruanjian.ouchn.cn/course/view.php?id=5055
handleOrigin = driver.current_window_handle
url = None
for course in allCourse:
    # print(">>开始刷视频,课程为:"+dict[courseCode])
    # 切换到课程学习列表页面
    driver.switch_to.window(handleOrigin)
    course.click()
    handles = driver.window_handles  # 获取当前浏览器的所有标签页
    driver.switch_to.window(handles[1])
    WebDriverWait(driver, TIME_OUT).until(EC.presence_of_element_located((By.TAG_NAME, "title")))

    hostName = str(driver.current_url).split("/")[2]
    print("SpileUrl : " + str(str(driver.current_url).split("/")))
    print("HostName:"+hostName)

    # 判断是否是 需要刷的课程
    if courseCode not in driver.current_url:
        print("该课程不是需要刷的课程:" + driver.title)
        driver.close()
        continue



    print("Cookie:" + str(driver.get_cookies()))

    cookieHeader = ""
    for cookie in driver.get_cookies():
        cookieHeader += cookie['name'] + "=" + cookie['value'] + ";"
    cookieHeader = cookieHeader[:-1]
    requestHeader = {
        "Host": hostName,
        "Connection": "keep-alive",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/87.0.4280.88Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": cookieHeader
    }

    # 每个专题中取一个视频即可
    # //ul[@class="flexsections flexsections-level-2"]/li
    pageIdList = []
    ids = []
    sectionDivOverviews = driver.find_elements_by_css_selector(".section.main.aft")
    for sectionItem in sectionDivOverviews:
        # 每个里面取一个
        videoItems = sectionItem.find_elements_by_tag_name("a");

        if len(videoItems) < 1 :
            continue
        # 视频支取一个,而文章页面全部取出来
        isVideo = True
        for videoItem in videoItems:

            href = videoItem.get_attribute("href")
            hrefSplit = str(href).split('=')
            imgTag = videoItem.find_elements_by_tag_name("img")

            if len(imgTag) < 1 :
                continue
            # core_h 是视频 page_h是页面 , core_h打开需要提交表单,page_h不需要提交表单,关闭即可
            imgSrc = imgTag[0].get_attribute("src")
            #print("imgSrc:"+imgSrc)
            if "core_h.png" in imgSrc and isVideo:
                id = {}
                id['val'] = hrefSplit[1]
                id['attr'] = 'url'
                ids.append(id)
                isVideo = False
            if "page_h.png" in imgSrc:
                pageIdList.append(hrefSplit[1])
    print("所有视频的ID:"+str(ids))
    print("所有文章的ID:" + str(pageIdList))
    # 循环每个专题中的首个未看过的 视频Id
    sectionName = ""
    for id in ids:
        # 防止503异常
        time.sleep(WAIT_TIME)
        print(">>>> step3 开始打开视频网页")
        # 打开视频页面
        videoUrl = "http://"+hostName+"/mod/"+id["attr"]+"/view.php?id=" + id['val']
        driver.get(videoUrl)
        # 有可能不是视频网页
        WebDriverWait(driver, TIME_OUT).until(EC.presence_of_element_located((By.TAG_NAME, "title")))
        palyBtn = driver.find_elements_by_xpath('//*[@data-title="点击播放"]')
        # 不是视频页面,直接回退 , 不在这里判断视频,在下边重新获取后
        # if len(palyBtn) == 0:
        #     print(">>>> 3.1 不是视频网页,回退:" +videoUrl )
        #     driver.back()
        #     continue

        # 获取专题的名称
        sectionDiv = driver.find_elements_by_id("list");
        if len(sectionDiv) ==1:
            span = sectionDiv[0].find_elements_by_tag_name("span");
            if len(span) == 1:
                sectionName = span[0].text

        # 重新获取专题所有的视频 id
        videoIdList = []
        videoIdListInPage =driver.find_elements_by_xpath('//li[@typ="url"]')
        # 获取需要点开视频网站的ID
        pageLiListInPage = driver.find_elements_by_xpath('//li[@typ="page"]')
        for videoLi in videoIdListInPage:
            # 该视频已经看过
            if "url(c).png" in videoLi.find_element_by_tag_name("img").get_attribute("src"):
                continue
            # 打开页面
            videoIdList.append(videoLi.get_attribute("i"))

        # 打开视频网页并迅速完成
        for videoId in videoIdList:
            # 防止503异常
            time.sleep(WAIT_TIME)
            videoUrl = "http://"+hostName+"/mod/url/view.php?id=" + videoId
            driver.get(videoUrl)
            WebDriverWait(driver, TIME_OUT).until(EC.presence_of_element_located((By.TAG_NAME, "title")))
            # 获取播放按钮
            palyBtn = driver.find_elements_by_xpath('//*[@data-title="点击播放"]')
            # 不是视频页面,直接回退
            if len(palyBtn) == 0:
                print(">>>> 3.2 不是视频网页,回退:" + driver.title)
                driver.back()
                continue

            urlSpilt = str(driver.current_url).split("?")
            # 拼接新参数 mid -> cmid
            requestParam = urlSpilt[1].replace("mid","cmid")
            # 直接请求完成视频
            response = requests.get("http://"+hostName+"/theme/blueonionre/modulesCompletion.php?"+requestParam , headers=requestHeader)
            print("返回结果: status_code:"+str(response.status_code) +"  content:" +str(response.content) )
        print(">>>> 该专题视频已全部刷完,专题:" + sectionName)

    # 打开page文章页面,因为文章页面已获取全部
    print(">>>>Step4 开始打开文章页面")
    for pageId in pageIdList:
        # 防止503异常
        time.sleep(WAIT_TIME)
        # http://shandong.ouchn.cn/mod/page/view.php?id=889096
        pageUrl = "http://" + hostName + "/mod/page/view.php?id=" + pageId
        # print("打开文章:"+pageUrl)
        print("打开文章：" + driver.title)
        driver.get(pageUrl)
    print(">>>>Step4 文章页面已全部打开")

    #关闭当前标签页
    print("******* 该课程已刷完 : " + driver.title + "***********")
    driver.close()
    # 课程刷完,因为是单课程直接退出循环
    break

endTime = datetime.now()
speedTime = (endTime-startTime).seconds
print("***************全部视频已刷完 "+ str(endTime)+"*************************" + "共耗时间(秒):"+ str(speedTime) )

# 关闭所有窗口
driver.quit()



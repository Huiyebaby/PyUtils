# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 10:13:43 2021
 
@author: kkrdfai
"""
 
 
from lxml import etree
import urllib.request
import os
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import re
 
mainUrl = 'https://www.gufengmh8.com'
referer = 'https://www.gufengmh8.com/'
 
"""
get_html_code 获取url对应HTML代码的方法
 
Args:
    url:
        网页的连接地址
 
Returns:
    htmlcode:
        网页的html代码，String型数据
"""
def get_html_code(url):
    max_count = 6
    htmlcode = ''
    for i in range(max_count):
        print('No.'+str(i)+'   start load:' + url)
        try:
            req_one = urllib.request.Request(url)
            req_one.add_header('User-Agent', 'Mozilla/6.0')
            res_one = urllib.request.urlopen(req_one, timeout=60)
            htmlcode = res_one.read().decode('utf-8')
            res_one.close()
            break
        except:
            if i < max_count:
                continue
            else:
                print('多次重复读取网页信息失败')
    time.sleep(0.1)
    return htmlcode
 
"""
makedir 创建文件目录的方法
 
Args:
    num:
        目录名，章节名，可以传入int或者string
"""
def makedir(num):
    if os.path.exists(str(num)):
        print('检测到：' + str(num) + '目录已建立，跳过该任务。')
        pass
    else:
        print('创建目录：' + str(num))
        os.mkdir(str(num))
 
"""
downLoadImg 下载图片的方法
 
Args:
    url:
        网页的连接地址
    picdir：
        目录名
    index：
        图片编号，也是图片的文件名
"""
def downLoadImg(url, picdir,index):
    header = {'Referer': referer, 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',}
 
    req = urllib.request.Request(url, headers=header)
 
    Max_Num = 6
    for i in range(Max_Num):
        try:
            req = urllib.request.urlopen(req, timeout=60)
             
             
            #虽然网页图片内的连接最后的后缀是jpg，但是根据二进制码明显发现不是jpg，右键保存发现是webp格式。所以下载的时候直接保存为webp格式
             
            with open(picdir + '/' + str(index)+'.webp', 'wb') as f:
                f.write(req.read())
                print('图片：' + picdir + '/' + str(index) + '.webp保存完毕')
            time.sleep(1)
            break
        except:
            if i < Max_Num - 1:
                continue
            else:
                print('URLError: <urlopen error timed out> All times is failed ')
                 
                 
"""
get_chapters_list 下载的主要逻辑方法
 
Args:
    url:
        网页的连接地址，这里需要传入漫画目录的url
"""
def get_chapters_list(url):
    #获取目录网页的全部html代码
    htmlcode = get_html_code(url)
    #etree解析html代码
    html = etree.HTML(htmlcode)
    #根据xpath获取全部的章节
    chapters = html.xpath('//*[@id="chapter-list-54"]/li/a')
         
    #开始循环，不断的通过每一章的url来调用selenium读取漫画图片的地址
    for i in chapters:
        #刚刚的xpath获取的是<a>标签，所以直接可以获取<a>标签的href属性，现在获得的就是这一章的URL
        url = i.get('href')
        # i 是父级<a>标签， 章节的地址可以直接获得，但是章节名称是a标签的span子节点的text内容，需要xpath获取下面的span标签，进而获取章节名称
        title = i.xpath('./span')[0].text
         
        print('开始读取：'+title+"  地址："+url)
         
        #调用使用selenium的方法来获取这一个章节里的全部url，然后返回一个图片url的list
        #注意传入参数，之前<a>标签获取的地址是相对路径，需要加上主域名才能正常访问
        piclist = get_picurl_by_browser(mainUrl+url)
         
        #设定初始页码
        index = 1
         
        #进一步循环，通过刚刚获得的全部图片连接，一张一张下载图片并根据index页码保存文件
        for j in piclist:
            print('开始下载：'+j)
            #创建章节文件夹
            makedir(title)
            #下载图片
            downLoadImg(j, title,index)
            #页面增加
            index+=1
     
 
 
 
"""
get_picurl_by_browser 通过章节地址来使用selenium自动读取这一章所有图片地址的方法
 
Args:
    ch_url:
        章节首页的URL
 
Returns:
    urllist:
        获取到的全部图片地址，数据类型为数组
"""
def get_picurl_by_browser(ch_url):
    #创建空数组
    urllist = []
    #webdriver调用谷歌chrome
    browser = webdriver.Chrome()
     
    #打开漫画章节首页
    browser.get(ch_url)
     
    #等待1秒钟，这里等待并不是为了等待图片加载，selenium会在网页加载完成后开始执行之后的代码，这里的等待是为了防止偶尔出现加载错误
    time.sleep(1)
     
    #通过xpath获取图片元素
    img = browser.find_element_by_xpath('//*[@id="images"]/img')
     
    #获得元素后，读取图片元素的地址，这次获取是获取首页的图片
    imgurl = img.get_attribute('src')
    #降首页图片的地址加入数组
    urllist.append(imgurl)
     
    #这里是获取这一章节一共有多少页漫画，获取到的是类似 （1/20）这样的网页内页数提示，下面这个是获取提示的p标签元素
    pageElement = browser.find_element_by_xpath('//*[@id="images"]/p')
    #从<p>标签里获取文本信息
    pageString = pageElement.get_attribute('innerText')
     
    #使用正则表达式获取上面信息中心的全部数字
    pattern = re.compile(r'\d+')
    pageNum = pattern.findall(pageString)
     
    #第一个数字永远是1，我们需要的总页码是第二个数字，也就是下标为1的元素。同时，第一页已经看到了，只需要翻总页数-1 页就可以看到最后一页了
    pagecount = int(pageNum[1])-1
     
    #循环开始翻页获取每一张图片的地址
    for i in  range(pagecount):
     
        time.sleep(1)
         
        #网站支持方向键翻页，可以使用selenium调用方向键右键翻页。
        #这里注意，不要获取图片元素，然后在图片上send_keys，我们翻页是全局时间翻页的。
        ActionChains(browser).send_keys(Keys.RIGHT).perform()
         
        #翻页后获取图片地址
        img = browser.find_element_by_xpath('//*[@id="images"]/img')
        imgurl = img.get_attribute('src')
        #继续保存进数组
        urllist.append(imgurl)
     
    #本章节的全部图片都获取完毕后，关闭窗口
    browser.close()
    return urllist
 
 
if __name__ == '__main__':
    urlch = "https://www.gufengmh8.com/manhua/liangbuyi/#chapters"
    get_chapters_list(urlch)
    
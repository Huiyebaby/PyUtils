#from tkinter import Tk
import tkinter as tk
import time,requests,re,json,os
import urllib.request
from selenium import webdriver
from PIL import Image
session =requests.session()
tm = time.time()
# 创建主窗口
win = tk.Tk()
# 设置标题
win.title("小红书抓图     作者：小发哥")
 
# 窗体大小设置
width = 1100
height = 800
# 获取屏幕分辨率
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()
position = f"{width}x{height}+{(screen_width-width)/2:.0f}+{(screen_height-height)/2:.0f}"
#win.geometry(position)
win.geometry('785x500')
# 进入消息循环，可以写控件
 
# 通用页面headers
 
 
# 创建提示文本
lb = tk.Label(win, text='小红书链接：')
 
# 创建文本框
entry = tk.Entry(win,width=80)# width 设置输入框的宽度，以字符为单位，默认值是20
# 创建一个多行文本框
t = tk.Text(win, width=105,height=30)
 
 
def getid(url, cookies):
    url = url
    headers = {
        'Host': 'xhslink.com',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'Mobile/15E148 MicroMessenger/8.0.2(0x18000234) NetType/WIFI Language/zh_CN',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }
    resp = session.get(url, headers=headers, allow_redirects=False)
    text = resp.content.decode('utf-8')
    #print(text)
    id = re.compile('<a href="https://www.xiaohongshu.com/discovery/item/(.*?)share').findall(text)[
        0].replace('?', '')  # 获取博主id
    print(id)
    appuid = re.compile("appuid=(.*?)&").findall(text)[0]  # 提交下次get请求必要数据
    print(appuid)
    url1 = 'https://www.xiaohongshu.com/discovery/item/' + id
    print(url1)
    headers1 = {
 
        'cookie': cookies,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'Mobile/15E148 MicroMessenger/8.0.2(0x18000236) NetType/WIFI Language/zh_CN',
        'accept-language': 'zh-cn',
        'accept-encoding': 'gzip, deflate'
    }
    data1 = {
        'share_from_user_hidden': 'true',
        'xhsshare': 'CopyLink',
        'appuid': appuid,
        'apptime': '1640424647'
    }
    resp1 = session.get(url1, headers=headers1, params=data1)
    text1 = resp1.content.decode('utf-8')
    cookies = requests.utils.dict_from_cookiejar(resp1.cookies)
    print(text1)
    # print(resp1.headers)
    videourl = re.compile('"url":"(.*?)"').findall(text1)[-1].encode('utf8').decode('unicode_escape')
    # print(videourl)
    name = re.compile('"nickname":"(.*?)"').findall(text1)[1].replace('*', '')
    traceId = re.compile('traceId":"(.*?)"}').findall(text1)
    txt = re.compile('description":"(.*?)",').findall(text1)[0]
    txtname = name + '.txt'
    # print(name)
    toPath2 = r'E:\小红书'  # D:\pycharm\自动下单目录\小红书\图片库
    toPath1 = os.path.join(toPath2 + "\\" + name + ' ' + id)
    if not os.path.exists(toPath1):
        os.makedirs(toPath1)
    # print(txt)
    # print(traceId)
    if 'v.xiaohongshu' in videourl:
 
        path = os.path.join(toPath1, id + ".mp4")
        urllib.request.urlretrieve(videourl, filename=path)
        toPath3 = os.path.join(toPath1 + '\\' + txtname)
        t.insert("insert", f"开始下载视频...\n")
        with open(toPath3, 'a', encoding='utf-8') as f:
            f.write(txt)
        print('小主，视频已下载' + '!' + '在这个目录下:' + toPath1 + '\n')
        t.insert("insert", f'小主，视频已下载' + '!' + '在这个目录下:' + toPath1 + '\n')
    else:
        t.insert("insert", f"开始下载图片...\n")
        for x in traceId:
            if text1.find('WebPage') > 0 :
                pic = 'http://sns-img-hw.xhscdn.com/' + x
                path = os.path.join(toPath1, str(x) + ".webp")#文件格式判断是否是webp格式
                urllib.request.urlretrieve(pic, filename=path)
                t.insert("insert", f"{pic}\n")
                #t.insert("insert", f"获取到{len(imgs)}张图片\n")
                time.sleep(2)
 
            else:
                pic = 'http://sns-img-hw.xhscdn.com/' + x
                path = os.path.join(toPath1, str(x) + ".jpg")
                urllib.request.urlretrieve(pic, filename=path)
                t.insert("insert", f"{pic}\n")
                #t.insert("insert", f"获取到{len(imgs)}张图片\n")
                print(pic)
 
        toPath3 = os.path.join(toPath1 + '\\' + txtname)
        with open(toPath3, 'a', encoding='utf-8') as f:
            f.write(txt)
        print('小主，图片已下载' + '!' + '在这个目录下:' + toPath1 + '\n')
        t.insert("insert", f'小主，图片已下载' + '!' + '在这个目录下:' + toPath1 + '\n')
 
    return id, appuid
 
def getcook():
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')  # 设置option
    driver = webdriver.Chrome(chrome_options=option)  # 调用带参数的谷歌浏览器
    driver.get(
        "https://www.xiaohongshu.com/discovery/item/60688b91000000002103cabc?xhsshare=CopyLink&appuid=5d655b6e000000000100656a&apptime=1619168976")
    time.sleep(5)
    cookies = driver.get_cookies()
    # print(cookies)
    # print(type(cookies))
    a = cookies[0]['value']
    timestamp2sig = cookies[0]['name']
    timestamp2 = cookies[1]['value']
    xhsuid = cookies[2]['value']
    xhsTrackerId = cookies[4]['value']
    cookies_1 = 'timestamp2' + '=' + timestamp2 + ';' + timestamp2sig + '=' + a + ';' + 'xhsuid' + '=' + xhsuid + ';' \
                + \
                'extra_exp_ids=gif_clt1,ques_clt1; xhsTracker=url=noteDetail&xhsshare=CopyLink;' + 'xhsTrackerId' + \
                '=' + xhsTrackerId
    with open('cookies.txt', 'w', encoding='utf-8') as f:
        f.write(cookies_1)
    return cookies_1
 
    # print(text)
 
 
# 分析网页图片
 
 
 
 
# 事件函数
def down_img():
    # print("hello world")
    # 获取文本框内容
    url = entry.get()
    try:
        with open('cookies.txt', 'r', encoding='utf-8') as f:
            cookies = f.readline()
            getid(url, cookies)
    except:
        cookies = getcook()
        getid(url, cookies)
 
# 创建按钮
btn = tk.Button(win,text = '点击下载', command = down_img)
 
 
lb.grid(row=1,column=0,padx=10,pady=20)
entry.grid(row=1,column=1,pady=20)
btn.grid(row=1,column=2,padx=10,pady=20)
t.grid(row=3,column=0,padx=20,columnspan=10)
 
win.mainloop()
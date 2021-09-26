# 1.导入所需模块
import requests
from bs4 import BeautifulSoup
import re
import os
 
# print(len(json_list)) # 英雄总数量：95个英雄
# print(json_list) # 打印结果,了解json_list的构造
 
 
#整体思路：从json文件获得每个英雄的详情页、名称、序号，然后去每个英雄的详情页获取皮肤的数量、各皮肤名称和对应链接
#最后注意命名，用os新建对应英雄名称的文件夹下载图片
url_main = 'https://pvp.qq.com/web201605/herolist.shtml'
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55'}  # 添加用户代{过}{滤}理
def getHtml(url):
    global headers
    r = requests.get(url, headers=headers,timeout=10)
    r.raise_for_status()
    r.encoding=r.apparent_encoding#防止乱码
    return r.text
# 由网址获取返回的text
 
def getLink():
    # global headers
    print("正在查找所有英雄链接......")
    # soup=BeautifulSoup(html,'html.parser')
    # heroList=soup.find_all('a',href=re.compile(r'herodetail/\d{3}.shtml'))#正则查找英雄链接，是个列表
    url = 'http://pvp.qq.com/web201605/js/herolist.json' #奇怪的json文件
    r = requests.get(url, headers=headers,timeout=10)
    r.encoding = r.apparent_encoding  # 防止乱码
    heroList = r.json()
    print("获取英雄链接成功!")
    for each in heroList:
        id = each['ename']  # 获得英雄序号
        link='herodetail/'+str(id)+'.shtml'#获取英雄所在链接
        name=each['cname']#获取英雄名字
        savePic(link, name, id)
    print("所有英雄的皮肤下载完成!")
#由
 
def savePic(link,name,id):#上面代码中返回的链接,名字和英雄序号
    url='https://pvp.qq.com/web201605/'+link
    html=getHtml(url)
    soup = BeautifulSoup(html, 'html.parser')
    skinlist=soup.find('ul',class_='pic-pf-list')['data-imgname']#寻找皮肤字符串
    skin_count=skinlist.count('&')#找到皮肤数量
    skinlist=skinlist.replace('&','')#去&
    for i in range(10):#去数字
        skinlist=skinlist.replace(str(i),'')
    skin_name=skinlist.split('|')#得到皮肤名字列表
    localPath = 'pic/' + name + '/'  # 创建每个英雄的文件夹
    if not os.path.exists(localPath):  # 新建文件夹,判断是否存在
        os.mkdir(localPath)
    url_base = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/'  # 图片网址固定前缀
    global headers
    for i in range(1, skin_count + 1):
        # 网址拼接, 构造完整的图片网址
        url_pic = url_base + str(id) + '/' + str(id) + '-bigskin-' + str(i) + '.jpg'
        try:
            # 获取图片信息
            print("正在下载"+name+"的"+skin_name[i - 1]+"皮肤图片")
            picture = requests.get(url_pic,headers=headers).content
            # print(picture) # 打印图片网址
            # 下载图片 文件路径为: pic/英雄名/英雄名-皮肤名.jpg (需要新建pic文件夹)
            with open('pic/' + name + '/' + skin_name[i - 1] + '.jpg', 'wb') as f:
                f.write(picture)
            print("--->成功!")
        except requests.exceptions.ConnectionError:
            print('数据异常或错误!当前图片无法下载')
    print("所有"+name+"的英雄皮肤下载完成!")
 
def main():
    # main = getHtml(url_main)
    getLink()
main()
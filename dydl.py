import requests
import json
import os
import time
import re
import sys
import winsound
"""
1.根据用户页面分享的字符串提取短url
2.根据短url加上302获取location,提取sec_id
3.拼接视频列表请求url
params = {
    'sec_uid' : 'MS4wLjABAAAAbtSlJK_BfUcuqyy8ypNouqEH7outUXePTYEcAIpY9rk',
    'count' : '200',
    'min_cursor' : '1612108800000',
    'max_cursor' : '1619251716404',
    'aid' : '1128',
    '_signature' : 'PtCNCgAAXljWCq93QOKsFT7QjR'
}
"""
headers = {
"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Mobile Safari/537.36"
}
##############################################
# 可以选择：
# 1文件内编辑好
# 2交互窗口输入
# 3命令行传参
# string  = 'https://v.douyin.com/ePPVX3Q/'
# string = input('INPUT URL (like:【在抖音，记录美好生活！ https://v.douyin.com/ekkTsYw/】):')
if(len(sys.argv)==1):
    string = input('INPUT URL (like:【在抖音，记录美好生活！ https://v.douyin.com/ekkTsYw/】):')
else:
    string = sys.argv[1]
 #############################################
try:
    shroturl = re.findall('[a-z]+://[\S]+', string, re.I|re.M)[0]
except IndexError:
    print('链接读取错误，程序退出')
    sys.exit(1)
else:
    print('短链接：'+shroturl)
    startpage = requests.get(url=shroturl, headers=headers, allow_redirects=False)
  
    location = startpage.headers['location']
    print(location)
    sec_uid = re.findall('(?<=sec_uid=)[a-z，A-Z，0-9, _, -]+', location, re.M|re.I)[0]
    getname = requests.get(url='https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid={}'.format(sec_uid), headers=headers).text
    print(getname)
    userinfo = json.loads(getname)
    name = userinfo['user_info']['nickname']
    print('用户名：'+userinfo['user_info']['nickname'])
    Path = name
    if os.path.exists(path=Path) == False:
        os.mkdir(path=Path)
    else:
        print('目录已存在')
    os.chdir(path=Path)
      
"""new function"""
year = ('2018','2019','2020','2021')
month = ('01','02','03','04','05','06','07','08','09','10','11','12')
j=1
zx_time_old=time.time()
#timepool = [x+'-'+y+'-01 00:00:00' for x in year for y in month ]
timepool = [x+'-'+y+'-01' for x in year for y in month ]
# print(timepool)
k = len(timepool)
for i in range(k) :
    if i < k-1 :
        beginarray = time.strptime(timepool[i], "%Y-%m-%d")
        #beginarray = time.strptime(timepool[i], "%Y-%m-%d %H:%M:%S")
        endarray = time.strptime(timepool[i+1], "%Y-%m-%d")
        #endarray = time.strptime(timepool[i+1], "%Y-%m-%d %H:%M:%S")
        t1 = int(time.mktime(beginarray) * 1000)
        t2 = int(time.mktime(endarray) * 1000)
        # print(t1,t2)
  
        params = {
            'sec_uid' : sec_uid,
            'count' : 200,
            'min_cursor' : t1,
            'max_cursor' : t2,
            'aid' : 1128,
            '_signature' : 'PtCNCgAAXljWCq93QOKsFT7QjR'
        }
        awemeurl = 'https://www.iesdouyin.com/web/api/v2/aweme/post/?'
        awemehtml = requests.get(url=awemeurl, params=params, headers=headers).text
        data = json.loads(awemehtml)
        print(data)
        # print(type(data))
        awemenum = len(data['aweme_list'])
        if(awemenum > 0):
           print('=============================================')
           print('从'+timepool[i]+'到'+timepool[i+1]+'共有【'+str(awemenum)+'】个视频')
           print('=============================================')
        # print(awemenum)
        break
        for i in range(awemenum):
        # 将文件名中含有Windows下有可能会产生错误的符号进行转义，变成全角符号
            videotitle = data['aweme_list'][i]['desc'].replace("?", "").replace("\"","＼").replace("\x83","＼").replace("\x08","＼").replace("\n","＼").replace("\r","＼").replace(":","：").replace("/","／").replace("|","｜").replace(":","：").replace("#","＃").replace(">","＞").replace("<","＜").replace("@抖音小助手","").replace("@DOU+小助手","").replace("@抖音科技","").replace("@抖音财经","").replace("@DOU知计划","")
            # 将生成的文件名从0开始排序，序号保留四位
            videotitle = str(j).rjust(4,'0')+'.'+videotitle
            # 全局计数从旧到新命名下载的文件
            j=j+1
            if (j>-1):
                print ('videotitle：'+videotitle)
                videourl = data['aweme_list'][i]['video']['play_addr']['url_list'][0]
                print ('videourl：'+videourl)
                start = time.time()
                print('视频：{} 开始下载'.format(videotitle))
                with open(videotitle+'.mp4', 'wb') as v:
                    try:
                        v.write(requests.get(url=videourl, headers=headers).content)
                        end = time.time()
                        cost = end - start
                        print('{}  下载耗时： {}秒'.format(videotitle, round(cost,2)))
                    except Exception as e:
                        print('下载错误')
        # print('下载结束')
        # break
            
zx_time_new=time.time()
duration=zx_time_new-zx_time_old
 
print('总计下载'+str(j)+'个文件，共耗时'+str(round(duration,2))+'秒，平均每个视频下载用时'+str(round(duration/j,2))+'秒')
winsound.Beep(1000,700)
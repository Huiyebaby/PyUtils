
import requests
from bs4 import BeautifulSoup
import os

headers = {
    'referer': "https://www.mzitu.com/",
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' 'AppleWebKit/537.36 (KHTML, like Gecko)' 'Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'
}


def all_url():
    for i in range(1, 200):
        try:
            urls = 'https://www.mzitu.com/xinggan/page/%s/' % i
            print(urls)
            html = requests.get(urls, headers=headers)
            stats = str(html.status_code)
            if stats == '200':
                content = BeautifulSoup(html.content, 'html.parser', from_encoding='gb18030')
                div = content.find(name='div', attrs={'class': 'postlist'})
                for li in div.find_all('li'):
                    a = li.find('a')['href']
                    print(a)
                    html1 = requests.get(a, headers=headers)
                    stats1 = str(html1.status_code)
                    soup = BeautifulSoup(html1.content, 'html.parser', from_encoding='gd18030')
                    em_list = soup.find_all('div', {'class': 'pagenavi'})
                    for span in em_list:
                        span1 = span.get_text()
                        print(span1[10:12])
                        for j in range(2, int(span1[10:12])):
                            urla = a + '/%s'%j
                            print(urla)
                            html2 = requests.get(urla, headers=headers)
                            stats2 = str(html2.status_code)
                            soup1 = BeautifulSoup(html2.content, 'html.parser', from_encoding='gd18030')
                            if stats2 == '200':
                                div_url = soup1.find('div', class_='main-image').find('img')['src']
                                div_name = soup1.find('div', class_='main-image').find('img')['alt']
                                div_name1 = soup1.find('div', class_='main-image').find('img')['alt'] + str(j)
                                PATH = 'D:\新建文件夹\mz' + "" + div_name
                                if not os.path.exists(PATH):
                                    os.mkdir(PATH)

                                pic = requests.get(div_url, headers=headers)
                                print("正在下载： " + div_name1)
                                with open(f"{PATH}\{div_name1}.jpg", "wb") as img:
                                    img.write(pic.content)
                            elif stats == '404':
                                break
            elif stats == '404':
                break
        except:
            print('访问频繁!')


all_url()
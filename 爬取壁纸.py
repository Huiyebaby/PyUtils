import math
import os
import time

from lxml import etree

import requests

temp_data = {
    'api': 'http://www.netbian.com/',
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    },
    'classification': [
        'rili', 'dongman', 'fengjing', 'meinv', 'youxi', 'yingshi', 'dongtai', 'weimei', 'sheji', 'huahui', 'dongwu',
        'jieri', 'renwu', 'meishi', 'shuiguo', 'jianzhu', 'tiyu', 'junshi', 'feizhuliu', 'huyan', 'lol',
        's/wangzherongyao', 'qita'
    ],
    'get_images_data': []
}

def get_images_list(url):
    html = requests.get(
        url,
        headers=temp_data['headers'],

    )
    html.encoding = 'GBK'
    html = etree.HTML(html.text)
    href = html.xpath('//div[@class="list"]/ul/li/a/@href')
    if not len(href):
        return temp_data['get_images_data']
    title = html.xpath('//div[@class="list"]/ul/li/a/img/@alt')
    for item in range(len(href)):
        temp_data['get_images_data'].append({
            'href': temp_data['api'] + href[item],
            'file_name': title[item]
        })
    return temp_data['get_images_data']

def get_page_images_url(url):
    html = requests.get(
        url,
        headers=temp_data['headers'],

    )
    html.encoding = 'GBK'
    html = etree.HTML(html.text)
    src = html.xpath('//div[@class="pic"]/p/a/img/@src')
    if len(src) == 1:
        return src[0]
    else:
        return 'error'

def down_images(path, images_url, images_name):
    images = get_page_images_url(images_url)
    if 'error' in images:
        return False
    if not os.path.exists(path):
        os.mkdir(path)
    file_name = path + images_name
    if not os.path.exists(file_name):
        images_file = requests.get(
            images,
            headers=temp_data['headers']
        )
        if 'image' in images_file.headers['Content-Type']:
            with open(file_name, 'wb') as f:
                f.write(images_file.content)
                return True
        else:
            return False
    else:
        return False

def run():
    print('''网站的壁纸按内容分类，共有 23 种，分别是：\n
        1. 日历    2. 动漫    3. 风景    4. 美女    5. 游戏    6. 影视    7. 动态\n
        8. 唯美    9. 设计    10.花卉    11.动物    12.节日    13.人物    14.美食\n
        15.水果    16.建筑    17.体育    18.军事    19.非主流  20.护眼    21.LOL\n
        22.王者荣耀 23.其他\n\n''')
    choice = int(input('按照分类下载，输入对应分类序号；随机下载，输入“0”。请输入：\n'))
    if choice > 22 or choice < 0:
        print('请输入正确的序号！')
        time.sleep(3)
        return False
    n = int(input("需要下载多少张壁纸？\n"))
    if n < 0:
        print('请输入正确的张数！')
        time.sleep(3)
        return False
    if choice == 0:
        choice = range(22)
    else:
        choice = choice - 1
    page_data = [
        temp_data['api'] + temp_data['classification'][choice]
    ]
    for i in range(2, math.ceil(n / 19) + 1):
        page_data.append(
            temp_data['api'] + '{name}/index_{num}.htm'.format(name=temp_data['classification'][choice], num=i))
    down_num = 0
    for pages in page_data:
        images_list_data = get_images_list(pages)
        if not len(images_list_data):
            print("获取图片列表失败！")
            time.sleep(3)
            return False
        for images_page_url in images_list_data:
            if down_num == n:
                print('下载完毕！')
                os.startfile('彼岸图片壁纸采集')
                time.sleep(3)
                return True
            if down_images('彼岸图片壁纸采集/', images_page_url['href'], images_page_url['file_name'] + '.jpg'):
                print(images_page_url['file_name'], '下载完成！')
                down_num = down_num + 1

if __name__ == '__main__':
    run()
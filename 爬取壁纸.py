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
    print('''��վ�ı�ֽ�����ݷ��࣬���� 23 �֣��ֱ��ǣ�\n
        1. ����    2. ����    3. �羰    4. ��Ů    5. ��Ϸ    6. Ӱ��    7. ��̬\n
        8. Ψ��    9. ���    10.����    11.����    12.����    13.����    14.��ʳ\n
        15.ˮ��    16.����    17.����    18.����    19.������  20.����    21.LOL\n
        22.������ҫ 23.����\n\n''')
    choice = int(input('���շ������أ������Ӧ������ţ�������أ����롰0���������룺\n'))
    if choice > 22 or choice < 0:
        print('��������ȷ����ţ�')
        time.sleep(3)
        return False
    n = int(input("��Ҫ���ض����ű�ֽ��\n"))
    if n < 0:
        print('��������ȷ��������')
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
            print("��ȡͼƬ�б�ʧ�ܣ�")
            time.sleep(3)
            return False
        for images_page_url in images_list_data:
            if down_num == n:
                print('������ϣ�')
                os.startfile('�˰�ͼƬ��ֽ�ɼ�')
                time.sleep(3)
                return True
            if down_images('�˰�ͼƬ��ֽ�ɼ�/', images_page_url['href'], images_page_url['file_name'] + '.jpg'):
                print(images_page_url['file_name'], '������ɣ�')
                down_num = down_num + 1

if __name__ == '__main__':
    run()
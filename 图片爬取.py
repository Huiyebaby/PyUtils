import requests, json, os, math, time, tqdm
from concurrent.futures import ThreadPoolExecutor

# 分类 url
category_url = 'http://service.aibizhi.adesk.com/v1/wallpaper/category'

# 壁纸 url
wallpaper_url = 'http://service.aibizhi.adesk.com/v1/wallpaper/category/{}/wallpaper'

# 获取到的分类列表
category_list = []

# 待下载的分类
down_num = 1

# 跳过数量
skip = 0

# 返回数量
limit = 20

headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'
}

# 获取图片分类
def _get_category():
    response = requests.get(url=category_url, headers=headers)
    response.encoding = 'gbk'
    data = json.loads(response.text)

    pc_category_name_list = []
    pc_category_id_list = []

    for item in data['res']['category']:
        name = item['name']
        cid = item['id']

        pc_category_name_list.append(name)
        pc_category_id_list.append(cid)

    category_list.append(pc_category_name_list)
    category_list.append(pc_category_id_list)

# 输入
def _show_input():

    input_str = ""
    for idx, item in enumerate(category_list[0]):
        input_str = input_str + str(idx + 1) + "-" + item + " "

    n_input = input(str(input_str) + "\n请输入下载分类：")

    if not n_input or not str.isdigit(n_input) or int(n_input) > len(category_list[0]):
        print("未输入任何分类,请重新输入!")
        _start()

    i_skip = input('请输入起始位置，默认为0：')

    if not i_skip:
        i_skip = 0
    elif not str.isdigit(i_skip):
        print("请输入数字！")
        _start()

    i_limit = input('请输入下载数量，默认为20：')

    if not i_limit:
        i_limit = 20
    elif not str.isdigit(i_limit):
        print("请输入数字！")
        _start()

    if int(i_limit) > 1000:
        i_limit = 1000

    global limit, skip, down_num

    skip = int(i_skip)
    limit = int(i_limit)
    down_num = int(n_input)

# 获取图片 url
def _get_img_url(down, skip, limit):    

    img_list = {}
    title_list = []
    href_list = []

    url = wallpaper_url.format(category_list[1][down - 1])

    # 每次最大获取20张图片链接
    t = 0
    while limit > 0:
        # 参数
        if limit > 20:
            params = '?skip={}'
            params = params.format(str(20 * t + skip))
        else:
            params = '?skip={}&limit={}'
            params = params.format(str(20 * t + skip), str(limit))

        # 获取 json
        response = requests.get(url=url + params, headers=headers)
        response.encoding = 'gbk'
        page_text = response.text

        arr = json.loads(page_text)

        # # 循环取出列表元素
        for ul in arr['res']['wallpaper']:
            href = ul['img']
            title = ul['id'] + '.jpg'

            # 将取出的图片链接和标题，存放到img_list中
            title_list.append(title)
            href_list.append(href)
        limit -= 20
        t += 1

    img_list = {'title': title_list, 'href': href_list}

    # 与本地文件夹内文件比较，去重
    if not os.path.exists(os.getcwd() + '/' + category_list[0][down - 1]):
        return img_list

    path = str(os.getcwd() + '/' + category_list[0][down - 1])
    filelist=os.listdir(path)

    # 倒序遍历删除已经下载过的图片
    for i in range(len(img_list['title']) - 1, -1, -1):
        if img_list['title'][i] in filelist:
            img_list['title'].remove(img_list['title'][i])
            img_list['href'].remove(img_list['href'][i])

    return img_list

# 下载
def _down_img(down_num):

    global skip, limit

    img_list = _get_img_url(down_num, skip, limit)
    filepath = category_list[0][down_num - 1]

    if not os.path.exists(os.getcwd() + '/' + filepath):
        os.mkdir(filepath)

    title_list = img_list['title']
    href_list = img_list['href']

    # 循环取出图片详情页地址和标题，下载，显示进度条
    for i in tqdm.trange(len(title_list)):

        title = title_list[i]
        img_url = href_list[i]

        # 将获取到到图片地址下载保存
        img_data = requests.get(img_url, headers=headers).content

        with open(filepath + '/' + title, 'wb') as fp:
            fp.write(img_data)

def _start():
    _get_category()
    _show_input()
    start = time.time()
    with ThreadPoolExecutor(8) as t:
            t.submit(_down_img, down_num) 
    end = time.time()
    print('——————程序执行完毕——————')
    print('——————耗时 ' + "{:.2f}".format(end-start) + '秒——————')

if __name__=='__main__':
    while True:
        _start()

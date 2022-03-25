import json
import multiprocessing
from os import makedirs
from os.path import exists
import requests
import logging
import re
from urllib.parse import urljoin
 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
 
BASE_URL = 'https://ssr1.scrape.center'
TOTAL_PAGE = 10
 
 
def scrape_page(url):
    logging.info('scraping %s...', url)  # 正常程序执行过程中的一些事件的触发记录 logging.info()
    try:
        response = requests.get(url)
        if response.status_code == 200:  # 网页响应状态码 == 200
            return response.text  # 返回element
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)
 
 
def scrape_index(page):  # 获取页码参数
    index_url = f'{BASE_URL}/page/{page}'  # url拼接
    return scrape_page(index_url)  # 调用scrape_page(url)，爬取每一页内容，返回每页HTML代码
 
 
def parse_index(html):
    pattern = re.compile('<a.*?href="(.*?)".*?class="name">')  # 正则表达式，获取电影详情链接
    items = re.findall(pattern, html)  # 非贪婪通用匹配，返回相应结果，赋值给items
    if not items:  # 如果items为空
        return []  # 返回空列表
    for item in items:  # 如果不为空，做遍历处理  item为链接详情（/detail/1）
        detail_url = urljoin(BASE_URL, item)  # 拼接  urljoin(域名，详情)
        logging.info('get detail url %s', detail_url)  # 输出日志，电影详情页面完整链接
        yield detail_url  # 生成器，将链接放入列表中，方便遍历使用
 
 
def scrape_detail(url):  # 创建方法，方便电影详情页链接调用scrape_page(url)
    return scrape_page(url)  # 再次返回HTML代码
 
 
def parse_detail(html):
    cover_pattern = re.compile(
        'class="item.*?<img.*?src="(.*?)".*?class="cover">', re.S)
    name_pattern = re.compile('<h2.*?>(.*?)</h2>')
    categories_pattern = re.compile('<button.*?category.*?<span>(.*?)</span>.*?</button>', re.S)
    published_at_pattern = re.compile('(\d{4}-\d{2}-\d{2})\s?上映')
    drama_pattern = re.compile('<div.*?drama.*?>.*?<p.*?>(.*?)</p>', re.S)
    score_pattern = re.compile('<p.*?score.*?>(.*?)</p>', re.S)
 
    cover = re.search(cover_pattern, html).group(1).strip() if re.search(cover_pattern, html) else None  # 如果取不到，返回空
    # strip() 用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列 strip('字符')
    name = re.search(name_pattern, html).group(1).strip() if re.search(name_pattern, html) else None
    categories = re.findall(categories_pattern, html) if re.findall(categories_pattern, html) else []
    published_at = re.search(published_at_pattern, html).group(1) if re.search(published_at_pattern, html) else None
    drama = re.search(drama_pattern, html).group(1).strip() if re.search(drama_pattern, html) else None
    score = float(re.search(score_pattern, html).group(1).strip()) if re.search(score_pattern, html) else None
 
    return {
        'cover': cover,
        'name': name,
        'categories': categories,
        'published_at': published_at,
        'drama': drama,
        'score': score
    }
 
 
RESULTS_DIR = 'results'  # 定义保存数据的文件夹
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)  # 判断文件夹是否存在，不存在就创建
 
 
def save_data(data):
    name = data.get('name')  # 获取电影名称
    data_path = f'{RESULTS_DIR}/{name}.json'  # 创建json文件，以电影名称命名
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    # 使用json.dump()方法将data转换为json格式并写入文件中；ensure_ascii=False不使用ascli编码，即，以正常的中文文本呈现；
    # indent=2设置json结果有两行缩进，让数据的格式显得更加美观
 
 
def main(page):
    index_html = scrape_index(page)
    detail_urls = parse_index(index_html)
    for detail_url in detail_urls:
        detail_html = scrape_detail(detail_url)
        data = parse_detail(detail_html)
        logging.info('get detail data %s', data)
        logging.info('saving data to jsin file')
        save_data(data)
        logging.info('data saved successfully')
 
 
if __name__ == '__main__':
    pool = multiprocessing.Pool()
    # 创建进程池，multiprocessing.Pool(processes=2)，有一个processes参数，这个参数可以不设置，如果
    # 不设置函数会跟根据计算机的实际情况来决定要运行多少个
    # 进程，我们也可自己设置，但是要考虑自己计算机的性能
    pages = range(1, TOTAL_PAGE + 1)  # 需要遍历的页码
    pool.map(main, pages)  # map()函数会遍历第二个参数的列表元素一个个的传入第一个参数我们的函数中，第一个参数是我们需要引用的函数  例一
    pool.close()  # 关闭进程池
    pool.join()  # 线程池内任务完成后，执行pool.join()后的代码
    logging.info('任务完成啦，哈哈哈！ %s')
 
# 例一
# import multiprocessing
# def main(page):
#     index_url = f'/page/{page}'
#     print(index_url)
# if __name__ == '__main__':
#     pool = multiprocessing.Pool()
#     pages = range(1, 11)  #
#     pool.map(main, pages)
#     pool.close()
#     pool.join()
#多进程：
import multiprocessing
import os

class ProcessClass(multiprocessing.Process):
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            if self.queue.empty():
                break
            else:
                item = self.queue.get()
                self.parse(item)

    def parse(self, item):
        print('[{}]号进程:{}'.format(os.getpid(), item))

def main():
    # 队列必须使用多进程的队列，使用queue模块会报错
    queue = multiprocessing.Queue()
    for i in range(20):
        queue.put(i)

    process_list = []
    process_num = 4
    for i in range(process_num):
        p = ProcessClass(queue)
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()

if __name__ == '__main__':
    main()
	
#多线程二
import queue
import threading

# 解析线程类
class Parse(threading.Thread):
    def __init__(self, number, data_list, req_thread):
        super(Parse, self).__init__()
        self.number = number
        self.data_list = data_list
        self.req_thread = req_thread
        self.is_parse = True  # 判断是否从数据队列里提取数据

    def run(self):
        print('启动%d号解析线程' % self.number)
        while True:
            # 如何判断解析线程的结束条件
            for t in self.req_thread:
                if t.is_alive():
                    break
            else:
                if self.data_list.qsize() == 0:
                    self.is_parse = False

            if self.is_parse:  # 解析
                try:
                    data = self.data_list.get(timeout=3)
                except Exception as e:
                    data = None
                if data is not None:
                    self.parse(data)
            else:
                break
        print('退出%d号解析线程' % self.number)

    # 页面解析函数
    def parse(self, data):
        # 下载文件
        pass

# 采集线程类
class Crawl(threading.Thread):
    def __init__(self, number, req_list, data_list):
        super(Crawl, self).__init__()
        self.number = number
        self.req_list = req_list
        self.data_list = data_list
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
        }

    def run(self):
        print('启动采集线程%d号' % self.number)
        while self.req_list.qsize() > 0:
            url = self.req_list.get()
            print('%d号线程采集：%s' % (self.number, url))
            # time.sleep(random.randint(1, 3))

            self.data_list.put("填充详细页面链接")  # 向数据队列里追加

def main():
    concurrent = 3
    conparse = 3

    # 生成请求队列
    req_list = queue.Queue()
    # 生成数据队列
    data_list = queue.Queue()

    # 填充请求数据
    for i in range(1, 13 + 1):
        base_url = 'https://www.baidu.com/{}.html'.format(i)
        req_list.put(base_url)

    # 生成N个采集线程
    req_thread = []
    for i in range(concurrent):
        t = Crawl(i + 1, req_list, data_list)  # 创造线程
        t.start()
        req_thread.append(t)

    # 生成N个解析线程
    parse_thread = []
    for i in range(conparse):
        t = Parse(i + 1, data_list, req_thread)  # 创造解析线程
        t.start()
        parse_thread.append(t)

    for t in req_thread:
        t.join()
    for t in parse_thread:
        t.join()

if __name__ == '__main__':
    main()
    
#多线程一
# -*- coding: utf-8 -*-
import time
from queue import Queue
from threading import Thread

class Demo(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            q_url = self.queue.get()
            try:
                self.parse(q_url)
            finally:
                self.queue.task_done()

    def parse(self, q_url):
        print("开始解析链接:", q_url)

if __name__ == '__main__':
    start = time.time()
    base_url = 'https://www.baidu.com/{}.html'
    url_list = [base_url.format(i) for i in range(1, 201)]

    queue = Queue()

    for x in range(20):
        worker = Demo(queue)
        worker.daemon = True
        worker.start()

    for url in url_list:
        queue.put(url)

    queue.join()

    print('下载完毕耗时:{}s'.format(round(time.time() - start, 2)))
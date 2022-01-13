import re
import aiohttp
import asyncio
import aiofiles
from fake_useragent import UserAgent
import requests
 
ua = UserAgent().random
 
class Spider(object):
 
    def __init__(self,cookies):
        self.headers = {'User-Agent': ua}
        self.cookies = cookies
        self.url = 'http://www.sogou.com/web'
        self.path = '.'                          #存储路径(默认当前路径)
 
    async def get_url(self, url,params):
        async with aiohttp.ClientSession() as client:
            async with client.get(url, headers=self.headers,params=params,cookies=self.cookies) as resp:
                if resp.status == 200:
                    return await resp.text()
 
    async def parsel_data(self,param,query):
        semaphore = asyncio.Semaphore(5)
        html = await self.get_url(self.url,param)
        excel_path = '/'.join([self.path,f'{query}.xlsx'])
        data_list = re.findall('""><!--awbg\d+-->(.*?)</a>',html)
        tasks = [asyncio.create_task(self.write_data(excel_path,data,semaphore)) for data in data_list]
        await asyncio.wait(tasks)
 
    async def write_data(self,path,data,semaphore):
        async with semaphore:
            async with aiofiles.open(path, 'a') as f:
                print(data)
                data = data + '\n'
                await f.write(data)
 
 
 
    async def main(self,):
        query = input('请输入要查询的域名：')
        print('--------------------开始爬取-------------------')
        for page in range(1,21):
            params = {
                "query": f"site:{query}",
                'page': int(page)
            }
            await self.parsel_data(params,query)
        print('--------------------爬取完成-------------------')
 
def get_new_cookies():    #获取最新的cookie防止访问次数超限
    url = 'https://v.sogou.com/v?ie=utf8&query=&p=40030600'
    headers = {'User-Agent': ua}
    rst = requests.get(url=url,
                       headers=headers,
                       allow_redirects=False,)
    cookies = rst.cookies.get_dict()
    return cookies
 
if __name__ == '__main__':
    cookie = get_new_cookies()
    run = Spider(cookie)
    asyncio.run(run.main())
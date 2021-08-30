import scrapy
import re
from urllib.request import urlretrieve
from pathlib import Path
import inspect
import os
import json

from tutorial.myItem import myItem


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["gllmh.com"]
    start_urls = [
        # "http://www.gllmh.com/ymgj/7949.html",
        "http://www.gllmh.com/ymgj/"
    ]
    def parse(self, response):
        listpages = response.xpath('/html/body/div[3]/div[1]/div[2]/li[@class="thisclass"]/text()');
        listlast =response.xpath('/html/body/div[3]/div[1]/div[2]/li[last()]/span/strong[1]');
        lastPage =list(listlast.extract())[0];
        thisPage =list(listpages.extract())[0]
        pages = filter(str.isdigit,str(lastPage))
        # 获取总页数
        lastpageIndex = ''.join(list(pages))
        detailHref = response.xpath('/html/body/div[3]/div[1]/ul/li/h3/a/@href').extract()
        detailtext = response.xpath('/html/body/div[3]/div[1]/ul/li/h3/a/@title').extract()
        print(detailHref)
        print(detailtext)
        # listTor = []
        # for index in range(0,len(detailHref)):
        #     tempTor = myItem();
        #
        #     # datas = json.dumps(response.text, ensure_ascii= False, indent=4, separators=(',', ': '))
        #     # json_data = json.loads(datas).encode('utf-8').decode('unicode_escape')
        #     tempTor['title']=detailtext[index]
        #     tempTor['desc']=detailHref[index].replace('/ymgj/','').replace('.html','')
        #     tempTor['link']='http://www.gllmh.com'+detailHref[index]
        #     listTor.append(dict(tempTor))
        # print(json.dumps(listTor).encode('utf-8').decode('unicode_escape'))
        # jsonFileName = 'list_0.json'
        # urlFile = response.url.replace('http://www.gllmh.com/ymgj/','').replace('.html','')
        # if(len(urlFile)>0):
        #     jsonFileName =urlFile+'.json'
        # jsonFilePath ='./image/ymgj/'+jsonFileName
        # print(os.path.exists(os.path.dirname(jsonFilePath)))
        # if(not os.path.exists(os.path.dirname(jsonFilePath))):
        #     os.makedirs(os.path.dirname(jsonFilePath))
        # with open (jsonFilePath,'w+') as file_object:
        #     file_object.write(json.dumps(listTor).encode('utf-8').decode('unicode_escape'))
        for page in  detailHref:
            pageUrl = 'http://www.gllmh.com'+page
            # _master
            yield scrapy.Request(pageUrl,callback=self.parse_master)
            print(pageUrl)
        # print(tor)
        # print(int(lastpageIndex))
        if(response.url != 'http://www.gllmh.com/ymgj/'):
            return;
        for index in range(1,int(lastpageIndex)+1):
            if(index != 1):
                exurl = 'http://www.gllmh.com/ymgj/list_'+str(index)+'.html'
                print(exurl)
                yield scrapy.Request(exurl,callback= self.parse)

    # "http://www.gllmh.com/ymgj/7949.html",
    # def parse_master(self, response):
    def parse_master(self, response):
        # print(response.body.decode('utf-8'))
        titlePage = filter(str.isdigit,str(response.url))
        # 获取总页数
        titlePageIndex = ''.join(list(titlePage))
        url_title = response.xpath('/html/body/div[3]/div[1]/div/div[2]/div[1]/h3/text()')
        url_time = response.xpath('/html/body/div[3]/div[1]/div/div[2]/div[1]/p/span[3]/text()')
        print(url_title.extract())
        print(url_time.extract())

        url_main_pic =response.xpath('/html/body/div[3]/div[1]/div/div[3]/section/p/img/@src')
        if(len(url_main_pic)<1):
            url_main_pic=response.xpath('/html/body/div[3]/div[1]/div/div[3]/section/section/p/img/@src')
        if(len(url_main_pic)<1):
            url_main_pic = response.xpath('/html/body/div[3]/div[1]/div/div[3]/p/img/@src')
        if(len(url_main_pic)<1):
            url_main_pic = response.xpath('/html/body/div[3]/div[1]/div/div[3]/img/@src')
        # /section
        # 第一页有section
        # /html/body/div[3]/div[1]/div/div[3]/section/p[2]/img
        print(url_main_pic.extract())
        img_index =0
        current_path =inspect.getfile(inspect.currentframe())
        dir_name=os.path.dirname(os.path.dirname(os.path.dirname(current_path)))
        my_file = Path('image/ymgj/'+titlePageIndex)
        imgFile =os.path.join(dir_name,my_file)
        print(imgFile);
        if os.path.exists(imgFile):
            print('存在')
        else:
            # 不存在则新建文件夹
            os.makedirs(imgFile)
        for imgsrc in url_main_pic.extract():
            img_index+=1
            print('1_'+str(img_index))
            if(os.path.exists('./image/ymgj/'+titlePageIndex+'/1_'+str(img_index)+'.jpg')):
                print('存在图片')
                break
            urlretrieve(imgsrc,'./image/ymgj/'+titlePageIndex+'/1_'+str(img_index)+'.jpg')
        url_page = response.xpath('/html/body/div[3]/div[1]/div/div[3]/section/div/div/li[1]/a/text()')
        if(len(url_page)<1):
            url_page = response.xpath('/html/body/div[3]/div[1]/div/div[3]/section/section/div/div/li[1]/a/text()')
        if(len(url_page)<1):
            url_page = response.xpath('/html/body/div[3]/div[1]/div/div[3]/div/div/li[1]/a/text()')
        if(len(url_page)<1):
            print('不走下一步')
            return;
        pages = list(filter(str.isdigit,str(url_page.extract())))[0]
        print(pages)
        for index in range(int(pages)):
            if index==0:
                next_page = titlePageIndex+'.html'
            else:
                if(os.path.exists('./image/ymgj/'+titlePageIndex+'/2_'+str(img_index)+'.jpg')):
                    print('存在图片，不走第二页')
                    break
                next_page = titlePageIndex + '_' + str(index+1)  + '.html'
                yield scrapy.Request('http://www.gllmh.com/ymgj/'+next_page,callback=self.parse_item)
            print('nextpage: %s' % next_page)


    def parse_item(self, response):
        thisurl =re.sub(r'_\d+.html','rrrrr',response.url)
        titlePage = filter(str.isdigit,str(thisurl))
        # 获取总页数
        titlePageIndex = ''.join(list(titlePage))
        # print(response.body.decode('utf-8'))
        url_title = response.xpath('/html/body/div[3]/div[1]/div/div[2]/div[1]/h3/text()')
        url_time = response.xpath('/html/body/div[3]/div[1]/div/div[2]/div[1]/p/span[3]/text()')
        print(url_title.extract())
        print(url_time.extract())
        url_main_pic =response.xpath('/html/body/div[3]/div[1]/div/div[3]/p/img/@src')
        if(len(url_main_pic)<1):
            url_main_pic=response.xpath('/html/body/div[3]/div[1]/div/div[3]/section/section/p/img/@src')
        if(len(url_main_pic)<1):
            url_main_pic = response.xpath('/html/body/div[3]/div[1]/div/div[3]/p/img/@src')
        if(len(url_main_pic)<1):
            url_main_pic = response.xpath('/html/body/div[3]/div[1]/div/div[3]/img/@src')
        # /section
        # 第一页有section
        # /html/body/div[3]/div[1]/div/div[3]/section/p[2]/img
        print(url_main_pic.extract())
        img_index =0
        current_path =inspect.getfile(inspect.currentframe())
        dir_name=os.path.dirname(os.path.dirname(os.path.dirname(current_path)))
        my_file = Path('image/ymgj/'+titlePageIndex)
        imgFile =os.path.join(dir_name,my_file)
        print(imgFile);
        thispages = response.xpath('/html/body/div[3]/div[1]/div/div[3]/div/div/li[@class="thisclass"]/a/text()');
        print(list(thispages.extract())[0]);
        if os.path.exists(imgFile):
            print('存在')
        else:
            # 不存在则新建文件夹
            os.makedirs(imgFile)
        for imgsrc in url_main_pic.extract():
            img_index+=1
            print(list(thispages.extract())[0]+'_'+str(img_index))
            if(os.path.exists('./image/ymgj/'+titlePageIndex+'/'+list(thispages.extract())[0]+'_'+str(img_index)+'.jpg')):
                print('存在图片')
                break
            urlretrieve(imgsrc,'./image/ymgj/'+titlePageIndex+'/'+list(thispages.extract())[0]+'_'+str(img_index)+'.jpg')
        # filename = response.url.split("/")[-2]
        # filePath = 'F:\\OneSelf\\GitPorject\\Py\\tutorial\\' + '1.txt'
        # with open(filePath, 'wb') as f:
        #     f.write(response.body.decode('utf-8').encode())

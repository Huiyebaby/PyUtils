import requests
import re
 
can_useip = []
cant_useip = []
ip_dict = {}
ip_list = []
port_list = []
timeout = int(input('请输入超时时间：'))
page = 1
 
url = 'http://httpbin.org/get'
def main():
    global ip_list,port_list,page
 
    url1 = 'https://www.kuaidaili.com/free/inha/'+str(page)+'/'
    res = requests.get(url1).text
 
    ip_list = re.findall('<td data-title="IP">(.*)</td>',res)
    port_list = re.findall('<td data-title="PORT">(.*)</td>',res)
    print('第%d页有'%page, len(ip_list),'个IP，正在检测第%d页ip是否存活'%page)
 
    for ip in range(len(ip_list)):
        ip_dict[ip_list[ip]] = port_list[ip]
 
    for i in list(ip_dict.items()):
        proxies = i[0] +':'+ str(i[1])
 
        ip = {
                'http':'http://'+proxies,
                'https':'https://'+proxies,
            }
        try:
            response = requests.get(url,proxies=ip,timeout=timeout)
            print(response.text)
            print(ip,'可以使用！')
            can_useip.append(proxies)
        except requests.exceptions.ProxyError as error:
            print(error)
            print(proxies,'已经失效！')
            cant_useip.append(proxies)
        except requests.exceptions.ConnectTimeout as error:
            print(error)
            print(proxies,'已经失效！')
            cant_useip.append(proxies)
        except requests.exceptions.ChunkedEncodingError as error:
            print(error)
            print(proxies, '已经失效！')
            cant_useip.append(proxies)
        except requests.exceptions.ReadTimeout as error:
            print(error)
            print(proxies, '已经失效！')
            cant_useip.append(proxies)
 
    print('第',page,'页筛选结束！共有%d个代{过}{滤}理可以使用，%d个已经失效。' % (len(can_useip),len(cant_useip)))
    page += 1
 
if __name__ == '__main__':
    all_page = int(input('要探测多少页的代{过}{滤}理：'))
    print(all_page,'页，共有：',all_page*15,'个代{过}{滤}理')
    for i in range(all_page):
        main()
    print('*'*80)
    print('筛选结束,以下是代{过}{滤}理状态：')
    print('可以使用的代{过}{滤}理：', can_useip)
    print('已经失效的代{过}{滤}理：', cant_useip)
    with open('存活代{过}{滤}理列表.txt','w') as f:
        for i in can_useip:
            f.write(i+'\n')
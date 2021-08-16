import requests
from lxml import etree
 
 
def web():
    response = requests.get('http://www.sjgsd.com/s/')
    print('状态码:', response.status_code)  # 打印状态码
    response.encoding = 'utf-8'  # 解码
 
    # 输出所有地区
    sel = etree.HTML(response.text)
    con1 = sel.xpath('/html/body/div[4]/dl/dd/a/@href')  # text()
    con2 = sel.xpath('/html/body/div[4]/dl/dd/a/text()')
    region = []
    for i, j in zip(con1, con2):
        init = [i, j]
        region.append(init)
 
    choice = input('输入要生成字典的地区 > ')
    for i in region:
        if choice == i[1]:
            choice2 = region.index(i) # 获取元素下标
            print(choice2,i[1])
 
    url = "http://www.sjgsd.com/" + region[choice2][0]
    web2(url)
 
 
def web2(url):
    number_paragraph = [130, 131, 132, 133, 134, 135, 136, 137, 138, 139,
                        150, 151, 152, 153, 155, 156, 157, 158, 159,
                        180, 181, 182, 183, 184, 185, 186, 187, 188, 189]
    global number
    number = []
 
    response = requests.get(url)
    print('状态码:', response.status_code)  # 打印状态码
    response.encoding = 'utf-8'  # 解码
 
    # 获取号码段
    sel = etree.HTML(response.text)
    for i in number_paragraph:
        con1 = sel.xpath('//*[@id="' + str(i) + '"]/dd/a/text()')
        for j in con1:
            number.append(j)
    print('一共有', len(number), '个号段\n共', len(number) * 10000, '个号码')
    input('回车继续 > ')
 
    generate_wordlist()
 
 
def generate_wordlist():
    wordlist = open('wordlist.txt', 'w')
 
    for i in number:
        for j in range(0, 10000):
            wordlist.write(str(i) + str("{:0>4d}".format(j)) + '\n')
    wordlist.close()
    print('生成字典完毕!')
 
 
if __name__ == '__main__':
    web()
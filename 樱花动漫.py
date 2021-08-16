from requests import get
import json
import re
 
mainurl = 'http://www.imomoe.la'
url1 = input()  # http://www.imomoe.la/player/5040-0-0.html
ex = '<script type="text/javascript" src="(/playdata/.*?.js).*?"></script>'
ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
ppurl = 'http://v.pptv.com/show/'
dllist = []
headers = {
    'Referer': url1,
    'User-Agent': ua
}
 
resp = get(url=url1)
url2 = re.findall(ex, resp.text, re.S)[0]
url2 = mainurl + url2
 
resp = get(url=url2, headers=headers)
tmp = re.findall(b'(\\[.*\\])', resp.content)[0]
dat = eval(tmp.decode('gbk'))
 
for l in dat:
    if l[0] == '优酷':
        for i in l[1]:
            vurl = re.findall('\$(.*?)\$', i)[0]
            if len(vurl) < 40:
                resp1 = get(url='https://v.jialingmm.net/mmletv/mms.php', params={'vid': vurl, 'type': 'letv'})
                vurl = re.findall('var video =  \'(.*?)\' ;', resp1.text, re.S)
            dllist.append(vurl)
        break
 
    if l[0] == '土豆' and re.findall('\$(.*?)\$', l[1][0])[0].isdigit() == False:
        for i in l[1]:
            print(i)
            vurl = re.findall('\$(.*?)\$', i)[0]
            resp1 = get(url=ppurl+vurl+'.html', headers={"User-Agent": ua})
            id = re.findall('var webcfg = [{]"id":(.*?)[,]', resp1.text, re.S)[0]
            resp2 = get(url=f'https://web-play.pptv.com/webplay3-0-{id}.xml?o=0&version=6&type=mhpptv&appid=pptv.web.h5&appplt=web&appver=4.0.7&cb=a', headers={"User-Agent": ua})
            dat = json.loads(resp2.text[2:-4])
            server = dat['childNodes'][3]['childNodes'][0]['childNodes'][0]
            rid = dat['childNodes'][-4]['rid']
            sum = len(dat['childNodes'][-4]['childNodes']) - 1
            kk = dat['childNodes'][-5]['childNodes'][-1]['childNodes'][0].split('%26')[0]
            ll = []
            for i in range(sum):
                vurl1 = f"https://{server}/{i}/0/1/{rid}?k={kk}&type=mhpptv"
                ll.append(vurl)
            dllist.append(ll)
        break
 
print(dllist)
print(len(dllist))
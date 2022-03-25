from pyppeteer import launch
import asyncio
import time
import json
import random
import cv2

def get_track(length):
    list = []
    x = random.randint(1,10)
    while length:
        list.append(x)
        length -= x
        if length > 0 and length <= 5:
            break
        elif 5 < length < 25:
            x = random.randint(2,length)
        else:
            x = random.randint(5,25)
    for i in range(length):
        list.append(1)
    return list

def change_size( file):
    image = cv2.imread(file, 1)  # 读取图片 image_name应该是变量
    img = cv2.medianBlur(image, 5)  # 中值滤波，去除黑色边际中可能含有的噪声干扰
    b = cv2.threshold(img, 15, 255, cv2.THRESH_BINARY)  # 调整裁剪效果
    binary_image = b[1]  # 二值图--具有三通道
    binary_image = cv2.cvtColor(binary_image, cv2.COLOR_BGR2GRAY)
    x, y = binary_image.shape
    edges_x = []
    edges_y = []
    for i in range(x):
        for j in range(y):
            if binary_image[j] == 255:
                edges_x.append(i)
                edges_y.append(j)

    left = min(edges_x)  # 左边界
    right = max(edges_x)  # 右边界
    width = right - left  # 宽度
    bottom = min(edges_y)  # 底部
    top = max(edges_y)  # 顶部
    height = top - bottom  # 高度
    pre1_picture = image[left:left + width, bottom:bottom + height]  # 图片截取
    return pre1_picture  # 返回图片数据
async def main(url):
    try:
        browser = await launch({'headless':False, 'dumpio': True, 'autoClose': False, 'args': ['--no-sandbox', '--window-size=1366,850']})
        page = await browser.newPage()
        await page.evaluateOnNewDocument('''() => {delete navigator.__proto__.webdriver;}''')
        await page.evaluateOnNewDocument('''() => {Object.defineProperty(navigator, 'webdriver', {get: () => undefined,});}''')
        await page.evaluateOnNewDocument('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-CN', 'cn'] }); }''')
        await page.evaluateOnNewDocument('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5, 6], }); }''')
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36')
        await page.setViewport({'width': 1366, 'height': 850})  # 更改浏览器分辨率
        await page.goto(url, {'waitUntil': 'domcontentloaded'})  # 进行第一次访问
        await page.waitFor(3000)
        authUrl = await page.content()
        if authUrl.find('向右拖动滑块填充拼图') != -1:
            el = await page.querySelector('#captcha_div > div > div.yidun_control')
            box = await el.boundingBox()
            while True:
                imageCard_list = []
                for imgItem in await page.xpath('//*[@id="captcha_div"]/div/div[1]/div/div[1]/img'):
                    imageCard = await (await imgItem.getProperty('src')).jsonValue()
                    imageCard_list.append(imageCard)
                from PIL import Image
                from io import BytesIO
                import requests
                import numpy as np
                target = 'target.jpg'  # 临时保存的图片名
                template = 'template.png'
                target_img = Image.open(BytesIO(requests.get(imageCard_list[0]).content))
                template_img = Image.open(BytesIO(requests.get(imageCard_list[1]).content))
                target_img.save(target)
                template_img.save(template)
                img_gray = cv2.imread(target, 0)
                img_rgb = change_size(template)
                template = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
                run = 1
                # 使用二分法查找阈值的精确值
                L = 0
                R = 1
                while run < 20:
                    run += 1
                    threshold = (R + L) / 2
                    if threshold < 0:
                        print('Error')
                        return None
                    loc = np.where(res >= threshold)
                    if len(loc[1]) > 1:
                        L += (R - L) / 2
                    elif len(loc[1]) == 1:
                        break
                    elif len(loc[1]) < 1:
                        R -= (R - L) / 2
                res = loc[1][0]
                await page.hover('#captcha_div > div > div.yidun_control > div.yidun_slider')  # 鼠标移动方块上
                await page.mouse.down({'delay': random.randint(20, 100), 'steps': 30})  # 鼠标拖动操作包括按下、移动、放开
                sixx = get_track(int(res+25))
                print(sixx)
                s = 0
                for i in sixx:
                    s += i
                    if i % 2:
                        await page.mouse.move(box['x'] + s, box['y'], {'delay': random.randint(20, 45), 'steps': 5})
                    else:
                        await page.mouse.move(box['x'] + s, random.randint(int(box['y']) + 10, int(box['y']) + 20), {'delay': random.randint(20, 45), 'steps': 5})
                await page.waitFor(random.randint(50, 150))
                await page.mouse.up({'delay': random.randint(20, 100), 'steps': 20})
                await page.waitFor(1000)
                authUrl = await page.content()
                if '向右拖动滑块填充拼图' in authUrl:
                    continue
                else:
                    user_ck = await page.xpath(f'//*[@id="submit-btn"]')
                    await user_ck[0].click()
                    await page.waitFor(1000)
                    authUrl = await page.content()
                    print('成功')
    except Exception as e:
        print(e)
    finally:
        if page.isClosed():
            pass
        else:
            await page.close()
if __name__ == '__main__':
    url ='http://app.miit-eidc.org.cn/miitxxgk/gonggao/xxgk/queryCpParamPage?dataTag=Z&gid=U3119671&pc=303'
    asyncio.get_event_loop().run_until_complete(main(url))

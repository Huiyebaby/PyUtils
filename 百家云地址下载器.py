# 已购买课程可以使用videoPlayerToken，但是我测试时候只能
def videoPlayerToken(courseId, video_id):
    url = "https://www.xxxxxx.com:xxxx/web/bjvod/videoPlayerToken"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'area': '0100000200',
        'companynum': '01000002',
        'content-length': '120',
        'content-type': 'application/json; charset=UTF-8',
        'origin': 'https://www.sjqhedu.cn',
        'referer': 'https://www.sjqhedu.cn/',
        'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'token': 'xxxxxxxxxxxxxxxxxxxxxxUo2g'
    }
    parameter = {
        "courseId": courseId,   # 课程ID
        "expires_in": 0,
        "t": str(int(round(time.time() * 1000))),
        "video_id": video_id    # 课程url(其实就是视频id号)
    }
    r = requests.post(url=url, headers=headers,
                      data=json.dumps(parameter, ensure_ascii=False).encode('utf-8'))
    json_str = json.loads(r.text)
    if "data" in json_str:
        return json_str['data']['token']
		
def getAllFormatPlayUrl(vid, tk):
    url = "https://www.baijiayun.com/vod/video/getAllFormatPlayUrl"
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'referer': 'https://www.sjqhedu.cn/',
        'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '30',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'cross-site'
    }
    parameter = {
        "vid": vid,    # 课程url(其实就是视频id号)
        "sid": "",
        "render": "jsonp",
        "client_type": "flash",
        "ver": 2,
        "token": tk,
        "callback": "jQuery00000000_10000000009",
        "_": str(int(round(time.time() * 1000))),
    }
    r = requests.get(url=url, headers=headers,
                     params=parameter)

    dick_str = r.text.replace("jQuery00000000_10000000009(", "").replace(")", "")
    return json.loads(dick_str)
    
def getCourseList():
    f = open('list1.json', encoding="utf8")
    t = json.load(f)
    return t['syllabus']
    
def Download():
    http = urllib3.PoolManager()   #下载视频使用urllib3库
    course_list = getCourseList()   # 获取全部课程
    # with open("test.txt", "w") as f:
    try:
        for courses in course_list:    # 遍历课程（1级目录）
            path = courses["name"].strip()
            if not os.path.isdir(path):
                os.mkdir(path)        # 创建文件夹保存视频
            for course in courses["list"]:  # 遍历课程（2级目录）/视频
                # print(course)
                if len(course["list"]) == 0:
                    token = videoPlayerToken(courseId=course["courseId"], video_id=course["url"])   # 获取token
                    if token == None:
                        continue

                    json_url = getAllFormatPlayUrl(course["url"], token)   # 获取加密的直链

                    mp4 = json_url["data"]["all_format_play_info"]["mp4"]  # 加密的直链的MP4的内容

                    if 'superHD' in mp4:
                        d_url = mp4["superHD"]["cdn_list"][0]["enc_url"]   # 获取其中一个加密的地址
                        r_url = js_code.call("decodeUrl", d_url)           # 获取真实直链
                        f_path = path + "/" + course["name"] + ".mp4"      # 下载视频病保存
                        # wget.download(r_url, path)  # 下载
                        r = http.request('GET', r_url)
                        with open(f_path, 'wb') as f:
                            f.write(r.data)

            # 下面内容重复就不再有注释了

                    if 'high' in mp4:
                        d_url = mp4["high"]["cdn_list"][0]["enc_url"]
                        r_url = js_code.call("decodeUrl", d_url)
                        f_path = path + "/" + course["name"] + ".mp4"
                        # wget.download(r_url, path)  # 下载
                        r = http.request('GET', r_url)
                        with open(f_path, 'wb') as f:
                            f.write(r.data)

                    if '720p' in mp4:
                        d_url = mp4["720p"]["cdn_list"][0]["enc_url"]
                        r_url = js_code.call("decodeUrl", d_url)
                        f_path = path + "/" + course["name"] + ".mp4"
                        # wget.download(r_url, path)  # 下载
                        r = http.request('GET', r_url)
                        with open(f_path, 'wb') as f:
                            f.write(r.data)

                else:
                    path = courses["name"].strip() + "/" + course["name"].strip()
                    if not os.path.isdir(path):
                        os.mkdir(path)
                        # print(courses["name"].strip()+"/"+course["name"].strip())
                    for c in course["list"]:
                        token = videoPlayerToken(courseId=c["courseId"], video_id=c["url"])
                        if token == None:
                            continue
                        content = c["name"] + " " + c["courseId"] + " " + c["url"] + " " + token
                        print(content)
                        # worksheet.write(i, 0, label=c["name"])
                        json_url = getAllFormatPlayUrl(c["url"], token)
                        j = 1
                        mp4 = json_url["data"]["all_format_play_info"]["mp4"]
                        print(mp4)
                        if 'superHD' in mp4:
                            d_url = mp4["superHD"]["cdn_list"][0]["enc_url"]
                            r_url = js_code.call("decodeUrl", d_url)
                            f_path = path + "/" + c["name"] + ".mp4"
                            # wget.download(r_url, path)  # 下载
                            r = http.request('GET', r_url)
                            with open(f_path, 'wb') as f:
                                f.write(r.data)

                        if 'high' in mp4:
                            d_url = mp4["high"]["cdn_list"][0]["enc_url"]
                            r_url = js_code.call("decodeUrl", d_url)
                            f_path = path + "/" + c["name"] + ".mp4"
                            # wget.download(r_url, path)  # 下载
                            r = http.request('GET', r_url)
                            with open(f_path, 'wb') as f:
                                f.write(r.data)

                        if '720p' in mp4:
                            d_url = mp4["720p"]["cdn_list"][0]["enc_url"]
                            r_url = js_code.call("decodeUrl", d_url)
                            f_path = path + "/" + course["name"] + ".mp4"
                            # wget.download(r_url, path)  # 下载
                            r = http.request('GET', r_url)
                            with open(f_path, 'wb') as f:
                                f.write(r.data)

    finally:
        r.release_conn()
        
if __name__ == '__main__':
    Download()
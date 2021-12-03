# -*- coding: utf-8 -*-
import binascii
import re
import requests
import time
import random
import hashlib
from Cryptodome.Cipher import AES

AESKEY = '8jhM5h6dezq4QifP'  # 请修改 一定是 16位的字符串
AESIV = 'tho3aAHJyZCWAfTG'  # 和KEY保持一致即可

class AESTool:
    def __init__(self):
        self.key = AESKEY.encode('utf-8')
        self.iv = AESIV.encode('utf-8')

    def pkcs7padding(self, text):
        """
        明文使用PKCS7填充
        """
        bs = 16
        length = len(text)
        bytes_length = len(text.encode('utf-8'))
        padding_size = length if (bytes_length == length) else bytes_length
        padding = bs - padding_size % bs
        padding_text = chr(padding) * padding
        self.coding = chr(padding)
        return text + padding_text

    def aes_encrypt(self, content):
        """
        AES加密
        """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        # 处理明文
        content_padding = self.pkcs7padding(content)
        # 加密
        encrypt_bytes = cipher.encrypt(content_padding.encode('utf-8'))
        # 重新编码
        result = binascii.b2a_hex(encrypt_bytes).upper()
        return result

    def aes_decrypt(self, content):
        """
        AES解密
        """
        generator = AES.new(self.key, AES.MODE_CBC, self.iv)
        content += (len(content) % 4) * '='
        # decrpyt_bytes = base64.b64decode(text)           #输出Base64
        decrpyt_bytes = binascii.a2b_hex(content)  # 输出Hex
        meg = generator.decrypt(decrpyt_bytes)
        # 去除解码后的非法字符
        try:
            result = re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f\n\r\t]').sub('', meg.decode())
        except Exception:
            result = '解码失败，请重试!'
        return result

def invite():
    #随机手机型号
    model_name = ["oppo-pedm00","oppo-peem00","oppo-peam00","oppo-x907","oppo-x909t",
                      "vivo-v2048a","vivo-v2072a","vivo-v2080a","vivo-v2031ea","vivo-v2055a",
                      "huawei-tet-an00","huawei-ana-al00","huawei-ang-an00","huawei-brq-an00","huawei-jsc-an00",
                      "xiaomi-mi 10s","xiaomi-redmi k40 pro+","xiaomi-mi 11","xiaomi-mi 6","xiaomi-redmi note 7",
                      "meizu-meizu 18","meizu-meizu 18 pro","meizu-mx2","meizu-m355","meizu-16th plus",
                      "samsung-sm-g9910","samsung-sm-g9960","samsung-sm-w2021","samsung-sm-f7070","samsung-sm-c7000",
                      "oneplus-le2120","oneplus-le2110","oneplus-kb2000","oneplus-hd1910","oneplus-oneplus a3010",
                      "sony-xq-as72","sony-f8132","sony-f5321","sony-i4293","sony-g8231",
                      "google-pixel","google-pixel xl","google-pixel 2","google-pixel 2 xl","google-pixel 3"]
    random_model_name = random.choice(model_name)

    #调用aes加密
    aes = AESTool()

    #注册账户
    t = str(int(round(time.time() * 1000)))
    #随机设备id
    device_id = "".join(random.choice("0123456789ABCDEF") for i in range(32))
    ns = 'com.jfm2110152DAA94115DC5C48038693654FFCC3AA095CBD093165B47BD7F15C8F83CA1BC9B&z4Y!s!2br' + t
    MD5ns = hashlib.md5(ns.encode(encoding='UTF-8')).hexdigest()
    Request_key = '{"new_key":"' + device_id + '","phone_type":"1","ns":"' + MD5ns + '","nt":"' + t + '","old_key":"YYqIkUniVrkDAACxRfIkIvsY","recommend":""}'
    MD5Request_key = aes.aes_encrypt(Request_key)
    HexMD5Request_key = MD5Request_key.decode('unicode_escape')
    body = 'token=no&token_id=no&phone_type=1&versions_code=1402&phone_model='+ random_model_name +'&request_key=' + HexMD5Request_key + '&app_id=1&ad_version=1'
    header = {
        'Cache-Control': 'no-cache',
        'Version': '210930',
        'channel_code': 'xc_tg18',
        'Referer': 'http://jk.b557b8.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'jk.b557b8.com',
        'User-Agent': 'okhttp/3.12.0'
    }
    urls = 'http://jk.256537.com/App/User/newLogin'
    Response_body = requests.post(url=urls, data=body, headers=header).text
    Response_body_Encrypt = Response_body[49:241]
    Response_body_Decrypt = aes.aes_decrypt(Response_body_Encrypt)
    token_id = Response_body_Decrypt[13:22]
    token = Response_body_Decrypt[33:65]

    #邀请
    Request_key2 = '{"code":"2UDYUB","ns":"' + MD5ns + '","nt":"' + t + '"}'  #code后填入你的邀请码
    Request_key_Encrypt2 = aes.aes_encrypt(Request_key2)
    HexRequest_key_Encrypt2 = Request_key_Encrypt2.decode('unicode_escape')
    body2 = 'token=' + token + '&token_id=' + token_id + '&phone_type=1&versions_code=1402&phone_model=' + random_model_name + '&request_key=' + HexRequest_key_Encrypt2 + '&app_id=1&ad_version=1'
    urls2 = 'http://jk.b557b8.com/App/AppUserInvitation/beOne'
    Response_body = requests.post(url=urls2, data=body2, headers=header) # 返回200即邀请成功
    print(Response_body.text)

if __name__ == '__main__':
    j = 0
    for i in range(50):  # 五十次即可永久去广告
        time.sleep(random.randint(1, 15))  # 设置随机延时
        invite()
        print("已刷{}次".format(i))
        j += 1
        if j == 50:
            break
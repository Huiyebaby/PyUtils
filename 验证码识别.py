#pip install ddddocr


import ddddocr
 
ocr = ddddocr.DdddOcr()
 
with open('test.png', 'rb') as f:
 
    img_bytes = f.read()
 
res = ocr.classification(img_bytes)
 
print(res)


  爬取数据的过程中难免遇到登录的问题,为了绕过登录,保存cookie是常见的的解决方法.
在遇到有验证码的问题时,无疑增加了获取cookie的难度.该python包,解决你的实际问题,避免了购买云打码或者自己搭建机器学习,训练模型的过程,话不多说,直接进入主题.

环境要求 :
目前已经支持python3.8以下的了，python3.8以上毫无问题。
调用方法:
pip install ddddocr

列子:
[Python] 纯文本查看 复制代码
?
01
02
03
04
05
06
07
08
09
10
11
import ddddocr
 
ocr = ddddocr.DdddOcr()
 
with open('test.png', 'rb') as f:
 
    img_bytes = f.read()
 
res = ocr.classification(img_bytes)
 
print(res)

########参数说明:
########DdddOcr 接受两个参数
########            
########
########参数名	
########默认值	
########说明
########
########use_gpu	
########False	
########Bool 是否使用gpu进行推理，如果该值为False则device_id不生效
########
########device_id	
########0	
########int cuda设备号，目前仅支持单张显卡
########        
########classification
########            
########
########参数名	
########默认值	
########说明
########
########img	
########0	
########bytes 图片的bytes格式
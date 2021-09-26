# # -*- coding: utf8 -*-
import json,requests
import requests
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

IDs=[111111,222222]#这里是需要监听的游戏APPID
url='https://store.steampowered.com/api/appdetails/?appids='

def main_handler(event, context):#这个是默认入口
    text_info=""
    isbuy=False
    for ID in IDs:
        ID=str(ID)
        res=requests.get(url+ID).json()
        if res[ID]["success"] is True:
            price=res[ID]["data"]["price_overview"]["final"]/100
            rawprice=res[ID]["data"]["price_overview"]["initial"]/100
            if rawprice>price:
                buy="正"
                isbuy=True#有一个降价了就通知
            else:
                buy="未"
            print("["+res[ID]["data"]["name"]+"@"+ID+"]当前价格：%s，历史价格：%s；【%s】在促销"%(price,rawprice,buy))
            text_info+="["+res[ID]["data"]["name"]+"@"+ID+"]当前价格：%s，历史价格：%s；【%s】在促销"%(price,rawprice,buy)+"\n\n"
        else:
            print("["+res[ID]["data"]["name"]+"@"+ID+"]读取失败！")
    if isbuy is True:
        sender_mail = '发送邮箱@qq.com' #这里填发件人邮箱，我选的QQ邮箱
        sender_pass = 'rgmxxxxxxceg' #这里填QQ邮箱SMTP授权码
        to='接收邮箱（可以还填自己的QQ邮箱）@52pojie.cn'
        msg_root = MIMEMultipart('mixed')# 设置总的邮件体对象，对象类型为mixed
        msg_root['From'] = '云函数steam价格监听'#发送人描述
        msg_root['To'] = to
        subject = 'steam监听价格变动！'  #邮件标题
        msg_root['subject'] = Header(subject, 'utf-8')

        text_sub = MIMEText(text_info, 'plain', 'utf-8')
        msg_root.attach(text_sub)

        try:
            sftp_obj =smtplib.SMTP('smtp.qq.com', 25)
            sftp_obj.login(sender_mail, sender_pass)
            sftp_obj.sendmail(sender_mail, to, msg_root.as_string())
            sftp_obj.quit()
            print('邮件推送成功!')

        except Exception as e:
            print('邮件推送失败！错误代码:')
            print(e)
    return text_info
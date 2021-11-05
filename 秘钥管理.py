import tkinter
from tkinter import *
from tkinter.ttk import Combobox
from tkinter.tix import Tk, Control, ComboBox
from tkinter.messagebox import showinfo, showwarning, showerror
import base64
import os
import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKC
from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5 as Signature_PKC
from tkinter import ttk
import webbrowser
 
file='dict_pwd.txt'
if not os.path.exists(file):
    fo = open(file, 'w')
    fo.close()
#注意就是下面的 if 语句
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
#pyinstaller -F -w 21313.py
class HandleRSA():
    def creatRSA_key(self):
        # 伪随机数生成器
        random_gen = Random.new().read
        # 生成秘钥对实例对象：2048是秘钥的长度
        rsa = RSA.generate(2048, random_gen)
        # Client的秘钥对的生成
        private_pem = rsa.exportKey()
        with open("client_private.pem", "wb") as f:
            f.write(private_pem)
        public_pem = rsa.publickey().exportKey()
        with open("client_public.pem", "wb") as f:
            f.write(public_pem)
 
    # Server使用Client的公钥对内容进行rsa 加密
    def encrypt(self, plaintext):
        """
        client 公钥进行加密
        plaintext:需要加密的明文文本，公钥加密，私钥解密
        """
        # 加载公钥
        rsa_key = RSA.import_key(open("client_public.pem").read())
        # 加密
        cipher_rsa = Cipher_PKC.new(rsa_key)
        en_data = cipher_rsa.encrypt(plaintext.encode("utf-8"))  # 加密
        # base64 进行编码
        base64_text = base64.b64encode(en_data)
        return base64_text.decode()  # 返回字符串
 
 
    # Client使用自己的私钥对内容进行rsa 解密
    def decrypt(self, en_data):
        """
        en_data:加密过后的数据，传进来是一个字符串
        """
        # base64 解码
        #try:
        base64_data = base64.b64decode(en_data.encode("utf-8"))
        # 读取私钥
        private_key = RSA.import_key(open("client_private.pem").read())
        # 解密
        cipher_rsa = Cipher_PKC.new(private_key)
        data = cipher_rsa.decrypt(base64_data, None)
        return data.decode()
        #except:
            #print('解密失败，秘钥对不匹配')
            #sys.exit('程序退出!')
a=HandleRSA()
 
root = Tk() # 初始化Tk()
root.title("个人密码管理器")    # 设置窗口标题
root.geometry("350x500+400+300")    # 设置窗口大小 注意：是x 不是*
root.resizable(False,False) # 设置窗口是否可以变化长/宽，False不可变，True可变，默认为True
root.tk.eval('package require Tix')  #引入升级包，这样才能使用升级的组合控件
 
secret_key='52pojie'
 
def click(event):
    webbrowser.open("https://www.52pojie.cn/")
 
#窗口界面
entry_lable1 = Label(root, text="输入秘钥")
entry_lable1.place(x=10,y=10,width=100,height=20)
key1=tkinter.StringVar(root,'')
entry_key1=tkinter.Entry(root,textvariable=key1,show='*')
entry_key1.place(x=120,y=10,width=200,height=20)
#增加密码
entry_lable2=Label(root, text="网站名称")
entry_lable2.place(x=10,y=40,width=100,height=20)
add_plat=tkinter.StringVar(root,'')
entry_plat=tkinter.Entry(root,textvariable=add_plat)
entry_plat.place(x=120,y=40,width=200,height=20)
#网站url
entry_label4=Label(root,text='网站链接')
entry_label4.place(x=10,y=70,width=100,height=20)
add_url=tkinter.StringVar(root,'')
entry_url=tkinter.Entry(root,textvariable=add_url)
entry_url.place(x=120,y=70,width=200,height=20)
#账号
entry_label5=Label(root,text='账号')
entry_label5.place(x=10,y=100,width=100,height=20)
add_account=tkinter.StringVar(root,'')
entry_account=Entry(root,textvariable=add_account)
entry_account.place(x=120,y=100,width=200,height=20)
#密码
entry_label3=Label(root,text="密码")
entry_label3.place(x=10,y=130,width=100,height=20)
add_pwd=tkinter.StringVar(root,'')
entry_pwd=tkinter.Entry(root,textvariable=add_pwd,show='*')
entry_pwd.place(x=120,y=130,width=200,height=20)
#请选择修改密码平台
entry_label6=Label(root,text='请选择平台')
entry_label6.place(x=10,y=190,width=100,height=20)
#取出平台名称名字
lst1 = []
with open(file, 'r', encoding='utf-8') as rf:
    b = rf.readlines()
    for i in b:
        c = a.decrypt(i)
        d = eval(c)
        e = d.get("网站名称")
        lst1.append(e)
value0=StringVar()
complatbox0=ttk.Combobox(root,textvariable=value0)
value0.set('请选择你要修改的网站')
complatbox0.place(x=120,y=190,width=200,height=20)
complatbox0['values']=lst1
#请选择平台
chose_plat=Label(root,text='请选择平台')
chose_plat.place(x=10,y=310,width=100,height=20)
value=StringVar()
complatBox=ttk.Combobox(root,textvariable=value)
value.set('请选择你要查询的网站')
complatBox.place(x=120,y=310,width=200,height=20)
complatBox['values']= lst1
#查询账号
account_label=Label(root,text='账号结果')
account_label.place(x=10,y=370,width=100,height=20)
account=tkinter.StringVar(root,'')
entry_account1=Entry(root,textvariable=account)
#entry_account1['state']='disabled'
entry_account1.place(x=120,y=370,width=200,height=20)
#查询url
url_label=Label(root,text='网站链接')
url_label.place(x=10,y=340,width=100,height=20)
url=tkinter.StringVar(root,'')
entry_url1=Entry(root,textvariable=url)
#entry_url1['state']='disabled'
entry_url1.place(x=120,y=340,width=200,height=20)
#查询密码
search_label3=Label(root,text='密码结果')
search_label3.place(x=10,y=400,width=100,height=20)
pwd=tkinter.StringVar(root,'')
entryPwd=Entry(root,textvariable=pwd)
#entryPwd['state']='disabled'
entryPwd.place(x=120,y=400,width=200,height=20)
#作者署名
text = Text(root)
text.place(x=145,y=460,width=60,height=20)
text.insert(INSERT, "作者博客")
text.tag_add("link","1.0","1.4")
text.tag_config("link", foreground="blue", underline = True)
text.tag_bind("link","<Button-1>",click)
#text['state']='disabled'
 
 
#添加密码
def button():
    if key1.get()!=secret_key:
        showwarning(title='警告',message='请输入正确的秘钥')
        sys.exit()
    if not (key1.get() and add_plat.get() and add_url and add_account and add_pwd.get()):
        showerror('出错，请同时输入秘钥、平台名称和密码')
    else:
        pwd_dict={"网站名称":f"{add_plat.get()}"
                  ,"网站链接":f"{add_url.get()}"
                  ,"账号":f"{add_account.get()}"
             ,"密码":f"{add_pwd.get()}"
              }
        b=a.encrypt(str(pwd_dict))
        with open(file,'a',encoding='utf-8') as f:
           f.write(b+'\n')
    button6()
#修改密码
def button1():
    if key1.get()!=secret_key:
        showwarning(title='警告',message='请输入正确的秘钥')
        sys.exit()
    pwd_dict = {"网站名称": f"{add_plat.get()}"
        , "网站链接": f"{add_url.get()}"
        , "账号": f"{add_account.get()}"
        , "密码": f"{add_pwd.get()}"
                }
    with open(file, 'r') as f:
        b = f.readlines()
    os.remove(file)
    f = open(file, 'w')
    f.close
    for i in b:  # i未解密
        c = a.decrypt(i)  # c已解密 字符串类型
        d=eval(c) #d转换为字典类型
        e=d["网站名称"]
        if value0.get() == e:
            with open(file, 'a') as wf:
                wf.write(a.encrypt(str(pwd_dict))+'\n')
        elif value0.get() != e:
            with open(file, 'a') as qf:
                qf.write(i)
    button6()
#删除密码
def button4():
    if key1.get()!=secret_key:
        showwarning(title='警告',message='请输入正确的秘钥')
        sys.exit()
    with open(file, 'r') as f:
        b = f.readlines()
    os.remove(file)
    f = open(file, 'w')
    f.close
    for i in b:  # i未解密
        c = a.decrypt(i)  # c已解密 字符串类型
        d = eval(c)  # d转换为字典类型
        e = d["网站名称"]
        if value0.get() != e:
            with open(file, 'a') as qf:
                qf.write(i)
        elif value0.get() == e:
            pass
    button6()
 
#创建秘钥
def button2():
    if key1.get()!=secret_key:
        showwarning(title='警告',message='请输入正确的秘钥')
        sys.exit()
    if os.path.exists('client_private.pem'):
        showinfo('提示','秘钥已存在！')
    else:
        a.creatRSA_key()
        showinfo('提示','秘钥创建成功!')
#查询密码
def button3():
    if key1.get()!=secret_key:
        showwarning(title='警告',message='请输入正确的秘钥')
        sys.exit()
    if value.get() == '请选择你要查询的网站':
        showwarning(title='警告', message='请选择你要查询的网站')
    with open(file, 'r', encoding='utf-8') as rf:
        b = rf.readlines()
        for i in b:
            c = a.decrypt(i)
            d = eval(c)
            if value.get() == d["网站名称"]:
                e = d["密码"]
                f = d["网站链接"]
                g = d["账号"]
                pwd.set(e)
                url.set(f)
                account.set(g)
            elif value.get()!=d["网站名称"]:
                pass
    button6()
 
 
#拉取lst
def button6():
    if key1.get()!=secret_key:
        showwarning(title='警告',message='请输入正确的秘钥')
        sys.exit()
    with open(file, 'r', encoding='utf-8') as rf:
        b = rf.readlines()
        lst1 = []
        for i in b:
            c = a.decrypt(i)
            d = eval(c)
            e = d.get("网站名称")
            lst1.append(e)
    complatBox['values'] = lst1
    complatbox0['values'] = lst1
 
 
#按钮处理
buttonADDpwd=tkinter.Button(root,text='增加密码',bg='white',fg='red',command=button)
buttonADDpwd.place(x=20,y=160,width=300,height=20)
 
buttonCHANGEpwd=tkinter.Button(root,text='修改密码',bg='white',fg='red',command=button1)
buttonCHANGEpwd.place(x=20,y=220,width=300,height=20)
 
buttonDELEpwd=tkinter.Button(root,text='删除密码',bg='white',fg='red',command=button4)
buttonDELEpwd.place(x=20,y=250,width=300,height=20)
 
buttonCreatRsa=tkinter.Button(root,text='创建秘钥',bg='white',fg='red',command=button2)
buttonCreatRsa.place(x=20,y=280,width=300,height=20)
 
buttonSEARCHpwd=tkinter.Button(root,text='查询密码',bg='white',fg='red',command=button3)
buttonSEARCHpwd.place(x=20,y=430,width=300,height=20)
 
 
 
 
 
root.mainloop()
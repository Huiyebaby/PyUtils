# subprocess 模块允许我们启动一个新进程，并连接到它们的输入/输出/错误管道，从而获取返回值
import subprocess
import re
 
# 用于判断OS的语言
import locale
loc_lang = locale.getdefaultlocale()
# print(loc_lang[0])
 
# 代码中用到的正则匹配模式字符串，提取出来以便不同语言系统使用，默认支持中文英文，其他语言需要更改匹配语句
if loc_lang[0] == "zh_CN":
    re_pattern = ["所有用户配置文件 : (.*)\r", "安全密钥               : 不存在", "关键内容            : (.*)\r"]
else:
    re_pattern = ["All User Profile     : (.*)\r", "Security key           : Absent", "Key Content            : (.*)\r"]
 
# 如果 capture_output 设为 true，stdout 和 stderr 将会被捕获
cmd_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode('gbk')
# print(cmd_output)
wifi_names = (re.findall(re_pattern[0], cmd_output))
# print(wifi_names)
wifi_list = []
if len(wifi_names) != 0:
    for name in wifi_names:
        # 每一个wifi的信息存储在一个字典里
        wifi_profile = {}
        profile_info = subprocess.run(["netsh", "wlan", "show", "profiles", name],
                                      capture_output=True).stdout.decode('gbk')
        # print(profile_info)
        # 判断wifi密码是否存储在windows计算机里，不存在则忽略
        if re.search(re_pattern[1], profile_info):
            continue
        else:
            wifi_profile["ssid"] = name
            # 密码存在时，加上命令参数“key=clear”显示wifi密码
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profiles", name, "key=clear"], 
                                    capture_output=True).stdout.decode('gbk')
            password = re.search(re_pattern[2], profile_info_pass)
            # print(password)
            if not password:
                wifi_profile["password"] = None
            else:
                wifi_profile["password"] = password[1]
        wifi_list.append(wifi_profile)
 
for i in range(len(wifi_list)):
    print(wifi_list[i])
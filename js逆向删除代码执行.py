import mitmproxy.http
import re

print('脚本初始化成功')

def request(flow: mitmproxy.http.HTTPFlow):
    pass

def response(flow: mitmproxy.http.HTTPFlow):
    if 'https://www.aqistudy.cn/' == flow.request.url:
        html = flow.response.text
        html = html.replace('txsdefwsw();', '// txsdefwsw();')
        html = html.replace("document.write('检测到非法调试, 请关闭调试终端后刷新本页面重试!');",
                            "return; document.write('检测到非法调试, 请关闭调试终端后刷新本页面重试!');")
        flow.response.text = html
    elif 'html/city_realtime.php' in flow.request.url:
        html = flow.response.text
        js = re.findall('eval\(.+', html)[0]
        html = html.replace(js, '// ' + js)
        flow.response.text = html
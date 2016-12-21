#-*- encoding: utf-8 -*-


import requests

#http://www.python-requests.org/en/latest/
def get(url, params = None, headers = None, cookies = None, timeout = 20, allow_redirects = True):
    '''
        使用requests扩展调用http-get
        url:访问url
        params:get参数
        headers:http头
        cookie:传入cookie
        timeout:超时时间，秒
        allow_redirects:是否支持跳转，默认为True支持
    '''
    r = requests.get(url = url, params = params, headers=headers, cookies=cookies)
    return r

def post(url, params = None, data = None, headers = None, filePath = None, cookies = None, allow_redirects = True):
    files = None
    if filePath != None:
        files = {'file': open(filePath, 'rb')}
    r = requests.post(url = url, params = params, data = data, files = files, headers=headers, cookies=cookies)
    return r


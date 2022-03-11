# 使用代理
# demo 4 ：使用从 http://www.goubanjia.com/，www.kuaidaili.com/dps 获取的代理列表
# 可以使用快代理在线测试代理可行性

import json
import random
import urllib
import urllib.request

import re
import requests
from bs4 import BeautifulSoup

from Proxy_pool.db import MySqlClient
from Proxy_pool.utils import dict2obj


def try_random_Proxy(proxy_list, retry):
    """
        Function : choose a proxy from the proxy list RANDOMLY!
        retry : number of retry
    """
    # 策略 1 随机选
    try:
        proxy = random.choice(proxy_list)

        proxy_obj = {'http': str(proxy)}
        print('Try %s ' % json.dumps(proxy_obj))

        httpProxyHandler = urllib.request.ProxyHandler(proxy_obj)
        opener = urllib.request.build_opener(httpProxyHandler)
        request = urllib.request.Request('http://www.baidu.com')
        response = opener.open(request, timeout=5)

        print('Worked !')
        return proxy_obj
    except Exception as e:
        print('Connect error:Please retry, error: %s' % e)
        if retry > 0:
            try_random_Proxy(retry - 1)


def try_ordered_Proxy(proxy):
    """
        Function : choose a proxy from the proxy list RANDOMLY!
        retry : index of proxy
    """
    # 策略 2 ：依次尝试选择
    try:
        proxy_obj = {'http': str(proxy)}
        print('Try %s ' % json.dumps(proxy_obj))

        httpProxyHandler = urllib.request.ProxyHandler(proxy_obj)
        opener = urllib.request.build_opener(httpProxyHandler)
        request = urllib.request.Request('http://www.baidu.com')
        response = opener.open(request, timeout=5)

        print('Worked !')
        return proxy_obj
    except Exception as e:
        print('[ORDERED select] Connect error : %s' % e)


def proxy_select():
    conn = MySqlClient()
    count = conn.count()
    print("count:" + str(count))
    proxy_list = conn.get_pass_proxy_list()
    if len(proxy_list) > 0:
        # 随机筛选适合代理列表中大部分能用的情况
        choice_ip = try_random_Proxy(proxy_list, 5)
        if choice_ip:
            return choice_ip
        print('--' * 20)
        # 依次尝试适合代理列表中大部分不可用的情况
        for p in proxy_list:
            choice_ip = try_ordered_Proxy(p)
            if choice_ip:
                return choice_ip
    else:
        print('=====[current moment has not available IP proxy]=====')
        return None


# python 3.8(urllib, urllib.requests)

my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"
]


def getHtml(url):
    random_head = random.choice(my_headers)
    kv = {
        'User-Agent': random_head
    }
    html = None
    try:
        proxy_ip = proxy_select()
        if proxy_ip:
            print('choice_ip: %s' % proxy_ip)
            httpProxyHandler = urllib.request.ProxyHandler(proxy_ip)
            opener = urllib.request.build_opener(httpProxyHandler)
            request = urllib.request.Request(url)
            response = opener.open(request, timeout=5)
            html_dict = {'text': response.read().decode("utf-8"), 'status_code': 200}
            html = dict2obj(html_dict)
    except Exception as e:
        html = None
        print("http proxy fail!, %s" % e)
    if not html:
        html = requests.Session().get(url=url, headers=kv, verify=False)
    return html


def parse_page(url):
    html = getHtml(url)
    soup = BeautifulSoup(html.text, 'html.parser')


# python 2.7(urllib2,requests)
#
# my_headers = [
#     "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"
# ]
#
#
# def getHtml(url):
#     random_head = random.choice(my_headers)
#     kv = {
#         'User-Agent': random_head
#     }
#     html = None
#     try:
#         proxy_ip = proxy_select()
#         if proxy_ip:
#             httpProxyHandler = urllib2.ProxyHandler(proxy_ip)
#             opener = urllib2.build_opener(httpProxyHandler)
#             response = opener.open(url, timeout=5)
#             html_dict = {'text': response.read().decode("utf-8"), 'status_code': 200}
#             html = dict2obj(html_dict)
#     except Exception as e:
#         html = None
#         print("http proxy fail!")
#     if not html:
#         html = requests.Session().get(url=url, headers=kv, verify=False)
#     return html


if __name__ == '__main__':
    parse_page("http://www.baidu.com")


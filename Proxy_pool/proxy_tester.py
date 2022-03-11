# 使用代理
# demo 4 ：使用从 http://www.goubanjia.com/，www.kuaidaili.com/dps 获取的代理列表
# 可以使用快代理在线测试代理可行性

import json
import random
import urllib
import urllib.request
from Proxy_pool.db import MySqlClient


def randomTryProxy(proxy_list, retry):
    '''
        Function : choose a proxy from the proxy list RANDOMLY!
        retry : number of retry
    '''
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
            randomTryProxy(retry - 1)


def inorderTryProxy(proxy):
    '''
        Function : choose a proxy from the proxy list RANDOMLY!
        retry : index of proxy
    '''
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
    except:
        print('Connect error:Please retry')


def proxy_select():
    proxy_list = []
    conn = MySqlClient()
    count = conn.count()
    print("count:" + str(count))
    proxy_list = conn.batch_pass_score()
    if len(proxy_list) > 0:
        # 随机筛选适合代理列表中大部分能用的情况
        choice_ip = randomTryProxy(proxy_list, 5)
        if choice_ip:
            return choice_ip
        print('--' * 20)
        # 依次尝试适合代理列表中大部分不可用的情况
        for p in proxy_list:
            choice_ip = inorderTryProxy(p)
            if choice_ip:
                return choice_ip
    else:
        print('=====[current moment has not available IP proxy]=====')
        return None


if __name__ == '__main__':
    selected_ip = proxy_select()
    print('choice_ip: %s' % selected_ip)



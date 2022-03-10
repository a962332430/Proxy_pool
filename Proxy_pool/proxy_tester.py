# 使用代理
# demo 4 ：使用从 http://www.goubanjia.com/，www.kuaidaili.com/dps 获取的代理列表
# 可以使用快代理在线测试代理可行性

import random
import urllib

# 10月18日 从快代理网站上找的免费代理。
proxylist = [
    {'http': '118.174.119.203:8080'},
    # {'http': '120.220.220.95:8085'},
    # {'http': '177.55.245.198:8080'},
    # {'http': '14.192.129.140:8080'},
    # {'http': '101.34.214.152:8001'},
    # {'http': '120.220.220.95:8085'},
    # {'http': '115.211.45.128:9000'},
]


def randomTryProxy(retry):
    '''
        Function : choose a proxy from the proxy list RANDOMLY!
        retry : number of retry
    '''
    # 策略 1 随机选
    try:
        proxy = random.choice(proxylist)

        print('Try %s : %s' % (retry, proxy))

        httpProxyHandler = urllib.request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(httpProxyHandler)
        request = urllib.request.Request('http://www.baidu.com')
        response = opener.open(request, timeout=5)

        print('Worked !')

    except:
        print('Connect error:Please retry')
        if retry > 0:
            randomTryProxy(retry - 1)


def inorderTryProxy(proxy):
    '''
        Function : choose a proxy from the proxy list RANDOMLY!
        retry : index of proxy
    '''
    # 策略 2 ：依次尝试选择
    try:

        print('Try %s ' % (proxy))

        httpProxyHandler = urllib.request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(httpProxyHandler)
        request = urllib.request.Request('http://www.baidu.com')
        response = opener.open(request, timeout=5)

        print('Worked !')

    except:
        print('Connect error:Please retry')


if __name__ == '__main__':
    # 随机筛选适合代理列表中大部分能用的情况
    randomTryProxy(5)
    print('--' * 20)
    # 依次尝试适合代理列表中大部分不可用的情况
    for p in proxylist:
        inorderTryProxy(p)


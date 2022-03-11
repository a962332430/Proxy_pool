import time
from multiprocessing import Process
from Proxy_pool.api import app
from Proxy_pool.getter import Getter
from Proxy_pool.tester import Tester
from Proxy_pool.db import MySqlClient
from Proxy_pool.setting import *
from Proxy_pool.utils import get_current_time


class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        """
        tester = Tester()
        while True:
            print('[%s] 开始测试代理：' % get_current_time())
            tester.run()
            time.sleep(cycle)
    
    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        """
        getter = Getter()
        while True:
            print('[%s] 开始抓取代理：' % get_current_time())
            getter.run()
            time.sleep(cycle)
    
    def schedule_api(self):
        """
        开启API
        """
        app.run(API_HOST, API_PORT)
    
    def run(self):
        print('代理池开始运行')

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()
        
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
        
        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()

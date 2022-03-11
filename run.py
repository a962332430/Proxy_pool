from Proxy_pool.scheduler import Scheduler
import sys
import io
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    try:
        s = Scheduler()
        s.run()
    except Exception as e:
        print('main exec error, %s' % e)
        main()


if __name__ == '__main__':
    main()

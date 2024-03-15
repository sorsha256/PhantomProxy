from threading import Thread
import random
import time
import asyncio
from phantomproxy.check_proxies import Proxy


def check_proxy(p):
    proxy = Proxy()
    proxy.base_name = './base/proxy.db'
    while True:
        asyncio.run(proxy.test_tcp(p))
        time.sleep(random.uniform(1.5, 5.5))


def main():
    num_threads = 30
    threads = []

    for p in range(num_threads):
        thread = Thread(target=check_proxy, args=(p,))
        threads.append(thread)
        time.sleep(random.uniform(0.1, 0.6))
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()

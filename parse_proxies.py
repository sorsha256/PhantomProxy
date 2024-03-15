import time
from tqdm import tqdm
from phantomproxy.parse_proxies import Proxy


if __name__ == "__main__":
    parse_proxy = Proxy()
    while True:
        parse_proxy.add_proxy()
        for i in tqdm(range(600), desc="Delay between scrape", ncols=100):
            time.sleep(1)

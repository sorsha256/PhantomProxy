import phantomproxy.SQLite
import requests
import base64
from tqdm import tqdm


class Proxy(phantomproxy.SQLite.SQLite):

    def add_proxy(self):
        self.base_name = './base/proxy.db'
        ss_aggregator = requests.get(
            'https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/splitted/ss.txt')
        print("Write ss_aggregator.txt ...")
        with open('./proxies/ss_aggregator.txt', 'w', encoding='utf-8') as file:
            file.write(ss_aggregator.text)
        shadow_aggregator = requests.get(
            'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Splitted-By-Protocol/ss.txt')
        shadow_aggregator = shadow_aggregator.text
        shadow_aggregator = base64.b64decode(shadow_aggregator).decode('utf-8')
        print("Write shadow_aggregator.txt ...")

        ss_aggregator = requests.get('https://raw.githubusercontent.com/mheidari98/.proxy/main/ss')
        print("Write mheidari98.txt ...")
        ss_aggregator = ss_aggregator.text
        ss_aggregator = base64.b64decode(ss_aggregator).decode('utf-8')
        with open('./proxies/mheidari98.txt', 'w', encoding='utf-8') as file:
            file.write(ss_aggregator)

        ss_aggregator = requests.get('https://raw.githubusercontent.com/Huibq/TrojanLinks/master/links/ss')
        print("Write Huibq.txt ...")
        ss_aggregator = ss_aggregator.text
        ss_aggregator = base64.b64decode(ss_aggregator).decode('utf-8')
        with open('./proxies/Huibq.txt', 'w', encoding='utf-8') as file:
            file.write(ss_aggregator)

        ss_aggregator = requests.get(
            'https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/ss.txt')
        print("Write Epodonios.txt ...")
        ss_aggregator = ss_aggregator.text
        ss_aggregator = base64.b64decode(ss_aggregator).decode('utf-8')
        with open('./proxies/Epodonios.txt', 'w', encoding='utf-8') as file:
            file.write(ss_aggregator)

        with open('./proxies/shadow_aggregator.txt', 'w', encoding='utf-8') as file:
            file.write(shadow_aggregator)
        with open('./proxies/shadow_aggregator.txt', 'r', encoding='utf-8') as file:
            ss = file.readlines()
        with open('./proxies/ss_aggregator.txt', 'r', encoding='utf-8') as file:
            ss += file.readlines()
        with open('./proxies/mheidari98.txt', 'r', encoding='utf-8') as file:
            ss += file.readlines()
        with open('./proxies/Huibq.txt', 'r', encoding='utf-8') as file:
            ss += file.readlines()
        with open('./proxies/Epodonios.txt', 'r', encoding='utf-8') as file:
            ss += file.readlines()
        _list_shadowsocks = []
        for shadowsocks in tqdm(ss, desc="Save ss in table", ncols=100):
            try:
                shadowsocks = shadowsocks.strip().split('#')[0]
                data, ip_port = shadowsocks.split('@')
                ip, port = ip_port.split(':')
                query = {'table': 'proxy_', 'ip': ip}
                if not self.select(**query):
                    query = {'table': 'proxy_', 'data': data, 'ip': ip, 'port': port, 'type': 'ss', 'status': 0}
                    self.insert(**query)
            except Exception:
                pass
        query = {'table': 'proxy_', 'selector': {'status': str(1)}, 'status': 0}
        self.update(**query)
        query = {'table': 'proxy_', 'selector': {'status': str(2)}, 'status': 0}
        self.update(**query)
        return _list_shadowsocks

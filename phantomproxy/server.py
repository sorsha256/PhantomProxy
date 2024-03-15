import phantomproxy.SQLite
import time
import asyncio
import pproxy
from threading import Thread
import socket


class RunProxy(phantomproxy.SQLite.SQLite):
    base_name = './base/proxy.db'
    dict_process = {}
    dict_error = {}

    @property
    def get_all_proxies(self):
        query = {'table': 'proxy_', 'alive': 1}
        return self.select(**query)

    def alive_status(self, proxy):
        query = {'table': 'proxy_', 'ip': proxy}
        # print(self.select(**query))
        return int(self.select(**query)[0][4])

    @property
    def proxies(self):
        query = {'table': 'run', 'status': 1}
        return self.select(**query)

    def assign_port(self, proxy):
        query = {'table': 'run', 'fetchall': False, 'status': 0}
        port = self.select(**query)[1]
        query = {'table': 'run', 'selector': {'port': str(port)}, 'proxy': proxy}
        self.update(**query)
        return port

    def proxy_exists(self, proxy):
        query = {'table': 'run', 'proxy': proxy}
        return self.select(**query)

    def change_status(self, port, status):
        query = {'table': 'run', 'selector': {'port': str(port)}, 'status': status}
        self.update(**query)

    def clear_port(self, port):
        query = {'table': 'run', 'selector': {'port': str(port)}, 'proxy': None}
        self.update(**query)

    def clear(self):
        query = {'table': 'run', 'status': 1}
        proxies = self.select(**query)
        for proxy in proxies:
            proxy, port, _ = proxy
            query = {'table': 'run', 'selector': {'port': str(port)}, 'proxy': None, 'status': 0}
            self.update(**query)

    def kill_thread(self, port):
        try:
            print(f"[{port}]: ", self.dict_process[f'{port}'], 'killed')
            self.dict_process[f'{port}'].join()
            self.change_status(port, 0)
            self.clear_port(port)
            self.dict_process[f'{port}'] = False
        except AttributeError:
            pass

    def execute_threads(self, proxy, port):
        asyncio.run(self.run_server(proxy, port))

    def change_status_proxy(self, proxy):
        query = {'table': 'proxy_', 'selector': {'ip': proxy}, 'alive': 0}
        self.update(**query)

    @staticmethod
    def is_port_available(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(('127.0.0.1', port))
        except OSError as e:
            if e.errno == 10013:
                return False
            else:
                print(e)
        finally:
            s.close()
        return True

    @staticmethod
    async def run_server(proxy, port):
        port = str(port)
        server = pproxy.Server(f'http://127.0.0.1:{port}')
        remote = pproxy.Connection(proxy)
        args = dict(rserver=[remote], verbose=print)
        handler = await server.start_server(args)
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            print('Server on port', port, 'stopped.')
            handler.close()
            await handler.wait_closed()

    def run(self):
        self.clear()
        self.dict_process = {}

        for i in range(1000):
            port = 9000 + i
            available = self.is_port_available(port)
            if available:
                self.dict_process[f"{9000 + i}"] = False
            if not available:
                self.change_status(port, 2)

        while True:
            proxies = self.get_all_proxies
            for proxy in proxies:
                data, ip, port  = proxy[0], proxy[1], proxy[2]
                proxy = f"{data}@{ip}:{port}"
                if not self.proxy_exists(proxy):
                    port = self.assign_port(proxy)
                    self.change_status(port, 1)
            for proxy in self.proxies:
                proxy, port, _ = proxy
                ip = proxy.split('@')[1].split(':')[0]
                alive = self.alive_status(ip)
                if alive:
                    if not self.dict_process[f'{port}']:
                        time.sleep(0.2)
                        try:
                            thread = Thread(target=self.execute_threads, args=(proxy, port))
                            thread.start()
                            self.dict_process[f'{port}'] = thread
                            print(f'[{port}]:', self.dict_process[f'{port}'], 'run')
                        except OSError:
                            self.change_status_proxy(proxy)

                elif not alive:
                    self.kill_thread(port)

            time.sleep(5)

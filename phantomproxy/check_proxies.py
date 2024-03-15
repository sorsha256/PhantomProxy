import os
import time
import pproxy
import argparse
import asyncio
import phantomproxy.SQLite


class Proxy(phantomproxy.SQLite.SQLite):

    async def test_tcp(self, p):
        query = {'table': 'proxy_', 'status': 0, 'fetchall': False}
        try:
            data, ip, port, _type_proxy, _alive, _status = self.select(**query)
            proxy = f"{data}@{ip}:{port}"
        except TypeError:
            time.sleep(300)
            return False
        query_status = {'table': 'proxy_', 'selector': {'ip': ip}, 'status': 2}
        self.update(**query_status)
        query_bad = {'table': 'proxy_', 'selector': {'ip': ip}, 'alive': 0, 'status': 1}
        try:
            conn = pproxy.Connection(proxy)

        except argparse.ArgumentTypeError:
            print(p, ip, "dead!")
            self.update(**query_bad)
            return False
        except ValueError:
            print(p, ip, "dead!")
            self.update(**query_bad)
            return False
        try:
            reader, writer = await asyncio.wait_for(conn.tcp_connect('www.tiktok.com', 80), timeout=1)
            writer.write(b'GET / HTTP/1.1\r\n'
                         b'Host: www.tiktok.com\r\n'
                         b'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                         b' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36\r\n'
                         b'Accept: */*\r\n'
                         b'\r\n')
            data = await asyncio.wait_for(reader.read(1024 * 16), timeout=1)
            data = data.decode()
            if "301 Moved Permanently" in data:
                query = {'table': 'proxy_', 'selector': {'ip': ip}, 'alive': 1, 'status': 1}
                self.update(**query)
                print(p, ip, "alive!")
            return data
        except Exception:
            self.update(**query_bad)
            return False
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                print(p, ip, "dead!")
                self.update(**query_bad)
                return False

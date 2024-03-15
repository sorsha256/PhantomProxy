<h1>PhantomProxy</h1>

This repository is designed to parse Shadowsocks from open sources on GitHub, verify them, and deploy them on the local server 127.0.0.1:9xxx.

<h2>Installation</h2>


Simply clone this repository to your device:

`git clone https://github.com/sorsha256/PhantomProxy.git`

You may need to install additional libraries, such as:

<link>https://github.com/qwj/python-proxy</link>


<h2>Usage</h2>
There are three executable files in this repository:


`parse_proxies.py`

`check_proxies.py`

`proxy_server.py`

<h3>Step 1: Parsing Shadowsocks</h3>

The primary file that needs to be executed is `parse_proxies.py` . All Shadowsocks are saved in `/proxies/name.txt`, and then their txt files are saved to the SQLite database. Actually, saving to text files is not justified, so if desired, you can rewrite it to save everything directly to the database.

`python3 parse_proxies.py`

<h3>Step 2: Proxy Verification</h3>

After all Shadowsocks have been parsed, they need to be validated, which can be done using the script:

`python3 check_proxies.py`

Proxies with a valid status are marked _1_ in the database and ready for use.

***Note***: Validation is performed by connecting and checking the connection to TikTok. If you need to change the resource to which you need to connect and perform validation, you need to modify the headers and URL in the file `/phantomproxy/check_proxies.py`, lines 34-40.
```python
reader, writer = await asyncio.wait_for(conn.tcp_connect('www.tiktok.com', 80), timeout=1)
writer.write(b'GET / HTTP/1.1\r\n'
  b'Host: www.tiktok.com\r\n'
  b'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
  b' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36\r\n'
  b'Accept: */*\r\n'
  b'\r\n')
```

<h3>Step 3: Launching the Local Server</h3>

After you have validated all proxies, you can confidently start and allocate all proxies on your local ports starting from 9000. The script checks ports from `9000` to `9999`, so be careful, they should not be occupied by anything else.

`python3 proxy_server.py`

*Now you are ready to use Shadowsocks through your local ports.*

```python
proxies = {"http": "http://127.0.0.1:{port}"}
response = requests.get(url=api_url, params=params, headers=headers, proxies=proxies)
```



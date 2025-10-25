import requests

# 代理池的地址
PROXY_POOL_URL = "http://localhost:5555/random"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
}

# 获取代理IP
def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None

PROXY_IP = get_proxy()

url = "http://127.0.0.1:5000/getInfo"

proxies = {
    "https": "http://{}".format(PROXY_IP)
}

# 添加X-Forwarded-For头
# X-Forwarded-For头通常包含客户端的真实IP地址
# 这样做是为了让服务器认为这是一个真正的用户发出的请求
# 这也是一种常见的反代理检测手段
headers['X-Forwarded-For'] = PROXY_IP

response = requests.get(
    url,
    headers=headers,
    proxies=proxies,
    verify=False  # 如果是https请求可能需要这个
)
print(response.text)
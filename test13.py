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

response = requests.get(
    url,
    headers=headers,
    proxies={
        "https":"http://{}".format(PROXY_IP)
        }
    )
print(response.text)
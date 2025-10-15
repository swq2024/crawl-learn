import requests

url = "http://localhost:5000/getInfo"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
}
response = requests.get(url, headers=headers)
print(response.text)

# https://mp.weixin.qq.com/s?__biz=Mzg2NzYyNjg2Nw==&mid=2247489917&idx=1&sn=aec8d83fd44d51bcb5a91c5a645347f2&chksm=ceb9e361f9ce6a776d1a576f6e94935cffc5469862b425a25ec3c8badb5a7bc7c38b155a7bbf&cur_album_id=2448798954764255234&scene=189#wechat_redirect
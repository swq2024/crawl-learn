import multiprocessing
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "https://movie.douban.com/top250"
TIMEOUT=8

def get_html(url):
    headers = {
        # User-Agent 随机化：防止被豆瓣反爬虫机制屏蔽
        "User-Agent": UserAgent().random,
    }
    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.text
        else:
            print("请求页面失败", response.status_code)
            return None
    except Exception as e:
        print("请求页面异常", str(e))
        return None

def parse_html(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        items = soup.find_all("div", class_="item")
        movies = []
        for item in items:
            title = item.find("span", class_="title").get_text()
            img = item.find("img")["src"]
            rating = item.find("span", class_="rating_num").get_text()
            quote_tag = item.find("p", class_="quote")
            quote = quote_tag.span.get_text() if quote_tag and quote_tag.span else ""
            movies.append({
                "title": title,
                "img": img + " ", 
                "rating": rating,
                "quote": quote
            })
        return movies
    except Exception as e:
        print("解析页面异常", str(e))
        return []

def save_to_csv(movies, filename="douban_top250_movies1.csv"):
    try:
        df = pd.DataFrame(movies)
        df.to_csv(filename, index=False, encoding="utf-8-sig")
    except Exception as e:
        print("保存CSV异常", str(e))

def main():
    all_movies = []
    for i in range(10):  # 250 movies, 25 per page
        url = f"{BASE_URL}?start={i*25}&filter="
        print(f"正在抓取第 {i+1} 页: {url}")
        html = get_html(url)
        if html:
            movies = parse_html(html)
            all_movies.extend(movies) # 合并结果
    save_to_csv(all_movies)
    print("数据已保存到 douban_top250_movies.csv")
    
if __name__ == "__main__":
    start = time.time()
    print("开始抓取豆瓣 Top 250 电影数据...")
    main()
    end = time.time()
    print(f"耗时: {round(end - start)} 秒")
    print("抓取完成.")

# def main(url):
#     html = get_html(url)
#     if html:
#         return parse_html(html)
#     return []

# if __name__ == "__main__":
#     start = time.time()
#     urls = [f"{BASE_URL}?start={i*25}&filter=" for i in range(0, 10)]
#     pool = multiprocessing.Pool(multiprocessing.cpu_count()) # 创建进程池并根据CPU的内核数量创建相应的进程池
#     results = pool.map(main, urls) # 并行执行多个任务
#     pool.close() # 使进程池不再接受新的任务
#     pool.join() # 等待进程池的所有进程执行完毕再结束

#     # 合并所有页的数据
#     all_movies = []
#     for movies in results:
#         all_movies.extend(movies)
#     save_to_csv(all_movies)
#     end = time.time()
#     print(f"耗时: {round(end - start)} 秒")
#     print("抓取完成.")

# https://mp.weixin.qq.com/s?__biz=Mzg2NzYyNjg2Nw==&mid=2247489916&idx=1&sn=8431cf83b36ba846a82fc5af540d9eb8&chksm=ceb9e360f9ce6a7676ae6f6cf34e9d8a9f222fedec4f761ad90ec5c6fe227f608ce25abce484&cur_album_id=2448798954764255234&scene=189#wechat_redirect
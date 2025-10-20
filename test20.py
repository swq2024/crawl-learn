from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
import os
import re
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

_url = 'https://www.doutupk.com/article/list/?page={page}'
urls = [_url.format(page=page) for page in range(1, 731+1)]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0'
}

# 创建带有重试机制的requests会话
# - 最多重试3次，每次重试间隔按指数增长(1, 2, 4秒)
# - 对500,502,503,504状态码自动重试
# - 同时适配http和https协议
def create_session():
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# 获取指定URL页面中的所有文章链接
# 参数:
#   session: requests会话对象
#   url: 要抓取的页面URL
# 返回:
#   成功: 包含所有文章链接的列表
#   失败: 空列表
def fetch_page_urls(session, url):
    try:
        resp = session.get(url, headers=headers, verify=False, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, 'lxml')
        return [a.get('href') for a in soup.find_all('a', class_=['list-group-item random_list', 'list-group-item random_list tg-article'])]
    except Exception as e:
        print(f"获取页面链接失败: {url}, 错误: {e}")
        return []

def clean_special_chars(text):
    # 移除除中英文、常见标点和特殊字符外的所有字符
    cleaned = re.sub(r'[^\w\u4e00-\u9fa5\s,.!?，。！？、\[\]()（）【】:：@#\$%\^&\*\-+=\|\\/<>"\'`~;；]', '', text)
    # 移除Windows文件名非法字符和控制字符
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', cleaned)
    # 去除首尾点号和空格，并截取前100个字符
    return cleaned.strip('. ')[:100]

# 获取指定URL的图片链接和标题
# 参数: session - 请求会话对象, url - 目标网页URL
# 返回: 包含标题和图片URL列表的字典
def fetch_image_urls(session, url):
    try:
        # 发送HTTP GET请求
        resp = session.get(url, headers=headers, timeout=10)
        # 检查HTTP响应状态
        resp.raise_for_status()
        # 解析HTML内容
        soup = BeautifulSoup(resp.content, 'lxml')
        # 获取并清理标题文本
        title = soup.find('div', class_='pic-title').find('h1').get_text().strip()
        return {
            'title': title,
            'images': [img.get('src') for img in soup.find('div', class_='pic-content').find_all('img')]
        }
    except Exception as e:
        print(f"获取图片链接失败: {url}, 错误: {e}")
        return {'title': '', 'images': []}

def download_image(session, img_url, dir_path, idx):
    # 下载图片并保存到指定目录
    try:
        # 获取图片扩展名，默认为.jpg
        img_ext = os.path.splitext(img_url)[1] or '.jpg'
        # 构造图片保存路径，格式为"目录/序号.扩展名"
        img_path = os.path.join(dir_path, f'{idx + 1}{img_ext}')
        
        # 检查图片是否已存在，避免重复下载
        if not os.path.exists(img_path):
            # 发送HTTP GET请求获取图片
            resp = session.get(img_url, headers=headers, timeout=30)
            # 检查HTTP响应状态
            resp.raise_for_status()
            # 将图片内容写入文件
            with open(img_path, 'wb') as f:
                f.write(resp.content)
            print(f'下载成功: {img_path}')
        return True
    except Exception as e:
        # 捕获并打印下载异常
        print(f"下载失败: {img_url}, 错误: {e}")
        return False

def process_category(session, cat_url):
    # 获取分类下的所有图片URL
    image_dict = fetch_image_urls(session, cat_url)
    # 如果没有图片则直接返回
    if not image_dict['images']:
        return
    
    # 清理分类标题中的特殊字符
    clean_title = clean_special_chars(image_dict['title'])
    # 创建保存图片的目录
    dir_path = os.path.join('doutupk_images', clean_title)
    os.makedirs(dir_path, exist_ok=True)
    
    # 使用线程池(最大5个线程)并发下载图片
    with ThreadPoolExecutor(max_workers=5) as executor:
        # 提交所有下载任务
        futures = [executor.submit(download_image, session, img_url, dir_path, idx) 
                  for idx, img_url in enumerate(image_dict['images'])]
        # 等待所有任务完成
        for future in as_completed(futures):
            future.result()

def write_image_optimized():
    # 使用线程池(最大3个线程)并行处理URL
    with ThreadPoolExecutor(max_workers=3) as executor:
        # 创建会话对象
        session = create_session()
        futures = []
        
        # 为每个URL提交处理任务到线程池
        for url in urls:
            futures.append(executor.submit(process_url, session, url))
            
        # 等待所有任务完成，处理结果或异常
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"处理URL失败: {e}")

# 处理给定URL，获取分类URL并使用线程池并行处理每个分类
def process_url(session, url):
    # 获取当前页面的所有分类URL
    category_urls = fetch_page_urls(session, url)
    if not category_urls:
        return
        
    # 使用最多5个线程的线程池并行处理每个分类
    with ThreadPoolExecutor(max_workers=5) as executor:
        # 为每个分类URL创建处理任务
        futures = [executor.submit(process_category, session, cat_url) 
                  for cat_url in category_urls]
        # 等待所有任务完成
        for future in as_completed(futures):
            future.result()

if __name__ == '__main__':
    start_time = time.time()
    try:
        write_image_optimized()
    except KeyboardInterrupt:
        print('用户终止了程序')
    except Exception as e:
        print(f'程序运行出错: {e}')
    finally:
        print(f'程序结束，总耗时: {time.time() - start_time:.2f}秒')

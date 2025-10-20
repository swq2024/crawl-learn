import os
import re
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from tqdm import tqdm

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        # 指定日志文件路径和编码
        logging.FileHandler('doutupk_downloader.log', encoding='utf-8-sig'),
        logging.StreamHandler()
    ],
    # encoding='utf-8-sig'  # 指定终端输出编码为utf-8-sig
)
logger = logging.getLogger(__name__)

# 配置常量
BASE_URL = 'https://www.doutupk.com'
START_PAGE = 1
END_PAGE = 731
MAX_WORKERS = 8  # 并发线程数
RETRY_TIMES = 3  # 重试次数
TIMEOUT = 10  # 请求超时时间
OUTPUT_DIR = 'doutupk_images2'  # 图片保存目录

# 创建全局会话
session = requests.Session()

# 配置重试策略
retry_strategy = Retry(
    total=RETRY_TIMES,
    backoff_factor=1, # 指数退避: 1, 2, 4秒
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

# 设置请求头
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0'
})

def clean_special_chars(text):
    """清理文件名中的特殊字符"""
    # 保留中文、英文、数字、基本标点和常见表情符号
    cleaned = re.sub(r'[^\w\u4e00-\u9fa5\s,.!?，。！？、\[\]()（）【】:：@#\$%\^&\*\-+=\|\\/<>"\'`~;；]', '', text)
    # 移除Windows文件名不允许的字符
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', cleaned)
    # 移除开头和结尾的空格和点
    cleaned = cleaned.strip('. ')   
    # 限制路径长度
    return cleaned[:100] if len(cleaned) > 100 else cleaned

def fetch_page_urls(page):
    """获取单个页面的所有分类链接"""
    url = f'{BASE_URL}/article/list/?page={page}'
    try:
        response = session.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        return [urljoin(BASE_URL, a.get('href')) 
                for a in soup.find_all('a', class_=['list-group-item random_list', 'list-group-item random_list tg-article'])]
    except Exception as e:
        logger.error(f"获取页面 {url} 失败: {str(e)}")
        return []

def fetch_image_info(category_url):
    """获取分类页面的图片信息"""
    try:
        response = session.get(category_url, timeout=TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        
        # 获取标题
        title_div = soup.find('div', class_='pic-title')
        title = clean_special_chars(title_div.find('h1').get_text().strip()) if title_div else "未知标题"
        
        # 获取图片链接
        pic_box = soup.find('div', class_='pic-content')
        img_tags = pic_box.find_all('img') if pic_box else []
        image_urls = [urljoin(BASE_URL, img.get('src')) for img in img_tags if img.get('src')]
        
        return {'title': title, 'images': image_urls, 'url': category_url}
    except Exception as e:
        logger.error(f"获取分类页面 {category_url} 失败: {str(e)}")
        return None

def download_image(image_info):
    """下载单个分类的所有图片"""
    if not image_info or not image_info['images']:
        return
    
    title = image_info['title']
    image_urls = image_info['images']
    category_url = image_info['url']
    
    # 创建目录
    dir_path = os.path.join(OUTPUT_DIR, title)
    os.makedirs(dir_path, exist_ok=True)
    
    # 下载图片
    for idx, img_url in enumerate(image_urls, 1):
        try:
            # 获取图片扩展名
            img_ext = os.path.splitext(img_url)[1].split('?')[0] or '.jpg'
            img_filename = f"{idx:03d}{img_ext}"
            img_path = os.path.join(dir_path, img_filename)
            
            # 跳过已存在的文件
            if os.path.exists(img_path):
                logger.info(f"跳过已存在文件: {img_path}")
                continue
            
            # 下载图片
            response = session.get(img_url, timeout=TIMEOUT)
            response.raise_for_status()
            
            # 保存图片
            with open(img_path, 'wb') as f:
                f.write(response.content)
            logger.info(f"下载成功: {img_path}")
            
        except Exception as e:
            logger.error(f"下载图片 {img_url} 失败: {str(e)}")
            continue

def main():
    start_time = time.time()
    
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 获取所有分类链接
    logger.info("开始获取分类链接...")
    category_urls = set()
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(fetch_page_urls, page) for page in range(START_PAGE, END_PAGE + 1)]
        for future in tqdm(as_completed(futures), total=len(futures), desc="获取分类链接"):
            category_urls.update(future.result())
    
    logger.info(f"共找到 {len(category_urls)} 个分类链接")
    
    # 获取图片信息
    logger.info("开始获取图片信息...")
    image_infos = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(fetch_image_info, url) for url in category_urls]
        for future in tqdm(as_completed(futures), total=len(futures), desc="获取图片信息"):
            result = future.result()
            if result:
                image_infos.append(result)
    
    logger.info(f"共获取到 {len(image_infos)} 个分类的图片信息")
    
    # 下载图片
    logger.info("开始下载图片...")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(download_image, info) for info in image_infos]
        for future in tqdm(as_completed(futures), total=len(futures), desc="下载图片"):
            future.result()
    
    end_time = time.time()
    logger.info(f"所有任务完成! 总耗时: {end_time - start_time:.2f}秒")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("用户终止了程序")
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}", exc_info=True)
    finally:
        session.close()
        logger.info("程序结束")
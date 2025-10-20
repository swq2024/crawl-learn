import requests
from bs4 import BeautifulSoup
import os
import re

_url = 'https://www.doutupk.com/article/list/?page={page}'
urls = [_url.format(page=page) for page in range(1, 731+1)]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0'
}

def fetch_page_urls(url): # 获取单个页面的所有分类链接
    url_links = []
    resp = requests.get(url, headers=headers, verify=False, timeout=10) # todo: 添加重试机制
    soup = BeautifulSoup(resp.content, 'lxml')
    img_category_list = soup.find_all('a', class_=['list-group-item random_list', 'list-group-item random_list tg-article'])
    for img in img_category_list:
        url_links.append(img.get('href'))
    return url_links

def clean_special_chars(text):
    """去除特殊字符但保留可见字符和表情符号"""
    # 保留中文、英文、数字、标点符号和常见表情符号
    cleaned = re.sub(r'[^\w\u4e00-\u9fa5\s,.!?，。！？、\[\]()（）【】:：@#\$%\^&\*\-+=\|\\/<>"\'`~;；]', '', text)
    # 额外移除Windows文件名不允许的字符
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', cleaned)
    # 移除开头和结尾的空格和点
    cleaned = cleaned.strip('. ')
    # 限制路径长度
    return cleaned[:100] if len(cleaned) > 100 else cleaned

def fetch_image_urls(url): # 每个页面获取图片链接
    dict_ = {}
    image_list = []
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, 'lxml')
    header_box = soup.find('div', class_='pic-title') # 获取标题所在的div
    title = clean_special_chars(header_box.find('h1').get_text().strip())
    pic_box = soup.find('div', class_='pic-content') # 获取所有图片所在的div
    img_tags = pic_box.find_all('img')

    for img in img_tags:
        image_list.append(img.get('src'))
        # img_url = img.get('src')
        # if img_url.startswith('http'):
        #     img_url = img_url.replace('http://', 'https://')
        # image_list.append(img_url)
    
    dict_['title'] = title
    dict_['images'] = image_list
    return dict_

def write_image():
    for page_url in urls:
        print(f'正在处理列表页面: {page_url}')
        category_urls = fetch_page_urls(page_url)
        print(f'在该页面共找到 {len(category_urls)} 个分类链接')
        for cat_url in category_urls:
            print(f'正在处理分类页面: {cat_url}')
            image_dict = fetch_image_urls(cat_url)
            print(image_dict['title'], f'共找到 {len(image_dict["images"])} 张图片')
            title = image_dict['title']
            image_list = image_dict['images']
            # 创建目录保存图片
            clean_title = clean_special_chars(title).strip()
            dir_path = os.path.join('doutupk_images2', clean_title) # 根目录下创建 doutupk_images 文件夹
            # 确保目录存在
            os.makedirs(dir_path, exist_ok=True)
            
            for idx, img_url in enumerate(image_list):
                print(f'正在下载图片: {img_url}')
                img_resp = requests.get(img_url, headers=headers)
                img_ext = os.path.splitext(img_url)[1]  # 获取图片扩展名
                img_filename = f'{idx + 1}{img_ext}'
                img_path = os.path.join(dir_path, img_filename)
                with open(img_path, 'wb') as f:
                    f.write(img_resp.content)
                    print(f'已成功下载并保存到: {img_path}')
                    print('*' * 20)
        
if __name__ == '__main__':
    try:
        write_image()
    except Exception as e:
        print(f'程序运行出错: {e}')
    except KeyboardInterrupt:
        print('用户终止了程序')
    finally:
        print('程序结束')

import requests
import re
import json

def getHTMLText(url):
    try:
        response = requests.get(url, timeout=30)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

def parsePage(html):
    pattern = re.compile(
        '<li>.*?list_num.*?(\\d+).</div>.*?<img src="(.*?)".*?class="name".*?title="(.*?)">.*?class="star">.*?class="tuijian">(.*?)</span>.*?class="publisher_info">.*?target="_blank">(.*?)</a>.*?class="publisher_info">.*?target="_blank">(.*?)</a></div>.*?<p><span\\sclass="price_n">&yen;(.*?)</span>.*?</li>', re.S
    )
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'rank': item[0],
            'image_url': item[1],
            'title': item[2],
            'recommendation': item[3],
            'author': item[4],
            'publisher': item[5],
            'price': item[6]
        }

def write_item_to_file(item, filename='books.txt'):
    print("开始写入数据 ===>" + str(item))
    with open(filename, 'a', encoding='UTF-8') as f:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')
        f.close()

def main(page):
    url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-' + str(page)
    html = getHTMLText(url)
    items = parsePage(html)

    for item in items:
        write_item_to_file(item)

if __name__ == '__main__':
    for i in range(1, 10):
        main(i)
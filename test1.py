import urllib.request
import re

# response = urllib.request.urlopen('http://www.baidu.com/', data=None, timeout=10)
# html = response.read()
# print(html.decode('utf-8'))

content = "Xiaoshuaib has 100 bananas"
pattern = re.compile('Xi.*?(\d+)\s.*s',re.S) # compile 方便后续复用该正则表达式
res = re.match(pattern,content)

print(res.group(1))
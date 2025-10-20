import pdfkit

custom_css = """
body, p, div, span, h1, h2, h3, h4, h5, h6, a, li, td {
    font-family: "Microsoft YaHei", "SimSun", "Arial Unicode MS", sans-serif !important;
}
"""

default_options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",  # 设置编码为 UTF-8
    'custom-header': [
        ('Accept-Encoding', 'gzip')
    ],
    'no-outline': None,
    # 注入自定义 CSS 来解决字体问题
    'user-style-sheet': custom_css,
    # 增加容错性，忽略一些加载错误，避免因个别资源加载失败导致整个页面渲染失败
    'load-error-handling': 'ignore',
    'load-media-error-handling': 'ignore',
    # 等待2秒后再执行JavaScript
    'javascript-delay': 2000,
}

path_wkthmltopdf = r"F:\\python-learn\\wkhtmltox\\bin\\wkhtmltopdf.exe"
default_config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

def file_to_pdf(input, filename='output.pdf'):
    pdfkit.from_file(input, output_path=filename, options=default_options, configuration=default_config)

def string_to_pdf(string, filename='output.pdf'):
    pdfkit.from_string(string, output_path=filename, options=default_options, configuration=default_config)

def url_to_pdf(url, filename='output.pdf'):
    pdfkit.from_string(url, output_path=filename, options=default_options, configuration=default_config)
if __name__ == "__main__":
    # 注意：pdf保存的文件名不可以带特殊字符(包括-,_)和中文字符，否则会报错
    # file_to_pdf("index.html", "index.pdf")
    # string_to_pdf("Hello World! 你好世界", "hello.pdf")
    url_to_pdf("https://www.example.com", "example.pdf")

# https://mp.weixin.qq.com/s?__biz=Mzg2NzYyNjg2Nw==&mid=2247489975&idx=1&sn=a52ab9885fa07396ea4446a3c5f73003&chksm=ceb9e3abf9ce6abdb60cf01cc601ea0874c26f4f0b59083d25948ddef5d80005ca772073e23b&cur_album_id=2448798954764255234&scene=189#wechat_redirect
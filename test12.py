from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/getInfo')
def getInfo():
    print("请求头信息:", request.headers)
    print("直接连接IP:", request.remote_addr)
    
    # 代理检测逻辑
    proxy_headers = ['X-Forwarded-For', 'Via', 'Forwarded']
    using_proxy = any(h in request.headers for h in proxy_headers)
    
    if str(request.headers.get('User-Agent')).startswith('python'):
        return '<h1>fuck off python user</h1>'
    elif using_proxy:
        return '<h1>Detected proxy usage</h1>'
    else:
        return '<h1>Hello World</h1>'

if __name__ == '__main__':
    app.run(debug=True)
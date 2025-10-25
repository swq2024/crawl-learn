from flask import Flask
from flask import request

app = Flask(__name__)

# 访问 http://127.0.0.1:5000/getInfo
@app.route('/getInfo')
def getInfo():
    print("请求头信息:", request.headers)
    print("直接连接IP:", request.remote_addr)
    
    # 获取真实代理IP
    real_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    print("代理IP:", real_ip)
    
    # 获取其他代理相关信息
    via = request.headers.get('Via', 'No Via Header')
    forwarded = request.headers.get('Forwarded', 'No Forwarded Header')
    print("Via:", via)
    print("Forwarded:", forwarded)
    
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
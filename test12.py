from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/getInfo')
def getInfo():
    print(request.headers)
    if(str(request.headers.get('User-Agent')).startswith('python')):
        return '<h1>fuck off python user</h1>'
    else:
        return '<h1>Hello World</h1>'

if __name__ == '__main__':
    app.run(debug=True)
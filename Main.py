from flask import Flask, abort, redirect, request
import json
import importlib

# 测试
a = importlib.import_module("w3.user")
a.invoke({"message": "input data is here"})

app = Flask(__name__, static_url_path='')  # , root_path='/'

@app.route('/')
def index():
    print('index...')
    return app.send_static_file('index.html')


@app.route('/user/<name>')
def sayHello(name):
    if name == 'baidu':
        return redirect('http://www.baidu.com')
    elif name == 'NO':
        return abort(404)

    return '<h1> Hello,%s </h1>' % name


@app.route('/invoke/<product>/<feature>', methods=['post'])
def invokeFeature(product, feature):
    featureStr = product + "." + feature

    # 动态载入包
    f = importlib.import_module(featureStr)

    # 得到输入参数
    inputData = json.loads(request.get_data())

    # 调用返回结果
    result = f.invoke(inputData)

    # 返回json数据
    return json.dumps(result)


# all url mapping
print (app.url_map)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)

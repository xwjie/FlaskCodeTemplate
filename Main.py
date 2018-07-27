#
# 晓风轻 https://github.com/xwjie/FlaskCodeTemplate
#
from flask import Flask, abort, redirect, request
import json
import importlib

# fixme why  static_url_path not work？？
app = Flask(__name__)  #  ,static_url_path='', root_path='/'

@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/user/<name>')
def sayHello(name):
    if name == 'baidu':
        return redirect('http://www.baidu.com')
    elif name == 'NO':
        return abort(404)

    return '<h1> Hello,%s </h1>' % name


# 动态调用模块功能
@app.route('/invoke/<product>/<feature>', methods=['post'])
def invokeFeature(product, feature):
    featureStr = product + "." + feature

    # 动态载入包
    f = importlib.import_module(featureStr)

    # 得到输入参数(json格式)
    inputData = json.loads(request.get_data())

    # 调用返回结果
    try:
        result = f.invoke(inputData)
        # 返回json数据
        return json.dumps(newResultBean(result))
    # 校验异常
    except Exception as e:
        return json.dumps(newCheckFail(e))


# 构建返回对象
def newResultBean(data):
    return {
        "data": data,
        "code": 0,
        "msg": "success"
    }


# 构建返回异常对象
def newCheckFail(e):
    return {
        "data": None,
        "code": 1,
        "msg": str(e)
    }


# all url mapping
print (app.url_map)

# 上线需要把debug=true去掉
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)

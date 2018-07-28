#
# 晓风轻 https://github.com/xwjie/FlaskCodeTemplate
#
from flask import Flask, abort, redirect, request, Response
import json
import importlib
import  pkgutil

app = Flask(__name__,static_url_path='')  #  , root_path='/'

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

@app.route('/login', methods=['post'])
def login():
    # 得到输入参数(form格式)
    username = request.form['username']
    password = request.form['password']
    print (username, password)

    result = False

    if username =="xwjie":
        result = True

    return toJson(newResultBean(result));

@app.route('/list', methods=['get'])
def listFeatures():
    # 得到所有package
    result =list(map(lambda a: a.name, filter(lambda a: a.ispkg, pkgutil.iter_modules(["."], ""))))

    print (result)
    #result = [(modelName, isPackage) for _, modelName, isPackage in pkgutil.iter_modules(["."], "")]

    # 返回json数据
    return toJson(newResultBean(result))


# 动态调用模块功能
@app.route('/invoke/<product>/<feature>', methods=['post'])
def invokeFeature(product, feature):
    featureStr = product + "." + feature
    try:
        # 动态载入包
        model = importlib.import_module(featureStr)

        # 得到输入参数(json格式)
        inputData = json.loads(request.get_data())

        # 调用返回结果
        result = model.invoke(inputData)
        # 返回json数据
        return toJson(newResultBean(result))
    # 校验异常
    except Exception as e:
        return toJson(newCheckFail(e))

# flask 返回json格式
# obj to json string, 声明Content-Type为json格式
def toJson(obj):
    return Response(json.dumps(obj), mimetype='application/json; charset=utf-8')

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

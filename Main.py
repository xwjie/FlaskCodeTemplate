#
# 晓风轻 https://github.com/xwjie/FlaskCodeTemplate
#
from flask import Flask, abort, redirect, request, Response, session
from flask import json
import importlib
import  pkgutil
from database import db_session, init_db
from models.User import  User
import jsonutil

app = Flask(__name__,static_url_path='')  #  , root_path='/'
app.secret_key = b'xiaofengqing'

print (app.secret_key)

#  create the database
init_db()


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/hello/<name>')
def sayHello(name):
    if name == 'baidu':
        return redirect('http://www.baidu.com')
    elif name == 'NO':
        return abort(404)

    return '<h1> Hello,%s </h1>' % name

# 得到当前登陆用户
@app.route("/user")
def currentUser():
    user = None

    # 如果登陆了
    if 'user' in session:
        user = session["user"]

    return toJson(newResultBean(user))

#执行登陆
@app.route('/login', methods=['post'])
def login():
    # 得到输入参数(form格式)
    username = request.form['username']
    password = request.form['password']

    print (username, password)

    user = None

    if username is not None:

        #
        user = User(username, password)
        db_session.add(user)
        db_session.commit()

        # 登陆后，保存到session里面
        # user无法放进去，无法序列化
        session['user'] = user._serialize()

    return toJson(newResultBean(user));

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
    jsonStr = json.dumps(obj, cls=jsonutil.AlchemyEncoder, ) # default=serialize
    #jsonStr = dumps(obj)
    print ('json str:' , jsonStr)
    return Response(jsonStr, mimetype='application/json; charset=utf-8')

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


# test
u = User("ddd", "password")
print (u.__dict__)
print(toJson(newResultBean(u)))

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# 上线需要把debug=true去掉
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)

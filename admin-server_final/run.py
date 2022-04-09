# coding=utf-8
import json
import os
import time
import configs
from flask import Flask, send_from_directory, request, jsonify, render_template, current_app
from itsdangrous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask_cors import CORS
import MysqlUtil as DBUtil
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# 加载配置文件
app.config.from_object(configs)
db = SQLAlchemy(app)
# db绑定app
db.init_app(app)
# 解决cors问题
cors = CORS(app, supports_credentials=True)

# api接口前缀
apiPrefix = '/api/v1/'

########## 文件上传API

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 设置文件上传的目标文件夹
basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径
ALLOWED_EXTENSIONS = {'bmp', 'png', 'gif', 'jpg', 'jpeg', 'mp4', 'rmvb', 'avi', 'ts', 'wav',
                      'midi', 'cda', 'mp3', 'wma'}  # 允许上传的文件后缀


# 判断文件是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# TODO: 对传入的相关参数进行处理
@app.route(apiPrefix + 'upload', methods=['POST'], strict_slashes=False)
def api_upload():
    print(request.values.items())
    token = request.values.get('token', None)
    if verify_login(token):
        file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])  # 拼接成合法文件夹地址
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)  # 文件夹不存在就创建
        f = request.files['file']  # 从表单的file字段获取文件
        if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
            fname = f.filename
            ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
            unix_time = int(time.time())
            new_filename = str(unix_time) + '.' + ext  # 修改文件名
            f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
            return jsonify({"message": "上传成功", "responseCode": 200})
        else:
            return jsonify({"message": "上传失败", "responseCode": -1, "detail_message": "文件类型不合格"})
    else:
        return jsonify({"message": "上传失败", 'token_message': '未登录', "responseCode": -1})


########## React访问flask资源

RESOURCE_FOLDER = 'resource'


@app.route('/js/<path:filename>')
def send_js(filename):
    dirpath = os.path.join(app.root_path, RESOURCE_FOLDER + '/js')
    return send_from_directory(dirpath, filename, as_attachment=True)


########## React访问flask上的NTF博物馆
@app.route('/api/museum', methods=['GET'], strict_slashes=False)
def api_museum():
    if request.method == 'GET':
        return render_template('index.html')


# # show photo
# @app.route('/show/<string:filename>', methods=['GET'])
# def show_photo(filename):
#     file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
#     if request.method == 'GET':
#         if filename is None:
#             pass
#         else:
#             image_data = open(os.path.join(file_dir, '%s' % filename), "rb").read()
#             response = make_response(image_data)
#             response.headers['Content-Type'] = 'image/png'
#             return response
#     else:
#         pass

########## Token接口
def generate_auth_token(data):
    expiration = 3600
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)  # expiration是过期时间
    # 利用唯一的用户名生成token
    token = s.dumps({'user_name': data['user_name']})
    # print(token)
    return token.decode()


def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    # print('qi', token)
    if token is not None:
        try:
            data = s.loads(token)
            return 'success'
        except SignatureExpired:
            return 'expired'  # valid token,but expired
        except BadSignature:
            return 'invalid'  # invalid token
        # if data.get('user_name') == user_data.get('user_name'):
        #     return 'success'
    else:
        return 'empty'


def verify_login(token):
    _token = verify_auth_token(token)
    if _token == 'success':
        return True
    else:
        return False


########## 注册接口
@app.route(apiPrefix + 'register', methods=['POST'], strict_slashes=False)
def register_user():
    json_str = request.get_data(as_text=True)
    user_data = json.loads(json_str)
    print(user_data)
    response = DBUtil.addOrUpdateUsers(user_data)
    response['responseCode'] = 200
    print(response)
    return jsonify(response)


# 动态检验用户名是否可用
@app.route(apiPrefix + 'checkUserName', methods=['POST'], strict_slashes=False)
def check_username():
    json_str = request.get_data(as_text=True)
    user_data = json.loads(json_str)
    response = DBUtil.checkUserNameRepeat(user_data)
    response['responseCode'] = 200
    return jsonify(response)


########## 登陆接口
@app.route(apiPrefix + 'login', methods=['POST'], strict_slashes=False)
def login_user():
    json_str = request.get_data(as_text=True)
    user_data = json.loads(json_str)
    # print('user_data',user_data)
    token = user_data.get('token', None)
    _token = verify_auth_token(token)
    if _token == 'success':
        response = {
            'code': 0,
            'message': "验证成功",
            'token_message': _token,
        }
    else:
        response = DBUtil.checkUsers(user_data)
        if response['message'] == '验证成功':
            # token并没有验证通过,但账号密码验证通过则生成新的token
            new_token = generate_auth_token(user_data)
            response['token_message'] = _token
            response['token'] = new_token
    response['responseCode'] = 200
    # print('response',response)
    return jsonify(response)


########## Staff接口

# @app.route(apiPrefix + 'updateStaff', methods=['POST'])
# def updateStaff():
#     data = request.get_data(as_text=True)
#     re = DBUtil.addOrUpdateStaff(data)
#     # if re['code'] >= 0: # 数据保存成功，移动附件
#     #     FileUtil.fileMoveDir(re['id'])
#     return json.dumps(re)
#
#
# @app.route(apiPrefix + 'getStaffList/<int:job>')
# def getStaffList(job):
#     array = DBUtil.getStaffList(job)  # [('1', '1', '1', '1', '1'), ('1', '1', '2', '3', '4'), ...] 二维数组
#     jsonStaffs = DBUtil.getStaffsFromData(array)
#     # print("jsonStaffs:", jsonStaffs)
#     return json.dumps(jsonStaffs)
#
#
# @app.route(apiPrefix + 'deleteStaff/<int:id>')
# def deleteStaff(id):
#     # return str(id)+"hi"
#     re = DBUtil.deleteStaff(id)
#     return re
#
#
# @app.route(apiPrefix + 'searchStaff_3')
# def searchStaff_3():
#     data = request.args.get('where')
#     print('searchStaff_3:', data)
#     where = json.loads(data)
#     array = DBUtil.searchStaff_3(where)
#     jsonStaffs = DBUtil.getStaffsFromData_3(array)
#     re = json.dumps(jsonStaffs)
#     return re
#
#
# ########## 管理员接口
#
# @app.route(apiPrefix + 'checkPassword', methods=['POST'])
# def checkPassword():
#     data = request.get_data(as_text=True)
#     re = DBUtil.myCheck(data)
#     return json.dumps(re)
#
#
# @app.route(apiPrefix + 'gotoAdmin')  # 进入管理员状态
# def gotoAdmin(data):
#     pass
#
#
# @app.route(apiPrefix + 'export_to_file')  # 导出到文件
# def export_to_file():
#     array = DBUtil.getStaffList(0)  # [('1', '1', '1', '1', '1'), ('1', '1', '2', '3', '4'), ...] 二维数组
#     re = Data2File.saveToFile(array)
#     return json.dumps(re)


if __name__ == "__main__":
    app.run(debug=True, port=4999)

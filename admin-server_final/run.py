# coding=utf-8
import json
import configs
from flask import Flask,request, jsonify, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
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


########## 登陆接口
@app.route(apiPrefix + 'login', methods=['POST'], strict_slashes=False)
def login_user():
    json_str = request.get_data(as_text=True)
    user_data = json.loads(json_str)
    # print('user_data',user_data)
    token = user_data.get('token', None)
    _token = verify_auth_token(token)
    response = DBUtil.checkAdmins(user_data)
    if _token == 'success':
        response['token_message'] = _token
    elif response['message'] == '验证成功':
        # token并没有验证通过,但账号密码验证通过则生成新的token
        new_token = generate_auth_token(user_data)
        response['token_message'] = _token
        response['token'] = new_token
    response['responseCode'] = 200
    print('response',response)
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

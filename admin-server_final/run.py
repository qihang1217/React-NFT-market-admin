# coding=utf-8
import json
import math
import configs
from flask import Flask, request, jsonify, current_app
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
apiPrefix = '/api/admin/'


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
    response = DBUtil.check_admins(user_data)
    success_flag = False
    if _token == 'success':
        response['token_message'] = _token
        success_flag = True
    elif response['message'] == '验证成功':
        # token并没有验证通过,但账号密码验证通过则生成新的token
        new_token = generate_auth_token(user_data)
        response['token_message'] = _token
        response['token'] = new_token
        success_flag = True
    if success_flag:
        # 登陆成功
        # 获取用户数据中的role_id
        role_id = response.get('role_id')
        if role_id:
            # 查询其权限
            res = DBUtil.get_own_roles(role_id)
            response['data'][0]['role'] = json.loads(res['menus'])
        else:
            response['data'][0]['role'] = []
    # print('response',response)
    return jsonify(response)


########## NFT分页列表接口
@app.route(apiPrefix + 'manage/product/list', methods=['GET'], strict_slashes=False)
def get_product_list():
    args = request.args.to_dict()
    page_num = int(args.get('pageNum'))
    page_size = int(args.get('pageSize'))
    res, status = DBUtil.get_products()
    total = len(res)
    pages = math.ceil((total + page_size - 1) / page_size)
    data_dict = {'pageNum': page_num, 'pageSize': page_size, 'list': res, 'total': total, 'pages': pages}
    response = {
        'status': status,
        'data': data_dict,
    }
    return jsonify(response)


@app.route(apiPrefix + '/manage/product/search', methods=['GET'], strict_slashes=False)
def search_product_list():
    args = request.args.to_dict()
    print(args)
    page_num = int(args.get('pageNum'))
    page_size = int(args.get('pageSize'))
    search_name = ''
    search_type = ''
    for item in args.keys():
        if not item in ['pageSize', 'pageNum']:
            search_type = item
            search_name = args.get(item)
    res, status = DBUtil.search_products(search_type, search_name)
    # 数据总数
    total = len(res)
    # 向上去整,算出分页的页数
    pages = math.ceil((total + page_size - 1) / page_size)
    data_dict = {'pageNum': page_num, 'pageSize': page_size, 'list': res, 'total': total, 'pages': pages}
    response = {
        'status': status,
        'data': data_dict,
    }
    return jsonify(response)


@app.route(apiPrefix + '/manage/product/updateStatus', methods=['POST'], strict_slashes=False)
def update_product_status():
    json_str = request.get_data(as_text=True)
    req_data = json.loads(json_str)
    pass_status = req_data.get('pass_status')
    product_id = req_data.get('product_id')
    status = DBUtil.update_product_status(product_id, pass_status)
    response = {
        'status': status,
    }
    return jsonify(response)


@app.route(apiPrefix + 'manage/category/list', methods=['GET'], strict_slashes=False)
def get_category_list():
    res, status = DBUtil.get_categories()
    response = {
        'status': status,
        'data': res,
    }
    return jsonify(response)


@app.route(apiPrefix + '/manage/category/add', methods=['POST'], strict_slashes=False)
def add_category():
    json_str = request.get_data(as_text=True)
    req_data = json.loads(json_str)
    category_name = req_data.get('categoryName')
    res, status = DBUtil.add_category(category_name)
    response = {
        'status': status,
        'data': res,
    }
    return jsonify(response)


@app.route(apiPrefix + '/manage/category/update', methods=['POST'], strict_slashes=False)
def update_category():
    json_str = request.get_data(as_text=True)
    req_data = json.loads(json_str)
    category_id = req_data.get('categoryId')
    category_name = req_data.get('categoryName')
    status = DBUtil.update_category(category_id, category_name)
    response = {
        'status': status,
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, port=4999)

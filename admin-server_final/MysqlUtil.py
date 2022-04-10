# -*- coding:utf-8 -*-
import pymysql
from run import db

pymysql.install_as_MySQLdb()


# 单表查询的数据转换为dict,然后可以jsonfiy
def class_to_dict(obj):
    is_list = obj.__class__ == [].__class__
    is_set = obj.__class__ == set().__class__
    if is_list or is_set:
        obj_arr = []
        for o in obj:
            dict = {}
            a = o.__dict__
            if "_sa_instance_state" in a:
                del a['_sa_instance_state']
            dict.update(a)
            obj_arr.append(dict)
        return obj_arr
    else:
        dict = {}
        a = obj.__dict__
        if "_sa_instance_state" in a:
            del a['_sa_instance_state']
        dict.update(a)
        return dict


# {
#   "real_name": "1",
#   "id_number": "1",
#   "age": "1",
#   "email": "1",
#   "prefix": "86",
#   "phone_number": "1",
#   "gender": "男",
#   "user_name": "1",
#   "password": "tF0l/p7VDxtzFoAijp2kEQ==",
#   "confirm": "1",
#   "agreement": true,
#   "email_end": "@qq.com"
# }

class Users(db.Model):
    # 创建Users类，映射到数据库中叫Users表
    __tablename__ = "Users"
    # 创建字段： id， 主键和自增涨
    user_id = db.Column(db.Integer, primary_key=True)
    # 创建字段：username， 长度为20的字符串，不允许为空
    real_name = db.Column(db.String(20), nullable=False)
    # 创建字段：id_name， 长度为18的字符串，不允许为空
    id_number = db.Column(db.String(18), nullable=False)
    # 创建字段：age，整数，不允许为空
    age = db.Column(db.Integer, nullable=False)
    # 创建字段：email，长度为30的字符串，不允许为空
    email = db.Column(db.String(30), nullable=False)
    # 创建字段：phone_number， 长度为20的字符串，不允许为空
    phone_number = db.Column(db.String(20), nullable=False)
    # 创建字段：gender， 长度为20的字符串，不允许为空
    gender = db.Column(db.String(2), nullable=False)
    # 创建字段：user_name， 长度为20的字符串，不允许为空,不可重复
    user_name = db.Column(db.String(20), nullable=False, unique=True)
    # 创建字段：password，长度为44的字符串(存储加密后的密码)，不允许为空
    password = db.Column(db.String(44), nullable=False)


class Products(db.Model):
    # 创建Roles类，映射到数据库中叫Roles表
    __tablename__ = "Products"
    # 创建字段： role_id， 主键和自增涨
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(20))
    owner_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    price = db.Column(db.Integer)
    pass_status = db.Column(db.Boolean)
    file_url = db.Column(db.String(100))
    description = db.Column(db.Text)


class Roles(db.Model):
    # 创建Roles类，映射到数据库中叫Roles表
    __tablename__ = "Roles"
    # 创建字段： role_id， 主键和自增涨
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20), unique=True)
    auth_name = db.Column(db.String(20))
    menus = db.Column(db.String(100))


class Admins(db.Model):
    # 创建Users类，映射到数据库中叫Users表
    __tablename__ = "Admins"
    # 创建字段： admin_id， 主键和自增涨
    admin_id = db.Column(db.Integer, primary_key=True)
    # 创建字段：admin_name， 长度为20的字符串，不允许为空,不可重复
    admin_name = db.Column(db.String(20), nullable=False, unique=True)
    # 创建字段：password，长度为44的字符串(存储加密后的密码)，不允许为空
    password = db.Column(db.String(44), nullable=False)
    # 创建字段：role_id，长度为5的字符串
    role_id = db.Column(db.Integer, db.ForeignKey('Roles.role_id'))


# 将创建好的实体类映射回数据库
db.create_all()

# 初始化一个admin账户
res = db.session.query(Admins).filter(Admins.admin_name == 'admin').all()
db.session.commit()
if len(res) == 0:
    use = Admins(admin_name='admin', password='ApUghu4n1mNSqH2grfnHUw==')
    db.session.add(use)
    db.session.commit()

# staffColumns = ("id", "service", "money", "card_number", "name", "phone", "project", \
#                 "shop_guide", "teacher", "financial", "remarks1", "collect_money", "remarks2")  # id没写可把我害惨了

AdminColumns = ("id", "user_name", "password")


def check_admins(admin_data):
    # 验证密码是否正确
    try:
        res = db.session.query(Admins).filter(Admins.admin_name == admin_data['user_name']).all()
        db.session.commit()
        if len(res) == 0:
            re = {
                'status': -1,
                'message': "用户不存在"
            }
        else:
            if admin_data["password"] == res[0].password:
                # 验证成功
                re = {
                    'status': 0,
                    'message': "验证成功",
                    'data': class_to_dict(res)
                }
            else:
                re = {
                    'status': -1,
                    'message': "验证失败"
                }
            return re
        return re
    except Exception as e:
        # print(repr(e))
        re = {
            'status': -1,
            'message': repr(e)
        }
        return re
    finally:
        db.session.close()


def get_own_roles(role_id):
    try:
        res = db.session.query(Roles).fileter(Roles.role_id == role_id).all()
        return class_to_dict(res)
    except Exception as e:
        print(repr(e))
    finally:
        db.session.close()


def get_products():
    try:
        return class_to_dict(db.session.query(Products).all()), 0
    except Exception as e:
        print(repr(e))
        return [{}], -1
    finally:
        db.session.close()


def search_products(search_type,search_name):
    try:
        if search_type=='productName':
            return class_to_dict(db.session.query(Products).filter(Products.product_name.contains(search_name)).all()), 0
        if search_type=='productDesc':
            return class_to_dict(db.session.query(Products).filter(Products.description.contains(search_name)).all()), 0
    except Exception as e:
        print(repr(e))
        return [{}], -1
    finally:
        db.session.close()


def update_product_status(product_id, pass_status):
    try:
        print(pass_status)
        print(type(pass_status))
        db.session.query(Products).filter(Products.product_id == product_id).update({'pass_status': pass_status})
        db.session.commit()
        return 0
    except Exception as e:
        print(repr(e))
        return -1
    finally:
        db.session.close()

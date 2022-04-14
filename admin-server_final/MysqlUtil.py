# -*- coding:utf-8 -*-
import pymysql
from sqlalchemy import and_

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


# 查询结果转换成json
class MixToJson:
    # 查询单条数据
    def single_to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # 多条数据
    def double_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result

    # 配合double_to_dict一起使用
    @staticmethod
    def to_json(all_vendors):
        v = [ven.dobule_to_dict() for ven in all_vendors]
        return v


class Users(db.Model, MixToJson):
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


class Categories(db.Model, MixToJson):
    # 创建Categories类，映射到数据库中叫Categories表
    __tablename__ = "Categories"
    # 创建字段： role_id， 主键和自增涨
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(20), unique=True)


class Products(db.Model, MixToJson):
    # 创建Roles类，映射到数据库中叫Roles表
    __tablename__ = "Products"
    # 创建字段： role_id， 主键和自增涨
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(20))
    owner_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    price = db.Column(db.Integer)
    # 通过状态.是否通过审核
    pass_status = db.Column(db.Boolean, default=False)
    # 审核状态,是否已经审核
    examine_status = db.Column(db.Boolean, default=False)
    # 用户有一次重复提交的机会
    usable_chances = db.Column(db.Integer, default=2)
    # 防止文件名可能的重复
    file_url = db.Column(db.String(30), unique=True)
    file_type = db.Column(db.String(100))
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('Categories.category_id'))


class Roles(db.Model, MixToJson):
    # 创建Roles类，映射到数据库中叫Roles表
    __tablename__ = "Roles"
    # 创建字段： role_id， 主键和自增涨
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20), unique=True)
    auth_name = db.Column(db.String(20))
    menus = db.Column(db.String(100))


class Admins(db.Model, MixToJson):
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
    user = Admins(admin_name='admin', password='ApUghu4n1mNSqH2grfnHUw==')
    db.session.add(user)
    db.session.commit()

# 初始化分类
res = db.session.query(Categories).all()
db.session.commit()
if len(res) == 0:
    Category1 = Categories(category_name='绘画')
    Category2 = Categories(category_name='书法')
    Category3 = Categories(category_name='文献')
    Category4 = Categories(category_name='票券')
    Category5 = Categories(category_name='商标')
    Category6 = Categories(category_name='邮票')
    Category7 = Categories(category_name='雕塑')
    Category8 = Categories(category_name='摄影')
    db.session.add_all([Category1, Category2, Category3, Category4, Category5, Category6, Category7, Category8])
    db.session.commit()

# staffColumns = ("id", "service", "money", "card_number", "name", "phone", "project", \
#                 "shop_guide", "teacher", "financial", "remarks1", "collect_money", "remarks2")  # id没写可把我害惨了

AdminColumns = ("id", "user_name", "password")


def check_admins(admin_data):
    # 验证密码是否正确
    try:
        res = Admins.query.filter(Admins.admin_name == admin_data['user_name']).all()
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
        res = Roles.query.fileter(Roles.role_id == role_id).all()
        return class_to_dict(res)
    except Exception as e:
        print(repr(e))
    finally:
        db.session.close()


def get_products():
    try:
        return class_to_dict(Products.query.filter(Products.usable_chances >= 1).all()), 0
    except Exception as e:
        print(repr(e))
        return [{}], -1
    finally:
        db.session.close()


def search_products(search_type, search_name):
    try:
        if search_name != '':
            # 对于查询结果进行筛选,不返回usable_chances为0的数据(正常情况下都不再返回该类数据,伪删除)
            if search_type == 'productStatus':
                if search_name == '通过':
                    search_name = 1
                elif search_name == '不通过':
                    search_name = 0
                return class_to_dict(
                    Products.query.filter(
                        and_(Products.pass_status == search_name, Products.usable_chances >= 1)).all()), 0
            elif search_type == 'examineStatus':
                if search_name == '已审核':
                    search_name = 1
                elif search_name == '未审核':
                    search_name = 0
                return class_to_dict(
                    Products.query.filter(
                        and_(Products.examine_status == search_name, Products.usable_chances >= 1)).all()), 0
            elif search_type == 'productName':
                return class_to_dict(
                    Products.query.filter(
                        and_(Products.product_name.contains(search_name), Products.usable_chances >= 1)).all()), 0
            elif search_type == 'productDesc':
                return class_to_dict(Products.query.filter(
                    and_(Products.description.contains(search_name), Products.usable_chances >= 1)).all()), 0
        else:
            # 搜索词为空时不进行筛选,返回整个结果
            return class_to_dict(Products.query.all()), 0
    except Exception as e:
        print(repr(e))
        return [{}], -1
    finally:
        db.session.close()


def update_product_status(product_id, pass_status):
    try:
        Products.query.filter(Products.product_id == product_id).update(
            {'pass_status': pass_status, 'examine_status': True})
        product = Products.query.filter(Products.product_id == product_id)
        # 当nft可审核次数大于0
        if product.usable_chances >= 1 and product.examine_status==0:
            product.usable_chances = product.usable_chances - 1
        else:
            # 当nft可审核次数为0时,不可再次修改其状态
            return -1
        db.session.commit()
        return 0
    except Exception as e:
        print(repr(e))
        return -1
    finally:
        db.session.close()


def get_categories():
    try:
        return class_to_dict(Categories.query.all()), 0
    except Exception as e:
        print(repr(e))
        return [{}], -1
    finally:
        db.session.close()


def add_category(category_name):
    try:
        Category = Categories(category_name=category_name)
        db.session.add(Category)
        db.session.commit()
        return class_to_dict(Categories.query.filter(Categories.category_name == category_name).all()), 0
    except Exception as e:
        print(repr(e))
        return [{}], -1
    finally:
        db.session.close()


def update_category(category_id, category_name):
    try:
        Categories.query.filter(Categories.category_id == category_id).update({'category_name': category_name})
        db.session.commit()
        return 0
    except Exception as e:
        print(repr(e))
        return -1
    finally:
        db.session.close()


def get_category_by_id(category_id):
    try:
        res = Categories.query.filter(Categories.category_id == category_id).first()
        db.session.commit()
        return res.single_to_dict(), 0
    except Exception as e:
        print(repr(e))
        return [{}], -1
    finally:
        db.session.close()


def get_product_by_id(product_id):
    try:
        res = Products.query.filter(Products.product_id == product_id).first()
        db.session.commit()
        return res.single_to_dict(), 0
    except Exception as e:
        print(repr(e))
        return [{}], -1
    finally:
        db.session.close()

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

# 创建模型类 - Models
class Admins(db.Model):
    # 创建Users类，映射到数据库中叫Users表
    __tablename__ = "Admins"
    # 创建字段： id， 主键和自增涨
    id = db.Column(db.Integer, primary_key=True)
    # 创建字段：admin_name， 长度为20的字符串，不允许为空,不可重复
    admin_name = db.Column(db.String(20), nullable=False, unique=True)
    # 创建字段：password，长度为44的字符串(存储加密后的密码)，不允许为空
    password = db.Column(db.String(44), nullable=False)


# 将创建好的实体类映射回数据库
# db.create_all()


# staffColumns = ("id", "service", "money", "card_number", "name", "phone", "project", \
#                 "shop_guide", "teacher", "financial", "remarks1", "collect_money", "remarks2")  # id没写可把我害惨了

AdminColumns = ("id","user_name", "password")


def checkAdmins(admin_data):
    # 验证密码是否正确
    try:
        res = db.session.query(Admins).filter(Admins.admin_name == admin_data['user_name']).all()
        db.session.commit()
        if len(res) == 0:
            re = {
                'code': -1,
                'message': "用户不存在"
            }
        else:
            print('+'*30,res[0])
            if admin_data["password"] == res[0].password:
                # 验证成功
                re = {
                    'code': 0,
                    'message': "验证成功",
                    'data':class_to_dict(res[0])
                }
            else:
                re = {
                    'code': -1,
                    'message': "验证失败"
                }
            return re
    except Exception as e:
        print(repr(e))
        re = {
            'code': -1,
            'message': repr(e)
        }
        return re
    finally:
        db.session.close()
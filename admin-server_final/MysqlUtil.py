# -*- coding:utf-8 -*-
import pymysql
from run import db

pymysql.install_as_MySQLdb()


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
class Users(db.Model):
    # 创建Users类，映射到数据库中叫Users表
    __tablename__ = "Users"
    # 创建字段： id， 主键和自增涨
    id = db.Column(db.Integer, primary_key=True)
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
    # 创建字段：password，长度为50的字符串，不允许为空
    password = db.Column(db.String(44), nullable=False)


# 将创建好的实体类映射回数据库
# db.create_all()


staffColumns = ("id", "service", "money", "card_number", "name", "phone", "project", \
                "shop_guide", "teacher", "financial", "remarks1", "collect_money", "remarks2")  # id没写可把我害惨了

staffColumns = ("id", "real_name", "id_name", "age", "email", "phone_number", "gender", "user_name", "password")


def addOrUpdateUsers(user_data):
    try:
        # 获取用户id,没有则赋为0
        id = user_data.get('id', 0)
        result = ''
        new_id = id
        perfix = user_data.get('prefix')
        email_end = user_data.get('email_end')
        # 删除与数据库无关的字段
        del user_data['confirm']
        del user_data['agreement']
        # 插入
        if id == 0:
            # 防止用户名重复
            res = db.session.query(Users).filter(Users.user_name == user_data['user_name']).all()
            db.session.commit()
            if len(res) == 0:
                keys = ''
                values = ''
                isFirst = True

                for key, value in user_data.items():
                    # 组装成正确的phone_number
                    if key == 'prefix':
                        continue
                    if key == 'phone_number':
                        value = perfix + '-' + value
                    # 组装成正确的email
                    if key == 'email_end':
                        continue
                    if key == 'email':
                        value = value + email_end
                    if isFirst:
                        isFirst = False
                    else:
                        keys += ','
                        values += ','
                    keys += key
                    if isinstance(value, str):
                        values += ("'%s'" % value)
                    else:
                        values += str(value)

                sql = "INSERT INTO Users (%s) values (%s)" % (keys, values)
                # print(sql)
                result = db.session.execute(sql)
                db.session.commit()
                # 获取插入数据后的主键id
                new_id = result.lastrowid
                result = '添加成功'
                # print(result)
            else:
                result = '用户名重复'
        else:
            # 修改
            update = ''
            isFirst = True
            for key, value in user_data.items():
                if key == 'id':
                    # 这个字段不用考虑，隐藏的
                    continue
                if isFirst:
                    isFirst = False
                else:
                    update += ','  # 相当于除了第一个，其他的都需要在最前面加','
                if value == None:
                    value = ""
                if isinstance(value, str):
                    update += (key + "='" + value + "'")
                else:
                    update += (key + "=" + str(value))
            where = "where id=" + str(id)
            sql = "update t_staff set %s %s" % (update, where)
            # print("=="*30)
            print(sql)
            db.session.execute(sql)
            db.session.commit()
            result = '更新成功'
            print(result)
        re = {
            'code': 0,
            'id': new_id,
            'message': result
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


def checkUserNameRepeat(user_data):
    # 防止用户名重复
    res = db.session.query(Users).filter(Users.user_name == user_data['user_name']).all()
    db.session.commit()
    if len(res) == 0:
        result = '用户名不重复'
    else:
        result = '用户名重复'
    re = {
        'code': 0,
        'message': result
    }
    db.session.close()
    return re


def checkUsers(user_data):
    # 验证密码是否正确
    try:
        res = db.session.query(Users).filter(Users.user_name == user_data['user_name']).all()
        db.session.commit()
        if len(res) == 0:
            re = {
                'code': -1,
                'message': "用户不存在"
            }
        else:
            # print(res[0])
            if user_data["password"] == res[0].password:
                # 验证成功
                re = {
                    'code': 0,
                    'message': "验证成功"
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

def checkUsers(user_data):
    # 验证密码是否正确
    try:
        res = db.session.query(Users).filter(Users.user_name == user_data['user_name']).all()
        db.session.commit()
        if len(res) == 0:
            re = {
                'code': -1,
                'message': "用户不存在"
            }
        else:
            # print(res[0])
            if user_data["password"] == res[0].password:
                # 验证成功
                re = {
                    'code': 0,
                    'message': "验证成功"
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

# def deleteStaff(id):
#     #根据staff的id号来删除该条记录
#     try:
#         sql = "delete from t_staff where id=%d" % (id)
#         print(sql)
#         cursor.execute(sql)
#         conn.commit()
#         re = {
#             'code':0,
#             'message':'删除成功',
#         }
#         return json.dumps(re)
#     except Exception as e:
#         re = {
#             'code': -1,
#             'message': repr(e)
#         }
#         return json.dumps(re)
#
# def getStaffList(job):
#     # 当job为0时，表示获取所有数据
#     tableName = 't_staff'
#     where = ''
#
#     columns = ','.join(staffColumns)
#     order = ' order by id desc'  #按照id的递减顺序排列，之后要改
#     sql = "select %s from %s%s%s" % (columns, tableName, where, order)
#     print(sql)
#
#     cursor.execute(sql)
#
#     dateList = cursor.fetchall()     # fetchall() 获取所有记录
#     return dateList
#
# def searchStaff_3(where):
#     #只搜索3个属性
#     try:
#         sql_where = ''
#         sql_like = ''
#
#         if where.get('job', 0) > 0:
#             sql_where = ("where job=" + str(where['job']))
#
#         where_like_items = []
#         for key, value in where.items():
#             if value=="":
#                 #如果为空的话，就不把该字段计入了
#                 continue
#             if isinstance(value, str) and len(value.strip()) > 0:
#                 where_item = (key + " like '%" + value + "%'")
#                 where_like_items.append(where_item)
#
#         if len(where_like_items) > 0:
#             sql_like = "(%s)" % ' or '.join(where_like_items)
#
#         if len(sql_where) > 0:
#             if len(sql_like) > 0:
#                 sql_where += (" and " + sql_like)
#         else:
#             if len(sql_like) > 0:
#                 sql_where = "where " + sql_like
#
#         my_tmp_staffColumns = ("card_number", "name", "phone")
#         columns = ','.join(my_tmp_staffColumns)
#         order = ' order by id desc'
#         sql = "select %s from t_staff %s%s" % (columns, sql_where, order)
#         print(sql)
#
#         cursor.execute(sql)
#
#         dateList = cursor.fetchall()     # fetchall() 获取所有记录
#         return dateList
#     except Exception as e:
#         print(repr(e))
#         return []
#
# def getStaffsFromData_3(dataList):
#     #只取第一条数据，因为只想获得"card_number", "name", "phone"
#     itemArray = dataList[0] if dataList else None
#     # print("itemArray:",itemArray)  #itemArray: ('1', '1', '12')
#     return itemArray
#
# def getStaffsFromData(dataList):
#     staffs = []
#     for itemArray in dataList:   # dataList数据库返回的数据集，是一个二维数组
#         #itemArray: ('1', '1', '2', '3', '4')
#         staff = {}
#         for columnIndex, columnName in enumerate(staffColumns):
#             columnValue = itemArray[columnIndex]
#             # if columnValue is None: #后面remarks要用，现在不需要
#             #     columnValue = 0 if columnName in (
#             #         'job', 'education', 'birth_year') else ''
#             staff[columnName] = columnValue
#
#         staffs.append(staff)
#
#     return staffs
#
# def toMd5(data):
#     #采用md5加密
#     return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()
#

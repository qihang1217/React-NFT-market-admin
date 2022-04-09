# 数据库部分
USERNAME = 'root'
PASSWORD = 'root'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'nft_market'
DB_URI = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8" % (USERNAME, PASSWORD, HOST, PORT, DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True


# token部分
COOKIE_EXPIRATION = 30 * 24 * 3600  # 秒（到期浏览器自动删除）
TOKEN_EXPIRATION = 30 * 24 * 3600  # 秒（到期报错SignatureExpired）
SECRET_KEY = 'Q#6@i%8)H'

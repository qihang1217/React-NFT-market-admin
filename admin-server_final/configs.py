# ���ݿⲿ��
USERNAME = 'root'
PASSWORD = 'root'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'nft_market'
DB_URI = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8" % (USERNAME, PASSWORD, HOST, PORT, DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True


# token����
COOKIE_EXPIRATION = 30 * 24 * 3600  # �루����������Զ�ɾ����
TOKEN_EXPIRATION = 30 * 24 * 3600  # �루���ڱ���SignatureExpired��
SECRET_KEY = 'Q#6@i%8)H'

CSRF_ENABLED = True  # 激活跨站点请求伪造保护
SECRET_KEY = 'stn-boo'

# 配置flask_sqlalchemy
username = 'root'
password = 'root'
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + username + ':' + password + '@localhost:3306/api?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = True
JSON_AS_ASCII = False
JSON_SORT_KEYS = False

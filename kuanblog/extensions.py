'''
@Author: your name
@Date: 2020-01-30 23:47:10
@LastEditTime : 2020-02-01 00:06:37
@LastEditors  : Please set LastEditors
@Description: In User Settings Edit
@FilePath: \11.宽的博客\kuanblog\extensions.py
'''
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


# 就可以使用current_user了
@login_manager.user_loader
def load_user(user_id):
    from kuanblog.models import Admin
    user = Admin.query.get(int(user_id))
    return user
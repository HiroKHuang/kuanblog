'''
@Author: your name
@Date: 2020-01-30 23:27:21
@LastEditTime : 2020-02-01 00:07:09
@LastEditors  : Please set LastEditors
@Description: In User Settings Edit
@FilePath: \11.宽的博客\kuanblog\__init__.py
'''
import os
# 导入Flask类，用于构造实例
from flask import Flask
# 导入蓝本实例
from kuanblog.blueprints.blog import blog_bp
from kuanblog.blueprints.admin import admin_bp

# 导入配置
from kuanblog.settings import config
# 导入扩展
from kuanblog.extensions import bootstrap, db, login_manager, csrf
from kuanblog.commands import register_commands
from kuanblog.models import Admin, Category

def create_app(config_name=None):
    # 加载配置
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    
    app = Flask('kuanblog')
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_shell_context(app)
    register_template_context(app)

    # 返回实例
    return app


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)

# 模板上下文
def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        return dict(admin=admin, categories=categories)
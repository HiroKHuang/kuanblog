'''
@Author: your name
@Date: 2020-01-30 23:33:57
@LastEditTime : 2020-01-31 16:30:06
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \11.宽的博客\kuanblog\settinfs.py
'''

import os

# 获取根目录的绝对地址
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# 配置一般设置两个东西：1.SECRET_KEY。2.SQLALCHEMY_DATABASE_URI和SQLALCHEMY_TRACK_MODIFICATIONS

class BaseConfig(object):
    # 意思是从环境变量获取SECRET_KEY的值，若没找到则使用‘secret string'
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 设置每个地方显示的项目数，多了则翻页。
    KUANBLOG_PER_PAGE = 10
    KUANBLOG_MANAGE_PER_PAGE = 15
    KUANBLOG_COMMENT_PER_PAGE = 15

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.db')

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'data.db'))

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

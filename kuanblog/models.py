'''
@Author: your name
@Date: 2020-01-30 23:53:55
@LastEditTime : 2020-01-31 23:17:05
@LastEditors  : Please set LastEditors
@Description: In User Settings Edit
@FilePath: \11.宽的博客\kuanblog\models.py
'''
from kuanblog.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

    # 与文章建立一对多关系
    articles = db.relationship("Article", back_populates="category")

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # 与分类建立多对一关系
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = db.relationship("Category", back_populates="articles")

    # 与评论建立一对多关系
    # db.relationship("对方的类名", back_populates="自己的关系名"（用于对方建立关系时的变量）)
    comments = db.relationship("Comment", back_populates="article", cascade="all, delete-orphan")

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # 与文章建立多对一关系
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    article = db.relationship("Article", back_populates="comments")

    # 评论内部建立邻接关系(还不是很懂)
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replied = db.relationship("Comment", back_populates="replies", remote_side=[id])
    replies = db.relationship("Comment", back_populates="replied", cascade="all")
'''
@Author: your name
@Date: 2020-01-31 08:43:39
@LastEditTime : 2020-01-31 22:15:11
@LastEditors  : Please set LastEditors
@Description: In User Settings Edit
@FilePath: \11.宽的博客\kuanblog\fakes.py
'''
from faker import Faker
import random
from kuanblog.models import Admin, Category, Article, Comment
from kuanblog.extensions import db

# 生成虚拟的文章分类
fake = Faker()

def fake_category(count=10):
    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

# 生成虚拟文章
def fake_articles(count=50):
    for i in range(count):
        article = Article(
            title = fake.sentence(),
            body = fake.text(2000),
            category = Category.query.get(random.randint(1, Category.query.count())),
            timestamp = fake.date_time_this_year()
        )
        db.session.add(article)
    db.session.commit()

# 生成虚拟评论
def fake_comments(count=500):
    for i in range(count):
        comment = Comment(
            author = fake.name(),
            body = fake.sentence(),
            timestamp = fake.date_time_this_year(),
            article = Article.query.get(random.randint(1, Article.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    salt = int(count*0.1)
    # 生成回复的回复
    for i in range(salt):
        comment = Comment(
            author = fake.name(),
            body = fake.sentence(),
            timestamp = fake.date_time_this_year(),
            replied = Comment.query.get(random.randint(1, Comment.query.count())),
            article = Article.query.get(random.randint(1, Article.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

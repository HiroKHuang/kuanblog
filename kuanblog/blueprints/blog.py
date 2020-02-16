'''
@Author: your name
@Date: 2020-01-30 23:24:27
@LastEditTime : 2020-02-01 12:25:00
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \11.宽的博客\kuanblog\blueprints\blog.py
'''
# 从flask中导入蓝本类
from flask import Blueprint
from flask import url_for, render_template, request, current_app
from kuanblog.models import Article, Category, Article

# 创建蓝本实例，第一个参数是蓝本名称，第二个传入块的名称
blog_bp = Blueprint("blog", __name__)

@blog_bp.route("/")
def index():
    # 从查询字符串获取当前页数
    page = request.args.get("page", 1, type=int)
    # 从配置中获取每页的数量
    per_page = current_app.config["KUANBLOG_PER_PAGE"]
    # 查询后使用paginate方法，第一个参数传入页数，第二个参数传入每页项目数
    pagination = Article.query.order_by(Article.timestamp.desc()).paginate(page, per_page=per_page)
    articles = pagination.items
    return render_template("blog/index.html", pagination=pagination, articles=articles)

@blog_bp.route("/about")
def about():
    return render_template("blog/about.html")

@blog_bp.route("/category/<int:category_id>")
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config["KUANBLOG_PER_PAGE"]
    pagination = Article.query.with_parent(category).order_by(Article.timestamp.desc()).paginate(page, per_page)
    articles = pagination.items
    return render_template('blog/category.html', category=category, pagination=pagination, articles=articles)

@blog_bp.route("/article/<int:article_id>")
def show_article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template("blog/article.html", article=article)

    
'''
@Author: your name
@Date: 2020-01-31 11:42:58
@LastEditTime : 2020-02-01 12:27:58
@LastEditors  : Please set LastEditors
@Description: In User Settings Edit
@FilePath: \11.宽的博客\kuanblog\blueprints\admin.py
'''
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from kuanblog.forms import LoginForm, ArticleForm, CategoryForm
from flask_login import login_user, current_user, logout_user, login_required
from kuanblog.models import Admin, Article, Category
from kuanblog.utils import redirect_back
from kuanblog.extensions import db


admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash("欢迎登录", "success")
                return redirect_back() # 返回上一个页面
            else:
                flash("密码或用户名错误", "warning")
        else:
            flash("没有设置管理员账号", "warning")
    return render_template('admin/login.html', form=form)

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("已登出用户", "info")
    return redirect_back()
    
@admin_bp.route('/article/manage')
@login_required
def manage_article():
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config['KUANBLOG_MANAGE_PER_PAGE']
    pagination = Article.query.order_by(Article.timestamp.desc()).paginate(page, per_page)
    articles = pagination.items
    return render_template('admin/manage_article.html', pagination=pagination, articles=articles)


@admin_bp.route('/article/<int:article_id>/delete')
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    flash("已删除文章", "success")
    return redirect_back()

@admin_bp.route('/article/<int:article_id>/edit', methods=["GET", "POST"])
@login_required
def edit_article(article_id):
    form = ArticleForm()
    article = Article.query.get_or_404(article_id)
    if form.validate_on_submit():
        article.title = form.title.data
        article.body = form.body.data
        article.category = Category.query.get(form.category.data)
        db.session.commit()
        flash("已完成文章的修改", "success")
        return redirect(url_for('admin.manage_article'))
    form.title.data = article.title
    form.body.data = article.body
    # 这个要注意下，我们只用了id就渲染出了对应的名称
    form.category.data = article.category_id
    return render_template('admin/edit_article.html', form=form)

@admin_bp.route('article/new', methods=["GET","POST"])
@login_required
def new_article():
    form = ArticleForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        article = Article(title=title, body=body, category=category)
        db.session.add(article)
        db.session.commit()
        flash('已新建一篇文章', 'success')
        return redirect(url_for(".manage_article"))
    return render_template('admin/new_article.html', form=form)

@admin_bp.route('/category/manage')
@login_required
def manage_category():
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config['KUANBLOG_MANAGE_PER_PAGE']
    pagination = Category.query.order_by(Category.name.asc()).paginate(page, per_page)
    categories = pagination.items
    return render_template('admin/manage_category.html', pagination=pagination, categories=categories)

@admin_bp.route('category/new', methods=["GET","POST"])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('已创建新类别', 'success')
        return redirect(url_for(".manage_category"))
    return render_template('admin/new_category.html', form=form)

@admin_bp.route("/category/<int:category_id>/delete")
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash("已删除类别", "success")
    return redirect_back()

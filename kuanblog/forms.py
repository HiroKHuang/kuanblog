'''
@Author: your name
@Date: 2020-01-31 11:33:46
@LastEditTime : 2020-02-01 08:23:35
@LastEditors  : Please set LastEditors
@Description: In User Settings Edit
@FilePath: \11.宽的博客\kuanblog\forms.py
'''
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length
from kuanblog.models import Category

class LoginForm(FlaskForm):
    username = StringField('用户名：', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码：', validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')
    
class ArticleForm(FlaskForm):
    title = StringField("文章标题", validators=[DataRequired(),Length(1,60)])
    category = SelectField("文章类别", coerce=int, default=1)
    body = CKEditorField("文章内容", validators=[DataRequired()])
    submit = SubmitField()
    
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, *kwargs)
        self.category.choices = [(category.id, category.name) for category in Category.query.order_by(Category.name).all()]
            
class CategoryForm(FlaskForm):
    name = StringField("文章类别", validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()
    
    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError("已有该文章类别")
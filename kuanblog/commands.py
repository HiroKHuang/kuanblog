'''
@Author: your name
@Date: 2020-01-31 09:18:10
@LastEditTime : 2020-01-31 22:17:00
@LastEditors  : Please set LastEditors
@Description: In User Settings Edit
@FilePath: \11.宽的博客\kuanblog\commands.py
'''
import click
from kuanblog.extensions import db
from kuanblog.models import Admin


def register_commands(app):
    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--article', default=50, help='Quantity of articles, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500')
    def forge(category, article, comment):
    
        from kuanblog.fakes import fake_category, fake_articles, fake_comments
        db.drop_all()
        db.create_all()

        click.echo('Generating %d categories...' % category)
        fake_category()

        click.echo('Generating %d articles' % article)
        fake_articles()

        click.echo('Generating %d comments' % comment)
        fake_comments()

        click.echo('Done')
    
    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        click.echo('Initializing the database...')
        db.create_all()
        
        admin = Admin.query.first()
        if admin:
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo("Creating the temporary administrator account...")
            admin = Admin(
                username = username,
            )
            admin.set_password(password)
            db.session.add(admin)
            
        db.session.commit()
        click.echo('Done')
            
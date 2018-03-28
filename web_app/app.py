from flask import Flask, render_template
from flask_admin import Admin

from web_app.views import PageModelView, MenuModelView


def create_app():

    flask_objek = Flask(__name__)

    flask_objek.config.from_pyfile('settings.py')

    from web_app.models import database, Page, Menu

    database.init_app(flask_objek)

    admin = Admin(flask_objek, name='Administrator', template_mode='bootstrap3')
    admin.add_view(PageModelView(Page, database.session))
    admin.add_view(MenuModelView(Menu, database.session))


    @flask_objek.route('/')
    def index():

        return render_template('index.html')

    return flask_objek

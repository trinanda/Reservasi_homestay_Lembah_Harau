from flask import Flask, render_template
from flask_admin import Admin

from web_app.views import PageModelView, MenuModelView, ImageView


def create_app():

    flask_objek = Flask(__name__, static_folder='files')

    flask_objek.config.from_pyfile('settings.py')

    from web_app.models import database, Page, Menu, Image

    database.init_app(flask_objek)

    admin = Admin(flask_objek, name='Administrator', template_mode='bootstrap3')
    admin.add_view(PageModelView(Page, database.session))
    admin.add_view(MenuModelView(Menu, database.session))
    admin.add_view(ImageView(Image, database.session))

    @flask_objek.route('/')
    @flask_objek.route('/<uri>')
    def index(uri=None):
        page = Page()
        print('yang di tes ini', uri)
        if uri is not None:
            page = Page.query.filter_by(url=uri).first()
        else:
            pass

        konten = 'Homepage'
        if page is not None:
            konten = page.konten

        menu = Menu.query.order_by('urutan')

        return render_template('index.html', CONTENT=konten, menu=menu)

    return flask_objek

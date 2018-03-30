from flask import Flask, render_template
from flask_admin import Admin

from web_app.views import PageModelView, MenuModelView, PilihKamarView


def create_app():

    flask_objek = Flask(__name__, static_folder='files')

    flask_objek.config.from_pyfile('settings.py')

    from web_app.models import database, Page, Menu, PilihKamar

    database.init_app(flask_objek)

    admin = Admin(flask_objek, name='Administrator', template_mode='bootstrap3')
    admin.add_view(PageModelView(Page, database.session))
    admin.add_view(MenuModelView(Menu, database.session))
    admin.add_view(PilihKamarView(PilihKamar, database.session))


    @flask_objek.route('/')
    @flask_objek.route('/<uri>')
    def index(uri=None):
        page = Page()
        if uri is not None:
            page = Page.query.filter_by(url=uri).first()
        else:
            pass

        konten = 'Homepage'
        if page is not None:
            konten = page.konten

        menu = Menu.query.order_by('urutan')

        return render_template('index.html', CONTENT=konten, menu=menu)


    @flask_objek.route('/penginapan')
    def product(uri=None):
        kamar = PilihKamar()
        if uri is not None:
            kamar = kamar.query.filter_by(id=1).first()
        else:
            pass

        if kamar is not None:
            nama_kamar = kamar.nama_kamar
            harga_kamar = kamar.harga_kamar
            foto_kamar = kamar.path

        return render_template('penginapan.html', NAMA_KAMAR=nama_kamar, HARGA_KAMAR=harga_kamar, FOTO_KAMAR=foto_kamar)


    return flask_objek

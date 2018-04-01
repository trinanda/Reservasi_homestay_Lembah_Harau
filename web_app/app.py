from flask import Flask, render_template
from flask_admin import Admin

from web_app.views import PageModelView, MenuModelView, PilihKamarView


def create_app():

    flask_objek = Flask(__name__, static_folder='files')

    flask_objek.config.from_pyfile('settings.py')

    from web_app.models import database, Page, Menu, Kamar
    database.init_app(flask_objek)

    admin = Admin(flask_objek, name='Administrator', template_mode='bootstrap3')
    admin.add_view(PageModelView(Page, database.session))
    admin.add_view(MenuModelView(Menu, database.session))
    admin.add_view(PilihKamarView(Kamar, database.session))


    @flask_objek.route('/')
    @flask_objek.route('/<uri>')
    def index(uri=None):
        page = Page()
        if uri is not None:
            page = Page.query.filter_by(url=uri).first()
        else:
            pass

        konten = 'Homepage!!!'
        if page is not None:
            konten = page.konten

        menu = Menu.query.order_by('urutan')

        return render_template('index.html', CONTENT=konten, MENU=menu)


    @flask_objek.route('/penginapan')
    @flask_objek.route('/<uri>')
    def kamar(uri=None, room=None):
        page = Page()
        if uri is not None:
            page = Page.query.filter_by(url=uri).first()
        else:
            pass

        konten = 'Homepage'
        if page is not None:
            konten = page.konten

        menu = Menu.query.order_by('urutan')

        kamar = Kamar()
        if room is not None:
            kamar = Kamar.query.filter_by(nama_kamar=room).first()
        else:
            pass

        room_foto = Kamar.query.first()
        room_foto = room_foto.path
        print('coba tes pat ini', room_foto)

        bedroom_name = "bedroom"
        room_price = "price"
        room_foto = 'foto kamar nya gimana..?'
        if kamar is not None:
            room_price = Kamar.query.first()
            room_price = room_price.harga_kamar
            bedroom_name = Kamar.query.first()
            bedroom_name = bedroom_name.nama_kamar
            room_foto = Kamar.query.first()
            room_foto = room_foto.path

        return render_template('penginapan.html', CONTENT=konten, MENU=menu,
                               NAMA_KAMAR=bedroom_name, HARGA_KAMAR=room_price, FOTO_KAMAR=room_foto)


    return flask_objek

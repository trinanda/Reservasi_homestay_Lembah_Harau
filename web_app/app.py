from flask import Flask, render_template, request
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


    @flask_objek.route('/penginapan', methods = ["GET", "POST"])
    @flask_objek.route('/<uri>')
    @flask_objek.route('/<id_kamar>')
    def kamar(uri=None, room=None, id_kamar=None):
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

        # template penginapan
        bedroom_name = "bedroom"
        room_price = "price"
        room_foto = 'foto kamar nya gimana..?'
        room_id = 'disini ID'
        if kamar is not None:
            room_price = Kamar.query.first()
            room_price = room_price.harga_kamar
            bedroom_name = Kamar.query.first()
            bedroom_name = bedroom_name.nama_kamar
            room_foto = Kamar.query.first()
            room_foto = room_foto.path
            room_id = Kamar.query.first()
            room_id = room_id.id_kamar
        # // penginapan
        urutan_kamar = Kamar.query.order_by('urutan_kamar')

        if request.method == "POST":
            room_price = Kamar.query.first()
            room_price = room_price.harga_kamar
            bedroom_name = Kamar.query.first()
            bedroom_name = bedroom_name.nama_kamar
            room_foto = Kamar.query.first()
            room_foto = room_foto.path
            room_id = Kamar.query.first()
            room_id = room_id.id_kamar
            return render_template("detail_kamar.html", NAMA_KAMAR=bedroom_name, HARGA_KAMAR=room_price,
                                   GAMBAR=room_foto, GAMBAR1=room_foto, id_kamar=room_id)
        else:
            pass

        return render_template('penginapan.html', CONTENT=konten, MENU=menu,
                               nama_kamar=bedroom_name, harga_kamar=room_price, foto_kamar=room_foto,
                               KAMARS=urutan_kamar, room_id=room_id)


    @flask_objek.route('/detail_kamar/<id_kamar>')
    def detail_kamar(id_kamar):
        kamar = Kamar()
        id_kamar = 'id kamar'
        if kamar is not None:
            id_kamar = Kamar.id_kamar
        return render_template('detail_kamar.html',id_kamar=id_kamar)

    return flask_objek

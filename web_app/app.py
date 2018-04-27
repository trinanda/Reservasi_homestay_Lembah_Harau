from flask import Flask, render_template, request, redirect
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

        konten = 'Hello!!!'
        if page is not None:
            konten = page.konten

        menu = Menu.query.order_by('urutan')

        return render_template('index.html', CONTENT=konten, MENU=menu)

    @flask_objek.route('/penginapan', methods = ["GET", "POST"])
    @flask_objek.route('/<uri>')
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

        try:
            room_price = Kamar.query.first()
            room_price = room_price.harga_kamar
        except AttributeError:
            return "Kamar belum ditambahkan pada database"

        if room is not None:
            kamar = Kamar.query.filter_by(nama_kamar=room).first()
        else:
            pass

        if kamar is not None:
            room_price = Kamar.query.first()
            room_price = room_price.harga_kamar
            bedroom_name = Kamar.query.first()
            bedroom_name = bedroom_name.nama_kamar
            room_foto = Kamar.query.first()
            room_foto = room_foto.room_images
            room_id = Kamar.query.first()
            room_id = room_id.id_kamar
            keterangan_kamar = Kamar.query.first()
            keterangan_kamar = keterangan_kamar.room_description

        urutan_kamar = Kamar.query.order_by('urutan_kamar')

        if request.method == "get":
            room_price = Kamar.query.first()
            room_price = room_price.harga_kamar
            bedroom_name = Kamar.query.first()
            bedroom_name = bedroom_name.nama_kamar
            room_foto = Kamar.query.first()
            room_foto = room_foto.room_images
            room_id = Kamar.query.first()
            room_id = room_id.id_kamar
            keterangan_kamar = Kamar.query.first()
            keterangan_kamar = keterangan_kamar.room_description
            return render_template("detail_kamar.html", NAMA_KAMAR=bedroom_name, HARGA_KAMAR=room_price,
                                   room_images=room_foto, room_description=keterangan_kamar)
        else:
            pass

        return render_template('penginapan.html', CONTENT=konten, MENU=menu,
                               nama_kamar=bedroom_name, harga_kamar=room_price, room_images=room_foto,
                               KAMARS=urutan_kamar, room_id=room_id, room_description=keterangan_kamar)


    @flask_objek.route('/detail_kamar/<id_kamar>', methods = ["GET", "POST"])
    def detail_kamar(id_kamar=None, nama_kamar=None, keterangan_kamar=None):
        id_kamar = request.args.get('id_kamar')
        nama_kamar = request.args.get('nama_kamar')
        harga_kamar = request.args.get('harga_kamar')
        keterangan_kamar = request.args.get('room_description')
        room_images1= request.args.get('room_images')

        kamar = Kamar()

        if request.method == "get":
            room_price = Kamar.query.first()
            room_price = room_price.harga_kamar
            bedroom_name = Kamar.query.first()
            bedroom_name = bedroom_name.nama_kamar

            lama_menginap = 1
            total_harga_penginapan = room_price * int(lama_menginap)
            try:
                total_harga_penginapan = int(harga_kamar) * 1
            except ValueError:
                return 'lama menginap belum dimasukan'
            return render_template("checkout.html", TOTAL_HARGA_PENGINAPAN=total_harga_penginapan, NAMA_KAMAR=bedroom_name,
                                   LAMA_HARI=lama_menginap )

        return render_template("detail_kamar.html", NAMA_KAMAR=nama_kamar, id_kamar=id_kamar,
                               HARGA_KAMAR=harga_kamar, room_description=keterangan_kamar, room_images=room_images1)


    @flask_objek.route('/checkout/<id_kamar>', methods = ["GET", "POST"])
    def checkout(id_kamar=None):
        harga_kamar = request.args.get('harga_kamar')
        nama_kamar = request.args.get('nama_kamar')
        lama_hari = request.args.get('lama_menginap')
        lama_menginap = request.args.get('lama_menginap')
        total_harga_penginapan = int(harga_kamar) * int(lama_menginap)
        try:
            total_harga_penginapan = int(harga_kamar) * 1
        except ValueError:
            return 'lama menginap belum dimasukan'
        return render_template("checkout.html", TOTAL_HARGA_PENGINAPAN=total_harga_penginapan, NAMA_KAMAR=nama_kamar,
                               LAMA_HARI=lama_hari)


    # @flask_objek.route('/testes')
    # def tes_checkout():
    #     return render_template("checkout.html")


    return flask_objek


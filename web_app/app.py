from flask import Flask, render_template, request, redirect
from flask_admin import Admin

from web_app.views import PageModelView, MenuModelView, PilihKamarView, InvoiceModelView


def create_app():

    flask_objek = Flask(__name__, static_folder='files')

    flask_objek.config.from_pyfile('settings.py')

    from web_app.models import database, Page, Menu, Kamar, Invoice
    database.init_app(flask_objek)

    admin = Admin(flask_objek, name='Administrator', template_mode='bootstrap3')
    admin.add_view(PageModelView(Page, database.session))
    admin.add_view(MenuModelView(Menu, database.session))
    admin.add_view(PilihKamarView(Kamar, database.session))
    admin.add_view(InvoiceModelView(Invoice, database.session))

    @flask_objek.route('/')
    @flask_objek.route('/<uri>')
    def index(uri=None):
        page = Page()
        if uri is not None:
            page = Page.query.filter_by(url=uri).first()
        else:
            pass

        try:
            isi_konten = Page.query.first()
            isi_konten = isi_konten.konten
        except AttributeError:
            return render_template('index.html')

        isi_konten = 'test'
        if page is not None:
            isi_konten = Page.query.first()
            isi_konten  = isi_konten .konten
        else:
            pass

        menu = Menu.query.order_by('urutan')

        return render_template('index.html', CONTENT=isi_konten,  MENU=menu)

    @flask_objek.route('/homepage')
    @flask_objek.route('/<uri>')
    def homepage():
        page = Page()

        isi_konten = Page.query.filter_by(id_halaman=1).first()

        menu = Menu.query.order_by('urutan')
        return render_template('homepage.html',MENU=menu, HOMEPAGE=isi_konten.konten)

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
        menu = Menu.query.order_by('urutan')

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
            room_foto = Kamar.query.first()
            room_foto = room_foto.room_images

            lama_menginap = 1
            total_harga_penginapan = room_price * int(lama_menginap)

            return render_template("checkout.html", TOTAL_HARGA_PENGINAPAN=total_harga_penginapan, NAMA_KAMAR=bedroom_name,
                                   LAMA_HARI=lama_menginap, ROOM_IMAGES= room_foto, HARGA_KAMAR=room_price)

        return render_template("detail_kamar.html", MENU=menu, NAMA_KAMAR=nama_kamar, id_kamar=id_kamar,
                               HARGA_KAMAR=harga_kamar, room_description=keterangan_kamar, room_images=room_images1)


    @flask_objek.route('/checkout/<id_kamar>', methods = ["GET", "POST"])
    def checkout(id_kamar=None):
        menu = Menu.query.order_by('urutan')

        harga_kamar = request.args.get('harga_kamar')
        nama_kamar = request.args.get('nama_kamar')
        foto_kamar = request.args.get('foto_kamar')
        lama_hari = request.args.get('lama_menginap')
        lama_menginap = request.args.get('lama_menginap')
        total_harga_penginapan = int(harga_kamar) * int(lama_menginap)

        if request.method == 'get':
            nama_lengkap = request.form.get('NAMA_LENGKAP')
            nomor_telepon = request.form.get('NOMOR_TELEPON')
            email_pemesan = request.form.get('EMAIL_PEMESAN')
            nama_kamar = request.form.get('NAMA_KAMAR')
            nama_kamar = request.form.get('LAMA_MENGINAP')
            harga_kamar = request.args.get('HARGA_KAMAR')
            return render_template("payment.html")

        return render_template("checkout.html", MENU=menu, TOTAL_HARGA_PENGINAPAN=total_harga_penginapan, NAMA_KAMAR=nama_kamar,
                               LAMA_MENGINAP=lama_hari, ROOM_IMAGES=foto_kamar, HARGA_KAMAR=harga_kamar)


    @flask_objek.route('/payment')
    def payment():
        menu = Menu.query.order_by('urutan')

        nama_pemesan = request.args.get('NAMA_LENGKAP')
        nomor_telepon = request.args.get('NOMOR_TELEPON')
        email_pemesan = request.args.get('EMAIL_PEMESAN')
        nama_kamar = request.args.get('NAMA_KAMAR')
        lama_menginap = request.args.get('LAMA_MENGINAP')
        harga_kamar = request.args.get('HARGA_KAMAR')

        if request.method == 'get':
            nomor_invoice = request.form.get('NOMOR_INVOICE')
            nama_pemesan = request.form.get('NAMA_PEMESAN')
            nomor_telepon = request.form.get('NOMOR_TELEPON')
            email_pemesan = request.form.get('EMAIL')
            nama_kamar = request.form.get('NAMA_KAMAR')
            lama_menginap = request.form.get('LAMA_MENGINAP')
            harga_total = request.form.get('HARGA_TOTAL')
            tanggal_pemesanan = request.form.get('TANGGAL_PEMESANAN')

            return render_template('transfer.html')

        return render_template("payment.html", MENU=menu, NAMA_PEMESAN=nama_pemesan, NAMA_KAMAR=nama_kamar, NOMOR_TELEPON=nomor_telepon,
                               EMAIL_PEMESAN=email_pemesan, LAMA_MENGINAP=lama_menginap, HARGA_KAMAR=harga_kamar)


    @flask_objek.route('/transfer', methods = ["GET", "POST"])
    def transfer(statuss="pending"):

        #get current date
        import time
        tanggal_pemesanan = time.strftime("%d/%m/%Y")
        # /get current date

        # get invoice number
        import string
        import random
        def generator_random(size=10, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for x in range(size))
        generate_invoice = 'HR' + generator_random() + 'INV'
        generate_invoice = str(generate_invoice)
        # /get invoice number

        nama_kamar = request.args.get('NAMA_KAMAR')
        lama_menginap = request.args.get('LAMA_MENGINAP')
        harga_kamar = request.args.get('HARGA_KAMAR')
        harga_total = int(lama_menginap) * int(harga_kamar)
        nama_pemesan = request.args.get('NAMA_PEMESAN')
        nomor_telepon = request.args.get('NOMOR_TELEPON')
        email_pemesan = request.args.get('EMAIL_PEMESAN')

        if request.method == 'POST':
            nomor_invoice = request.form.get('NOMOR_INVOICE')
            nomor_invoice = str(nomor_invoice)
            print('coba tes ini ', nomor_invoice, type(nomor_invoice))
            nama_pemesan = request.form.get('NAMA_PEMESAN')
            nomor_telepon = request.form.get('NOMOR_TELEPON')
            email_pemesan = request.form.get('EMAIL_PEMESAN')
            nama_kamar = request.form.get('NAMA_KAMAR')
            lama_menginap = request.form.get('LAMA_MENGINAP')
            harga_total_pemesan_kamar = request.form.get('HARGA_TOTAL')
            tanggal_pemesanan = request.form.get('TANGGAL_PEMESANAN')

            status = statuss

            insert_ke_db = Invoice(nomor_invoice, nama_pemesan, nomor_telepon, email_pemesan, nama_kamar, lama_menginap,
                             harga_total_pemesan_kamar, tanggal_pemesanan, status)
            database.session.add(insert_ke_db)
            database.session.commit()

            return render_template('transfer.html')


        return render_template('transfer.html', NAMA_KAMAR=nama_kamar, NAMA_PEMESAN=nama_pemesan, NOMOR_TELEPON=nomor_telepon,
                               EMAIL_PEMESAN=email_pemesan, LAMA_MENGINAP=lama_menginap, HARGA_KAMAR=harga_kamar,
                               HARGA_TOTAL=harga_total, TANGGAL_PEMESANAN=tanggal_pemesanan,
                               NOMOR_INVOICE=generate_invoice)


    # from web_app.models import Invoice, database
    # @flask_objek.route('/tesinsert', methods = ["GET", "POST"])
    # def tesinsert(statuss="pending"):
    #
    #     if request.method == 'POST':
    #
    #         id = request.form.get('id')
    #         data = request.form.get('data')
    #         status = statuss
    #         new_ex = Invoice(id, data, status)
    #         database.session.add(new_ex)
    #         database.session.commit()
    #
    #     return render_template('example_insert.html')

    return flask_objek


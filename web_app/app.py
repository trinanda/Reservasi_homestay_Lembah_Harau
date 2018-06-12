import sys, os

from flask_security.utils import encrypt_password

sys.path.append(os.getcwd() + '/web_app') #sesuai dengan mark directory as sources

import flask_admin
from flask import Flask, render_template, request, redirect, url_for
from flask_admin import Admin, helpers as admin_helpers
from flask_mail import Mail, Message
from flask_security import SQLAlchemyUserDatastore, Security

from views import PageModelView, MenuModelView, PilihKamarView, InvoiceView, MyModelView
# from settings import MAIL_USERNAME, MAIL_PASSWORD, TWLIO_ACCOUNT_SID, TWLIO_AUTH_TOKEN
from settings import TWLIO_ACCOUNT_SID, TWLIO_AUTH_TOKEN
from smtplib import SMTP_SSL
from twilio.rest import Client
from models import database, Page, Menu, Kamar, Invoice, User, Role

#gmail import package dependencies
import base64
import httplib2

from email.mime.text import MIMEText
from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

from flask_wtf import FlaskForm, RecaptchaField

from shapely import wkb, wkt
from binascii import unhexlify

def create_app():

    flask_objek = Flask(__name__, static_folder='files')

    flask_objek.config.from_pyfile('settings.py')

    database.init_app(flask_objek)


    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(database, User, Role)
    security = Security(flask_objek, user_datastore)

    admin = Admin(flask_objek, name='Administrator', base_template='my_master.html', template_mode='bootstrap3')
    admin.add_view(PageModelView(Page, database.session))
    admin.add_view(MenuModelView(Menu, database.session))
    admin.add_view(PilihKamarView(Kamar, database.session))
    admin.add_view(InvoiceView(Invoice, database.session))
    admin.add_view(MyModelView(Role, database.session))
    admin.add_view(MyModelView(User, database.session))


    # define a context processor for merging flask-admin's template context into the
    # flask-security views.
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
            return render_template('index_page.html')

        isi_konten = 'test'
        if page is not None:
            isi_konten = Page.query.first()
            isi_konten  = isi_konten .konten
        else:
            pass

        menu = Menu.query.order_by('urutan')

        return render_template('index_page.html', CONTENT=isi_konten,  MENU=menu)


    @security.context_processor
    @flask_objek.route('/admin')
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )

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
            keterangan_kamar = keterangan_kamar.keterangan_kamar
            lokasi_kamar = Kamar.query.first()
            lokasi_kamar = lokasi_kamar.lokasi

            data = str(lokasi_kamar)
            binnary = unhexlify(data)
            point = wkb.loads(binnary)
            longitude = point.y
            latitude = point.x

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
            keterangan_kamar = keterangan_kamar.keterangan_kamar
            lokasi_kamar = Kamar.query.first()
            lokasi_kamar = lokasi_kamar.lokasi
            return render_template("detail_kamar.html", id_kamar=room_id, NAMA_KAMAR=bedroom_name, HARGA_KAMAR=room_price,
                                   room_images=room_foto, keterangan_kamar=keterangan_kamar, lokasi_kamar=lokasi_kamar,
                                   LATITUDE=latitude, LONGITUDE=longitude)
        else:
            pass

        return render_template('penginapan.html', CONTENT=konten, MENU=menu, KAMARS=urutan_kamar)


    @flask_objek.route('/detail_kamar/<id_kamar>', methods = ["GET", "POST"])
    def detail_kamar(id_kamar=None, nama_kamar=None, keterangan_kamar=None):
        menu = Menu.query.order_by('urutan')

        id_kamar = request.args.get('id_kamar')
        nama_kamar = request.args.get('nama_kamar')
        harga_kamar = request.args.get('harga_kamar')
        keterangan_kamar = request.args.get('keterangan_kamar')
        room_images1= request.args.get('room_images')
        lokasi = request.args.get('lokasi')
        data = str(lokasi)
        binnary = unhexlify(data)
        point = wkb.loads(binnary)
        longitude = str(point.y)
        latitude = str(point.x)

        lihat_lokasi = 'https://www.google.com/maps/@'+longitude+','+latitude+',17.25z'

        kamar = Kamar()

        if request.method == "get":
            room_price = Kamar.query.first()
            room_price = room_price.harga_kamar
            bedroom_name = Kamar.query.first()
            bedroom_name = bedroom_name.nama_kamar
            room_foto = Kamar.query.first()
            room_foto = room_foto.room_images
            room_id = Kamar.query.first()
            room_id = room_id.id_kamar

            lama_menginap = 1
            total_harga_penginapan = room_price * int(lama_menginap)

            return render_template("checkout.html", TOTAL_HARGA_PENGINAPAN=total_harga_penginapan, NAMA_KAMAR=bedroom_name,
                                   LAMA_HARI=lama_menginap, ROOM_IMAGES= room_foto, HARGA_KAMAR=room_price, ID_KAMAR=room_id)

        return render_template("detail_kamar.html", MENU=menu, NAMA_KAMAR=nama_kamar, id_kamar=id_kamar,
                               HARGA_KAMAR=harga_kamar, keterangan_kamar=keterangan_kamar, room_images=room_images1,
                               LATITUDE=longitude, LONGITUDE=latitude, LIHAT_LOKASI=lihat_lokasi)





    @flask_objek.route('/checkout/<id_kamar>', methods = ["GET", "POST"])
    def checkout(id_kamar=None):
        menu = Menu.query.order_by('urutan')

        id_kamar = request.args.get('id_kamar')
        harga_kamar = request.args.get('harga_kamar')
        nama_kamar = request.args.get('nama_kamar')
        foto_kamar = request.args.get('foto_kamar')
        lama_hari = request.args.get('lama_menginap')
        lama_menginap = request.args.get('lama_menginap')
        total_harga_penginapan = int(harga_kamar) * int(lama_menginap)

        class LoginForm(FlaskForm):
            recaptcha = RecaptchaField()

        captha = LoginForm()

        if captha.validate_on_submit():
            if request.method == 'get':
                nama_lengkap = request.form.get('NAMA_LENGKAP')
                nomor_telepon = request.form.get('NOMOR_TELEPON')
                email_pemesan = request.form.get('EMAIL_PEMESAN')
                nama_kamar = request.form.get('NAMA_KAMAR')
                nama_kamar = request.form.get('LAMA_MENGINAP')
                harga_kamar = request.args.get('HARGA_KAMAR')
                id_kamar = request.args.get('ID_KAMAR')
                return render_template("payment.html")

        return render_template("checkout.html", ID_KAMAR=id_kamar, MENU=menu, TOTAL_HARGA_PENGINAPAN=total_harga_penginapan, NAMA_KAMAR=nama_kamar,
                               LAMA_MENGINAP=lama_hari, ROOM_IMAGES=foto_kamar, HARGA_KAMAR=harga_kamar, captha=captha)


    @flask_objek.route('/payment')
    def payment():
        menu = Menu.query.order_by('urutan')

        nama_pemesan = request.args.get('NAMA_LENGKAP')
        nomor_telepon = request.args.get('NOMOR_TELEPON')
        email_pemesan = request.args.get('EMAIL_PEMESAN')
        nama_kamar = request.args.get('NAMA_KAMAR')
        lama_menginap = request.args.get('LAMA_MENGINAP')
        harga_kamar = request.args.get('HARGA_KAMAR')
        id_kamar = request.args.get('ID_KAMAR')

        if request.method == 'get':
            nomor_invoice = request.form.get('NOMOR_INVOICE')
            nama_pemesan = request.form.get('NAMA_PEMESAN')
            nomor_telepon = request.form.get('NOMOR_TELEPON')
            email_pemesan = request.form.get('EMAIL')
            nama_kamar = request.form.get('NAMA_KAMAR')
            lama_menginap = request.form.get('LAMA_MENGINAP')
            harga_total = request.form.get('HARGA_TOTAL')
            tanggal_pemesanan = request.form.get('TANGGAL_PEMESANAN')
            id_kamar = request.form.get('ID_KAMAR')

            return render_template('transfer.html')

        return render_template("payment.html", MENU=menu, NAMA_PEMESAN=nama_pemesan, NAMA_KAMAR=nama_kamar, NOMOR_TELEPON=nomor_telepon,
                               EMAIL_PEMESAN=email_pemesan, LAMA_MENGINAP=lama_menginap, HARGA_KAMAR=harga_kamar, ID_KAMAR=id_kamar)


    @flask_objek.route('/transfer', methods=["GET", "POST"])
    def transfer(statuss="pending"):

        # get current date
        import time
        tanggal_pemesanan = time.strftime("%d/%m/%Y")
        tanggal_pemesanan_untuk_admin = time.strftime("%Y-%m-%d %H:%M:%S")
        # /get current date

        # get invoice number
        import string
        import random
        def generator_random(size=10, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for x in range(size))

        generate_invoice = 'HR' + generator_random() + 'INV'
        # /get invoice number

        nama_kamar = request.args.get('NAMA_KAMAR')
        lama_menginap = request.args.get('LAMA_MENGINAP')
        harga_kamar = request.args.get('HARGA_KAMAR')
        harga_total = int(lama_menginap) * int(harga_kamar)
        nama_pemesan = request.args.get('NAMA_PEMESAN')
        nomor_telepon = request.args.get('NOMOR_TELEPON')
        email_pemesan = request.args.get('EMAIL_PEMESAN')
        id_kamar = request.args.get('ID_KAMAR')


        if request.method == 'POST':
            nomor_invoice = request.form.get('NOMOR_INVOICE')

            id_kamar = request.form.get('ID_KAMAR')
            nama_pemesan = request.form.get('NAMA_PEMESAN')
            nomor_telepon = request.form.get('NOMOR_TELEPON')
            email_pemesan = request.form.get('EMAIL_PEMESAN')
            nama_kamar = request.form.get('NAMA_KAMAR')
            lama_menginap = request.form.get('LAMA_MENGINAP')
            harga_total_pemesan_kamar = request.form.get('HARGA_TOTAL')
            tanggal_pemesanan = request.form.get('TANGGAL_PEMESANAN_UNTUK_ADMIN')
            status = statuss

            # # fitur ini untuk sementara di non-aktivkan, karena di server vps digital ocean tidak jalan karena port SMPT di block
            # # selama 60 hari dari pendaftaran
            #################### send_email untuk pemesan
            # to_pemesan = email_pemesan
            #
            # subject_to_pemesan = '---Harau Homestay Reservation---'
            # message_to_pemesan  = 'Terima kasih Telah Menggunakan Layanan Kami, Anda telah memesan kamar ' + nama_kamar + \
            #           ' selama ' + lama_menginap + ' hari, dan biaya total nya adalah ' + harga_total_pemesan_kamar +\
            #           ' ribu rupiah, Kami akan segera mengkonfirmasi setelah pembayaran selesai dilakukan \n' + \
            #           '---Terima kasih, Salam dari kami Harau Homestay Reservation---'

            # gmail_username = MAIL_USERNAME
            # gmail_password = MAIL_PASSWORD
            #
            # msg = Message(subject_to_pemesan, sender=gmail_username, recipients=[to_pemesan])
            # msg.body = message_to_pemesan
            #
            # mail = Mail(flask_objek)
            # mail.connect()
            # mail.send(msg)
            ##############################---------------###

            #fitur ini untuk sementara di non-aktivkan, karena di server vps digital ocean tidak jalan karena port SMPT di block
            #selama 60 hari dari pendaftaran
            #### EMAIL SMTP_SSL ##
            msg_to_admin = 'Pelanggan atas nama ' + nama_pemesan + ' dengan send_email '+ email_pemesan + ' dan' + \
                           ' nomor telepon ' + nomor_telepon +' telah memesan kamar ' +\
                           nama_kamar + ' selama ' + lama_menginap + \
                           ' hari, dan harga totalnya ' + str(harga_total)
            # try:
            #     server = SMTP_SSL('smtp.gmail.com', 465)
            #     server.ehlo()
            #     server.login(gmail_username, gmail_password)
            #     server.sendmail('zidanecr7kaka@gmail.com', 'pythonpayakumbuh@gmail.com', msg_to_admin)
            #     server.quit()
            # except:
            #     return 'send_email gagal terkirim'
            ###/> EMAIL SMTP_SSL ###

            ##################
            ###### TWILIO ####
            # Your Account SID from twilio.com/console
            account_sid = TWLIO_ACCOUNT_SID
            # Your Auth Token from twilio.com/console
            auth_token = TWLIO_AUTH_TOKEN

            client = Client(account_sid, auth_token)

            message = client.messages.create(
                # to="+6282174853636",/up
                to="+6281275803651",
                from_="+12014307127",
                body=msg_to_admin)

            #######-->/ TWILIO ########
            ####################################

            ####################################
            #send gmail
            # Path to the client_secret.json file downloaded from the Developer Console
            # import json
            # with open('client_secret.json', 'r') as json_data:
            #     data = json.load(json_data)
            CLIENT_SECRET_FILE = 'web_app/api/client_secret.json'

            # Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
            OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.compose'

            # Location of the credentials storage file
            STORAGE = Storage('web_app/api/gmail.storage')

            # Start the OAuth flow to retrieve credentials
            flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
            http = httplib2.Http()

            # Try to retrieve credentials from storage or run the flow to generate them
            credentials = STORAGE.get()
            if credentials is None or credentials.invalid:
                credentials = run_flow(flow, STORAGE, http=http)

            # Authorize the httplib2.Http object with our credentials
            http = credentials.authorize(http)

            # Build the Gmail service from discovery
            gmail_service = build('gmail', 'v1', http=http)


            # TO PEMESAN

            to_pemesan = email_pemesan

            subject_to_pemesan = '---Harau Homestay Reservation---'
            message_to_pemesan = 'Terima kasih Telah Menggunakan Layanan Kami, Anda telah memesan kamar ' + nama_kamar + \
                                     ' selama ' + lama_menginap + ' hari, dan biaya total nya adalah ' + harga_total_pemesan_kamar + \
                                     ' ribu rupiah, Kami akan segera mengkonfirmasi setelah pembayaran selesai dilakukan \n' + \
                                     '---Terima kasih, Salam dari kami Harau Homestay Reservation---'
            # create a message to send
            # message_to_pemesan = MIMEText("Terima kasih telah memesan kamar melalui Harau Reservation")
            message_to_pemesan = MIMEText(message_to_pemesan)
            message_to_pemesan['to'] = to_pemesan
            # message_to_pemesan['from'] = "python.api123@gmail.com"
            message_to_pemesan['from'] = "zidanecr7kaka@gmail.com"
            message_to_pemesan['subject'] = subject_to_pemesan
            raw_to_pemesan = base64.urlsafe_b64encode(message_to_pemesan.as_bytes())
            raw_to_pemesan = raw_to_pemesan.decode()
            body_to_pemesan = {'raw': raw_to_pemesan}

                # send it
            try:
                message_to_pemesan = (
                gmail_service.users().messages().send(userId="me", body=body_to_pemesan).execute())
                print('Message Id: %s' % message_to_pemesan['id'])
                print(message_to_pemesan)
            except Exception as error:
                print('An error occurred: %s' % error)

            # TO ADMIN
            # create a message to send
            message_to_admin = MIMEText(msg_to_admin)
            message_to_admin['to'] = "pythonpayakumbuh@gmail.com"
            # message_to_admin['from'] = "python.api123@gmail.com"
            message_to_admin['from'] = "zidanecr7kaka@gmail.com"
            message_to_admin['subject'] = "Ada yang memesan kamar"
            raw_to_admin = base64.urlsafe_b64encode(message_to_admin.as_bytes())
            raw_to_admin = raw_to_admin.decode()
            body_to_admin = {'raw': raw_to_admin}

            # send it
            try:
                message_to_admin = (
                    gmail_service.users().messages().send(userId="me", body=body_to_admin).execute())
                print('Message Id: %s' % message_to_admin['id'])
                print(message_to_admin)
            except Exception as error:
                print('An error occurred: %s' % error)


            insert_ke_db = Invoice(id_kamar, nomor_invoice, nama_pemesan, nomor_telepon, email_pemesan, nama_kamar,
                                       lama_menginap,
                                       harga_total_pemesan_kamar, tanggal_pemesanan, status)
            database.session.add(insert_ke_db)
            database.session.commit()

            return redirect('http://192.168.100.3:7575/success')

        return render_template('transfer.html', NAMA_KAMAR=nama_kamar, NAMA_PEMESAN=nama_pemesan,
                           NOMOR_TELEPON=nomor_telepon,
                               EMAIL_PEMESAN=email_pemesan, LAMA_MENGINAP=lama_menginap, HARGA_KAMAR=harga_kamar,
                               HARGA_TOTAL=harga_total, TANGGAL_PEMESANAN=tanggal_pemesanan,
                               TANGGAL_PEMESANAN_UNTUK_ADMIN=tanggal_pemesanan_untuk_admin,
                               NOMOR_INVOICE=generate_invoice, ID_KAMAR=id_kamar)

    @flask_objek.route('/success', methods=['GET', 'POST'])
    def success():
        return render_template('success.html')


    return flask_objek


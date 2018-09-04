import sys, os

from flask_security.utils import verify_password
from flask_uploads import configure_uploads, UploadSet, IMAGES
import pdfkit
from werkzeug.utils import secure_filename

sys.path.append(os.getcwd() + '/web_app') #sesuai dengan mark directory as sources

from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from flask_admin import Admin, helpers as admin_helpers
from flask_security import SQLAlchemyUserDatastore, Security

from views import PageModelView, MenuModelView, PilihKamarView, InvoiceView, MyModelView, HomestayView, LoginFormView, \
    RegisterFormView, file_path
# from settings import MAIL_USERNAME, MAIL_PASSWORD, TWLIO_ACCOUNT_SID, TWLIO_AUTH_TOKEN
from settings import TWLIO_ACCOUNT_SID_NONE_UPGRADED_FOR_ADMIN, TWLIO_AUTH_TOKEN_NONE_UPGRADED_FOR_ADMIN, \
    TWLIO_ACCOUNT_SID_UPGRADED_FOR_USER, TWLIO_AUTH_TOKEN_UPGRADED_FOR_USER
from twilio.rest import Client
from models import database, Page, Menu, Kamar, Invoice, User, Role, Homestay
from form import AddKamarForm, EditKamarForm

#gmail import package dependencies
import base64
import httplib2

from email.mime.text import MIMEText
from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

from flask_wtf import FlaskForm, RecaptchaField

from shapely import wkb
from binascii import unhexlify

from flask_googlemaps import GoogleMaps
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash


def create_app():

    flask_objek = Flask(__name__, static_folder='files')

    flask_objek.config.from_pyfile('settings.py')

    database.init_app(flask_objek)

    GoogleMaps(flask_objek)

    bootstrap = Bootstrap(flask_objek)
    login_manager = LoginManager()
    login_manager.init_app(flask_objek)
    login_manager.login_view = 'login'

    photos = UploadSet('photos', IMAGES)
    configure_uploads(flask_objek, photos)
    # patch_request_class(flask_objek)  # set maximum file size, default is 16MB

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(database, User, Role)
    security = Security(flask_objek, user_datastore)

    admin = Admin(flask_objek, name='Administrator', base_template='my_master.html', template_mode='bootstrap3')
    admin.add_view(PageModelView(Page, database.session))
    admin.add_view(MenuModelView(Menu, database.session))
    admin.add_view(HomestayView(Homestay, database.session))
    admin.add_view(PilihKamarView(Kamar, database.session))
    admin.add_view(InvoiceView(Invoice, database.session))
    admin.add_view(MyModelView(Role, database.session))
    admin.add_view(MyModelView(User, database.session))


    url_index = 'http://127.0.0.1:7575/'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

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

        isi_konten = ''
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

        kamar = Kamar('','','','','','','','')
        homestay = Homestay()
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
            room_id = Kamar.query.first()
            room_id = room_id.id_kamar
            room_price = Kamar.query.first()
            room_price = room_price.harga_kamar
            bedroom_name = Kamar.query.first()
            bedroom_name = bedroom_name.nama_kamar
            room_foto = Kamar.query.first()
            room_foto = room_foto.room_images

            keterangan_kamar = Kamar.query.first()
            keterangan_kamar = keterangan_kamar.keterangan_kamar

            lokasi_kamar = Homestay.query.first()
            lokasi_kamar = lokasi_kamar.lokasi_homestay
            data = str(lokasi_kamar)
            binnary = unhexlify(data)
            point = wkb.loads(binnary)
            longitude = point.y
            latitude = point.x

        urutan_kamar = Kamar.query.order_by('urutan_kamar')

        if request.method == "POST":
            session['LONGITUDE'] = longitude
            session['LATITUDE'] = latitude
            session['HARGA_KAMAR'] = room_price
            session['NAMA_KAMAR'] = bedroom_name
            session['keterangan_kamar'] = keterangan_kamar
            return render_template("detail_kamar.html")
        else:
            pass

        return render_template('penginapan.html', CONTENT=konten, MENU=menu, KAMARS=urutan_kamar)


    @flask_objek.route('/detail_kamar/<id_kamar>', methods = ["GET", "POST"])
    def detail_kamar(id_kamar=None):
        id_kamar = Kamar.query.filter_by(id_kamar=id_kamar).first()
        id_kamar = id_kamar.id_kamar

        # nama_homestay = Homestay.query.filter_by(id_homestay=id_kamar).first()
        # nama_homestay = nama_homestay.nama_homestay

        result, nama_homestay = database.session.query(Kamar.homestay_name, Homestay.nama_homestay).join(Homestay).filter(Kamar.id_kamar == id_kamar).first()
        # nama_homestay = nama_homestay.homestay_name

        nama_kamar = Kamar.query.filter_by(id_kamar=id_kamar).first()
        nama_kamar = nama_kamar.nama_kamar
        harga_kamar = Kamar.query.filter_by(id_kamar=id_kamar).first()
        harga_kamar = harga_kamar.harga_kamar

        keterangan_kamar = Kamar.query.filter_by(id_kamar=id_kamar).first()
        keterangan_kamar = keterangan_kamar.keterangan_kamar

        # lokasi = Homestay.query.filter_by(id_homestay=id_kamar).first()
        # lokasi = lokasi.lokasi_homestay
        result, lokasi = database.session.query(Kamar, Homestay.lokasi_homestay).join(Homestay).filter(Kamar.id_kamar == id_kamar).first()

        data = str(lokasi)
        binnary = unhexlify(data)
        point = wkb.loads(binnary)
        longitude = str(point.y)
        latitude = str(point.x)

        menu = Menu.query.order_by('urutan')

        room_images1= request.args.get('room_images')

        status_kamar = Kamar.query.filter_by(id_kamar=id_kamar).first()
        status_kamar = status_kamar.status


        lihat_lokasi = 'https://www.google.com/maps/@' + longitude + ',' + latitude + ',17.25z'

        kosong = 'Kosong'
        sedang_digunakan = 'Sedang di gunakan'

        button_penginapan = 'Booking Kamar'
        form_action_for_detail_kamar = url_index + 'checkout/{{ id_kamar }}'
        if status_kamar == sedang_digunakan:
            status_kamar = 'Mohon maaf, saat ini kamar sedang penuh'
            button_penginapan = 'Cari kamar lain'
            form_action_for_detail_kamar = url_index + 'penginapan'
            if button_penginapan == 'Cari kamar lain':
                return render_template("detail_kamar.html", MENU=menu, NAMA_KAMAR=nama_kamar, id_kamar=id_kamar,
                                       HARGA_KAMAR=harga_kamar, keterangan_kamar=keterangan_kamar,
                                       room_images=room_images1, LATITUDE=longitude, LONGITUDE=latitude,
                                       LIHAT_LOKASI=lihat_lokasi, KAMAR_TERSEDIA=status_kamar, BUTTON_PENGINAPAN=button_penginapan,
                                       FORM_ACTION_FOR_DETAIL_KAMAR=form_action_for_detail_kamar, NAMA_HOMESTAY=nama_homestay)

        elif status_kamar == kosong:
            status_kamar = ' '

        kamar = Kamar('','','','','','','','')
        if request.method == 'get':
            global lama_inap
            room_foto = Kamar.query.first()
            room_foto = room_foto.room_images
            room_id = Kamar.query.first()
            room_id = room_id.id_kamar
            lama_menginap = request.form.get('lama_menginap')

            return render_template("checkout.html")

        session['NAMA_HOMESTAY'] = nama_homestay
        session['NAMA_KAMAR'] = nama_kamar
        session['HARGA_KAMAR'] = harga_kamar
        session['ID_KAMAR'] = id_kamar
        session['FOTO_KAMAR'] = room_images1


        return render_template("detail_kamar.html", MENU=menu, NAMA_KAMAR=nama_kamar, id_kamar=id_kamar,
                               keterangan_kamar=keterangan_kamar, room_images=room_images1,
                               LATITUDE=longitude, LONGITUDE=latitude, LIHAT_LOKASI=lihat_lokasi, KAMAR_TERSEDIA=status_kamar,
                               BUTTON_PENGINAPAN=button_penginapan, FORM_ACTION_FOR_DETAIL_KAMAR=form_action_for_detail_kamar,
                               HARGA_KAMAR=harga_kamar, NAMA_HOMESTAY=nama_homestay)


    @flask_objek.route('/checkout/<id_kamar>', methods = ["GET", "POST"])
    def checkout(id_kamar=None):
        if 'NAMA_KAMAR' in session.keys():
            nama_kamar = session['NAMA_KAMAR']
        else:
            nama_homestay = None
        if 'NAMA_HOMESTAY' in session.keys():
            nama_homestay = session['NAMA_HOMESTAY']
        else:
            nama_kamar = None
        if 'HARGA_KAMAR' in session.keys():
            harga_kamar = session['HARGA_KAMAR']
        else:
            harga_kamar = None
        if 'lama_menginap' in session.keys():
            lama_menginap = session['lama_menginap']
        else:
            lama_menginap = None

        lama_menginap = request.args.get('lama_menginap')
        session['LAMA_MENGINAP'] = lama_menginap
        total_harga_penginapan = int(lama_menginap) * int(harga_kamar)
        session['HARGA_TOTAL'] = total_harga_penginapan

        foto_kamar = session['FOTO_KAMAR']

        menu = Menu.query.order_by('urutan')

        class LoginForm(FlaskForm):
            recaptcha = RecaptchaField()

        captha = LoginForm()

        if captha.validate_on_submit():
            if request.method == 'get':
                nama_lengkap = request.form.get('NAMA_LENGKAP')
                nomor_telepon = request.form.get('NOMOR_TELEPON')
                email_pemesan = request.form.get('EMAIL_PEMESAN')
                return render_template("payment.html")


        return render_template("checkout.html", ID_KAMAR=id_kamar, MENU=menu, TOTAL_HARGA_PENGINAPAN=total_harga_penginapan,
                               NAMA_KAMAR=nama_kamar, NAMA_HOMESTAY=nama_homestay, LAMA_HARI=lama_menginap,
                               ROOM_IMAGES=foto_kamar, captha=captha)


    @flask_objek.route('/payment', methods = ["GET", "POST"])
    def payment(statuss="pending"):
        menu = Menu.query.order_by('urutan')

        harga_kamar = session['HARGA_KAMAR']
        nama_pemesan = request.args.get('NAMA_LENGKAP')
        nomor_telepon = request.args.get('NOMOR_TELEPON')
        email_pemesan = request.args.get('EMAIL_PEMESAN')
        nama_kamar = session['NAMA_KAMAR']
        lama_menginap = session['LAMA_MENGINAP']
        harga_total = session['HARGA_TOTAL']
        harga_total = str(harga_total)
        id_kamar = session['ID_KAMAR']
        session['NAMA_LENGKAP'] = nama_pemesan
        session['NOMOR_TELEPON'] = nomor_telepon
        session['EMAIL_PEMESAN'] = email_pemesan

        # get current date
        import time
        tanggal_pemesanan = time.strftime("%d/%m/%Y")
        tanggal_pemesanan_untuk_admin = time.strftime("%Y-%m-%d %H:%M:%S")
        session['TANGGAL_PEMESANAN'] = tanggal_pemesanan
        session['TANGGAL_PEMESANAN_UNTUK_ADMIN'] = tanggal_pemesanan_untuk_admin
        tanggal_pemesanan = session['TANGGAL_PEMESANAN']
        tanggal_pemesanan_untuk_admin = session['TANGGAL_PEMESANAN_UNTUK_ADMIN']
        # /get current date

        # get invoice number
        import string
        import random
        def generator_random(size=10, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for x in range(size))

        generate_invoice = 'HR' + generator_random() + 'INV'
        session['GENERATE_INVOICE'] = generate_invoice
        nomor_invoice = session['GENERATE_INVOICE']
        # /get invoice number

        if request.method == 'POST':
            status = statuss
            session['TANGGAL_PEMESANAN'] = tanggal_pemesanan
            msg_to_admin = 'Pelanggan atas nama ' + nama_pemesan + ' dengan email '+ email_pemesan + ' dan' + \
                           ' nomor telepon ' + nomor_telepon +' telah memesan kamar ' +\
                           nama_kamar + ' selama ' + lama_menginap + \
                           ' hari, dan harga totalnya ' + str(harga_total)


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
            message_to_pemesan = 'Terima kasih ' + nama_pemesan + ' telah Menggunakan Layanan Kami, Anda telah memesan kamar ' + nama_kamar + \
                                     ' selama ' + lama_menginap + ' hari, dan biaya total nya adalah ' + harga_total + \
                                     ' rupiah, Kami akan segera mengkonfirmasi setelah pembayaran selesai dilakukan \n' + \
                                     '---Terima kasih, Salam dari kami Harau Homestay Reservation---'


            ##################
            ###### TWILIO ####

            # for admin notifications
            # Your Account SID from twilio.com/console
            account_sid_admin = TWLIO_ACCOUNT_SID_NONE_UPGRADED_FOR_ADMIN
            # # Your Auth Token from twilio.com/console
            auth_token_admin = TWLIO_AUTH_TOKEN_NONE_UPGRADED_FOR_ADMIN
            #

            sms_admin = Client(account_sid_admin, auth_token_admin)
            #
            message_admin = sms_admin.messages.create(
                to="+6281275803651",
                from_="+12132961837",  # this non upgrade number
                body=msg_to_admin)

            print(message_admin.sid)

            # ############################ SMS for user ##########################
            # # for user notifications
             # Your Account SID from twilio.com/console
            account_sid_user = TWLIO_ACCOUNT_SID_UPGRADED_FOR_USER
            # # # Your Auth Token from twilio.com/console
            auth_token_user = TWLIO_AUTH_TOKEN_UPGRADED_FOR_USER
            # #
            sms_client = Client(account_sid_user, auth_token_user)
            # #
            nomor_telepon_pemesan = nomor_telepon
            message_pemesan = sms_client.messages.create(
                to=nomor_telepon_pemesan,
                from_="+12014307127",   # this upgraded number
                body=message_to_pemesan)
            #
            #
            # ######-->/ TWILIO ########
            ###################################


            # create a message to send
            message_to_pemesan = MIMEText("Terima kasih telah memesan kamar melalui Harau Reservation")
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
                                       lama_menginap, harga_total, tanggal_pemesanan_untuk_admin, status)
            database.session.add(insert_ke_db)
            database.session.commit()

            status_kamar = Kamar.query.filter_by(id_kamar=id_kamar).first()
            status_kamar.status = 'Sedang di gunakan'
            database.session.commit()

            page = render_template('transfer.html', NAMA_KAMAR=nama_kamar, NOMOR_TELEPON=nomor_telepon,
                               EMAIL_PEMESAN=email_pemesan, LAMA_MENGINAP=lama_menginap,
                               HARGA_KAMAR=harga_kamar, TANGGAL_PEMESANAN=tanggal_pemesanan,
                               NOMOR_INVOICE=generate_invoice, HARGA_TOTAL=harga_total)


            return page


        return render_template("payment.html", MENU=menu)


    @flask_objek.route('/transfer', methods= ['POST', 'GET'])
    def transfer():
        nama_kamar = session['NAMA_KAMAR']
        nomor_telepon = session['NOMOR_TELEPON']
        email_pemesan = session['EMAIL_PEMESAN']
        lama_menginap = session['LAMA_MENGINAP']
        harga_kamar = session['HARGA_KAMAR']
        tanggal_pemesanan = session['TANGGAL_PEMESANAN']
        generate_invoice = session['GENERATE_INVOICE']
        harga_total = session['HARGA_TOTAL']

        if request.method == "POST":
            page = render_template('transfer.html', NAMA_KAMAR=nama_kamar, NOMOR_TELEPON=nomor_telepon,
                                   EMAIL_PEMESAN=email_pemesan, LAMA_MENGINAP=lama_menginap,
                                   HARGA_KAMAR=harga_kamar, TANGGAL_PEMESANAN=tanggal_pemesanan,
                                   NOMOR_INVOICE=generate_invoice, HARGA_TOTAL=harga_total)

            css = 'web_app/static/bootstrap-combined.min.css'
            pdf = pdfkit.from_string(page, False, css=css)
            response = make_response(pdf)
            response.headers['Content-Type'] = 'applications/pdf'
            response.headers['Content-Disposition'] = 'inline; filename=invoice.pdf'

            return response
        return redirect(url_index)

    @flask_objek.route('/success')
    def success():
        return render_template('success.html')



    @flask_objek.route('/signup', methods=['GET', 'POST'])
    def signup():
        form = RegisterFormView()

        try:
            if form.validate_on_submit():
                hashed_password = generate_password_hash(form.password.data, method='sha256')
                new_user = User(email=form.email.data, password=hashed_password)
                database.session.add(new_user)
                database.session.commit()

                return '<h1>User telah berhasil dibuat, silahkan coba untuk login \
                       <a href=' + url_index + 'login>Login</a></h1>'
                # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
        except:
            return '<html><h2> Data yang di inputkan harus unique, sepertinya salah satu data yang Anda Masukan sudah terdaftar, ' \
                   'Mohon ulangi input data dengan teliti...!!!  <br> <a href=' + url_index + 'signup>Ulangi Input Data</a></h2></html>'

        return render_template('signup.html', form=form)

    @flask_objek.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginFormView(request.form)
        if request.method == 'POST':
            if form.validate_on_submit():
                session['email'] = request.form['email']
                user = User.query.filter_by(email=form.email.data).first()
                if verify_password(user.password, form.password.data):
                    user.authenticated = True
                    database.session.add(user)
                    database.session.commit()
                    login_user(user)
                    login_user(user, remember=form.remember.data)
                    return redirect(url_for('dashboard'))
                else:
                    return '<h1>Invalid username or password</h1>'
            # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

        return render_template('login.html', form=form)

    @flask_objek.route('/dashboard')
    @login_required
    def dashboard():
        if 'email' in session:
            nama_homestay = current_user.homestay_name
            all_user_homestay = Kamar.query.filter_by(user_id=current_user.id)
            return render_template('dashboard.html', kamar=all_user_homestay, NAMA_HOMESTAY=nama_homestay)
        else:
            return redirect(url_for('index'))


    @flask_objek.route('/add', methods=['GET', 'POST'])
    @login_required
    def tambah_kamar():
        nama_homestay = current_user.homestay_name
        form = AddKamarForm(request.form)
        if request.method == 'POST' and 'photo' in request.files:
            if form.validate_on_submit():
                filename = photos.save(request.files['photo'])
                new_kamar = Kamar(current_user.homestay_name, form.nama_kamar.data, form.keterangan_kamar.data, form.harga_kamar.data,
                                  form.status.data, current_user.id, current_user.homestay_id, False, filename)
                database.session.add(new_kamar)
                database.session.commit()
                return redirect(url_for('dashboard'))

        return render_template('tambah_kamar.html', form=form, NAMA_HOMESTAY=nama_homestay)



    @flask_objek.route('/user_profile')
    @login_required
    def user_profile():
        return render_template('user_profile.html')

    @flask_objek.route('/kamar_edit/<kamar_id>', methods=['GET', 'POST'])
    def kamar_edit(kamar_id):
        nama_homestay = current_user.homestay_name
        data = database.session.query(Kamar, User).join(User).filter(Kamar.id_kamar == kamar_id).first()
        form = EditKamarForm(request.form)
        if request.method == 'POST':
            if form.validate_on_submit():
                if current_user.is_authenticated and data.Kamar.user_id == current_user.id:
                    data = Kamar.query.filter_by(id_kamar=kamar_id).first()
                    new_nama_kamar = form.nama_kamar.data
                    new_keterangan_kamar = form.keterangan_kamar.data
                    new_harga_kamar = form.harga_kamar.data
                    new_status_kamar = form.status.data
                    try:
                        data.nama_kamar = new_nama_kamar
                        data.keterangan_kamar = new_keterangan_kamar
                        data.harga_kamar = new_harga_kamar
                        data.status = new_status_kamar
                        database.session.commit()

                    except Exception as e:
                        return {'error': str(e)}
                return redirect(url_for('dashboard'))

        return render_template('edit_kamar.html', form=form, kamar=data, NAMA_HOMESTAY=nama_homestay)

    @flask_objek.route('/kamar_delete/<kamar_id>')
    def kamar_delete(kamar_id):
        data = database.session.query(Kamar, User).join(User).filter(Kamar.id_kamar == kamar_id).first()
        if data.Kamar.is_public:
            return render_template('kamar_detail.html', kamar=data)
        else:
            try:
                if current_user.is_authenticated and data.Kamar.user_id == current_user.id:
                    data = Kamar.query.filter_by(id_kamar=kamar_id).first()
                    database.session.delete(data)
                    database.session.commit()
            except:
                return 'Tidak bisa delete data kamar, karena kamar sedang digunakan'
        return redirect(url_for('dashboard'))

    @flask_objek.route('/kamar/<kamar_id>')
    def kamar_details(kamar_id):
        kamar_with_user = database.session.query(Kamar, User).join(User).filter(Kamar.id_kamar == kamar_id).first()
        if kamar_with_user is not None:
            if kamar_with_user.Kamar.is_public:
                return render_template('kamar_detail.html', kamar=kamar_with_user)
            else:
                if current_user.is_authenticated and kamar_with_user.Kamar.user_id == current_user.id:
                    return render_template('kamar_detail.html', kamar=kamar_with_user)
                # else:
                #    flash('Error! Incorrect permissions to access this mantan.', 'error')
        else:
            flash('Error! Recipe does not exist.', 'error')
        return redirect(url_for('index'))

    @flask_objek.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    return flask_objek


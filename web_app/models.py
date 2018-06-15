from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Numeric, Unicode, UnicodeText
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from geoalchemy2.types import Geometry
from sqlalchemy_imageattach.entity import Image, image_attachment

database = SQLAlchemy()

class Page(database.Model):
    __tablename__ = 'page'
    id_halaman = Column(Integer, primary_key=True)
    judul = Column(String)
    tag = Column(String)
    konten = Column(String)
    url = Column(String)

    def __repr__(self):
        return self.judul

class Menu(database.Model):
    __tablename__ = 'menu'
    id_menu = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    urutan = Column(Integer)

    page_id = Column(Integer, ForeignKey('page.id_halaman'))
    halaman = relationship('Page', backref=backref('Link dari menu', uselist=False))

    def __repr__(self):
        return self.title


class Kamar(database.Model):
    __tablename__ = 'kamar'
    id_kamar = Column(Integer, primary_key=True)
    nama_kamar = Column(String)
    lokasi = database.Column(Geometry("POINT"))
    keterangan_kamar = Column(String)
    room_images = Column(database.Unicode(128))
    harga_kamar = Column(Integer)
    kamar_tersedia = Column(Integer)
    urutan_kamar = Column(Integer)

    def __repr__(self):
        return '{}'.format(self.nama_kamar)

    def __init__(self, kurangi_jumlah_kamar):
        self.kamar_tersedia = kurangi_jumlah_kamar

class Invoice(database.Model):
    __tablename__ = "invoice"
    nomor_invoice = Column(String, primary_key=True, unique=True)
    nama_pemesan = Column(String(15))
    nomor_telepon = Column(Numeric)
    email_pemesan = Column(String)
    nama_kamar= Column(String)
    lama_menginap = Column(Integer)
    harga_total_pemesan_kamar = Column(Integer)
    tanggal_pemesanan = Column(DateTime)

    kamar_id = Column(Integer, ForeignKey(Kamar.id_kamar), nullable=False)
    # id_kamar = relationship('Kamar')

    PENDING = "pending"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    status_pembayaran = database.Column(database.Enum(PENDING, CONFIRMED, REJECTED, name='status_pembayaran', default=PENDING))

    def __init__(self, id_kamar, nomor_invoice, nama_pemesan, nomor_telepon, email_pemesan,
                 nama_kamar, lama_menginap, harga_total_pemesan_kamar, tanggal_pemesanan, status):
        self.kamar_id = id_kamar
        self.nomor_invoice = nomor_invoice
        self.nama_pemesan = nama_pemesan
        self.nomor_telepon = nomor_telepon
        self.email_pemesan = email_pemesan
        self.nama_kamar = nama_kamar
        self.lama_menginap = lama_menginap
        self.harga_total_pemesan_kamar = harga_total_pemesan_kamar
        self.tanggal_pemesanan = tanggal_pemesanan
        self.status_pembayaran = status



# Define models
roles_users = database.Table(
    'roles_users',
    database.Column('user_id', database.Integer(), database.ForeignKey('user.id')),
    database.Column('role_id', database.Integer(), database.ForeignKey('role.id'))
)


class Role(database.Model, RoleMixin):
    id = database.Column(database.Integer(), primary_key=True)
    name = database.Column(database.String(80), unique=True)
    description = database.Column(database.String(255))

    def __str__(self):
        return self.name


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    first_name = database.Column(database.String(255))
    last_name = database.Column(database.String(255))
    email = database.Column(database.String(255), unique=True)
    password = database.Column(database.String(255))
    active = database.Column(database.Boolean())
    confirmed_at = database.Column(database.DateTime())
    roles = database.relationship('Role', secondary=roles_users,
                            backref=database.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email








from passlib.handlers import bcrypt
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Numeric, Unicode, UnicodeText
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from geoalchemy2.types import Geometry
from sqlalchemy_imageattach.entity import Image, image_attachment
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from datetime import datetime

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


class Homestay(database.Model):
    __tablename__ = 'homestay'
    id_homestay = Column(Integer, primary_key=True)
    nama_homestay = Column(String, unique=True)
    lokasi_homestay = database.Column(Geometry("POINT"))

    def __repr__(self):
        return '{}'.format(self.nama_homestay)


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
    email = database.Column(database.String(255), unique=True)
    password = database.Column(database.String(255))
    active = database.Column(database.Boolean())
    confirmed_at = database.Column(database.DateTime())
    roles = database.relationship('Role', secondary=roles_users,
                            backref=database.backref('users', lazy='dynamic'))
    homestay_id = Column(Integer, ForeignKey(Homestay.id_homestay))
    homestay_name = relationship(Homestay)


    def __init__(self, email='', password='', active=False, roles=None):
        self.email = email
        self.password = password
        self.active = active
        self.roles = roles


    def __str__(self):
        return self.email

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        """Requires use of Python 3"""
        return str(self.id)

    def __repr__(self):
        return '<User {0}>'.format(self.name)


class Kamar(database.Model):
    __tablename__ = 'kamar'
    id_kamar = Column(Integer, primary_key=True)
    nama_kamar = Column(String)
    keterangan_kamar = Column(String)
    room_images = Column(database.Unicode(128))
    harga_kamar = Column(Integer)
    is_public = database.Column(database.Boolean(), nullable=False)

    KOSONG = 'Kosong'
    SEDANG_DIGUNAKAN = 'Sedang di gunakan'
    status = Column(Enum(KOSONG, SEDANG_DIGUNAKAN, name='status_kamar', default=KOSONG))

    urutan_kamar = Column(Integer)

    homestay_id = Column(Integer, ForeignKey(Homestay.id_homestay))
    homestay_name = relationship(Homestay)

    def __repr__(self):
        return '{}'.format(self.nama_kamar)

    user_id = Column(Integer, ForeignKey(User.id))

    def __init__(self, homestay_name='', nama_kamar='', keterangan_kamar='', harga_kamar='',
                 status=KOSONG, id=1, homestay_id='', is_public=False, filename=''):
        self.homestay_name = homestay_name
        self.nama_kamar = nama_kamar
        self.keterangan_kamar = keterangan_kamar
        self.harga_kamar = harga_kamar
        self.status = status
        self.user_id = id
        self.homestay_id = homestay_id
        self.is_public = is_public
        self.room_images = filename


class Invoice(database.Model):
    __tablename__ = "invoice"
    nomor_invoice = Column(String, primary_key=True, unique=True)
    nama_pemesan = Column(String(15))
    nomor_telepon = Column(String)
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


from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Numeric, Unicode
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy


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
    room_description = Column(String)
    room_images = Column(database.Unicode(128))
    harga_kamar = Column(Integer)
    urutan_kamar = Column(Integer)

    def __repr__(self):
        return '{}'.format(self.nama_kamar)


class Invoice(database.Model):
    __tablename__ = "Invoice"
    nomor_invoice = Column(String, primary_key=True, unique=True)
    nama_pemesan = Column(String(15))
    nomor_telepon = Column(Numeric)
    email_pemesan = Column(String)
    nama_kamar= Column(String)
    lama_menginap = Column(Integer)
    harga_total_pemesan_kamar = Column(Integer)
    tanggal_pemesanan = Column(DateTime)

    PENDING = "pending"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    status_pembayaran = database.Column(database.Enum(PENDING, CONFIRMED, REJECTED, name='status_pembayaran', default=PENDING))

    def __init__(self, nomor_invoice, nama_pemesan, nomor_telepon, email_pemesan,
                 nama_kamar, lama_menginap, harga_total_pemesan_kamar, tanggal_pemesanan, status):
        self.nomor_invoice = nomor_invoice
        self.nama_pemesan = nama_pemesan
        self.nomor_telepon = nomor_telepon
        self.email_pemesan = email_pemesan
        self.nama_kamar = nama_kamar
        self.lama_menginap = lama_menginap
        self.harga_total_pemesan_kamar = harga_total_pemesan_kamar
        self.tanggal_pemesanan = tanggal_pemesanan
        self.status_pembayaran = status





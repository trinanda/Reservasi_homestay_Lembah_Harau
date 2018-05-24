from sqlalchemy import Column, Integer, String, ForeignKey, Enum
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
    id_menu = Column(Integer, primary_key=True)
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
    __tablename__ = "invoice"
    invoice_id = Column(Integer, primary_key=True)
    example_data = Column(String)

    PENDING = "pending"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    status = database.Column(database.Enum(PENDING, CONFIRMED, REJECTED, name='status', default=PENDING))

    def __init__(self, id, data, status):
        self.invoice_id = id
        self.example_data = data
        self.status = status




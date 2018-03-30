from sqlalchemy import Column, Integer, String, ForeignKey
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


class PilihKamar(database.Model):
    __tablename__ = 'pilih_kamar'
    id_kamar = database.Column(database.Integer, primary_key=True)
    nama_kamar = database.Column(database.Unicode(64))
    harga_kamar = database.Column(database.Integer)
    path = database.Column(database.Unicode(128))

    def __unicode__(self):
        return self.name




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


class Kamar(database.Model):
    __tablename__ = 'kamar'
    id_kamar = Column(Integer, primary_key=True)
    nama_kamar = Column(String)
    harga_kamar = Column(Integer)
    path = Column(database.Unicode(128))


    # def __repr__(self):
    #     return self.nama_kamar

    def __unicode__(self):
        return self.name


    def __repr__(self):
        return '{}'.format(self.nama_kamar)




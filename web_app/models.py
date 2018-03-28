from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

database = SQLAlchemy()

class Page(database.Model):
    __tablename__ = 'page'
    id_halaman = Column(Integer, primary_key=True)
    judul = Column(String)
    tag = Column(String)
    konten = Column(String)
    url = Column(String)

class Menu(database.Model):
    __tablename__ = 'menu'
    id_menu = Column(Integer, primary_key=True)
    title = Column(String)
    urutan = Column(Integer)

    page_id = Column(Integer, ForeignKey('page.id_halaman'))
    halaman = relationship('Page', backref=backref('Link dari menu', uselist=False))

    def __repr__(self):
        return self.title

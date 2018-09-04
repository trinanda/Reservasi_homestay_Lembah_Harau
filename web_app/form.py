from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileStorage


KOSONG = 'Kosong'
SEDANG_DIGUNAKAN = 'Sedang di gunakan'


class AddKamarForm(FlaskForm):
    nama_kamar = StringField('Nama Kamar', validators=[DataRequired()])
    keterangan_kamar = StringField('Keterangan Kamar', validators=[DataRequired()])
    harga_kamar = IntegerField('Harga Kamar', validators=[DataRequired()])
    status = SelectField('status_kamar',choices=[(KOSONG, KOSONG), (SEDANG_DIGUNAKAN, SEDANG_DIGUNAKAN)])


class nama_kamar_changeForm(FlaskForm):
    nama_kamar = StringField('Nama Kamar', validators=[DataRequired()])


class EditKamarForm(FlaskForm):
    nama_kamar = StringField('Nama Kamar', validators=[DataRequired()])
    keterangan_kamar = StringField('Keterangan Kamar', validators=[DataRequired()])
    harga_kamar = IntegerField('Harga Kamar', validators=[DataRequired()])
    status = SelectField('status_kamar', choices=[(KOSONG, KOSONG), (SEDANG_DIGUNAKAN, SEDANG_DIGUNAKAN)])

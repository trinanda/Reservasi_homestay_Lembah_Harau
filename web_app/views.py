from flask_admin.contrib.sqla import ModelView

from wtforms import TextAreaField, form
from wtforms.widgets import TextArea
from jinja2 import Markup
from flask_admin import form
from flask_admin.contrib import sqla
from sqlalchemy.event import listens_for
import os
import os.path as op
from flask import url_for
from web_app.models import Kamar

# cekdeitor
class CKEditorWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += " ckeditor"
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKEditorWidget, self).__call__(field, **kwargs)

class CKEditorField(TextAreaField):
    widget = CKEditorWidget()

# cekdeitor

class PageModelView(ModelView):
    form_overrides = dict(konten=CKEditorField)

    create_template = 'admin/ckeditor.html'
    edit_template = 'admin/ckeditor.html'
    column_list = ('judul', 'tag')


class MenuModelView(ModelView):
    column_list = ('title', 'urutan')
    pass


class InvoiceView(ModelView):
    column_list = ('nomor_invoice', 'nama_pemesan', 'nomor_telepon', 'email_pemesan', 'nama_kamar',
                   'lama_menginap', 'harga_total_pemesan_kamar', 'tanggal_pemesanan', 'status_pembayaran')
    pass

# Create directory for file fields to use
file_path = op.join(op.dirname(__file__), 'files')
try:
    os.mkdir(file_path)
except OSError:
    pass


# Delete hooks for models, delete files if models are getting deleted
@listens_for(Kamar, 'after_delete')
def del_image(mapper, connection, target):
    if target.room_images:
        # Delete image
        try:
            os.remove(op.join(file_path, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(file_path,
                              form.thumbgen_filename(target.path)))
        except OSError:
            pass


# Administrative views
class PilihKamarView(sqla.ModelView):
    form_overrides = dict(room_description=CKEditorField)
    create_template = 'admin/ckeditor.html'
    edit_template = 'admin/ckeditor.html'
    column_list = ('nama_kamar', 'room_images', 'harga_kamar')
    def _list_thumbnail(view, context, model, name):
        if not model.room_images:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.room_images)))

    column_formatters = {
        'room_images': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'room_images': form.ImageUploadField('Room Images',
                                      base_path=file_path,
                                      thumbnail_size=(100, 100, True))
    }


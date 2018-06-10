from flask_admin.contrib.sqla import ModelView

from wtforms import TextAreaField, form
from wtforms.widgets import TextArea
from jinja2 import Markup
from flask_admin import form
from flask_admin.contrib import sqla
from sqlalchemy.event import listens_for
import os
import os.path as op
from flask import url_for, request, redirect, abort

#disable this line will affect to delete data on table Kamar
from web_app.models import Kamar
# enable this line if you want to migrations data with alembic
# from models import Kamar

from flask_security import current_user

from flask_admin.contrib.geoa import ModelView as GeoModelView


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



class UserAkses(ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('user'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class AdminAkses(ModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class PageModelView(AdminAkses):
    form_overrides = dict(konten=CKEditorField)

    create_template = 'admin/ckeditor.html'
    edit_template = 'admin/ckeditor.html'
    column_list = ('judul', 'tag')


class MenuModelView(AdminAkses):
    column_list = ('title', 'urutan')
    pass


class InvoiceView(AdminAkses):
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



class MapView(GeoModelView):
    pass

# Administrative views
class PilihKamarView(UserAkses, MapView):
    form_overrides = dict(keterangan_kamar=CKEditorField)
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

# Create customized model view class
class MyModelView(AdminAkses):
    pass


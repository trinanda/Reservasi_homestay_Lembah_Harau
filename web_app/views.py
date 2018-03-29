import imghdr

from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField
from wtforms import TextAreaField, ValidationError
from wtforms.widgets import TextArea


class CKEditorWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += " ckeditor"
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKEditorWidget, self).__call__(field, **kwargs)

class CKEditorField(TextAreaField):
    widget = CKEditorWidget()

class PageModelView(ModelView):
    form_overrides = dict(konten=CKEditorField)

    create_template = 'admin/ckeditor.html'
    edit_template = 'admin/ckeditor.html'
    list_kolom = ('title' 'tag')


class MenuModelView(ModelView):
    pass


class UserAdminView(ModelView):

   def picture_validation(form, field):
      if field.data:
         filename = field.data.filename
         if filename[-4:] != '.jpg':
            raise ValidationError('file must be .jpg')
         if imghdr.what(field.data) != 'jpeg':
            raise ValidationError('file must be a valid jpeg image.')
      field.data = field.data.stream.read()
      return True

   form_columns = ['id','url_pic', 'pic']
   column_labels = dict(id='ID', url_pic="Picture's URL", pic='Picture')

   def pic_formatter(view, context, model, name):
       return 'NULL' if len(getattr(model, name)) == 0 else 'a picture'

   column_formatters =  dict(pic=pic_formatter)
   form_overrides = dict(pic= FileUploadField)
   form_args = dict(pic=dict(validators=[picture_validation]))
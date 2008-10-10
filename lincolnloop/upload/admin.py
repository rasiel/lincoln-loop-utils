from django import forms
from django.conf import settings
from django.contrib import admin

from lincolnloop.upload.models import FileUpload
from lincolnloop.upload.widgets import AdminImageWidget

class FileUploadForm(forms.ModelForm):
    upload = forms.FileField(widget=AdminImageWidget, required=False)
    class Media:
        js = ['%supload_media/jquery.js' % settings.GONDOLA_MEDIA_URL,
              '%supload_media/photo-edit.js' % settings.GONDOLA_MEDIA_URL,]

    class Meta:
        model = FileUpload

class FileUploadAdmin(admin.ModelAdmin):
    form = FileUploadForm
    list_display = ('title', 'upload_date', 'upload', 'mime_type')

admin.site.register(FileUpload, FileUploadAdmin)

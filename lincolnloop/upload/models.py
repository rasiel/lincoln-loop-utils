from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
import mimetypes

class FileUpload(models.Model):
    upload_date = models.DateTimeField(auto_now_add=True)
    upload = models.FileField(upload_to="uploads")
    title = models.CharField(max_length=100)
    description = models.CharField(blank=True, max_length=200)
    content_type = models.CharField(editable=False, max_length=100)
    sub_type = models.CharField(editable=False, max_length=100)

    class Meta:
        ordering = ['upload_date', 'title']

    def __unicode__(self):
        return self.title

    def mime_type(self):
        return '%s/%s' % (self.content_type, self.sub_type)

    def type_slug(self):
        return slugify(self.sub_type)

    def is_image(self):
        return self.content_type == 'image'

    def get_absolute_url(self):
        return '%s%s' % (settings.MEDIA_URL, self.upload)

    def save(self, force_insert=False, force_update=False):
        file_path = '%s%s' % (settings.MEDIA_ROOT, self.upload)
        (mime_type, encoding) = mimetypes.guess_type(file_path)
        try:
            [self.content_type, self.sub_type] = mime_type.split('/')
        except:
            self.content_type = 'text'
            self.sub_type = 'plain'
        super(FileUpload, self).save(force_insert, force_update)

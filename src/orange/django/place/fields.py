'''
Created on 2011-5-16

@author: James
'''
from PIL import Image
from django.db import models
from django.db.models.fields.files import ImageFieldFile
import os.path

class ThumbnailImageFieldFile(ImageFieldFile):

    def _get_thumb_path(self):
        return __add_thumb(self.path)

    def _get_thumb_url(self):
        return __add_thumb(self.url)

    thumb_path = property(_get_thumb_path)
    thumb_url = property(_get_thumb_url)

    def save(self, name, content, save=True):
        super(ThumbnailImageFieldFile, self).save(name, content, save)
        img = Image.open(self.path)
        img.thumbnail((self.field.thumb_width, self.field.thumb_height), Image.ANTIALIAS)
        img.save(self.thumb_path, 'JPEG')

    def delete(self, save=True):
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super(ThumbnailImageFieldFile, self).delete(save)

class ThumbnailImageField(models.ImageField):

    attr_class = ThumbnailImageFieldFile

    def __init__(self, thumb_width=128, thumb_height=128, *args, **kwargs):
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height
        super(ThumbnailImageField, self).__init__(*args, **kwargs)

def __add_thumb(image_nmae):
    parts = image_nmae.split('.')
    parts.insert(-1, 'thumb')
    if parts[-1].lower() not in ['jpeg', 'jpg']:
        parts[-1] = 'jpg'
    return '.'.join(parts)
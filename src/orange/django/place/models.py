'''
Created on 2011-5-1

@author: James
'''
from django.contrib import admin
from django.db import models
from django.db.models import permalink
from django.db.models.base import ModelState
from django.db.models.fields.files import ImageFieldFile
from django.db.models.query import QuerySet
from orange.django.place.fields import ThumbnailImageField

class User(models.Model):
    login_id = models.CharField(max_length=50)
    login_id_type = models.IntegerField()
    device_id = models.CharField(max_length=150)
    device_model = models.CharField(max_length=50)
    device_os = models.IntegerField()
    country_code = models.CharField(max_length=20)
    language = models.CharField(max_length=20)
    device_token = models.CharField(max_length=150)
    email = models.EmailField()
    create_date = models.DateTimeField()

class Place(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    app_id = models.CharField(max_length=50)
    create_date = models.DateTimeField()
    post_type = models.IntegerField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    radius = models.IntegerField()
    desc = models.CharField(max_length=100)

class Post(models.Model):
    user_id = models.CharField(max_length=100)
    app_id = models.CharField(max_length=50)
    place_id = models.CharField(max_length=100)
    content_type = models.IntegerField()
    text_content = models.CharField(max_length=200)
    create_date = models.DateTimeField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    user_longitude = models.FloatField()
    user_latitude = models.FloatField()

class Photo(models.Model):
    object_id = models.CharField(max_length=100)
    caption = models.CharField(max_length=250, blank=True)
    image = ThumbnailImageField(upload_to='photos')

    @classmethod
    def json_default(cls, obj):
        if isinstance(obj, QuerySet):
            return [entity for entity in obj]
        if isinstance(obj, models.Model):
            return obj.to_dict()
        raise TypeError(repr(obj) + ' is not JSON serializable')

    def to_dict(self):
        dict = {}
        for name in self.__dict__.keys():
            column = self.__getattribute__(name)
            if isinstance(column, ImageFieldFile):
                dict['url'] = column.url
                dict['thumb_url'] = column.thumb_url
            elif isinstance(column, ModelState) or name == '_entity_exists':
                continue
            elif name == '_original_pk':
                dict['id'] = column
            else:
                dict[name] = column
        return dict

    @permalink
    def get_absolute_url(self):
        return ('place.photo.views.get', None, {'post_id': self.post_id})

class UserAdmin(admin.ModelAdmin):
    list_display =('login_id', 'login_id_type', 'device_model')

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('object_id', 'image', 'caption')

admin.site.register(User, UserAdmin)
admin.site.register(Photo, PhotoAdmin)
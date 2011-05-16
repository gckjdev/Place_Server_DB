'''
Created on 2011-5-1

@author: James
'''
from django.db import models

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
    register_time = models.DateTimeField()

class Place(models.Model):
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    caption = models.CharField(max_length=100)
    create_time = models.DateTimeField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()

class Post(models.Model):
    author = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    thread_id = models.CharField(max_length=100)
    create_time = models.DateTimeField()
    longitude = models.FloatField()
    latitude = models.FloatField()


'''
Created on 2011-5-1

@author: James
'''
from orange.cassandra.orm import Model
import pycassa

class User(Model):
    '''
    classdocs
    '''
    name = pycassa.String()
    email = pycassa.String()
    register_time = pycassa.DateTime()
    
class Place(Model):
    '''
    classdocs
    '''
    name = pycassa.String()
    owner = pycassa.String()
    caption = pycassa.String()
    create_time = pycassa.DateTime()
    longitude = pycassa.FloatString()
    latitude = pycassa.FloatString()

class Post(Model):
    '''
    classdocs
    '''
    author = pycassa.String()
    content = pycassa.String()
    thread_id = pycassa.String()
    create_time = pycassa.DateTime()
    longitude = pycassa.FloatString()
    latitude = pycassa.FloatString()


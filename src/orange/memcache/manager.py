'''
Created on 2011-5-1

@author: James
'''
import memcache

def get_client():
    return memcache.Client(['192.168.1.52:11211'], debug=1)
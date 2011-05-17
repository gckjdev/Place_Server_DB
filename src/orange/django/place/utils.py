'''
Created on 2011-5-16

@author: James
'''
from django.http import HttpResponse
import json

def get_json_response(obj, cls=None):
    json_default = None
    if cls:
        json_default = cls.json_default
    json = to_json(obj, json_default)
    print json
    return HttpResponse(json, content_type='application/json')

def to_json(obj, default=None):
    return json.dumps(obj, default=default)

def _add_thumb(s):
    parts = s.split('.')
    parts.insert(-1, 'thumb')
    if parts[-1].lower() not in ['jpeg', 'jpg']:
        parts[-1] = 'jpg'
    return '.'.join(parts)

class IndexColumnFamily():
    IDX_DEVICE_ID = 'idx_device_id'
    IDX_LOGIN_ID = 'idx_login_id'
    IDX_USER_OWN_PLACES = 'idx_user_own_places'

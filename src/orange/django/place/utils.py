'''
Created on 2011-5-16

@author: James
'''
import json

def to_json(cls, obj):
    return json.dumps(obj, default=cls.json_default)

def _add_thumb(s):
    parts = s.split('.')
    parts.insert(-1, 'thumb')
    if parts[-1].lower() not in ['jpeg', 'jpg']:
        parts[-1] = 'jpg'
    return '.'.join(parts)

class IndexColumnFamily():
    IDX_DEVICE_TOKEN = 'idx_device_token'
    IDX_LOGIN_ID = 'idx_login_id'

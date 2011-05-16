'''
Created on 2011-5-16

@author: James
'''
import json

def to_json(cls, obj):
    return json.dumps(obj, default=cls.json_default)

class IndexColumnFamily():
    IDX_DEVICE_TOKEN = 'idx_device_token'
    IDX_LOGIN_ID = 'idx_login_id'

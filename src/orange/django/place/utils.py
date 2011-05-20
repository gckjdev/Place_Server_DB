'''
Created on 2011-5-16

@author: James
'''
from django.http import HttpResponse
import json
import logging
import os
import sys

__logger = logging.getLogger(__name__)

def get_json_response(obj, cls=None):
    json_default = None
    if cls:
        json_default = cls.json_default
    obj_json = json.dumps(obj, default=json_default)
    __logger.debug('[SEND] %s' % obj_json)
    return HttpResponse(obj_json, content_type='application/json')

def get_dj_settings():
    settings = os.environ['DJANGO_SETTINGS_MODULE']
    if settings:
        __import__(settings)
        return sys.modules[settings]


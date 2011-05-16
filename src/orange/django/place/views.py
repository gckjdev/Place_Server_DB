'''
Created on 2011-5-16

@author: James
'''
from django.http import HttpResponse
from orange.django.place.utils import to_json

def get_json_response(cls, obj):
    return HttpResponse(to_json(cls, obj), content_type='application/json')
'''
Created on 2011-5-16

@author: James
'''

class ErrorException(Exception):
    code = 0
    def __init__(self, error_code):
        self.code = error_code

# How to Import Me?
# from orange.place import *

ERROR_SUCCESS = 0

# Parameter Error
ERROR_PARAMETER                 = 10001

# User Errors
ERROR_LOGINID_EXIST             = 20001
ERROR_DEVICEID_EXIST            = 20002
ERROR_LOGINID_DEVICE_BOTH_EXIST = 20003  
ERROR_USERID_NOT_FOUND          = 20004

# Place Error
ERROR_PLACE_NAME_EXIST          = 30001
ERROR_PLACE_NOT_FOUND           = 30002

# Post Error
ERROR_POST_NOT_FOUND            = 40001

# DB Error
ERROR_CASSANDRA                 = 80001

# System Error
ERROR_SYSTEM                    = 90001

# The following Erros are to be deleted
PARAM_ERROR = 4002
AUTH_ERROR = 4003

INTERNAL_ERROR = 5001
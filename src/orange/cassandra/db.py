'''
Created on 2011-5-5

@author: James
'''
from orange.django.place.utils import get_dj_settings
from orange.logging import paramlog
from pycassa.cassandra.ttypes import NotFoundException
import logging
import pycassa

__logger = logging.getLogger(__name__)

__servers = ['localhost:9160']
__keyspace = 'PlaceKS'
settings = get_dj_settings()
if settings:
    db = settings.DATABASES['default']
    __servers = [db['HOST'] + ':' + db['PORT']]
    __keyspace = db['NAME']

__pool = pycassa.connect(__keyspace, __servers)

def get_column_family(cf_name):
    return pycassa.ColumnFamily(__pool, cf_name, autopack_names=False, autopack_values=False)

def get_column_family_map(cls):
    return pycassa.ColumnFamilyMap(cls, get_column_family(cls.__name__))

def create_index_clause(conditions):
    expressions = []
    for condition in conditions:
        expression = pycassa.create_index_expression(condition[0], condition[1], op=condition[2])
        expressions.append(expression)
    return pycassa.create_index_clause(expressions)

@paramlog
def set_column_value(cf_name, key, column_name, value):
    cf = pycassa.ColumnFamily(__pool, cf_name)
    cf.insert(key, {column_name: value})

@paramlog
def get_column_count(cf_name, key):
    cf = pycassa.ColumnFamily(__pool, cf_name)
    cf.get_count(key)

@paramlog
def get_columns(cf_name, key, column_start='', column_count=30):
    cf = pycassa.ColumnFamily(__pool, cf_name)
    try:
        ret = cf.get(key, column_reversed=True, column_start=column_start, column_count=column_count)
    except NotFoundException:
        ret = {}
    return ret

@paramlog
def multi_get(cf_name, keys):
    cf = pycassa.ColumnFamily(__pool, cf_name)
    return cf.multiget(keys)


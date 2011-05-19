'''
Created on 2011-5-5

@author: James
'''
import pycassa
from pycassa.cassandra.ttypes import NotFoundException

def get_pool(keyspace='PlaceKS', servers=['192.168.1.101:9160']):
    return pycassa.connect(keyspace, servers)

def get_column_family(cf_name):
    return pycassa.ColumnFamily(get_pool(), cf_name, autopack_names=False, autopack_values=False)

def get_column_family_map(cls):
    return pycassa.ColumnFamilyMap(cls, get_column_family(cls.__name__))

def create_index_clause(conditions):
    expressions = []
    for condition in conditions:
        expression = pycassa.create_index_expression(condition[0], condition[1], op=condition[2])
        expressions.append(expression)
    return pycassa.create_index_clause(expressions)

def set_column_value(cf_name, key, column_name, value):
    print 'set_column_value, cf_name=', cf_name, ',key=', key, ",column_name=", column_name, ',value=', value
    cf = pycassa.ColumnFamily(get_pool(), cf_name)
    cf.insert(key, {column_name: value})

def get_column_count(cf_name, key):
    cf = pycassa.ColumnFamily(get_pool(), cf_name)
    cf.get_count(key)

def get_columns(cf_name, key, column_start='', column_count=30):
    cf = pycassa.ColumnFamily(get_pool(), cf_name)
    try:
        ret = cf.get(key, column_reversed=True, column_start=column_start, column_count=column_count)
    except NotFoundException:
        ret = {}
    return ret

def multi_get(cf_name, keys):
    cf = pycassa.ColumnFamily(get_pool(), cf_name)
    return cf.multiget(keys)

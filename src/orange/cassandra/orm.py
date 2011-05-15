'''
Created on 2011-5-5

@author: James
'''
from orange.cassandra import db
from pycassa.types import Column
import uuid

class Model(object):

    @classmethod
    def all(cls):
        column_family_map = db.get_column_family_map(cls)
        return column_family_map.get_range()

    @classmethod
    def store(cls, instance):
        column_family_map = db.get_column_family_map(cls)
        instance.key = cls.generateKey()
        column_family_map.insert(instance)
        return instance.key

    @classmethod
    def get(cls, key):
        column_family_map = db.get_column_family_map(cls)
        return column_family_map.get(key)

    @classmethod
    def find(cls, conditions):
        column_family_map = db.get_column_family_map(cls)
        index_clause = db.create_index_clause(conditions);
        return column_family_map.get_indexed_slices(index_clause)

    @classmethod
    def generateKey(cls):
        return uuid.uuid1().get_hex()

    @classmethod
    def json_default(cls, obj):
        if obj.__class__.__name__ == 'generator':
            return list(obj)
        if isinstance(obj, Model):
            return obj.to_dict()
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        raise TypeError(repr(obj) + ' is not JSON serializable')

    def to_dict(self):
        dict = {'key': self.key}
        for name, column in self.__class__.__dict__.iteritems():
            if isinstance(column, Column):
                dict[name] = self.__getattribute__(name)
        return dict


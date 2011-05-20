'''
Created on 2011-5-3

@author: James
'''
from datetime import datetime
from orange.cassandra import db
from orange.django.place import IdxCF
from orange.django.place.models import Post, Place
from orange.place import errors
from orange.place.errors import ErrorException
import logging
import uuid

__logger = logging.getLogger(__name__)

def register_user(user): 
    di_count = db.get_column_count(IdxCF.IDX_DEVICE_ID, user.device_id)
    li_count = db.get_column_count(IdxCF.IDX_LOGIN_ID, user.login_id)
    #__logger.debug('<register_user> device count=%d, login_id count=%d' % (di_count, li_count))    
    if di_count > 0 and li_count > 0:
        __logger.warning('<register_user> login_id(%s) and device(%s) both exist' % (user.login_id, user.device_id))
        raise ErrorException(errors.ERROR_LOGINID_DEVICE_BOTH_EXIST)
    elif li_count > 0:
        __logger.warning('<register_user> login_id(%s) exist' % user.login_id)
        raise ErrorException(errors.ERROR_LOGINID_EXIST)
    elif di_count > 0: 
        __logger.warning('<register_user> device(%s) exist' % user.device_id)
        raise ErrorException(errors.ERROR_DEVICEID_EXIST) 
    user.create_date = datetime.utcnow()
    user.save()
    db.set_column_value(IdxCF.IDX_DEVICE_ID, user.device_id, user.id, '')
    db.set_column_value(IdxCF.IDX_LOGIN_ID, user.login_id, user.id, '')

def new_place(place):
    place.create_date = datetime.utcnow()
    place.save()
    db.set_column_value(IdxCF.IDX_USER_OWN_PLACES, place.user_id, uuid.UUID(place.id), '')

def new_post(post):
    post.create_date = datetime.utcnow()
    post.save()
    db.set_column_value(IdxCF.IDX_PLACE_POSTS, post.place_id, uuid.UUID(post.id), '')
    db.set_column_value(IdxCF.IDX_USER_POSTS, post.user_id, uuid.UUID(post.id), '')
    followed_count = db.get_column_count(IdxCF.IDX_PLACE_FOLLOWED_USERS, post.place_id)
    if followed_count > 0:
        user_id_dict = db.get_columns(IdxCF.IDX_PLACE_FOLLOWED_USERS, post.place_id, column_count=followed_count)
        for user_id in user_id_dict.keys():
            db.set_column_value(IdxCF.IDX_USER_TIMELINE, str(user_id), uuid.UUID(post.id), '')

def reply_post(place_id, post_id, reply):
    reply.thread_id = post_id
    new_post(place_id, reply)
    db.set_column_value('PostReplies', post_id, uuid.UUID(reply.id), '')

def get_entity(cls, key):
    return cls.objects.get(key)

def get_all_entities(cls):
    return cls.objects.all()

def get_place_posts(place_id, before, max_count):
    if (before) or (len(before) == 0):
        start_column = ""
    else:
        start_column = uuid.UUID(before)

    post_id_dict = db.get_columns(IdxCF.IDX_PLACE_POSTS, place_id, column_start=start_column, column_count=max_count)

    return [Post.objects.get(id=key) for key in post_id_dict.keys()];

def get_nearby_places(latitude, longtitude):
    return Place.objects.all() #TODO: 

def user_follow_place(user_id, place_id):
    db.set_column_value(IdxCF.IDX_USER_FOLLOW_PLACES, user_id, uuid.UUID(place_id), '')
    db.set_column_value(IdxCF.IDX_PLACE_FOLLOWED_USERS, place_id, uuid.UUID(user_id), '')

def get_post_replies(post_id):
    reply_id_dict = db.get_columns('PostReplies', post_id)
    replies = []
    for key in reply_id_dict.keys():
        reply = Post.objects.get(key.get_hex())
        replies.append(reply)
    return replies

def get_user_post():
    pass

def get_timeline():
    pass


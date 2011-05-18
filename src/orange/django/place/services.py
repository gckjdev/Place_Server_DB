'''
Created on 2011-5-3

@author: James
'''
from datetime import datetime
from orange.cassandra import db
from orange.django.place.exceptions import UserExistError
from orange.django.place.models import Post
from orange.django.place.utils import IndexColumnFamily
import uuid

def register_user(user):
    di_count = db.get_column_count(IndexColumnFamily.IDX_DEVICE_ID, user.device_id)
    if di_count > 0:
        raise UserExistError
    li_count = db.get_column_count(IndexColumnFamily.IDX_LOGIN_ID, user.device_id)
    if li_count > 0:
        raise UserExistError
    user.register_time = datetime.utcnow()
    user.save()
    db.set_column_value(IndexColumnFamily.IDX_DEVICE_ID, user.device_id, user.id, '')
    db.set_column_value(IndexColumnFamily.IDX_LOGIN_ID, user.login_id, user.id, '')

def new_place(place):
    place.create_time = datetime.utcnow()
    place.save()
    db.set_column_value(IndexColumnFamily.IDX_USER_OWN_PLACES, place.id, '')

def new_post(post):
    post.create_time = datetime.utcnow()
    post.save()
    db.set_column_value(IndexColumnFamily.IDX_PLACE_POSTS, post.place_id, uuid.UUID(post.id), '')
    db.set_column_value(IndexColumnFamily.IDX_USER_POSTS, post.user_id, uuid.UUID(post.id), '')

def reply_post(place_id, post_id, reply):
    reply.thread_id = post_id
    new_post(place_id, reply)
    db.set_column_value('PostReplies', post_id, uuid.UUID(reply.id), '')

def get_entity(cls, key):
    return cls.objects.get(key)

def get_all_entities(cls):
    return cls.objects.all()

def get_place_posts(place_id):
    post_id_dict = db.get_columns('PlacePosts', place_id)
    posts = []
    for key in post_id_dict.keys():
        post = Post.objects.get(key.get_hex())
        posts.append(post)
    return posts;

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


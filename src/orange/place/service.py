'''
Created on 2011-5-3

@author: James
'''
from datetime import datetime
from orange.cassandra import db
from orange.place.model import Post, Place, User
import uuid

def register_user(user):
    user.register_time = datetime.now()
    User.store(user)

def new_place(place):
    place.create_time = datetime.now()
    Place.store(place)

def new_post(place_id, post):
    post.create_time = datetime.now()
    Post.store(post)
    db.set_column_value('PlacePosts', place_id, uuid.UUID(post.key), '')

def reply_post(place_id, post_id, reply):
    reply.thread_id = post_id
    new_post(place_id, reply)
    db.set_column_value('PostReplies', post_id, uuid.UUID(reply.key), '')

def get_place(key):
    return Place.get(key)

def get_post(key):
    return Post.get(key)

def get_place_list():
    return Place.all()

def get_place_posts(place_id):
    post_id_dict = db.get_columns('PlacePosts', place_id)
    posts = []
    for key in post_id_dict.keys():
        post = Post.get(key.get_hex())
        posts.append(post)
    return posts;

def get_post_replies(post_id):
    reply_id_dict = db.get_columns('PostReplies', post_id)
    replies = []
    for key in reply_id_dict.keys():
        reply = Post.get(key.get_hex())
        replies.append(reply)
    return replies

def get_user_post():
    pass

def get_timeline():
    pass


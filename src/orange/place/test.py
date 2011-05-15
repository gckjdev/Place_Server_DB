# -*- coding: utf-8 -*-
'''
Created on 2011-4-24

@author: James
'''
from orange.place import service
from orange.place.model import Post, Place, User

def main():
    user = User()
    user.email = 'tom@abc.com'
    user.name = 'Tom'
    service.register_user(user)

    place = Place()
    place.name = 'City Plazza'
    place.owner = 'Tom'
    service.new_place(place)

    post = Post()
    post.author = 'Tom'
    post.content = '吃饭的有木有'
    service.new_post(place.key, post)

    reply = Post()
    reply.author = 'Ken'
    reply.content = '都城的有木有'
    service.reply_post(place.key, post.key, reply)

if __name__ == "__main__":
    main()
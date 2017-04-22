#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import json
import requests
from pymongo import MongoClient
from InstagramAPI import InstagramAPI

# TODO: Fill in username and password
InstagramAPI = InstagramAPI("<username>", "<password>")
InstagramAPI.login()

users = [
    'yiyun.zhu',
    'dd_max_',
]
url_get_user_id = 'https://www.instagram.com/{0}/?__a=1'

# MongoDB
client = MongoClient("localhost", 27017, connect=False)
db = client.instagram
summary = db.summary

for user in users:
    print 'Fetching ' + user

    content = json.loads(requests.get(url_get_user_id.format(user)).content)
    user_id = str(content.get('user').get('id'))
    user_feeds = InstagramAPI.getTotalUserFeed(user_id)

    feeds = len(user_feeds)
    likes = 0
    comments = 0
    reviews = 0
    for feed in user_feeds:
        likes += feed.get('like_count', 0)
        comments += feed.get('comment_count', 0)

    print 'feeds: ' + str(feeds) \
          + ', likes: ' + str(likes) \
          + ', comments: ' + str(comments)

    # Restore data
    summary.insert({
        'user': user,
        'feeds': feeds,
        'likes': likes,
        'comments': comments,
        'reviews': reviews,
    })

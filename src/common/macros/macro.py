#coding=utf-8
from collections import OrderedDict

USERS_PER_PAGE = 20

ADDITIVES_PER_PAGE = 10

FOODS_PER_PAGE = 15

MAX_PAGE = 15

MAX_FOLLOW_NUM = 450

BLOG_POSTS_PER_PAGE = 10

ACTIVITY_PER_PAGE = 20

PASSWORD_SALT = '!QAZ@WSXcde3)Okm9i'

MAX_UPLOAD_SIZE = 10

MAX_AVATAR_SIZE = 2

HOT_ADDITIVE_INTERVAL = 300

HOT_FOOD_INTERVAL = 300

EVENTS = {
    'USER_ACTIVATION': 'user_activation',
    'USER_CREATE': 'user_create',
    'USER_FOLLOW': 'user_follow',
    'USER_UNFOLLOW': 'user_unfollow',
    'FOOD_LIKE': 'food_like',
    'FOOD_UNLIKE': 'food_unlike',
    'FOOD_CREATE': 'food_create',
    'FOOD_UPLOAD': 'food_upload',
    'FOOD_DELETE': 'food_delete',
    'FOOD_COMMENT_ADD': 'food_comment_add',
    'FOOD_COMMENT_DELETE': 'food_comment_delete',
    'ADDITIVE_LIKE': 'additive_like',
    'ADDITIVE_UNLIKE': 'additive_unlike',
    'ADDITIVE_CREATE': 'additive_create',
    'ADDITIVE_UPLOAD': 'additive_upload',
    'ADDITIVE_DELETE': 'additive_delete',
    'ADDITIVE_COMMENT_ADD': 'additive_comment_add',
    'ADDITIVE_COMMENT_DELETE': 'additive_comment_delete',
    'BLOG_ADD': 'blog.after_insert',
    'BLOG_EDIT': 'blog.after_update',
    'BLOG_DELETE': 'blog_delete',
    'BLOG_COMMENT_ADD': 'blog_comment.after_insert',
}

ACTIVITY_ACTION = {
    'ADDITIVE_CREATE': 100,
    'ADDITIVE_LIKE': 101,
    'ADDITIVE_UNLIKE': 103,
    'ADDITIVE_COMMENT_ADD': 104,
    'ADDITIVE_COMMENT_DELETE': 105,
    'ADDITIVE_DELETE': 106,
    'FOOD_CREATE': 100,
    'FOOD_LIKE': 101,
    'FOOD_UNLIKE': 103,
    'FOOD_COMMENT_ADD': 104,
    'FOOD_COMMENT_DELETE': 105,
    'FOOD_DELETE': 106,
    'USER_CREATE': 200,
    'USER_ACTIVATION': 201,
    'USER_FOLLOW': 202,
    'USER_UNFOLLOW': 203,
    'BLOG_ADD': 301,
    'BLOG_EDIT': 302,
    'BLOG_DELETE': 303,
    'BLOG_COMMENT_ADD': 304,
}

AVATAR_SIZE = {
    's': '48x48^',
    'm': '100x100^',
    'l': '160x160^',
}

PHOTO_SIZE = {
    's': '70x70^',
    'm': '215x215^',
    'l': '1200x12000',
}

ADDITIVE_STATS = 'addi_stats'
FOOD_STATS = 'addi_stats'

REDIS_KEY = {
    'FOOD_COUNT': 'h_food_cnt',
    'ADDITIVE_COUNT': 'h_addi_cnt',
    'USER_LIKED_COUNT': 'h_usr_lkd_cnt', # 被喜欢的次数
    'USER_LIKES_COUNT': 'h_usr_lks_cnt', # 喜欢的照片的张数
    'TABLE_ITEMS': 'h_tbl_tms:{table}',
    'USER_MESSAGE': 'l_usr_msg:{user_id}',
    'HOT_SEARCHS': 'set_hot_searchs',
}

USER_LEVEL = [0, 10, 100, 500, 1000]
USER_LEVEL_CN = [u'小兔崽', u'功夫兔', u'普京兔', u'流氓兔', u'无敌兔']
USER_LEVEL_PHOTOS_PER_WEEK = [10, 20, 30, 40, 50]

INVITE_NUM = [5, 10, 15, 20, 25]

#coding=utf-8
import math
import datetime
import shutil
import time
import urllib2
import os
import re
import redis
import logging
import uuid
from hashlib import sha1
import subprocess
from collections import OrderedDict
from itertools import repeat

from tornado import escape
from tornado.options import options
from macros.macro import PASSWORD_SALT, AVATAR_SIZE, USER_LEVEL

def hash_password(password):
    return sha1('{password}{salt}'.format(
        password = sha1(password).hexdigest(),
        salt = PASSWORD_SALT)).hexdigest()

def gen_invite_key():
    return sha1(str(uuid.uuid4())).hexdigest()[:16]

def _process(body, base_save_path, size, user_id):
    hashval = sha1(body).hexdigest()[:17]
    save_path = os.path.join(base_save_path, str(user_id), hashval)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    origin_path = '{0}/{1}.jpg'.format(save_path, sha1(hashval+PASSWORD_SALT).hexdigest()[:17])
    with open(origin_path, 'wb') as f:
        f.write(body)

    for size_name, size_val in size.items():
        _save_path = os.path.join(save_path, '{0}.jpg'.format(size_name))
        if size_val[-1:] == '^':
            convert_cmd = ['convert', origin_path, '-resize', '%s^'%size_val,
                    '-gravity', 'Center', '-extent', size_val[:-1], _save_path]
        else:
            process = subprocess.Popen("identify " + origin_path + " | awk '{print $3}'", shell=True, stdout = subprocess.PIPE)
            width, height = process.communicate()[0][:-1].split('x')
            if int(width) > int(size_val.split('x')[0]):
                convert_cmd = ['convert', origin_path, '-resize', size_val, _save_path]
            else:
                shutil.copy2(origin_path, _save_path)

        proc = subprocess.Popen(convert_cmd)
        proc.communicate()
        if proc.returncode != 0:
            logging.error('convert thumbnail failed')
    return hashval

def process_photo_url(url, user_id):
    try_num = 3
    result = None
    for i in range(try_num):
        try:
            result = urllib2.urlopen(url).read()
            break
        except Exception:
            continue
    if result:
        return _process(result, options.photo_save_path, PHOTO_SIZE, user_id)
    return False

def process_photo(body, user_id):
    return _process(body, options.photo_save_path, PHOTO_SIZE, user_id)

def process_avatar(body, user_id):
    return _process(body, options.avatar_save_path, AVATAR_SIZE, user_id)

def get_additive_detail(hashval, user_id):
    additive_path = os.path.join(options.additive_save_path, str(user_id), hashval, 'm.jpg')
    process = subprocess.Popen("""identify -format "%[DETAIL:*]%" """ + additive_path + """ | sed 's/\(.\{46\}\).*/\1/'""", shell=True, stdout = subprocess.PIPE)
    result = process.communicate()
    details = [item for item in result[0].split('\n') if len(item) > 5]
    meta = ('Make', 'Model', 'FocalLength', 'FNumber', 'ExposureTime',
            'ISOSpeedRatings', 'DateTimeOriginal')
    detail_dict = OrderedDict(zip(meta, repeat('', len(meta) - 1)))
    for detail in details:
        key,val = detail.split('=')
        key = key[5:]
        if key in meta:
            detail_dict[key] = val

    return detail_dict

def get_food_part(hashval, user_id):
    food_path = os.path.join(options.food_save_path, str(user_id), hashval, 'm.jpg')
    process = subprocess.Popen("""identify -format "%[PART:*]%" """ + food_path + """ | sed 's/\(.\{46\}\).*/\1/'""", shell=True, stdout = subprocess.PIPE)
    result = process.communicate()
    parts = [item for item in result[0].split('\n') if len(item) > 5]
    meta = ('Make', 'Model', 'FocalLength', 'FNumber', 'ExposureTime',
            'ISOSpeedRatings', 'DateTimeOriginal')
    part_dict = OrderedDict(zip(meta, repeat('', len(meta) - 1)))
    for part in parts:
        key,val = part.split('=')
        key = key[5:]
        if key in meta:
            part_dict[key] = val

    return part_dict

def nl2br(content):
    content = escape.xhtml_escape(content)
    return content.replace('\n', '<br />')

def keep_order(result, field, order_list):
    current_order = {}
    for item in result:
        current_order[getattr(item, field)] = attr_dict(item.to_dict())

    ordered_result = []
    for item in order_list:
        ordered_result.append(current_order[item])
    return ordered_result

def attr_dict(dct):
    class AttributeDict(dict):
        __getattr__ = dict.__getitem__
        __setattr__ = dict.__setitem__
    return AttributeDict(dct)

def get_redis_client():
    if not get_redis_client.__dict__.get('redis_client'):
        get_redis_client.__dict__['redis_client'] = redis.Redis(host = options.redis_host,
                                   port = options.redis_port,
                                   db = options.redis_db,
                                   password = options.redis_password)
    return get_redis_client.redis_client

def calculate_karma(search_count, created):
    return '%.4f' % (math.log(int(search_count)+1, 10) + (float(created) / 45000))

def calculate_user_level(user):
    liked_count = int(user.liked_count)
    for index, value in enumerate(USER_LEVEL):
        if liked_count == value:
            return index
        if liked_count < value:
            return index - 1

def set_message(handler, message, type = 'error'):
    handler.set_cookie('message', u'{0}|{1}'.format(type, message))

class cached_property(object):
    def __init__(self, func, name = None, doc = None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func

    def __get__(self, obj, type = None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.__name__, None)
        if value is None:
            value = self.func(obj)
            obj.__dict__[self.__name__] = value
        return value

def check_user_exists(func):
    import models
    def wrapper(self, username):
        user = models.User().find_by_username(username)
        if not user:
            return self.render('error/user_not_exists.html')
        self.user = user
        return func(self, username)
    return wrapper

def check_additive_permission(func):
    import models
    def wrapper(self, additive_id, *args, **kwargs):
        additive = models.Additive().find(additive_id)
        if not additive or additive.status != 0:
            return self.send_error_json({'message': 'additive not exists'})

        if additive.user_id != self.current_user.id:
            return self.send_error_json({'message': 'permission denied'})

        self.additive = additive
        return func(self, additive_id, *args, **kwargs)
    return wrapper

def check_food_permission(func):
    import models
    def wrapper(self, food_id, *args, **kwargs):
        food = models.Food().find(food_id)
        if not food or food.status != 0:
            return self.send_error_json({'message': 'food not exists'})

        if food.user_id != self.current_user.id:
            return self.send_error_json({'message': 'permission denied'})

        self.food = food
        return func(self, food_id, *args, **kwargs)
    return wrapper

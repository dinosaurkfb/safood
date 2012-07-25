#coding=utf-8
from urlparse import urlparse
import re
import markdown
import random
from datetime import datetime
import logging
from tornado.options import options
from macros.macro import REDIS_KEY
from utils import get_redis_client

def get_avatar_url(handler, user, size):
    if not user.avatar_hash:
        return '/static/img/default_avatar_{0}.jpg'.format(size)
    return 'http://{domain}/{user.id}/{user.avatar_hash}/{size}.jpg'.format(
        domain = options.avatar_domain,
        user = user,
        size = size)

def get_food_avatar_url(handler, user, size):
    if not user.avatar_hash:
        return '/static/img/default_food_avatar_{0}.jpg'.format(size)
    return 'http://{domain}/{user.id}/{user.avatar_hash}/{size}.jpg'.format(
        domain = options.avatar_domain,
        user = user,
        size = size)

def get_photo_url(handler, photo, size):
    return "http://{photo_domain}/{photo.user_id}/{photo.hash}/{size}.jpg".format(
            photo_domain = options.photo_domain,
            photo = photo,
            size = size)

def get_host(handler, url):
    host = urlparse(url).netloc
    host_sections = host.split('.')
    return '{0}.{1}'.format(host_sections[-2], host_sections[-1])

def get_message(handler):
    if handler.current_user:
        redis_client = get_redis_client()
        redis_key = REDIS_KEY['USER_MESSAGE'].format(user_id = handler.current_user.id)
        if redis_client.llen(redis_key):
            return redis_client.rpop(redis_key).split('|')

    message = handler.get_cookie('message')
    handler.clear_cookie('message')
    return message.split('|') if message else None

def timesince(handler, dt, default=u"just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    diff = datetime.now() - datetime.fromtimestamp(dt)
    
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        if period >= 1:
            return "%d %s ago" % (period, singular if period == 1 else plural)

    return default

def render_comment(handler, content):
    result = re.sub(r'@([^\(]+)\((.*?)\)', r'@<a href="/user/\2">\1</a>', content)
    return nl2br(handler, result)

def md2html(handler, content):
    return markdown.markdown(content)

def nl2br(handler, content):
    return content.replace("\n", '<br />')

def home_sentence(handler):
    sentences = [
            u'易粪而食，面对食品安全没人可以独善其身，驱猛兽而百姓宁，亮出你的态度！',
            u'多用天然添加剂，少用化学添加剂，不用伪劣添加剂',
            u'民以食为天，食以安为先',
            ]
    random.shuffle(sentences)
    return sentences[0]

def can_delete_photo(handler, photo):
    if handler.current_user and handler.current_user.id == photo.user_id:
        if not photo.likes_count and not photo.comments_count:
            return True
    return False

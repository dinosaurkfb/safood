#coding=utf-8
import time
import datetime
import logging
from blinker import signal
from formencode import validators

from macros.macro import EVENTS, REDIS_KEY
import models
from utils import get_redis_client, calculate_karma

additive_delete = signal(EVENTS['ADDITIVE_DELETE'])

class Additive(models.base.BaseThing):
    _additive_name_error = {'empty': u'添加剂名称不能为空'}
    _additive_effect_error = {'empty': u'添加剂功能不能为空'}

    name = validators.String(
            not_empty = True,
            strip = True,
            messages = _additive_name_error)

    effect = validators.String(
            not_empty = True,
            strip = True,
            messages = _additive_effect_error)

    def create(self):
        self.status = 0
        self.created = time.time()
        self.karma = calculate_karma(0, self.created)
        self.save()
        if self.saved:
            signal(EVENTS['ADDITIVE_CREATE']).send(self)
            return self.id

    def search(self, val):
        result = self.where('name', 'like', val)\
            .where('cns', 'like', val)\
            .or_findall()
        return result

    def delete(self):
        self.status = -1
        self.save()
        signal(EVENTS['ADDITIVE_DELETE']).send(self)

    def get_hot(self, limit, offset):
        return Additive().order_by('-karma').findall_by_status(0, limit = limit, offset = offset)

    def get_hot_count(self):
        return Additive().count_by_status(0)

    @property
    def creator(self):
        return models.User().find(self.user_id)


#coding=utf-8
import time
import datetime
import logging
from blinker import signal
from formencode import validators

from macros.macro import EVENTS, REDIS_KEY
import models
from utils import get_redis_client, calculate_karma

food_delete = signal(EVENTS['FOOD_DELETE'])

class Food(models.base.BaseThing):
    _food_name_error = {'empty': u'食品名称不能为空'}

    name = validators.String(
            not_empty = True,
            strip = True,
            messages = _food_name_error)

    def search(self, val):
        result = self.where('name', 'like', val)\
            .findall()
        return result

    def create(self):
        self.status = 0
        self.created = self.updated = time.time()
        self.karma = calculate_karma(0, self.created)
        self.save()
        if self.saved:
            signal(EVENTS['FOOD_CREATE']).send(self)
            return self.id

    def delete(self):
        self.status = -1
        self.save()
        signal(EVENTS['FOOD_DELETE']).send(self)

    def get_hot(self, limit, offset):
        return Food().order_by('-karma').findall_by_status(0, limit = limit, offset = offset)

    def get_hot_count(self):
        return Food().count_by_status(0)

    @property
    def creator(self):
        return models.User().find(self.user_id)


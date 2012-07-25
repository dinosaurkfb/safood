#coding=utf-8
import time
import datetime
import logging
from formencode import validators
from collections import OrderedDict

from macros.macro import EVENTS, REDIS_KEY
import models

class Food_Part(models.base.BaseThing):
    @property
    def creator(self):
        return models.User().find(self.user_id)

    def get(self, food_id):
        self.reset()
        meta_dict = OrderedDict()
        return self.where('food_id', '=', food_id).order_by('id').findall()

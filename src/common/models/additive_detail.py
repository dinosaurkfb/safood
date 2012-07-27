#coding=utf-8
import time
import datetime
import logging
from formencode import validators
from macros.macro import EVENTS, REDIS_KEY
import models

class Additive_Detail(models.base.BaseThing):
    @property
    def creator(self):
        return models.User().find(self.user_id)

    def get(self, additive_id):
        self.reset()
        meta_dict = {}
        meta = self.where('additive_id', '=', additive_id).find()
        for item in meta:
            meta_dict[item.key] = item.value
        return meta_dict

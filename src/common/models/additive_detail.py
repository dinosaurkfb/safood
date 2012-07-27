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
        meta = self.where('additive_id', '=', additive_id).find()
        meta_dict = meta.to_dict()
        return meta_dict if meta_dict else {k:None for k in self.columns}

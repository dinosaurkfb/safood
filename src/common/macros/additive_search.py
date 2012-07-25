#coding=utf-8
import time
from blinker import signal

from macros.macro import EVENTS
import models

additive_delete = signal(EVENTS['ADDITIVE_DELETE'])

class Additive_Search(models.base.BaseThing):
    def search(self, user_id, additive_id):
        searchd = self.where('user_id', '=', user_id)\
                    .where('additive_id', '=', additive_id)\
                    .find()
        if not searchd:
            self.reset()
            self.user_id = user_id
            self.additive_id = additive_id
            self.save()
            signal(EVENTS['ADDITIVE_SEARCH']).send(self)
            return self.saved
        return False

    def unsearch(self, user_id, additive_id):
        searchd = self.where('user_id', '=', user_id)\
                    .where('additive_id', '=', additive_id)\
                    .find()
        if searchd:
            signal(EVENTS['ADDITIVE_UNSEARCH']).send(self)
            self.reset()
            rowcount = self.where('user_id', '=', user_id)\
                .where('additive_id', '=', additive_id)\
                .delete()
            return rowcount
        return False

    @additive_delete.connect
    def _additive_delete(additive):
        Additive_Search().where('additive_id', '=', additive.id).delete()

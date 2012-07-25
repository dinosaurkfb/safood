#coding=utf-8
import time
import datetime
import logging
from formencode import validators
from collections import OrderedDict

import models

class Ingredient(models.base.BaseThing):
    @property
    def creator(self):
        return models.User().find(self.user_id)

    def get(self, part_id):
        self.reset()
        return self.where('part_id', '=', part_id).order_by('id').findall()
    def get_additive(self, part_id):
        searchs = self.query(
            '''
SELECT `id`, `name`
FROM `safood`.`additive` 
where id = any
(select t.additive_id from 
(SELECT   * FROM `safood`.`ingredient` where part_id = {0} ORDER BY `id` DESC)
as t)
                    '''.format(part_id)
            ).fetchall()
        return searchs

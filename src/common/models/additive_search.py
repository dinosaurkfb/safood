#coding=utf-8
import logging
import models
from utils import get_redis_client
from macros.macro import REDIS_KEY, EVENTS
from blinker import signal

class Additive_Search(models.base.BaseThing):
    @property
    def hot_searchs(self):
        searchs = self.query(
            '''
SELECT   `name`, `id`
FROM `safood`.`additive` 
where id = any
(select t.additive_id from 
(SELECT   * FROM `safood`.`additive_search` ORDER BY `search` DESC LIMIT 4)
as t)
                    '''
            ).fetchall()
        return searchs


#coding=utf-8
import logging
import tornado
import json
from handlers.base import BaseHandler
import models
from macros.macro import MAX_UPLOAD_SIZE, FOODS_PER_PAGE
from helpers import nl2br
from utils import get_food_part, check_food_permission

class SearchHandler(BaseHandler):
    def fill_food_label(self, food):
        return u'{{"label":"{0}", "category":"搜食品>>"}}'.format(food['name'])
    def fill_additive_label(self, additive):
        return u'{{"label":"{0}", "category":"搜添加剂>>"}}'.format(additive['name'])
    def get(self):
        search_key = self.get_argument('term', '')
        result = u'['
        food_matched = models.Food().search(u'%{0}%'.format(search_key))
        for f in food_matched.to_dict_list():
            result = result + self.fill_food_label(f) + u','

        additives_matched = models.Additive().search(u'%{0}%'.format(search_key))
        for a in additives_matched.to_dict_list():
            result = result + self.fill_additive_label(a) + u','

        if result[-1] == u',':
            result = result[:-1] + u']'
        else:
            result = result + u']'
        ret = [{"label":"annttop C13","category":"Products"}]
        test = '[{"label":"测试23", "category":"Additive"},{"label":"测试2", "category":"Additive"},{"label":"测试2", "category":"Additive"},{"label":"测试2", "category":"Additive"}]'
        print result
        return self.write(result)


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
        template_prefix = 'partial/' if self.is_ajax_request else ''
        search_key = self.get_argument('q', '')
        if search_key:
            food_matched = models.Food().search(u'%{0}%'.format(search_key))
            additives_matched = models.Additive().search(u'%{0}%'.format(search_key))
            return self.render(
                '{0}search_result.html'.format(template_prefix),
                key = search_key,
                foods = food_matched.to_dict_list(),
                additives = additives_matched.to_dict_list()
                )

        search_key = self.get_argument('term', '')
        if not search_key:
            return self.redirect(self.request.headers['Referer'])
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
        print result
        return self.write(result)

    def post(self):
        search_key = self.get_argument('q', '')
        if self.is_ajax_request:
            return self.send_success_json(location=u'/search_result?q={0}'.format(tornado.escape.url_escape(search_key)))
        else:
            print u'/search_result?q={0}'.format(search_key)
            print u'/search_result?q={0}'.format(tornado.escape.url_escape(search_key))
            return self.redirect(u'/search_result?q={0}'.format(tornado.escape.url_escape(search_key)))

# class SearchResultHandler(BaseHandler):
#     def get(self):
#         template_prefix = 'partial/' if self.is_ajax_request else ''
#         search_key = self.get_argument('q', '')
#         food_matched = models.Food().search(u'%{0}%'.format(search_key))
#         additives_matched = models.Additive().search(u'%{0}%'.format(search_key))
#         return self.render(
#             '{0}search_result.html'.format(template_prefix),
#             key = search_key,
#             foods = food_matched.to_dict_list(),
#             additives = additives_matched.to_dict_list()
#             )

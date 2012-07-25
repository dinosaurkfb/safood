#coding=utf-8
import logging
import tornado
import json
from handlers.base import BaseHandler, BaseAdditivesHandler, BaseUserAdditivesHandler
import models
from macros.macro import MAX_UPLOAD_SIZE, ADDITIVES_PER_PAGE
from helpers import nl2br
from utils import get_additive_detail, check_additive_permission

class AdditiveApiHandler(BaseHandler):
    def _incr_view_counts(self, additive):
        viewed_additive_ids = self.get_cookie('viewed_additive_ids', '').split(',')
        if str(additive.id) not in (viewed_additive_ids):
            viewed_additive_ids += [additive.id]
            additive.views_count += 1
            additive.save()
            self.set_cookie('viewed_additive_ids', ','.join(map(str, viewed_additive_ids)))

    def get(self):
        additive_id = self.get_argument('id', -1)
        additive = models.Additive().find(additive_id)
        if not additive or additive.status != 0:
            return self.send_error_json('additive_not_exists')

        self._incr_view_counts(additive)
        
        result = additive.to_dict()
        print(u"additive name:{0}".format(result['name']))
        del result['id']
        del result['user_id']
        del result['status']
        details = models.Additive_Detail().find(additive_id)
        if details:
            details_dict = details.to_dict()
            del details_dict['id']
            del details_dict['additive_id']
            result.update(details_dict)
        return self.write(result)


class AdditiveSearchApiHandler(BaseHandler):
#    @tornado.web.authenticated
    def post(self, additive_id):
        additive = models.Additive().find(additive_id)
        if not additive:
            return self.render('error/additive_not_exists.html')

        models.Additive_Search().search(self.current_user.id, additive_id)
        return self.send_success_json()

    def get(self):
        val = self.get_argument('q')
        additives = models.Additive().search(u'%{0}%'.format(val))
        return self.write({u'result': additives.to_dict_list()})

class HotAdditivesApiHandler(BaseAdditivesHandler):
    def get(self):
        return self._write('hot')

class LatestAdditivesApiHandler(BaseAdditivesHandler):
    def get(self):
        return self._write('latest')

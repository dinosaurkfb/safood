#coding=utf-8
import logging
import tornado
import json
from handlers.base import BaseApiHandler, BaseAdditivesApiHandler
import models
from macros.macro import MAX_UPLOAD_SIZE, ADDITIVES_PER_PAGE
from helpers import nl2br
from utils import get_additive_detail, check_additive_permission

class AdditiveApiHandler(BaseApiHandler):
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
            return self.write({})

        self._incr_view_counts(additive)
        
        result = additive.to_dict()
        del result['id']
        del result['user_id']
        del result['status']
        details = models.Additive_Detail().get(additive.id)
        if details:
            del details['id']
            del details['additive_id']
            result.update(details)
        return self.write(result)


class AdditiveSearchApiHandler(BaseApiHandler):
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

class HotAdditivesApiHandler(BaseAdditivesApiHandler):
    def get(self):
        return self._write('hot')

class LatestAdditivesApiHandler(BaseAdditivesApiHandler):
    def get(self):
        return self._write('latest')


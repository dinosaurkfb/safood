#coding=utf-8
import logging
import tornado
import json
from handlers.base import BaseHandler, BaseAdditivesHandler, BaseUserAdditivesHandler
import models
from macros.macro import MAX_UPLOAD_SIZE, ADDITIVES_PER_PAGE
from helpers import nl2br
from utils import get_additive_detail, check_additive_permission

class AdditiveHandler(BaseHandler):
    def _incr_view_counts(self, additive):
        viewed_additive_ids = self.get_cookie('viewed_additive_ids', '').split(',')
        if str(additive.id) not in (viewed_additive_ids):
            viewed_additive_ids += [additive.id]
            additive.views_count += 1
            additive.save()
            self.set_cookie('viewed_additive_ids', ','.join(map(str, viewed_additive_ids)))

    def get(self, additive_id):
        additive = models.Additive().find(additive_id)
        if not additive or additive.status != 0:
            return self.render('error/additive_not_exists.html')

        self._incr_view_counts(additive)
        
        return self.render('partial/additive.html',
                           additive = additive,
                           additive_detail = models.Additive_Detail().find(additive_id)
                           )

    @tornado.web.authenticated
    def post(self):
        additive = models.Additive(
                name = self.get_argument('name', ''),
                alias = self.get_argument('alias', ''),
                user_id = self.current_user.id,
                effect = self.get_argument('effect', ''),
                cns = self.get_argument('cns', ''),
                ins = self.get_argument('ins', ''),
                safe4child = self.get_argument('safe4child', ''),
                )
        additive_id = additive.create()

        if additive_id:
            additive.save()

            tags = self.get_argument('tag', '')
            if tags:
                for tag in tags.split(' '):
                    models.Additive_Tag(additive_id = additive_id, tag = tag).save()
            
            if self.get_argument('detail_adi', ''):
                for item in ('adi', 'ld50', 'apply_range', 'safe_status', 'using_status', 'safe_risk', 'safe_rank', 'preparation', 'preparation_short'):
                    value = self.get_argument('detail_{0}'.format(item), '')
                    models.Additive_Detail(
                            additive_id = additive_id,
                            key = item,
                            value = value).save()
            else:
                detail = get_additive_detail(additive.hash, self.current_user.id)
                for key, value in detail.items():
                    models.Additive_Detail(
                            additive_id = additive_id,
                            key = key,
                            value = value).save()

            self.send_success_json(location='/additive/{0}/via/mine'.format(additive_id))
        else:
            self.send_error_json(additive.errors)


class AdditiveUpdateHandler(BaseHandler):
    @check_additive_permission
    @tornado.web.authenticated
    def post(self, additive_id):
        title = self.get_argument('title', '')
        content = self.get_argument('content', '')
        if title:
            self.additive.title = title
            self.additive.content = content
            self.additive.save()
            return self.send_success_json()
        return self.send_error_json({'message': 'update failed'})

class AdditiveSearchHandler(BaseHandler):
#    @tornado.web.authenticated
    def post(self, additive_id):
        additive = models.Additive().find(additive_id)
        if not additive:
            return self.render('error/additive_not_exists.html')

        models.Additive_Search().search(self.current_user.id, additive_id)
        return self.send_success_json()

    def get(self, additive_id):
        additive = models.Additive().find(additive_id)
        if not additive or additive.status != 0:
            return self.render('error/additive_not_exists.html')

        self._incr_view_counts(additive)
        
        return self.render('partial/additive.html',
                           additive = additive,
                           additive_detail = models.Additive_Detail().find(additive_id),
                           )

class AdditiveUploadHandler(BaseHandler):
    def get(self):
        template_prefix = 'partial/' if self.is_ajax_request else ''
        return self.render('{0}upload.html'.format(template_prefix))

class HotAdditivesHandler(BaseAdditivesHandler):
    def get(self):
        return self._render('hot')

class LatestAdditivesHandler(BaseAdditivesHandler):
    def get(self):
        return self._render('latest')

class AdditiveUserHandler(BaseUserAdditivesHandler):
    def get(self, additive_id):
        additive = models.Additive().find(additive_id)
        if not additive or additive.status != 0:
            return self.render('error/additive_not_exists.html')

        # used in BaseUserAdditivesHandler
        self.user = models.User().find(additive.user_id)
        return self._render('additives', additive = additive)

class AdditiveMineHandler(BaseAdditivesHandler):
    def get(self, additive_id):
        additive = models.Additive().find(additive_id)
        if not additive or additive.status != 0:
            return self.render('error/additive_not_exists.html')
        kind = 'mine_upload' if self.current_user else 'hot'
        return self._render(kind, additive = additive)

class AdditiveHotHandler(BaseAdditivesHandler):
    def get(self, additive_id):
        additive = models.Additive().find(additive_id)
        if not additive or additive.status != 0:
            return self.render('error/additive_not_exists.html')

        return self._render('hot', additive = additive)

class AdditiveDeleteHandler(BaseHandler):
    @check_additive_permission
    @tornado.web.authenticated
    def post(self, additive_id):
        self.additive.delete()
        return self.send_success_json(location = '/')

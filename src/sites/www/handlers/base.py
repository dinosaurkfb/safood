#coding=utf-8
import logging
from tornado.options import options
import tornado.web
import thing
import models
from macros.macro import  USERS_PER_PAGE, ADDITIVES_PER_PAGE, FOODS_PER_PAGE
from utils import keep_order

from tornado.escape import utf8

class BaseHandler(tornado.web.RequestHandler):

    def send_error_json(self, data):
        return self.write({
            'status': 'error',
            'content': data
            })

    def send_success_json(self, **data):
        return self.write({
            'status': 'ok',
            'content': data
            })

    def get_current_user(self):
        user_id = self.get_secure_cookie('o_O')
        if not user_id:
            return None

        return models.User().find(user_id)

    @property
    def notification_count(self):
        return models.Notification().count_by_receiver_id_and_is_new(self.current_user.id, 1)

    @property
    def is_admin(self):
        return self.current_user and self.current_user.is_admin

    @property
    def is_ajax_request(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def get(self, dummy):
        self.render("404.html")

class BaseApiHandler(BaseHandler):
    CALLBACK = 'callback' # define callback argument name
    
    def finish(self, chunk=None):
        """Finishes this response, ending the HTTP request."""
        assert not self._finished
        if chunk: self.write(chunk)
        
        # get client callback method
        callback = utf8(self.get_argument(self.CALLBACK))
        # format output with jsonp
        self._write_buffer.insert(0, callback + '(')
        self._write_buffer.append(')')
        
        # call base class finish method
        super(BaseApiHandler, self).finish() # chunk must be None

class BaseAdditivesHandler(BaseHandler):
    def _render(self, kind, additive = None, tag_name = None):
        template_prefix = 'partial/' if self.is_ajax_request else ''
        offset = (int(self.get_argument('page', 1)) - 1) * ADDITIVES_PER_PAGE

        if kind == 'hot':
            page_path = '/additives/hot'
            additives_title = u'热门添加剂'
            additives_type = 'hot'
            additives = (models.Additive().order_by('-karma')
                      .findall_by_status(0, limit = ADDITIVES_PER_PAGE, offset = offset))
            total_items = models.Additive().count_by_status(0)
        if kind == 'latest':
            page_path = '/additives/latest'
            additives_title = u'最新添加剂'
            additives_type = 'latest'
            additives = models.Additive().findall_by_status(0, limit = ADDITIVES_PER_PAGE, offset = offset)
            total_items = models.Additive().count_by_status(0)
        elif kind == 'mine_upload':
            page_path = '/mine/additives'
            additives_title = u'我添加的添加剂'
            additives_type = 'user'
            additives = models.Additive().findall_by_user_id_and_status(
                self.current_user.id, 0, limit = ADDITIVES_PER_PAGE, offset = offset)
            total_items = models.Additive().count_by_user_id_and_status(self.current_user.id, 0)
        elif kind == 'tag':
            page_path = u'/tag/{0}'.format(tag_name)
            additives_title = u'带有"{0}"标签的添加剂'.format(tag_name)
            additives_type = u'tag/{0}'.format(tag_name)
            additive_ids = models.Additive_Tag().findall_by_tag(
                        tag_name, limit = ADDITIVES_PER_PAGE, offset = offset)\
                        .get_field('additive_id')
            additives = []
            for additive_id in additive_ids:
                additives.append(models.Additive().find(additive_id))

            total_items = models.Additive_Tag().count_by_tag(tag_name)

        return self.render('{0}additives.html'.format(template_prefix),
                additives_title = additives_title,
                additives_type = additives_type,
                additives = additives,
                total_items = total_items,
                page_path = page_path,
                current_additive = additive,
                )

class BaseAdditivesApiHandler(BaseApiHandler):
    def _write(self, kind, additive = None, tag_name = None):
        template_prefix = 'partial/' if self.is_ajax_request else ''
        offset = (int(self.get_argument('page', 1)) - 1) * ADDITIVES_PER_PAGE

        result = {}
        if kind == 'hot':
#           result['title'] = u'热门添加剂'
            result['path'] = '/additives/hot'
            result['type'] = 'hot'
            additives = (models.Additive().order_by('-karma')
                      .findall_by_status(0, limit = ADDITIVES_PER_PAGE, offset = offset))
        elif kind == 'latest':
#            result['title'] = u'最新添加剂'
            result['path'] = '/additives/latest'
            result['type'] = 'latest'
            additives = models.Additive().findall_by_status(0, limit = ADDITIVES_PER_PAGE, offset = offset)
        result['total'] = models.Additive().count_by_status(0)
        result['additives'] = additives.to_dict_list()
        return self.write(result)

class BaseUserAdditivesHandler(BaseHandler):
    def _render(self, kind, additive = None):
        template_prefix = 'partial/' if self.is_ajax_request else 'user_'
        offset = (int(self.get_argument('page', 1)) - 1) * ADDITIVES_PER_PAGE

        fullname = self.user.fullname
        if self.current_user and self.user.id == self.current_user.id:
            fullname = u'我'

        if kind == 'additives':
            page_path = '/user/{0}/additives'.format(self.user.username)
            additives_title = u'{0}的添加剂'.format(fullname)
            additives_type = 'user'
            additives = models.Additive().findall_by_user_id_and_status(
                self.user.id, 0, limit = ADDITIVES_PER_PAGE, offset = offset)
            total_items = models.Additive().count_by_user_id_and_status(self.user.id, 0)

        return self.render('{0}additives.html'.format(template_prefix),
                additives_title = additives_title,
                additives_type = additives_type,
                additives = additives,
                total_items = total_items,
                page_path = page_path,
                current_additive = additive,
                )


class BaseFoodsHandler(BaseHandler):
    def _render(self, kind, food = None, tag_name = None):
        template_prefix = 'partial/' if self.is_ajax_request else ''
        offset = (int(self.get_argument('page', 1)) - 1) * FOODS_PER_PAGE

        if kind == 'hot':
            page_path = '/foods/hot'
            foods_title = u'热门食物'
            foods_type = 'hot'
            foods = (models.Food().order_by('-karma')
                      .findall_by_status(0, limit = FOODS_PER_PAGE, offset = offset))
            total_items = models.Food().count_by_status(0)
        if kind == 'latest':
            page_path = '/foods/latest'
            foods_title = u'最新食物'
            foods_type = 'latest'
            foods = models.Food().findall_by_status(0, limit = FOODS_PER_PAGE, offset = offset)
            total_items = models.Food().count_by_status(0)
        elif kind == 'mine_upload':
            page_path = '/mine/foods'
            foods_title = u'我添加的食物'
            foods_type = 'user'
            foods = models.Food().findall_by_user_id_and_status(
                self.current_user.id, 0, limit = FOODS_PER_PAGE, offset = offset)
            total_items = models.Food().count_by_user_id_and_status(self.current_user.id, 0)
        elif kind == 'tag':
            page_path = u'/tag/{0}'.format(tag_name)
            foods_title = u'带有"{0}"标签的食物'.format(tag_name)
            foods_type = u'tag/{0}'.format(tag_name)
            food_ids = models.Food_Tag().findall_by_tag(
                        tag_name, limit = FOODS_PER_PAGE, offset = offset)\
                        .get_field('food_id')
            foods = []
            for food_id in food_ids:
                foods.append(models.Food().find(food_id))

            total_items = models.Food_Tag().count_by_tag(tag_name)

        return self.render('{0}foods.html'.format(template_prefix),
                foods_title = foods_title,
                foods_type = foods_type,
                foods = foods,
                total_items = total_items,
                page_path = page_path,
                current_food = food,
                )

class BaseFoodsApiHandler(BaseApiHandler):
    def _write(self, kind, food = None):
        template_prefix = 'partial/' if self.is_ajax_request else ''
        offset = (int(self.get_argument('page', 1)) - 1) * FOODS_PER_PAGE

        result = {}
        if kind == 'hot':
            result['title'] = u'热门食物'
            result['path'] = '/foods/hot'
            result['type'] = 'hot'
            foods = (models.Food().order_by('-karma')
                      .findall_by_status(0, limit = FOODS_PER_PAGE, offset = offset))
        if kind == 'latest':
            result['title'] = u'最新食物'
            result['path'] = '/foods/latest'
            result['type'] = 'latest'
            foods = models.Food().findall_by_status(0, limit = FOODS_PER_PAGE, offset = offset)

        result['total'] = models.Food().count_by_status(0)
        result['foods'] = foods.to_dict_list()
        return self.write(result)

class BaseUserFoodsHandler(BaseHandler):
    def _render(self, kind, food = None):
        template_prefix = 'partial/' if self.is_ajax_request else 'user_'
        offset = (int(self.get_argument('page', 1)) - 1) * FOODS_PER_PAGE

        fullname = self.user.fullname
        if self.current_user and self.user.id == self.current_user.id:
            fullname = u'我'

        if kind == 'foods':
            page_path = '/user/{0}/foods'.format(self.user.username)
            foods_title = u'{0}的食品'.format(fullname)
            foods_type = 'user'
            foods = models.Food().findall_by_user_id_and_status(
                self.user.id, 0, limit = FOODS_PER_PAGE, offset = offset)
            total_items = models.Food().count_by_user_id_and_status(self.user.id, 0)

        return self.render('{0}foods.html'.format(template_prefix),
                foods_title = foods_title,
                foods_type = foods_type,
                foods = foods,
                total_items = total_items,
                page_path = page_path,
                current_food = food,
                )


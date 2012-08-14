#coding=utf-8
import logging
import tornado
import json
from handlers.base import BaseHandler, BaseFoodsHandler, BaseUserFoodsHandler
import models
from macros.macro import MAX_UPLOAD_SIZE, FOODS_PER_PAGE
from helpers import nl2br
from utils import get_food_part, check_food_permission

class FoodHandler(BaseHandler):
    def _incr_view_counts(self, food):
        viewed_food_ids = self.get_cookie('viewed_food_ids', '').split(',')
        if str(food.id) not in (viewed_food_ids):
            viewed_food_ids += [food.id]
            food.views_count += 1
            food.save()
            self.set_cookie('viewed_food_ids', ','.join(map(str, viewed_food_ids)))

    def get(self, food_id):
        food = models.Food().find(food_id)
        if not food or food.status != 0:
            return self.render('error/food_not_exists.html')

        self._incr_view_counts(food)
        
        food_parts = models.Food_Part().findall_by_food_id(food_id)
        i_dict = {}
        for part in food_parts:
            ingredients = models.Ingredient().get_additive(part.id)
            i_dict[part.name] = ingredients
        
        return self.render('partial/food.html',
                           food = food,
                           i_dict = i_dict
                           )

    @tornado.web.authenticated
    def post(self):
        food = models.Food(
                name = self.get_argument('name', ''),
                user_id = self.current_user.id,
                )
        food_id = food.create()

        if food_id:
            food.save()

            if self.get_argument('part', ''):
                for item in ('part'):
                    value = self.get_argument('detail_{0}'.format(item), '')
                    models.Food_Part(
                            food_id = food_id,
                            key = item,
                            value = value).save()
            else:
                part = get_food_part(food.hash, self.current_user.id)
                for key, value in part.items():
                    models.Food_Part(
                            food_id = food_id,
                            key = key,
                            value = value).save()

            self.send_success_json(location='/food/{0}/via/mine'.format(food_id))
        else:
            self.send_error_json(food.errors)


class FoodUpdateHandler(BaseHandler):
    @check_food_permission
    @tornado.web.authenticated
    def post(self, food_id):
        title = self.get_argument('title', '')
        content = self.get_argument('content', '')
        if title:
            self.food.title = title
            self.food.content = content
            self.food.save()
            return self.send_success_json()
        return self.send_error_json({'message': 'update failed'})

class FoodSearchHandler(BaseHandler):
#    @tornado.web.authenticated
    def post(self, food_id):
        food = models.Food().find(food_id)
        if not food:
            return self.render('error/food_not_exists.html')

        models.Food_Search().search(self.current_user.id, food_id)
        return self.send_success_json()

    def get(self, food_id):
        food = models.Food().find(food_id)
        if not food or food.status != 0:
            return self.render('error/food_not_exists.html')

        self._incr_view_counts(food)
        
        return self.render('partial/food.html',
                           food = food,
                           )

class FoodUploadHandler(BaseHandler):
    def get(self):
        template_prefix = 'partial/' if self.is_ajax_request else ''
        return self.render('{0}food_upload.html'.format(template_prefix))

class FoodEditHandler(BaseHandler):
    def get(self, food_id):
        template_prefix = 'partial/' if self.is_ajax_request else ''
        food = models.Food().find(food_id)
        if not food or food.status != 0:
            return self.render('error/food_not_exists.html')

        q = self.get_argument('q', '')
        if not q:
            food_parts = models.Food_Part().findall_by_food_id(food_id)
            i_dict = {}
            for part in food_parts:
                ingredients = models.Ingredient().get_additive(part.id)
                i_dict[part.name] = ingredients
        
            return self.render('partial/food_edit.html',
                               food = food,
                               i_dict = i_dict
                               )
        food_parts = models.Food_Part().findall_by_food_id(food_id)
        rows = []
        for part in food_parts:
            ingredients = models.Ingredient().get_additive(part.id)
            i_list = [i[1] for i in ingredients]
            rows.append({"id": part.id, "name": part.name, "addis":i_list})
        
        result = {
            "total":"1",
            "page":"1",
            "records":"2",
            "rows":rows,
            }
        return self.write(result)

    def post(self, food_id):
        template_prefix = 'partial/' if self.is_ajax_request else ''
        
        part_id = self.get_argument('id', '')
        part_name = self.get_argument('name', '')
        addis = self.get_argument('addis', '')
        print(u'part_id={0}, part_name={1}, addis={2}, food_id = {3}'.format(part_id, part_name, addis, food_id))

        addi_list = addis.split(',')
        for a in addi_list:
            if not models.Additive().findall_by_name(a):
                return self.send_error_json(u"数据库中不存在此添加剂:{0}".format(a))
                
        return self.send_success_json()

class HotFoodsHandler(BaseFoodsHandler):
    def get(self):
        return self._render('hot')

class LatestFoodsHandler(BaseFoodsHandler):
    def get(self):
        return self._render('latest')

class FoodUserHandler(BaseUserFoodsHandler):
    def get(self, food_id):
        food = models.Food().find(food_id)
        if not food or food.status != 0:
            return self.render('error/food_not_exists.html')

        # used in BaseUserFoodsHandler
        self.user = models.User().find(food.user_id)
        return self._render('foods', food = food)

class FoodMineHandler(BaseFoodsHandler):
    def get(self, food_id):
        food = models.Food().find(food_id)
        if not food or food.status != 0:
            return self.render('error/food_not_exists.html')
        kind = 'mine_upload' if self.current_user else 'hot'
        return self._render(kind, food = food)

class FoodHotHandler(BaseFoodsHandler):
    def get(self, food_id):
        food = models.Food().find(food_id)
        if not food or food.status != 0:
            return self.render('error/food_not_exists.html')

        return self._render('hot', food = food)

class FoodDeleteHandler(BaseHandler):
    @check_food_permission
    @tornado.web.authenticated
    def post(self, food_id):
        self.food.delete()
        return self.send_success_json(location = '/')

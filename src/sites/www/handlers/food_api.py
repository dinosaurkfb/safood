#coding=utf-8
import logging
import tornado
import json
from handlers.base import BaseApiHandler, BaseFoodsApiHandler
import models
from macros.macro import MAX_UPLOAD_SIZE, FOODS_PER_PAGE
from helpers import nl2br
from utils import get_food_part, check_food_permission

class FoodApiHandler(BaseApiHandler):
    def _incr_view_counts(self, food):
        viewed_food_ids = self.get_cookie('viewed_food_ids', '').split(',')
        if str(food.id) not in (viewed_food_ids):
            viewed_food_ids += [food.id]
            food.views_count += 1
            food.save()
            self.set_cookie('viewed_food_ids', ','.join(map(str, viewed_food_ids)))

#    def get(self, food_id):
    def get(self):
        food_id = self.get_argument('id', -1)
        food = models.Food().find(food_id)
        if not food or food.status != 0:
            return self.write({})

        self._incr_view_counts(food)
        
        result = {}
        result['food_name'] = food.name
        food_parts = models.Food_Part().get(food_id)
        parts_list = []
        for part in food_parts:
            ingredients = models.Ingredient().get_additive(part.id)
            part_dict = {}
            part_dict['part_name'] = part.name
            part_dict['ingredients'] = map(lambda (id, name): {'id': id, 'name':name}, ingredients)
            parts_list.append(part_dict)
            
        result['parts'] = parts_list
        return self.write(result)

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


class FoodSearchApiHandler(BaseApiHandler):
#    @tornado.web.authenticated
    def post(self, food_id):
        food = models.Food().find(food_id)
        if not food:
            return self.render('error/food_not_exists.html')

        models.Food_Search().search(self.current_user.id, food_id)
        return self.send_success_json()

    def get(self):
        val = self.get_argument('q')
        foods = models.Food().search(u'%{0}%'.format(val))
        return self.write({u'result':foods.to_dict_list()})

class HotFoodsApiHandler(BaseFoodsApiHandler):
    def get(self):
        return self._write('hot')

class LatestFoodsApiHandler(BaseFoodsApiHandler):
    def get(self):
        return self._write('latest')



#coding=utf-8
import logging
import time

from tornado.options import options
import tornado.web

from base import BaseHandler, BaseAdditivesHandler
import models

class HomeHandler(BaseAdditivesHandler):
    def get(self):
        return self._render('hot')

class AboutHandler(BaseHandler):
    def get(self):
        return self.render('about.html')

# class LocalHandler(BaseHandler):
#     def get(self):
#         return self.render('jsonp.html')

# class JsonpHandler(BaseHandler):
#     def get(self):
#         code = self.get_argument('code')
#         callback = self.get_argument('callback')
#         js = u'{0}({{"code":"{1}", "price":1780, "tickets":5}});'.format(callback, code)
#         return self.write(js)

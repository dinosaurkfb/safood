
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

# -*- coding: utf-8 -*-

import tornado.web
from . import BaseHandler


class IndexHandler(BaseHandler):
    def get(self):
        self.render("desktop/aboutme.html")
        # self.render("index.tpl")

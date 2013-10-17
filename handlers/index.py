# -*- coding: utf-8 -*-

import tornado.web
from . import BaseHandler
from datetime import datetime
import utils



class IndexHandler(BaseHandler):
    def get(self, page=1):

        posts = self.Pagination(self.db.posts, page, self.per_page)

        template_values = dict()
        template_values["posts"] = posts
        template_values["dateformat"] = utils.dateformat
        self.render("desktop/index.html", **template_values)

# -*- coding: utf-8 -*-

import tornado.web
from . import BaseHandler
from utils import dateformat

class ShowHandler(BaseHandler):
    def get(self):
        tags = self.db.tags.find_one()

        template_values = dict()
        template_values["tags"] = tags["tags"]
        template_values["_id"] = str(tags["_id"])
        template_values["dateformat"] = dateformat

        return self.write_json(template_values)


class ShowByTagHandler(BaseHandler):
    def get(self, tag):
        page = int(self.get_argument("p", 1))
        key = {"tags": tag}
        posts = self.Pagination(self.db.posts, page, self.per_page,  key)

        if not posts.items:
            raise tornado.web.HTTPError(404)
        template_values = dict()
        template_values["posts"] = posts
        template_values["tag"] = tag
        template_values["dateformat"] = dateformat


        self.render("desktop/show_by_tag.html", **template_values)

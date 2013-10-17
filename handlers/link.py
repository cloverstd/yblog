# -*- coding: utf-8 -*-

import tornado.web
from . import BaseHandler
from datetime import datetime

class AddHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("desktop/admin/link_add.html")

    @tornado.web.authenticated
    def post(self):
        name = self.get_argument("name")
        url = self.get_argument("url")
        description = self.get_argument("description")

        if url[:7] == "http://":
            pass
        elif url[:8] == "https://":
            pass
        else:
            url = "http://" + url

        link = dict(name=name,
                    url=url,
                    description=description,
                    date=datetime.now())

        self.db.friends.insert(link)

        self.redirect("/admin/link/add")

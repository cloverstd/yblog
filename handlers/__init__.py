#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import config
from tornado.options import options
import pymongo
import json
import os
import memcache


def get_site():
    cache = memcache.Client(['127.0.0.1:11211'], debug=True)
    if cache.get("site") is None:
        site = dict(title=config.SITE_NAME,
                    subtitle=config.SUBTITLE,
                    description=config.DESCRIPTION,
                    duoshuo=config.DUOSHUO,
                    author=config.AUTHOR,
                    ga=config.GA)
        cache.set("site", json.dumps(site), 3600 * 24)

    return json.loads(cache.get("site"))


class BaseHandler(tornado.web.RequestHandler):
    # @property
    # def con(self):
        # return self.application.con

    # @property
    # def db(self):
        # return self.application.db

    def initialize(self):
        self.con = pymongo.Connection(
            host=options.db_host, port=int(options.db_port))

        self.db = self.con[options.db_name]
        if "SERVER_SOFTWARE" in os.environ:
            self.db.authenticate(options.db_user, options.db_pass)
        self.per_page = config.PER_PAGE
        # self.db.authenticate(options.db_user, options.db_pass)

    def get_current_user(self):
        return self.get_secure_cookie("username")

    def render(self, template_name, **kwargs):
        # if not self.request.path.startswith("/admin"):
        # kwargs["site"] = dict(title=config.SITE_NAME,
        #                       subtitle=config.SUBTITLE,
        #                       description=config.DESCRIPTION,
        #                       duoshuo=config.DUOSHUO,
        #                       author=config.AUTHOR,
        #                       ga=config.GA)
        kwargs["site"] = get_site()
        super(BaseHandler, self).render(template_name, **kwargs)

    def write_json(self, d):
        self.set_header("Content-Type", "application/json;charset=utf-8")
        self.write(json.dumps(d))

    def on_finish(self):
        self.con.disconnect()

    class Pagination(object):

        def __init__(self, collection, page, per_page, key=None):
            self.collection = collection
            self.page = int(page) - 1
            self.per_page = int(per_page)
            self.key = key
            self.index = 0

        @property
        def items(self):
            return list(self.collection.find(self.key).sort("_id", -1).skip(self.per_page * self.page).limit(self.per_page))

        @property
        def has_next(self):
            if (self.page + 1) * self.per_page > self.collection.find().count():
                return False
            return True

        @property
        def has_prev(self):
            if self.page == 0:
                return False
            return True

        @property
        def prev_num(self):
            if self.has_prev:
                return self.page + 1 - 1
            return 1

        @property
        def next_num(self):
            if self.has_next:
                return self.page + 1 + 1
            return self.page

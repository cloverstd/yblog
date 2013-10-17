# -*- coding: utf-8 -*-

import tornado.web
from . import BaseHandler
from datetime import datetime
import calendar
from utils import dateformat
import memcache
import json


def get_days_by_month(year, month):
    return calendar.monthrange(int(year), int(month))[1]


def archive_cache(method):
    import functools

    def wrapper(self, *args, **kwargs):
        #print args, kwargs
        cache = memcache.Client(['127.0.0.1:11211'],debug=True)
        if len(args) == 0:
            if cache.get("archive"):
                return method(self,  posts=json.loads(cache.get("archive")), *args, **kwargs)

            posts = [dict(title=post["title"], date=post["date"]) for post in self.db.posts.find() ]
            cache.set("archive", json.dumps(posts))
            return method(self,  posts=json.loads(cache.get("archive")), *args, **kwargs)

        elif len(args) == 1:
            print args
        elif len(args) == 2:
            print args
        return method(self, *args, **kwargs)
    return wrapper


class ArchiveHandler(BaseHandler):
    # @archive_cache
    def get(self):
        posts = self.db.posts.find()

        template_value = dict()
        template_value["posts"] = list(posts)
        template_value["year"] = None
        template_value["month"] = None
        template_value["dateformat"] = dateformat

        self.render("desktop/archive.html", **template_value)


class YearHandler(BaseHandler):
    # @archive_cache
    def get(self, year):
        end_date = datetime(int(year), 12, 31)
        start_date = datetime(int(year), 1, 1)

        query_key = {
            "date": {
            "$gte": start_date,
            "$lte": end_date
            }
        }
        posts = list(self.db.posts.find(query_key))
        if not posts:
            raise tornado.web.HTTPError(404)
        template_value = dict()
        template_value["posts"] = list(posts)
        template_value["year"] = year
        template_value["month"] = None
        template_value["dateformat"] = dateformat

        self.render("desktop/archive.html", **template_value)


class YearMonthHandler(BaseHandler):
    # @archive_cache
    def get(self, year, month):
        end_date = datetime(
            int(year), int(month), get_days_by_month(year, month))
        start_date = datetime(int(year), int(month), 1)

        query_key = {
            "date": {
            "$gte": start_date,
            "$lte": end_date
            }
        }

        posts = list(self.db.posts.find(query_key))
        if not posts:
            raise tornado.web.HTTPError(404)
        template_value = dict()
        template_value["posts"] = posts
        template_value["year"] = year
        template_value["month"] = month
        template_value["dateformat"] = dateformat

        self.render("desktop/archive.html", **template_value)

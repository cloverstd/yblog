#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.wsgi
import tornado.ioloop
from tornado.options import define, options
import config
import os.path
import pymongo
from routes import handlers

if "SERVER_SOFTWARE" in os.environ:
    pass
else:
    define("db_host", default="localhost")
    define("db_port", default=27017, type=int)
    define("db_name", default=config.DB_NAME)
    define("db_user", default="")
    define("db_pass", default="")
define("username", default=config.USERNAME)
define("password", default=config.PASSWORD)


class Application(tornado.web.Application):

    def __init__(self):
        # handlers = []
        settings = dict(
            autoescape=None,
            xsrf_cookies=True,
            cookie_secret=config.COOKIE_SECRET,
            login_url='/admin/login',
            template_path=os.path.join(
                os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            debug=config.DEBUG,
        )

        super(Application, self).__init__(handlers, **settings)

        # db
        # con = pymongo.Connection(host=options.db_host, port=options.db_port)
        # db = con[options.db_name]
        # db.authenticate(options.db_user, options.db_pass)
        # self.con = con
        # self.db = db


class BAE(tornado.wsgi.WSGIApplication):

    def __init__(self):
        # handlers = []
        settings = dict(
            autoescape=None,
            xsrf_cookies=True,
            cookie_secret=config.COOKIE_SECRET,
            login_url='/admin/login',
            template_path=os.path.join(
                os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            debug=config.DEBUG,
        )

        super(BAE, self).__init__(handlers, **settings)
        from bae.core import const
        define("db_host", default=const.MONGO_HOST)
        define("db_port", default=const.MONGO_PORT, type=int)
        define("db_name", default=config.DB_NAME)
        define("db_user", default=const.MONGO_USER)
        define("db_pass", default=const.MONGO_PASS)
        # db
        # con = pymongo.Connection(host=options.db_host, port=int(options.db_port))
        # db = con[options.db_name]
        # db.authenticate(options.db_user, options.db_pass)
        # self.con = con
        # self.db = db

if "SERVER_SOFTWARE" in os.environ:
    from bae.core.wsgi import WSGIApplication
    application = WSGIApplication(BAE())
else:
    appilication = Application()
    appilication.listen(8080)
    print "http://localhost:8080"
    tornado.ioloop.IOLoop.instance().start()

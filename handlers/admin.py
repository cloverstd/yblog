# -*- coding: utf-8 -*-

import tornado.web
from tornado.options import options
from . import BaseHandler

def login(self):
    self.set_secure_cookie("username", "blogusername")

def logout(self):
    self.clear_cookie("username")


class LoginHandler(BaseHandler):
    def get(self):
        template_values = dict()
        template_values["next"] = self.get_argument("next", "/admin")
        self.render("desktop/admin/login.html", **template_values)

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        go = self.get_argument("next", "/admin")

        template_values = dict()
        if username == options.username and password == options.password:
            template_values["status"] = True
            template_values["err_msg"] = ""
            template_values["err_code"] = -1
            template_values["go"] = go
            login(self)

        else:
            template_values["status"] = False
            template_values["err_msg"] = "密码错误"
            template_values["err_code"] = 1

        return self.write_json(template_values);

class LogoutHandler(BaseHandler):
    def get(self):
        logout(self)
        self.write("登出")
        self.redirect("/")


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("desktop/admin/index.html")

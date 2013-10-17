# -*- coding: utf-8 -*-

import tornado.web
from . import BaseHandler
from markdown import markdown
from datetime import datetime
from utils import dateformat
from bson.objectid import ObjectId


# 修改 db.tags
def add_tags(self, tags):
    for i in range(len(tags)):
        tags[i] = tags[i].lower().encode("utf-8").decode("utf-8")

    tags_db = self.db.tags.find_one()
    if tags_db:
        tags = list(set(tags_db["tags"]) | set(tags))
        self.db.tags.update(tags_db, {"tags": tags})
    else:
        self.db.tags.insert({"tags": tags})


class AddHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        tags = self.db.tags.find_one()
        if tags:
            tags = tags["tags"]
        else:
            tags = list()

        template_values = dict()
        template_values["tags"] = tags
        self.render("desktop/admin/post_add.html", **template_values)

    @tornado.web.authenticated
    def post(self):
        title = self.get_argument("title")
        slug = self.get_argument("slug")
        tags = self.get_arguments("tag")
        content = self.get_argument("content")

        if slug == '':
            slug = title

        content_html = markdown(content,
                                extensions=['codehilite(linenums=True)'])
        post = dict(title=title,
                    slug=slug,
                    tags=tags,
                    content=content,
                    content_html=content_html,
                    date=datetime.now())

        self.db.posts.insert(post)

        add_tags(self, tags)

        self.redirect("/article/%s" % slug, permanent=True)


class ShowHandler(BaseHandler):
    def get(self, slug):
        post = self.db.posts.find_one({"slug": slug})
        template_values = dict()
        template_values["post"] = post
        template_values["dateformat"] = dateformat

        if post:
            self.render("desktop/post.html", **template_values)
        else:
            raise tornado.web.HTTPError(404)


class ListHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        posts = self.db.posts.find()
        template_values = dict()
        template_values["posts"] = posts

        self.render("desktop/admin/post_list.html", **template_values)


class EditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, post_id):
        post = self.db.posts.find_one({'_id': ObjectId(post_id)})
        tags = self.db.tags.find_one()
        if tags:
            tags = tags["tags"]
        else:
            tags = list()

        template_values = dict()
        template_values["post"] = post
        template_values["tags"] = tags

        if post:
            self.render("desktop/admin/post_edit.html", **template_values)
        else:
            raise tornado.web.HTTPError(404)

    @tornado.web.authenticated
    def post(self, post_id):
        title = self.get_argument("title")
        slug = self.get_argument("slug")
        tags = self.get_arguments("tag")
        content = self.get_argument("content")

        if slug == '':
            slug = title

        post = self.db.posts.find_one({'_id': ObjectId(post_id)})

        content_html = markdown(content,
                                extensions=['codehilite(linenums=True)'])
        new_post = dict(title=title,
                        slug=slug,
                        tags=tags,
                        content=content,
                        content_html=content_html,
                        # date=datetime.now())
                        date=post["date"])
        self.db.posts.update({"_id": post["_id"]}, new_post)

        add_tags(self, tags)

        self.redirect("/article/%s" % slug, permanent=True)


class DeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, post_id):
        self.db.posts.remove({"_id": ObjectId(post_id)})
        self.write_json({"status": True})

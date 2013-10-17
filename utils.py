#!/usr/bin/env python
# -*- coding: utf-8 -*-


def dateformat(date):
    return date.strftime("%b %d %Y")


if __name__ == "__main__":
	import pymongo
	from datetime import datetime
	con = pymongo.Connection()
	db = con["testdb10"]
	for i in range(10):
	    post = dict(title="this is a test",
	            slug="test%d" % i,
	            tags=["test"],
	            content=None,
	            content_html=None,
	            date=datetime(2012, 1, 2))
	    db.posts.insert(post)

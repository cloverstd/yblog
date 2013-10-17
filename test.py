#!/usr/bin/env python
# -*- coding: utf-8 -*-

import memcache


cache = memcache.Client(['127.0.0.1:11211'],debug=True)

# cache.set("foo", "bar", time=20)

print cache.get("foo")

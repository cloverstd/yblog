# -*- coding: utf-8 -*-

from handlers import index, admin, post, tag, archive, about, link
handlers = []
handlers.append((r'/', index.IndexHandler))
handlers.append((r'/page/(\d+)', index.IndexHandler))
handlers.append((r'/admin/login', admin.LoginHandler))
handlers.append((r'/admin', admin.IndexHandler))
handlers.append((r'/admin/logout', admin.LogoutHandler))
handlers.append((r'/article/(.*)', post.ShowHandler))
handlers.append((r'/admin/post', post.ListHandler))
handlers.append((r'/admin/post/add', post.AddHandler))
handlers.append((r'/admin/post/list', post.ListHandler))
handlers.append((r'/admin/post/edit/([0-9a-zA-Z]+)', post.EditHandler))
handlers.append((r'/admin/post/delete/([0-9a-zA-Z]+)', post.DeleteHandler))
handlers.append((r'/tag', tag.ShowHandler))
handlers.append((r'/tag/(.*)', tag.ShowByTagHandler))
handlers.append((r'/archive/(\d+)', archive.YearHandler))
handlers.append((r'/archive/(\d+)/(\d+)', archive.YearMonthHandler))
handlers.append((r'/archive', archive.ArchiveHandler))
handlers.append((r'/aboutme', about.IndexHandler))
handlers.append((r'/admin/link/add', link.AddHandler))

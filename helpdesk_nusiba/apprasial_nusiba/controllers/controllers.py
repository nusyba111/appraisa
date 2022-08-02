# -*- coding: utf-8 -*-
# from odoo import http


# class Apprasial(http.Controller):
#     @http.route('/apprasial/apprasial', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/apprasial/apprasial/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('apprasial.listing', {
#             'root': '/apprasial/apprasial',
#             'objects': http.request.env['apprasial.apprasial'].search([]),
#         })

#     @http.route('/apprasial/apprasial/objects/<model("apprasial.apprasial"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('apprasial.object', {
#             'object': obj
#         })

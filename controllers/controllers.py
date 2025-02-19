# -*- coding: utf-8 -*-
# from odoo import http


# class InventoryAdjWizard(http.Controller):
#     @http.route('/inventory_adj_wizard/inventory_adj_wizard', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inventory_adj_wizard/inventory_adj_wizard/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('inventory_adj_wizard.listing', {
#             'root': '/inventory_adj_wizard/inventory_adj_wizard',
#             'objects': http.request.env['inventory_adj_wizard.inventory_adj_wizard'].search([]),
#         })

#     @http.route('/inventory_adj_wizard/inventory_adj_wizard/objects/<model("inventory_adj_wizard.inventory_adj_wizard"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inventory_adj_wizard.object', {
#             'object': obj
#         })


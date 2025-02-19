# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductInv(models.TransientModel):
    _name = 'product.inv'
    _description = 'inventory movement report'

    product = fields.Many2one(comodel_name="product.product", required=True)
    start_date = fields.Datetime(required=True, default=fields.Datetime.now)
    end_date = fields.Datetime(required=True, default=fields.Datetime.now)
    location = fields.Many2one(comodel_name="stock.location", required=True)
    
    @api.model
    def inventory_balance(self, start_date, end_date, location):
        balance = 0
        movements = []

        stock_moves = self.env['stock.move'].search([
            ('product_id', '=', self.product.id),
            ('state', '=', 'done'),
            '|',
            ('location_id', '=', location.id),
            ('location_dest_id', '=', location.id),
            ('date', '>=', start_date),
            ('date', '<=', end_date)
        ], order='date asc')

        opening_moves = self.env['stock.move'].search([
            ('product_id', '=', self.product.id),
            ('state', '=', 'done'),
            '|',
            ('location_id', '=', location.id),
            ('location_dest_id', '=', location.id),
            ('date', '<', start_date)
        ])

        opening_balance = sum(
            move.product_uom._compute_quantity(move.product_uom_qty, move.product_id.uom_id)
            if move.location_dest_id.id == location.id else
            -move.product_uom._compute_quantity(move.product_uom_qty, move.product_id.uom_id)
            for move in opening_moves
            if move.location_dest_id.id != move.location_id.id and move.location_id.id != move.location_dest_id.id
        )

        balance = opening_balance
        movements.append({
            'reference': 'Opening',
            'incoming': '',
            'outgoing': '',
            'UOM': '',
            'balance': opening_balance,
        })

        print("this is also a new file", stock_moves)

        for move in stock_moves:
            if move.location_dest_id.id != move.location_id.id and move.location_id.id != move.location_dest_id.id:
                if move.location_dest_id.id == location.id:
                    converted_qty = move.product_uom._compute_quantity(move.product_uom_qty, move.product_id.uom_id)
                    balance += converted_qty
                    movements.append({
                        'reference': move.reference or move.name,
                        'incoming': converted_qty,
                        'outgoing': '',
                        'UOM': move.product_id.uom_id.name,
                        'balance': balance,
                    })
                    # production.product_uom_id._compute_quantity(production.product_qty, production.product_id.uom_id)
                elif move.location_id.id == location.id:
                    converted_qty = move.product_uom._compute_quantity(move.product_uom_qty, move.product_id.uom_id)
                    balance -= converted_qty
                    movements.append({
                        'reference': move.reference or move.name,
                        'incoming': '',
                        'outgoing': converted_qty,
                        'UOM': move.product_id.uom_id.name,
                        'balance': balance,
                    })

        movements.append({
            'reference': "Closing",
            'incoming': '',
            'outgoing': '',
            'UOM': '',
            'balance': balance,
        })


        return movements

# quantity_done_converted = move.product_uom._compute_quantity(move.quantity, move.product_id.product_uom)
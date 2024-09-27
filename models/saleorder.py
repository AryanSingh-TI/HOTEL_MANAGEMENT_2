from odoo import models, fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    room_type = fields.Selection(related='product_id.room_type', string="Room Type", store=True , readonly=True)

from odoo import fields,api,models,_

class HotelCustomer(models.Model):
    _inherit='res.partner'

    is_hotel_customer = fields.Boolean(string="Is a hotel Customer")


from odoo import fields,api,models,_

class HotelRoom(models.Model):
    _inherit = 'product.product'

    room_type = fields.Selection([
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite')
    ], string='Room Type')
    price = fields.Monetary(string='Price per Day',  currency_field='currency_id')
    availability = fields.Selection([
        ('available', 'Available'),
        ('occupied', 'Occupied')
    ], string='Availability')

    room_image = fields.Binary(string = "Room Image")
    currency_id = fields.Many2one('res.currency', string='Currency')

    purchase_ok = fields.Boolean(default=False)

    is_hotel_room =  fields.Boolean(string="is Hotel Room")

    is_available = fields.Boolean(string="Is Hotel Room Available",default=True)
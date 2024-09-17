from odoo import api,fields,models,_

class HotelEmployee(models.Model):
    _inherit='hr.employee'

    is_hotel_employee=fields.Boolean(string="Is Hotel Employee")
from odoo import fields,api,models,_
from odoo.exceptions import ValidationError

class HotelCustomer(models.Model):
    _inherit='res.partner'

    is_hotel_customer = fields.Boolean(string="Is a hotel Customer")
    aadhaar_number = fields.Char(string="Aadhaar Card")


    @api.constrains('phone')
    def _check_phone(self):
        
        validate_phone = self.env['ir.config_parameter'].sudo().get_param('hotel.validate_phone', default=False)
        
        if validate_phone:
            for customer in self:
                if customer.phone and len(customer.phone) != 10:
                    raise ValidationError(_("Phone number must be exactly 10 digits."))
    
    @api.constrains('aadhaar_number')
    def _check_aadhaar_number(self):
        for record in self:
            # Fetch the validated Aadhaar setting
            validated_aadhaar = self.env['ir.config_parameter'].sudo().get_param('hotel.validated_aadhaar', default=False)
            
            # Apply validation only if the setting is enabled
            if validated_aadhaar:
                if not record.aadhaar_number or len(record.aadhaar_number) != 12:
                    raise ValidationError("Aadhaar Number must be 12 digits long.")
                
    
    
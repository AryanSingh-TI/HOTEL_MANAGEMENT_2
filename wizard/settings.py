from odoo import fields,api,models,_
from odoo.exceptions import ValidationError

class HotelSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    validate_phone = fields.Boolean(string="Validate Phone Number")
    company_id = fields.Many2one('res.company', string="Company", required=True, default=lambda self: self.env.company)
    validated_aadhaar = fields.Boolean(string="Validate Aadhaar Number")

    @api.model
    def get_values(self):
        res = super(HotelSettings, self).get_values()
        current_company = self.env.company
        validate_phone = self.env['ir.config_parameter'].sudo().get_param('hotel.validate_phone', default=False)
        validated_aadhaar = self.env['ir.config_parameter'].sudo().get_param('hotel.validated_aadhaar',default=False)
        res.update(
            validate_phone=bool(validate_phone),
            validated_aadhaar=bool(validated_aadhaar),
        )
        return res

    def set_values(self):
        super(HotelSettings, self).set_values()
        current_company = self.company_id.id
        self.env['ir.config_parameter'].sudo().set_param('hotel.validate_phone', self.validate_phone)
        self.env['ir.config_parameter'].sudo().set_param('hotel.validated_aadhaar',self.validated_aadhaar)

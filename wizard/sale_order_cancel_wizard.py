# models/sale_order_cancel_wizard.py
from odoo import models, fields, api
import logging

class SaleOrderCancelWizard(models.TransientModel):
    _name = 'sale.order.cancel.wizard'
    _description = 'Wizard for Canceling Sale Order'

    sale_order_name = fields.Char(string="Sale Order Name")
    sale_order_total = fields.Float(string="Sale Order Total")
    sale_order_partner_id = fields.Many2one('res.partner',string="Customer Information")

    description = fields.Text(string='Cancellation Reason', required=True)
    employee_id = fields.Many2one('hr.employee', string='Cancelled by', required=True)

    @api.model
    def default_get(self,fields):
        _logger = logging.getLogger(__name__)
        _logger.info("#################################### FIELDS ###############################################")
        _logger.info(fields)
        res =  super(SaleOrderCancelWizard,self).default_get(fields)
        _logger.info("#################################### RES ###############################################")
        _logger.info(res)
        context = self.env.context
        if context['sale_order_partner_id']:
            res['sale_order_partner_id'] = context.get('sale_order_partner_id')

        return res
    

    def confirm_cancel(self):
        _logger = logging.getLogger(__name__)
        
        sale_order_id = self.env.context.get('active_id')
        sale_order = self.env['sale.order'].browse(sale_order_id)

        sale_order.write({
            'cancelled_by': self.employee_id.id,
            'cancel_reason': self.description,
        })

        sale_order.with_context(is_clicked_by_user=False).action_cancel()
        _logger.info("#########################################INSIDE CONFIRM CANCEL#############################################")
        _logger.info(self.env.context)

        return {'type': 'ir.actions.act_window_close'}

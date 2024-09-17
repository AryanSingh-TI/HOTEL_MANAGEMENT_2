# models/sale_order_cancel_wizard.py
from odoo import models, fields, api

class SaleOrderCancelWizard(models.TransientModel):
    _name = 'sale.order.cancel.wizard'
    _description = 'Wizard for Canceling Sale Order'

    description = fields.Text(string='Cancellation Reason', required=True)
    employee_id = fields.Many2one('hr.employee', string='Cancelled by', required=True)

    def confirm_cancel(self):
        
        sale_order_id = self.env.context.get('active_id')
        sale_order = self.env['sale.order'].browse(sale_order_id)

        sale_order.write({
            'cancelled_by': self.employee_id.id,
            'cancel_reason': self.description,
        })

        sale_order.action_cancel()

        return {'type': 'ir.actions.act_window_close'}

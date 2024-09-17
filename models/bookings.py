from odoo import fields,api,models,_
from odoo.exceptions import ValidationError

class HotelBookings(models.Model):
    _inherit='sale.order'
    
    is_hotel_booking = fields.Boolean(string="Is Hotel Booking")

    booking_state = fields.Selection([
        ("new","New"),
        ("waiting","Waiting"),
        ("booked","Boooked"),
        ("cancelled","Cancelled")
    ],string="Booking State",default="new")


    room_state = fields.Selection([
        ("not_available","Not Available"),
        ("partially_available","Partially Available"),
        ("available","Available")
    ],string="State of the Booking",compute="_compute_the_state_of_the_rooms",readonly="True")

    cancelled_by = fields.Many2one('hr.employee', string='Cancelled by',readonly=True)
    cancel_reason = fields.Text(string='Cancellation Reason',readonly=True)

    @api.depends('order_line.product_id.is_available')
    def _compute_the_state_of_the_rooms(self):
        for record in self:
            l=[]
            for orders in record.order_line:
                if orders.product_id.is_hotel_room:
                    l.append(orders.product_id.is_available)
            if all(l):
                record.room_state = "available"
            elif any(l):
                record.room_state = "partially_available"
            else:
                record.room_state = "not_available"

    def action_confirm(self):
        for record in self:
            if record.room_state=="available":
                record.booking_state = "booked"
            elif record.room_state=="partially_available":
                record.booking_state = "waiting"
            else:
                raise ValidationError(_("No Rooms are available"))

    def action_cancel(self):
        
        if self.env.context.get('is_clicked_by_user'):
            
            super(HotelBookings, self).action_cancel()

            for record in self:
                if record.is_hotel_booking:
                    record.booking_state = 'cancelled'

            return {
                'name': 'Cancel Sale Order',
                'view_mode': 'form',
                'res_model': 'sale.order.cancel.wizard',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context': {
                    'active_id': self.id,
                },
            }
    
    
    
    
    




    

    

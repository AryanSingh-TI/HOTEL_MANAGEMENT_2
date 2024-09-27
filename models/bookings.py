from odoo import fields,api,models,_
from odoo.exceptions import ValidationError
import logging
import qrcode
import base64
from io import BytesIO

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

    room_type = fields.Selection([
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('suite', 'Suite Room')
    ], string="Room Type")

    validity_date = fields.Date(string="Check-in-Date",required=True,default=fields.Date.context_today)
    
    check_out_date = fields.Date(stirng="Check-out-Date",required=True)

    @api.constrains('order_line')
    def _check_order_line(self):
        for order in self:
            if not order.order_line:
                raise ValidationError("You must add at least one order line.")

    @api.model
    def create(self, vals):
        vals['company_id'] = self.env.company.id  # Set the current company
        return super(HotelBookings, self).create(vals)
    

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
            
    def action_report(self):
        for record in self:
            if record.booking_state in ["booked","cancelled"]:
                return self.env.ref('HOTEL_MANAGEMENT_2.action_report_sale_order').report_action(record)
            else:
                raise ValidationError(_("Need to be available or cancel state for a report"))

    def action_cancel(self):
        _logger=logging.getLogger(__name__)
        _logger.info(self.env.context)
        
        if self.env.context.get('is_clicked_by_user'):
            _logger.info("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ACTION CANCEL CALLED WITH USER CLICK@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            _logger.info(self.env.context)
            return {
                'name': 'Cancel Sale Order',
                'view_mode': 'form',
                'res_model': 'sale.order.cancel.wizard',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context': {
                    'active_id': self.id,
                    'default_sale_order_name' : self.name,
                    'default_sale_order_total': self.amount_total,
                    'sale_order_partner_id' : self.partner_id.id
                },
            }
        
        else:

            _logger.info("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ACTION CANCEL CALLED WITHOUT USER CLICK@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            _logger.info(self.env.context)
            super(HotelBookings, self).action_cancel()

            for record in self:
                if record.is_hotel_booking:
                    record.booking_state = 'cancelled' 

    qr_code = fields.Binary("QR Code", compute='generate_qr_code')

    def generate_qr_code(self):
        for rec in self:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr_data = f"Invoice No: {rec.name}, Customer: {rec.partner_id.name}, Amount Total: {rec.amount_total}"
            qr.add_data(qr_data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            temp = BytesIO()
            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())
            rec.update({'qr_code': qr_image})
    
    @api.depends('order_line.price_total')
    def _compute_total_price(self):
        for order in self:
            
            order.total_price = sum([line.price_total for line in order.order_line])
        
    total_price = fields.Float(string="Total Price",compute='_compute_total_price',store=True)


    def action_report_template(self):
        for order in self:
            if order.booking_state in ['cancelled','booked']:
                return self.env.ref("HOTEL_MANAGEMENT_2.template_report").report_action(order)
            else:
                raise ValidationError(_("The booking state must be cancelled or booking state"))
    
    def action_draft(self):
        _logger=logging.getLogger(__name__)
        for record in self:
                
            super(HotelBookings, record).action_draft()

            if not record.exists():
                _logger.info("##############################################The record no longer exists.###############################################")
                #raise ValidationError(_("##############################################The record no longer exists.###############################################"))
            
            _logger.info("##############################################The record exists.###############################################")
            email_to = 'recipient@example.com'
            email_cc = 'cc@example.com'         
            email_bcc = 'bcc@example.com'        
            subject = f"Cancellation of Order: {record.name}"
            _logger.info(record)
            _logger.info("##############################################GETTING MAIL VALUES.###############################################")
            mail_values = {
                'subject': subject,
                'body_html': record._get_email_body(),
                'email_to': email_to,
                'email_cc': email_cc,
                'attachment_ids': record._get_attachment()
            }

            _logger.info("##############################################GOT MAIL VALUES.###############################################")
            mail = self.env['mail.mail'].create(mail_values)
            mail.send()
            _logger.info(mail)
            _logger.info("##############################################MAIL SENT.###############################################")
            _logger.info("Email sent for order: %s", record.name)

            

    def _get_email_body(self):
        _logger=logging.getLogger(__name__)
        body = """
        <div style="background-color: black; color: white; padding: 20px;">
            <h1 style="font-family: 'Gothic Font';">Order Cancellation</h1>
            <p>Your order <strong>{}</strong> has been canceled.</p>
            <p>Thank you for your understanding.</p>
        </div>
        """.format(self.name)
        _logger.info("##############################################GOT BODY.###############################################")
        _logger.info(body)
        return body

    def _get_attachment(self):
        for record in self:
            _logger = logging.getLogger(__name__)
            
            _logger.info(record)
            report_action = self.env.ref('sale.action_report_saleorder')
            _logger.info("####################################################################GOT REPORT ACTION#################################################")
            _logger.info(report_action)
           
            _logger.info(record)
            if report_action:
                _logger.info("####################################################################REPORT ACTION DOES EXIST#################################################")
                pdf_content, report_format = self.env['ir.actions.report']._render_qweb_pdf('HOTEL_MANAGEMENT_2.template_report_id', set(self.ids))
                _logger.info(pdf_content)
               
                _logger.info(record)
                attachment = self.env['ir.attachment'].create({

                    'name': f"{record.name}_sale_order.pdf",
                    'type': 'binary',
                    'datas': base64.b64encode(pdf_content),
                    'res_model': 'sale.order',  
                    'res_id': record.id,
                    'mimetype': 'application/pdf',
                })
                _logger.info("####################################Attachment created with ID:################################################ %s", attachment)
                return [(4, attachment.id)]
            else:
                _logger.error("#################################################Report action not found: sale.report_saleorder_document########################################")
            return []
    def send_booking_confirmation_email(self):
        template_id = self.env.ref('HOTEL_MANAGEMENT_2.booking_confirmation_email_template')

        if template_id:
            for record in self:
                # pdf_content , pdf_format = self.env['ir.actions.report']._render_qweb_pdf('HOTEL_MANAGEMENT_2.booking_confirmation_email_template',set(self.ids))

                # attachment = self.env['ir.attachment'].create({

                #     'name' : f"{record.name}_confirmed",
                #     'type' : 'binary',
                #     'datas': base64.b64encode(pdf_content),
                #     'res_model':'sale.order',
                #     'res_id':record.id,
                #     'mimetype':'application/pdf',
                # })

                template_id.send_mail(record.id,force_send=True)
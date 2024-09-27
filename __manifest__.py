{
    'name': 'Hotel Management System 2',
    'version': '1.0',
    'category': 'management',
    'summary': 'Manage hotel floors, rooms, customers, and bookings.',
    'author': 'Aryan',
    'depends': ['base','product','sale','hr','sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/room_view.xml',
        'views/customer_view.xml',
        'views/bookings_view.xml',
        'views/employee_view.xml',
        'views/department_view.xml',
        'views/sale_order_cancel_wizard_views.xml',
        'views/settings.xml',
        'views/report_sale_order.xml',
        'views/template_report.xml',
        'views/inherit_template_report.xml',
        'views/inherit_quotation_report.xml',
        'views/inherit_accounts_report_for_total.xml',
        'views/email_template_confirmation.xml',
    ],
    'autoinstall' : True
    
}

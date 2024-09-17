{
    'name': 'Hotel Management System 2',
    'version': '1.0',
    'category': 'management',
    'summary': 'Manage hotel floors, rooms, customers, and bookings.',
    'author': 'Aryan',
    'depends': ['base','product','sale','hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/room_view.xml',
        'views/customer_view.xml',
        'views/bookings_view.xml',
        'views/employee_view.xml',
        'views/department_view.xml',
        'views/sale_order_cancel_wizard_views.xml',
    ],
    'autoinstall' : True
    
}

# -*- coding: utf-8 -*-
{
    'name': "hr_end_of_service_srcs",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','srcs_financial_requests','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/end_of_service_view.xml',
        'views/indemnity_config_view.xml',
        'views/reasons_end_of_service_config_view.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
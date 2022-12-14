# -*- coding: utf-8 -*-
{
    'name': "hr_training_plan",

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
    'depends': ['base','hr_training', 'survey','account','accounting_srcs'],#'hr_custom'

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/training_plan_security.xml',
         'data/sequence.xml',
         'data/ir_cron.xml',
        'views/views.xml',
        'views/templates.xml',
        'report/template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

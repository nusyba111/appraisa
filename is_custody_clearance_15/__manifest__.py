#######################################################################
#    IntelliSoft Software                                             #
#    Copyright (C) 2017 (<http://intellisoft.sd>) all rights reserved.#
#######################################################################

{
    'name': 'IntelliSoft Custody Clearance 15',
    'author': 'IntelliSoft Software',
    'website': 'http://www.intellisoft.sd',
    'description': "A module that allows for custody clearance. Migrated to Odoo 12.",
    'depends': ['account', 'is_accounting_approval_15','hr'],
    'category': 'Accounting',
    'data': [
        'security/security_view.xml',
        'security/ir.model.access.csv',
        'views/clearance_sequence.xml',
        'views/clearance_approval_view.xml',
        'views/reports_registration.xml',
        'views/report_clearance_approval.xml',
    ],
    'installable': True,
    'auto_install': False,
}
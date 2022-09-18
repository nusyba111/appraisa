# -*- coding: utf-8 -*-
{
    'name': "SRCS Accounting ",

    'summary': """
        """,

    'description': """
    """,
    'version': '15.0',
    'author': "IATL International",
    'website': "http://www.iatl-sd.com",
    'category': 'Accounting/Common',
    'depends': ['account','account_budget','account_accountant','base'],
    'data': [
        'security/srcs_security_groups.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/donors.xml',
        'views/journal.xml',
<<<<<<< HEAD
        'views/currency_conversion.xml',
        'views/budget.xml',
        'views/transfer_budget_line.xml',

=======
        'views/budget_revision.xml',
        'views/budget.xml',
        'views/currency_conversion.xml',
        'views/account_voucher_view.xml',
        'views/menu.xml',
       
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
    ],
}

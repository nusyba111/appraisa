# -*- coding: utf-8 -*-
{
    'name': "HR Assigment SRCS",

    'summary': """
        """,

    'description': """
        
    """,

    'author': "IATL International",
    'website': "http://www.iatl-sd.com",
    'license': "AGPL-3",
    'category': 'HR',
    'depends': ['hr','srcs_branch','hr_employee_srcs'],
    'data': [
        # 'security/security_views.xml',
        'security/ir.model.access.csv',
        'views/hr_views.xml',
        'report/report_actions.xml',
        'report/hr_assingment_report_template.xml',

    ],
}

# -*- coding: utf-8 -*-
###############################################################################
#
#    IATL-Intellisoft International Pvt. Ltd.
#    Copyright (C) 2021 Tech-Receptives(<http://www.iatl-intellisoft.com>).
#
###############################################################################

{
    'name': "Application SRCS",

    'author': "IATL Intellisoft International",
    'website': "http://www.iatl-intellisoft.com",
    'category': 'Human Resource',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_recruitment', 'srcs_branch'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/view_application_inherit.xml',
        'report/application_report.xml',
        'report/application _srcs_template.xml',
        'report/header_footer.xml',
        'report/refrence.xml',
        'report/interview.xml',
        'report/invoice.xml',
        'report/general.xml',
        'wizard/main_data.xml',
        'wizard/job_position.xml',
        'wizard/Main_Data.xml',
        'wizard/general.xml',
        'wizard/select_job.xml',
        

    ],

}

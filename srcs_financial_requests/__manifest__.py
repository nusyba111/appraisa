{
    'name': "SRCS Financial Request ",

    'summary': """
        """,

    'description': """
    """,
    'version': '15.0',
    'author': "IATL International",
    'website': "http://www.iatl-sd.com",
    'category': 'Accounting/Common',
    'depends': ['accounting_srcs','ii_simple_check_management','hr'],
    'data': [
        'security/ir.model.access.csv',
        'data/seqence.xml',
        'views/cash_request.xml',
        'views/payment_request.xml',
        'views/payment_clearanse.xml',
        'views/branch_loan_clearanse.xml',
        'views/employee_code.xml',
        'views/payment_filter.xml',
        'reports/cash_report.xml',
        'reports/payment_request.xml',
    ],
}
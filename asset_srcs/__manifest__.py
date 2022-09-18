{
    'name': "SRCS Asset ",

    'summary': """
        """,

    'description': """
    """,
    'version': '15.0',
    'author': "IATL International",
    'website': "http://www.iatl-sd.com",
    'category': 'Accounting/Common',
    'depends': ['account_asset','accounting_srcs'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/asset_srcs.xml',
    ],
}
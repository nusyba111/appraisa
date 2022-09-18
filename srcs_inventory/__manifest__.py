{
    'name': "SRCS Inventory",

    'summary': """
        """,

    'description': """
    """,
    'version': '15.0',
    'author': "IATL International",
    'website': "http://www.iatl-sd.com",
    # 'category': 'Accounting/Common',
    'depends': ['srcs_purchase', 'stock'],
    'data': [
            'security/ir.model.access.csv',
            'views/srcs_stock.xml',
            'views/product.xml',
            # 'report/pin_card_report_view.xml',
            'wizard/warehouse_report_view.xml',
            'wizard/recieved_report_view.xml',
            'wizard/health_report_view.xml',
            'wizard/pin_card_view.xml',

    ],
}
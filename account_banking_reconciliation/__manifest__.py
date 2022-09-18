# Copyright (C) 2019 Open Source Integrators
# <https://www.opensourceintegrators.com>
# Copyright (C) 2011 NovaPoint Group LLC (<http://www.novapointgroup.com>)
# Copyright (C) 2004-2010 OpenERP SA (<http://www.openerp.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "SRCS Bank Reconcilation",
    "summary": "Check transactions that cleared the bank",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "category": "Accounting and Financial Management",
    "author": "NovaPoint Group LLC, "
              "Open Source Integrators, "
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/account-reconcile",
    "depends": [
<<<<<<< HEAD
        "account","hr"
=======
        "account","hr","accounting_srcs"
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
    ],
    "data": [
        "security/account_banking_reconciliation.xml",
        "security/ir.model.access.csv",
        "views/account_banking_reconciliation.xml",
        "views/account_move_line.xml",
        # "report/bank_statement_report.xml",
        # "report/bank_statement_report.xml",
        "report/reconciliation_report.xml",
        # "report/report_bank_statement_detail.xml"
        ],
    "installable": True,
    # "development_status": "Stable",
    # "maintainers": ["max3903"],
}

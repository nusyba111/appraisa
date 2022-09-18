# -*- coding: utf-8 -*-
###############################################################################
#
#    IATL-Intellisoft International Pvt. Ltd.
#    Copyright (C) 2021 Tech-Receptives(<http://www.iatl-intellisoft.com>).
#
###############################################################################
from datetime import timedelta


from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, AccessError
from collections import defaultdict

from odoo.tools import float_compare, get_lang, format_date

from odoo.addons.purchase.models.purchase import PurchaseOrder as Purchase
from odoo.osv.expression import AND, NEGATIVE_TERM_OPERATORS

class ResBranch(models.Model):
    _name = 'res.branch'

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code")
    company_id = fields.Many2one('res.company', string="Region Name",
                                 default=lambda self: self.env.user.company_id)
<<<<<<< HEAD
=======
    location_id = fields.Many2one('account.analytic.account',domain="[('type','=','location')]")
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44

    @api.model_create_multi
    def create(self, vals):
        res = super(ResBranch, self).create(vals)
        location = self.env['account.analytic.account'].create(
            {
                'name': res.name,
                'type': 'location',
                'branch_id':res.id,
                'code': res.code,
            }
        )

        # res = super(ResBranch, self).create(vals)
        res.write({'location_id': location.id})
        print ("\nlocation:",location.id,"\n\n")
        return res

class ResUsers(models.Model):
    _inherit = 'res.users'

    current_branch = fields.Many2one("res.branch", string="Current Branch")
    allowed_branchs = fields.Many2many("res.branch", string="Allowed Branch")

    @api.constrains('current_branch', 'allowed_branchs')
    def _current_branch_on_allowed_branchs(self):
        if (self.current_branch.id not in self.allowed_branchs.ids):
            raise UserError(('Current branch must be in allowed branches!!'))


class accountMoveInherit(models.Model):
    _inherit = 'account.move'

    branch_id = fields.Many2one(comodel_name="res.branch",
                                string="Branch",
                                readonly=True,
                                default=lambda self: self.env.user.current_branch)


class accountMoveLine(models.Model):
    _inherit = 'account.move.line'

    branch_id_line = fields.Many2one(related='move_id.branch_id', string="Branch")

    # @api.onchange('product_id')
    # def get_analytic_account(self):
    #     for rec in self:
    #         rec.analytic_account_id = rec.move_id.branch_id.account_id.id


class accountPaymentInherit(models.Model):
    _inherit = 'account.payment'

    branch_id = fields.Many2one(comodel_name="res.branch",
                                string="Branch",
                                default=lambda self: self.env.user.current_branch,
                                )
    transfer_to = fields.Many2one('res.branch', string='Destination Branch')

# class ProductTemplate(models.Model):
#     _inherit = 'product.template'


#     arabic_name = fields.Char(string="Arabic Name", required=False, )
#     branch_ids = fields.Many2many(comodel_name="res.branch", string="Branch")
#     is_sapre = fields.Boolean('Spare')


# class productCategoryInherit(models.Model):
#     _inherit = 'product.category'

#     branch_ids = fields.Many2many(comodel_name="res.branch", string="Branch")
#     arabic_name = fields.Char(string="Arabic Name", required=False, )


class accountJournalInherit(models.Model):
    _inherit = 'account.journal'

    branch_id = fields.Many2one(comodel_name="res.branch",
                                string="Branch",
                                default=lambda self: self.env.user.current_branch.id)

    # allowed_users = fields.Many2many("res.users", string="Allowed users")


# class productProductInherit(models.Model):
#     _inherit = 'product.product'

#     @api.model
#     def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
#         args = args or []
#         domain = []
#         if (name or '').strip():
#             domain = ['|','|',
#                       ('name', operator, name),
#                       ('arabic_name', operator, name),
#                       ('default_code', operator, name)
#                       ]
#             if operator in NEGATIVE_TERM_OPERATORS:
#                 domain = domain[1:]
#         return self._search(AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

#     branch_id = fields.Many2one(comodel_name="res.branch",
#                                 string="Branch",
#                                 default=lambda self: self.env.user.current_branch.id)
#     # product_tmpl_id
#     arabic_name = fields.Char(related='product_tmpl_id.arabic_name',string="Arabic Name", required=False, )

class ConveriosnCurrency(models.Model):
    _inherit = 'currency.conversion'

    branch_id = fields.Many2one(comodel_name="res.branch",
                                string="Branch",
                                readonly=True,
                                default=lambda self: self.env.user.current_branch)

# class ConveriosnCurrency(models.Model):
#     _inherit = 'crossovered.budget'

#     def _get_default_project(self):
#         # for rec in self:
#             branch_project = self.env['account.analytic.account'].search([('branch_id','=',self.env.user.current_branch.id),('type','=','project')])
#             self.project_id = branch_project
#             print('_______________project',branch_project)

#     project_id = fields.Many2one('account.analytic.account',string='Project', required=True, domain="[('type','=','project')]", default=_get_default_project)

    

class ConveriosnCurrency(models.Model):
    _inherit = 'account.analytic.account'

    branch_id = fields.Many2one(comodel_name="res.branch",
                                string="Branch",
                                readonly=True,
                                default=lambda self: self.env.user.current_branch)

class SrcAssetBranch(models.Model):
    _inherit = "account.asset"

    branch_id = fields.Many2one(comodel_name="res.branch",
                                string="Branch",
                                readonly=True,
                                default=lambda self: self.env.user.current_branch)

class SrcAssetOperationBranch(models.Model):
    _inherit = "asset.opertaion"

    transfer_to = fields.Many2one('res.branch', string='Transfer To')
    branch_id = fields.Many2one(comodel_name="res.branch",
                                string="Branch",
                                readonly=True,
                                related='asset_id.branch_id')

class SrcsCashRequestBranch(models.Model):
    _inherit = "cash.request"

    branch_id = fields.Many2one(comodel_name="res.branch",
                                string="Branch",
                                readonly=True,
                                default=lambda self: self.env.user.current_branch)

class SrcsPayment(models.Model):
    _inherit = "payment.request"

    branch_id = fields.Many2one(comodel_name="res.branch",
                                string="Branch",
                                readonly=True,
                                default=lambda self: self.env.user.current_branch)


class SrcsBankReconcialtion(models.Model):
    _inherit = "bank.acc.rec.statement"

    branch_id = fields.Many2one(comodel_name="res.branch",
                                string="Branch",
                                readonly=True,
                                default=lambda self: self.env.user.current_branch)

class SrcsBudgetTransfer(models.Model):
<<<<<<< HEAD
    _inherit = "budget.line.transfer"
=======
    _inherit = "budget.revision"
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44

    branch_id = fields.Many2one(comodel_name="res.branch",
                                string="Branch",
                                readonly=True,
<<<<<<< HEAD
                                default=lambda self: self.env.user.current_branch)
=======
                                default=lambda self: self.env.user.current_branch)


class SrcBudget(models.Model):
    _inherit = "crossovered.budget"

    branch_id = fields.Many2one(comodel_name="res.branch",
                                string="Branch",
                                readonly=True,
                                default=lambda self: self.env.user.current_branch)
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44

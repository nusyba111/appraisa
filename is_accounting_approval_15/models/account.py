#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
#    Description: Accounting Approval                                        #
#    Author: IntelliSoft Software                                            #
#    Date: Aug 2015 -  Till Now                                              #
##############################################################################


from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import Warning, ValidationError, _logger, UserError


##############################################
class FinanceApprovalCheckLines(models.Model):
    _name = 'finance.approval.check.line'
    _description = 'Finance Approval Checks.'

    finance_id = fields.Many2one('finance.approval', string='Finance Approval', ondelete="cascade")
    Account_No = fields.Char(string='Account No')
    Check_no = fields.Char('Check No', required=True)
    Bank_id = fields.Many2one(related='journal_id.bank_id')
    check_date = fields.Date('Check Date', required=True)
    journal_id = fields.Many2one('account.journal', 'Bank/Cash Journal',
                                 help='Payment journal.',
                                 domain="[('type', 'in', ['bank'])]")
    exp_account = fields.Many2one('account.account', string="Expense or Debit Account", required=True)
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')
    amount = fields.Float('Check Amount', required=True)


########################################
class FinanceApprovalLine(models.Model):
    _name = 'finance.approval.line'
    _description = 'Finance Approval details.'

    finance_id = fields.Many2one('finance.approval', string='Finance Approval', ondelete="cascade")
    name = fields.Char('Narration', required=True)
    amount = fields.Float('Amount', required=True)
    notes = fields.Char('Notes')
    exp_account = fields.Many2one('account.account', string="Expense or Debit Account")
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')
    partner_id = fields.Many2one('res.partner', string='Partner')
    payment_method_name = fields.Many2one('account.payment.method')
    pa_name = fields.Char(related="payment_method_name.name")


#####################################
# add financial approval
class FinanceApproval(models.Model):
    _name = 'finance.approval'
    _description = 'A model for tracking finance approvals.'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'approval_no'
    _order = 'id desc'


    approval_no = fields.Char('Approval No.', help='Auto-generated Approval No. for finance approvals')
    activity_ids = fields.One2many('mail.activity', 'finance_id', 'Activity')
    name = fields.Char('Details', compute='_get_description', store=True, readonly=True)
    fa_date = fields.Date('Date', default=datetime.now(), required=True)
    requester = fields.Char('Requester', required=True, default=lambda self: self.env.user.name, readonly=True)
    request_amount = fields.Float('Requested Amount', required=True)
    request_currency = fields.Many2one('res.currency', 'Currency',
                                       default=lambda self: self.env.user.company_id.currency_id)
    f_limit = fields.Float('Finance Manager Limit', default=lambda self: self.env.user.company_id.f_limit)
    request_amount_words = fields.Char(string='Amount in Words', readonly=True, default=False, copy=False,
                                       compute='_compute_text', translate=True)

    @api.onchange('journal_id')
    def get_payment_method_name(self):
        if not self.journal_id:
            self.payment_method_name = False
        elif self.journal_id.type == 'cash':
            self.payment_method_name = self.env['account.payment.method'].search(
                [('code', '=', 'manual'), ('payment_type', '=', 'outbound')], limit=1).id

    department_id = fields.Many2one('hr.department', string="Department",
                                    default=lambda self: self.env.user.employee_id.department_id.id, readonly=True)
    beneficiary = fields.Many2one('res.partner', 'Beneficiary')
    reason = fields.Char('Narration', required=True)
    expense_item = fields.Char('Expense Item')
    state = fields.Selection([('draft', 'Request'),
                              ('dir_app', 'Direct Manager Approval'),
                              ('au_app', 'Auditor Approval'),
                              ('gm_as_app', 'GM Assistant Approval'),
                              ('gm_app', 'General Manager Approval'),
                              ('fm_app', 'Financial Manager Approval'),
                              ('ca_app', 'To validate'),
                              ('reject', 'Rejected'),
                              ('tr_app', 'To Validate'),
                              ('validate', 'Validated'),
                              ('done', 'Done'),
                              ('cleared', 'Cleared')],
                             string='Finance Approval Status', default='draft', track_visibility='onchange')
    manager_id = fields.Many2one('res.users', string='Approve')
    fc_app_id = fields.Many2one('res.users', string='Approve FC')
    au_app_id = fields.Many2one('res.users', string="Manager Approval By")
    gm_app_id = fields.Many2one('res.users', string="Financial  Approval By")
    ca_app_id = fields.Many2one('res.users', string="Validated By")
    exp_account = fields.Many2one('account.account', string="Expense or Debit Account")
    payment_method = fields.Selection(
        selection=[('cash', 'Cash'), ('cheque', 'Cheque'), ('transfer', 'Transfer'),
                   ('trust', 'Trust'), ('other', 'Other')], string='Payment Method')

    @api.onchange('journal_id')
    def payment_method_name_domain(self):
        payment_method_ids = []
        if self.journal_id:
            for line in self.journal_id.outbound_payment_method_line_ids:
                payment_method_ids.append(line.payment_method_id.id)
            return {'domain': {'payment_method_name': [('id', 'in', payment_method_ids)]}}

    payment_method_name = fields.Many2one('account.payment.method',
                                          domain=payment_method_name_domain)

    payment_method_code = fields.Char(
        related='payment_method_name.code',
        help="Technical field used to adapt the interface to the payment type selected.")
    pa_name = fields.Char(related="payment_method_name.name")
    journal_id = fields.Many2one('account.journal', 'Bank/Cash Journal',
                                 help='Payment journal.',
                                 domain="[('type', 'in', ['bank', 'cash'])]")
    bank_journal_id = fields.Many2one('account.journal', 'Check bank Journal',
                                      help='Payment journal.',
                                      domain=[('type', '=', 'bank')])
    move_id = fields.Many2one('account.move', 'Journal Entry', readonly=True)
    mn_remarks = fields.Text('Manager Remarks')
    auditor_remarks = fields.Text('Reviewer Remarks')
    fm_remarks = fields.Text('Finance Man. Remarks')
    gm_remarks = fields.Text('General Man. Remarks')
    view_remarks = fields.Text('View Remarks', readonly=True, compute='_get_remarks', store=True)
    partner_id = fields.Many2one('res.partner', string='Supplier')

    property_account_payable_id = fields.Many2one('account.account', string="",
                                                  related='partner_id.property_account_payable_id')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)

    # add company_id to allow this module to support multi-company
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    # adding analytic account
    analytic_account = fields.Many2one('account.analytic.account', string='Analytic Account/Cost Center')

    checks_id = fields.One2many('check_followups.check_followups', 'finance_id', 'chq Ref')
    finance_approval_line_ids = fields.One2many('finance.approval.line', 'finance_id',
                                                string='Finance Approval Details')
    finance_approval_check_line_ids = fields.One2many('finance.approval.check.line', 'finance_id',
                                                      string='Finance Approval Details')
    custody = fields.Boolean(string='Custody')
    department_manager_id = fields.Many2one('res.users', string="Department Manager",
                                            related='department_id.manager_id.user_id')
    department_approve = fields.Boolean('Approve', compute='_get_approve')
    on_credit = fields.Boolean('On Credit?', copy=False)
    credit_account_id = fields.Many2one('account.account', 'Credit Account')
    # Finance Approval
    fn_req_gm_approval = fields.Boolean(string="GM Approval", )
    fn_req_gm_approval_amount = fields.Float(string="Minimum Amount", required=False,
                                             readonly=False)

    gm_ass_id = fields.Many2one('res.users', string="General Manager Assistant")
    gm_id = fields.Many2one('res.users', string="General Manager")
    fm_id = fields.Many2one('res.users', string="Financial Manager")
    tr_id = fields.Many2one('res.users', string="Teller")
    approved_amount = fields.Float(string="Approved Amount", required=False, compute='get_approved_amount', store=True,
                                   readonly=False)
    tot_lines_amount = fields.Float(string="", required=False, compute='compute_tot_lines_amount')
    tot_cleared_amount = fields.Float(string="Cleared Amount", required=False, readonly=True, copy=False)
    un_cleared_amount = fields.Float(string="Uncleared Amount", required=False, compute='compute_un_cleared_amount',
                                     copy=False)
    is_cleared = fields.Boolean(string="Cleared", readonly=True, copy=False)

    @api.depends('request_amount')
    def get_approved_amount(self):
        self.approved_amount = self.request_amount


    @api.depends('finance_approval_line_ids')
    def compute_tot_lines_amount(self):
        tot_lines_amount = 0
        for line in self.finance_approval_line_ids:
            tot_lines_amount += line.amount
        self.tot_lines_amount = tot_lines_amount

    @api.depends('tot_lines_amount', 'tot_cleared_amount')
    def compute_un_cleared_amount(self):
        for rec in self:
            rec.un_cleared_amount = rec.approved_amount - rec.tot_cleared_amount
            if rec.un_cleared_amount < 0:
                rec.un_cleared_amount = 0
            if rec.un_cleared_amount == 0:
                rec.is_cleared = True

    @api.model
    def default_get(self, fields):
        res = super(FinanceApproval, self).default_get(fields)
        res['fn_req_gm_approval'] = self.env['ir.config_parameter'].sudo().get_param(
            'is_accounting_approval_15.fn_req_gm_approval')
        res['fn_req_gm_approval_amount'] = float(
            self.env['ir.config_parameter'].sudo().get_param('is_accounting_approval_15.fn_req_gm_approval_amount'))
        return res

    @api.depends('department_manager_id', 'state')
    def _get_approve(self):
        for rec in self:
            rec.department_approve = False
            if rec.state == 'dir_app' and rec.department_manager_id.id == self.env.user.id:
                rec.department_approve = True

    # Generate name of approval automatically
    @api.depends('approval_no', 'requester', 'beneficiary')
    def _get_description(self):
        self.name = (self.approval_no and ("Approval No: " + str(self.approval_no)) or " ") + "/" + (
                self.requester and ("Requester: " + self.requester) or " ") + "/" \
                    + (self.beneficiary and ("Beneficiary: " + self.beneficiary) or " ") + "/" + (
                            self.reason and ("Reason: " + self.reason) or " ")

    # Return request amount in words
    @api.depends('request_amount', 'request_currency')
    def _compute_text(self):
        from . import money_to_text_en
        for r in self:
            r.request_amount_words = money_to_text_en.amount_to_text(r.request_amount,
                                                                     r.request_currency.name)

    # Generate name of approval automatically
    @api.depends('mn_remarks', 'auditor_remarks', 'fm_remarks', 'gm_remarks')
    def _get_remarks(self):
        self.view_remarks = (self.mn_remarks and ("Manager Remarks: " + str(self.mn_remarks)) or " ") + "\n\n" + (
                self.auditor_remarks and ("Account Manager Remarks: " + str(self.auditor_remarks)) or " ") + "\n\n" + (
                                    self.fm_remarks and (
                                    "Financial Man. Remarks: " + self.fm_remarks) or " ") + "\n\n" + (
                                    self.gm_remarks and ("General Man. Remarks: " + self.gm_remarks) or " ")

    # validation
    @api.constrains('request_amount')
    def request_amount_validation(self):
        if self.request_amount <= 0:
            raise Warning(_("Request Amount Must be greater than zero!"))

    @api.model
    def create(self, vals):
        res = super(FinanceApproval, self).create(vals)
        # get finance approval sequence no.
        next_seq = self.env['ir.sequence'].get('finance.approval.sequence')
        res.update({'approval_no': next_seq})
        return res

    ############################################
    # added to allow for Direct manager approval
    # odoo15
    def action_cleared(self):
        state = 'cleared'
        self.state = state

    def action_gm_ass_approval(self):
        state = 'gm_as_app'
        self.state = state
        return True

    def action_gm_or_fm_approval(self):
        if self.fn_req_gm_approval and self.request_amount > self.fn_req_gm_approval_amount:
            state = 'gm_app'
            self.state = state
        else:
            state = 'fm_app'
            self.state = state
        self.gm_ass_id = self.env.user
        return True

    def action_fm_approval(self):
        state = 'fm_app'
        self.state = state
        self.gm_id = self.env.user
        return True

    # added to allow for Finance approval
    def manager_approval(self):
        state = 'fm_app'
        self.manager_id = self.env.user.id
        self.state = state
        return True

    # added to allow for Finance approval
    def finance_approval(self):
        # state = 'au_app'
        state = 'tr_app'
        self.fm_id = self.env.user.id
        self.state = state
        return True


    def general_approval(self):
        state = 'fm_app'
        self.gm_app_id = self.env.user.id
        self.state = state
        return True

    #############################################

    def cancel_button(self):
        self.move_id.button_cancel()
        self.move_id.unlink()
        self.state = 'draft'

    # reject finance approval
    def reject(self):

        self.state = 'reject'
        # Update footer message
        message_obj = self.env['mail.message']
        message = _("State Changed  Confirm -> <em>%s</em>.") % (self.state)
        msg_id = self.message_post(body=message)

    def action_view_checks(self):
        '''
        This function returns an action that display existing delivery orders
        of given sales order ids. It can either be a in a list or in a form
        view, if there is only one delivery order to show.
        '''
        action = self.env.ref('ii_simple_check_management.check_followups_vendor').read()[0]

        checks = self.mapped('checks_id')
        if len(checks) > 1:
            action['domain'] = [('id', 'in', checks.ids)]
        elif checks:
            action['views'] = [(self.env.ref('ii_simple_check_management.check_followups_form').id, 'form')]
            action['res_id'] = checks.id
        return action

    # validate, i.e. post to account moves
    def move_check_followups(self):
        if self.finance_approval_check_line_ids:
            for line1 in self.finance_approval_check_line_ids:
                if not line1.exp_account:
                    raise ValidationError(_("Please select account!"))
                debit_vals = {
                    'name': self.approval_no + str(line1.Check_no),
                    'partner_id': self.partner_id.id,
                    'account_id': line1.exp_account.id,
                    'currency_id': self.request_currency.id,
                    'amount_currency': line1.amount,
                    'debit': line1.amount / self.request_currency.rate,
                    'analytic_account_id': line1.analytic_account_id.id,
                    'company_id': self.company_id.id,
                }
                MONTH_LIST = [('1', 'Jan'), ('2', 'Feb'), ('3', 'Mar'), ('4', 'Apr'), ('5', 'May'), ('6', 'Jun'),
                              ('7', 'Jul'), ('8', 'Aug'), ('9', 'Sep'), ('10', 'Oct'), ('11', 'Nov'), ('12', 'Dec')]
                month = MONTH_LIST[int(datetime.now().strftime('%m')) - 1]
                year = datetime.now().strftime('%Y')
                month1 = MONTH_LIST[int(line1.check_date.strftime('%m')) - 1]
                year1 = line1.check_date.strftime('%Y')
                if month == month1 and year == year1:
                    check_state = 'donev'
                    credit_vals = {
                        'name': self.approval_no + str(line1.Check_no),
                        'partner_id': self.partner_id.id,
                        'account_id': line1.journal_id.default_account_id.id,
                        'currency_id': self.request_currency.id,
                        'amount_currency': -line1.amount,
                        'credit': line1.amount / self.request_currency.rate,
                        'company_id': self.company_id.id,
                    }
                else:
                    check_state = 'out_standing'
                    credit_vals = {
                        'name': self.approval_no + str(line1.Check_no),
                        'partner_id': self.partner_id.id,
                        'account_id': line1.journal_id.payment_credit_account_id.id,
                        'currency_id': self.request_currency.id,
                        'amount_currency': -line1.amount,
                        'credit': line1.amount / self.request_currency.rate,
                        'company_id': self.company_id.id,
                    }
                vals = {
                    'journal_id': line1.journal_id.id,
                    'move_type': 'entry',
                    'date': datetime.today(),
                    'ref': self.approval_no,
                    'company_id': self.company_id.id,
                    'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
                }
                move = self.env['account.move'].create(vals)
                move.action_post()

                dictionary = {
                    'name': self.approval_no,
                    # 'account_holder': self.company_id.id,
                    'Date': line1.check_date,
                    'finance_id': self.id,
                    'finance_line_id': line1.id,
                    'bank_id': line1.Bank_id.id,
                    # 'beneficiary_id': self.partner_id.id,
                    'amount': line1.amount,
                    'currency_id': self.request_currency.id,
                    'check_no': line1.Check_no,
                    'approval_check': True,
                    'state': check_state,
                    'type': 'outbound',
                    'communication': self.approval_no,
                    'company_id': self.company_id.id,
                }
                check = self.env['check_followups.check_followups'].create(dictionary)
                log = {
                    'move_id': move.id,
                    'name': self.approval_no,
                    'date': line1.check_date,
                    'Check': check.id,
                    'finance_id': self.id,
                }
                # log_obj = self.env['check_followups.checklogs']
                self.env['check_followups.checklogs'].create(log)

        return vals

    def move_without_check(self):
        entrys = []
        total = 0.0
        if self.on_credit:
            credit_account = self.credit_account_id
            journal = self.env['account.journal'].search([('type', '=', 'general')], limit=1)
        else:
            credit_account = self.journal_id.default_account_id
            journal = self.journal_id
        if self.finance_approval_line_ids:
            for line1 in self.finance_approval_line_ids:
                if not line1.exp_account:
                    raise ValidationError(_("Please select account!"))
                total += line1.amount

                debit_val = {
                    'name': line1.name,
                    'partner_id': self.partner_id.id,
                    'account_id': line1.exp_account.id,
                    'debit': line1.amount,
                    'analytic_account_id': line1.analytic_account_id.id,
                    'company_id': self.company_id.id,
                }
                entrys.append((0, 0, debit_val))
            credit_vals = {
                'name': self.reason,
                'partner_id': False,
                'account_id': credit_account.id,
                'credit': total,
                'company_id': self.company_id.id,
            }
            entrys.append((0, 0, credit_vals))
        vals = {
            'journal_id': journal.id,
            'date': self.fa_date,
            'ref': self.approval_no,
            'company_id': self.company_id.id,
            'line_ids': entrys
        }
        return vals

    def validate(self):
        if self.tot_lines_amount != self.approved_amount and not self.on_credit:
            raise UserError(
                'Finance Approval Details Total  Amount Should Equal The Approved Amount')
        if not self.journal_id:
            raise ValidationError('Please select Bank/Cash Journal.!')
        if self.on_credit:
            if not self.credit_account_id:
                raise UserError('Please Select The Credit Account.!')
            credit = []
            debit = []
            credit.append((0, 0, {
                'account_id': self.journal_id.default_account_id.id,
                'name': self.reason,
                'credit': self.approved_amount,
            }))
            credit.append((0, 0, {
                'account_id': self.credit_account_id.id,
                'name': self.reason,
                'debit': self.approved_amount,
            }))
            move = self.env['account.move'].create({
                'journal_id': self.journal_id.id,
                'ref': self.approval_no,
                'line_ids': credit,
            })
            move.action_post()
            self.state = 'validate'
            self.ca_app_id = self.env.user.id
            self.move_id = move.id
        if not self.on_credit:
            self.activity_ids.unlink()
            line_ids = []
            for x in self.finance_approval_line_ids:
                line = (0, 0, {
                    'name': x.name,
                    'account_id': x.exp_account.id,
                    'analytic_account_id': x.analytic_account_id.id,
                    'amount': x.amount,

                })
                line_ids.append(line)

            if not self.exp_account and self.custody == True:
                raise Warning(_("Expense or debit account must be selected!"))

            if not self.journal_id and not self.bank_journal_id and not self.on_credit:
                raise Warning(_("Journal must be selected!"))

            # account move entry
            if self.request_currency == self.env.user.company_id.currency_id:

                # corresponding details in account_move_line
                if self.payment_method_code != 'check_printing':
                    self.move_id = self.env['account.move'].create(self.move_without_check())
                    self.move_id.post()
                    self.state = 'validate'
                    self.ca_app_id = self.env.user.id
                elif self.payment_method_code == 'check_printing':
                    self.move_check_followups()
                    self.state = 'validate'
                    self.ca_app_id = self.env.user.id
            elif self.request_currency != self.env.user.company_id.currency_id:
                if self.payment_method_code != 'check_printing':
                    entrys = []
                    if self.finance_approval_line_ids:
                        total = 0
                        for line1 in self.finance_approval_line_ids:
                            total += line1.amount
                        if self.on_credit:
                            credit_account = self.credit_account_id
                            journal = self.env['account.journal'].search([('type', '=', 'general')], limit=1)
                        else:
                            credit_account = self.journal_id.default_account_id
                            journal = self.journal_id
                        credit_vals = {
                            'name': self.reason,
                            'partner_id': self.partner_id.id,
                            'account_id': credit_account.id,
                            'currency_id': self.request_currency.id,
                            'amount_currency': -total,
                            'credit': total / self.request_currency.rate,
                            'company_id': self.company_id.id,
                        }
                        entrys.append((0, 0, credit_vals))
                        # if total != self.request_amount:
                        #     raise UserError('Request amount and sum of details amount must be equal ')
                        for line in self.finance_approval_line_ids:
                            if not line.exp_account:
                                raise ValidationError(_("Please select account!"))
                            # if line.pa_name == 'Manual':
                            debit_val = {
                                'name': line.name,
                                'partner_id': line.partner_id.id,
                                'account_id': line.exp_account.id,
                                'debit': line.amount / self.request_currency.rate,
                                'currency_id': self.request_currency.id,
                                'amount_currency': line.amount,
                                'analytic_account_id': line.analytic_account_id.id,
                                'company_id': self.company_id.id,
                            }
                            entrys.append((0, 0, debit_val))
                    else:
                        debit_vals = {
                            'name': self.name,
                            'partner_id': self.partner_id.id,
                            'account_id': self.exp_account.id,
                            'debit': self.request_amount > 0.0 and self.request_amount or 0.0,
                            'analytic_account_id': self.analytic_account.id,
                            'credit': self.request_amount < 0.0 and -self.request_amount or 0.0,
                            'company_id': self.company_id.id,
                        }
                        entrys.append((0, 0, debit_vals))
                    vals = {
                        'journal_id': journal,
                        'date': self.fa_date,
                        'ref': self.approval_no,
                        'company_id': self.company_id.id,
                        'line_ids': entrys
                        # 'line_ids': [(0, 0, debit_val), (0, 0, credit_val)]
                    }
                    # add lines
                    self.move_id = self.env['account.move'].create(vals)
                    self.move_id.post()
                    # Change state if all went well!
                    self.state = 'validate'
                    self.tr_id = self.env.user.id
                elif self.payment_method_code == 'check_printing':
                    self.move_check_followups()
                    self.state = 'validate'
                    self.tr_id = self.env.user.id
            else:
                raise Warning(_("An issue was faced when validating!"))

        # Update footer message
        message_obj = self.env['mail.message']
        message = _("State Changed  Confirm -> <em>%s</em>.") % (self.state)
        msg_id = self.message_post(body=message)
        self.env['mail.activity'].search([('user_id', '=', self.env.uid), ('res_id', '=', self.id)]).action_done()

    def set_to_draft(self):
        self.state = 'draft'
        self.manager_id = None
        self.fc_app_id = None
        self.au_app_id = None
        self.gm_app_id = None
        self.ca_app_id = None

        # Update footer message
        message_obj = self.env['mail.message']
        message = _("State Changed  Confirm -> <em>%s</em>.") % (self.state)
        msg_id = self.message_post(body=message)


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    finance_id = fields.Many2one('finance.approval', string='Activity')

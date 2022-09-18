from odoo import fields, api, models, _
from datetime import datetime
from odoo.exceptions import UserError, ValidationError


class custody_clearance(models.Model):
    _name = 'custody.clearance'
    _description = 'A model for tracking custody clearance.'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'clearance_no'
    _order = 'id desc'

    clearance_no = fields.Char('Clearance No.', help='Auto-generated Clearance No. for custody clearances')
    cc_date = fields.Date('Date', default=fields.Date.today(), )
    requester = fields.Char('Requester', required=True, default=lambda self: self.env.user.name)
    is_partially_clearance = fields.Boolean(string="Partially Clearance", )
    payment_request_id = fields.Many2one('payment.request', 'Payment Request',domain="[('state', '=', 'payment'),('is_cleared','=',False),('user_id','=',requester),('is_working_addvance','=',True)]")
    clearance_amount_new = fields.Float(compute='approval_reference', string='Requested Amount', store=True, )
    # un_cleared_amount = fields.Float('Uncleared Amount', readonly=True)
    clearance_currency = fields.Many2one('res.currency', 'Currency')
    difference_amount = fields.Float('Difference Amount', readonly=True)
    # clearance_amount_words = fields.Char(string='Amount in Words', readonly=True, default=False, copy=False, compute='_compute_text', translate=True)
    reason = fields.Char('Reason')
    on_credit = fields.Boolean('On Credit?', copy=False)
    state = fields.Selection([
        ('draft','Draft'),('department', 'Department/Partner'),('finance','Finance Approval'),('internal','Internal Auditor'),
        ('secretary','Secretary General'),('payment','Payment'),('cleared', 'Cleared'),
    ], default='draft', string='State')
    # journal_id = fields.Many2one('account.journal', 'Bank/Cash Journal',
    #                             help='Payment journal.',
    #                             domain=[('type', 'in', ['bank', 'cash'])])
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    manager_id = fields.Many2one('res.users', string='Manager')
    mn_app_id = fields.Many2one('res.users', string="Manager Approval By")
    au_app_id = fields.Many2one('res.users', string="Reviewer Approval By")
    fm_app_id = fields.Many2one('res.users', string="Financial Approval By")
    at_app_id = fields.Many2one('res.users', string="Validated By")
    clearance_journal_id = fields.Many2one('account.journal', 'Clearance Journal', help='Clearance Journal')
    cr_account = fields.Many2one('account.account', string="Credit Account")
    pay_from = fields.Many2one('res.partner', string='Pay From')
    move_id = fields.Many2one('account.move', 'Clearance Journal Entry', readonly=True, copy=False)
    move2_id = fields.Many2one('account.move', 'Payment/Receipt Journal Entry', readonly=True, copy=False )
    custody_clearance_line_ids = fields.One2many('payment.request.clearance.lines', 'custody_clearance_id', string='Clearance Details')
    department_id = fields.Many2one('hr.department','Department')
    
    @api.depends('payment_request_id')
    def approval_reference(self):
        for rec in self:
            rec.clearance_amount_new = 0.0
            payment_obj = rec.payment_request_id
            if payment_obj:
                rec.clearance_amount_new = rec.payment_request_id.total_amount
            
    # Return clearance amount in words
    # @api.depends('clearance_amount', 'clearance_currency')
    # def _compute_text(self):
    #     from . import money_to_text_en

    #     self.clearance_amount_words = ''
    #     self.clearance_amount_words = money_to_text_en.amount_to_text(self.clearance_amount, self.clearance_currency.name)

    def action_department(self):
        self.write({'state': 'department'})

    def action_finance(self):
        self.write({'state': 'finance'})
    
    def action_internal(self):
        self.write({'state': 'internal'})

    def action_secretary(self):
        self.write({'state': 'secretary'})

    def payment(self):
        self.validate()
        self.write({'state':'payment'})

    # overriding create to save number with commit
    @api.model
    def create(self, vals):
        res = super(custody_clearance, self).create(vals)
        # get custody clearance sequence no.
        next_seq = self.env['ir.sequence'].get('custody.clearance.sequence')
        res.update({'clearance_no': next_seq})
        return res

    @api.onchange('payment_request_id')
    def _onchange_payment_request_id(self):
        lines = []
        for rec in self:
            if rec.payment_request_id:
                # rec.requested_amount = rec.payment_request_id.total_amount
                rec.clearance_currency = rec.payment_request_id.request_currency.id
                rec.reason = rec.payment_request_id.reason
                rec.clearance_journal_id = rec.payment_request_id.journal_id.id
                rec.cr_account = rec.payment_request_id.pay_to.address_home_id.property_account_receivable_id.id 
                rec.pay_from = rec.payment_request_id.pay_to.address_home_id.id
                # rec.un_cleared_amount = rec.difference_amount
                for line in rec.payment_request_id.budget_line_ids:
                    rec.custody_clearance_line_ids = [(5,0,0)]
                    vals = {
                        'currency_id': line.currency_id.id,
                        'donor_id': line.donor_id.id,
                        'project_id': line.project_id.id,
                        'account_id': line.account_id.id,
                        'analytic_activity_id': line.analytic_activity_id.id,
                        'payment_request_id': line.payment_request_id.id,
                        'payment_currency': line.payment_currency.id,
                        'request_amount': line.request_amount,
                        'budget_balance': line.budget_balance,
                        'location_id': line.location_id.id,
                        'crossovered_budget_id': line.crossovered_budget_id.id,
                    }
                    lines.append((0,0,vals)) 
                self.update({'custody_clearance_line_ids': lines})


    # validate, i.e. post to account moves
    @api.model
    def get_currency(self, line=None, total=None):
        if total:
            if self.clearance_currency != self.env.user.company_id.currency_id:
                return total / self.clearance_currency.rate
            else:
                return total
        if self.clearance_currency != self.env.user.company_id.currency_id:
            return line.amount / self.clearance_currency.rate
        else:
            return line

    
    # validate and check difference
    def validate(self):
        if not self.clearance_journal_id:
            raise ValidationError(_("Clearance journal must be selected!"))
        if not self.cr_account:
            raise ValidationError(_("Credit account must be selected!"))

        #################
        # clearance part#
        #################
        # account move entry
        db_total = 0
        entries = []
        for line in self.custody_clearance_line_ids:
            # print(line.amount)
            if not line.account_id:
                raise ValidationError(_("Please select account!"))
            # print('here custody',self.move_id.id)
            debit_val = {
                'move_id': self.move_id.id,
                'name': self.clearance_no,
                'account_id': line.account_id.id,
                'debit': line.request_amount,
                'analytic_account_id': line.project_id.id,
                'activity_id': line.analytic_activity_id.id,
                'location_id': line.location_id.id,
                'currency_id': (self.clearance_currency != self.env.user.company_id.currency_id)
                               and self.clearance_currency.id or None,
                'amount_currency': (self.clearance_currency != self.env.user.company_id.currency_id) and line.request_amount
                                   or None,
                # 'company_id': self.company_id.id,
            }
            entries.append((0, 0, debit_val))
            db_total += line.request_amount

        # create credit entry which is total of debit
        credit_val = {
            'move_id': self.move_id.id,
            'name': self.clearance_no,
            'account_id': self.cr_account.id,
            'credit': self.get_currency(total=db_total),
            'currency_id': (self.clearance_currency != self.env.user.company_id.currency_id)
                           and self.clearance_currency.id or None,
            'amount_currency': (self.clearance_currency != self.env.user.company_id.currency_id) and -(db_total)
                               or None,
            # 'company_id': self.company_id.id,
        }
        entries.append((0, 0, credit_val))

        vals = {
            'journal_id': self.clearance_journal_id.id,
            'date': datetime.today(),
            'ref': self.clearance_no,
            # 'company_id': self.company_id.id,
            'line_ids': entries,
        }

        self.move_id = self.env['account.move'].create(vals)

        ##################
        # difference part#
        ##################
        # get difference
        self.difference_amount = self.clearance_amount_new - db_total
        if self.difference_amount == 0:
            print('gggggg')
            # Change state if all went well!
            # self.schedule_fm()
            # self.state = 'validate'
            # self.approval_id.state = 'cleared'
            if self.payment_request_id:
                self.payment_request_id.is_cleared = True
                # self.payment_request_id.un_cleared_amount = 0
            
            self.at_app_id = self.env.user.id

        # difference greater
        elif self.difference_amount > 0:
            # account move entry
            if self.clearance_currency == self.env.user.company_id.currency_id:
                for line in self.custody_clearance_line_ids:
                    temp_move_line_db = {
                        'move_id': self.move2_id.id,
                        'name': self.clearance_no + ": Receipt of difference",
                        'account_id': self.clearance_journal_id.default_account_id.id,
                        'debit': self.difference_amount,
                        # 'activity_id': line.analytic_activity_id.id,
                        # 'location_id': line.location_id.id,
                        # 'company_id': self.company_id.id,
                    }

                # add credit entry
                temp_move_line_cr = {'move_id': self.move2_id.id,
                                     'name': self.clearance_no + ": Receipt of difference",
                                     'account_id': self.cr_account.id,
                                     'credit': self.difference_amount,
                                     
                                    #  'company_id': self.company_id.id,
                                     }
                account_move_vals = {'journal_id': self.clearance_journal_id.id,
                                     'date': datetime.today(),
                                     'ref': self.clearance_no,
                                    #  'CS': self.requester,
                                    #  'company_id': self.company_id.id,
                                     'line_ids': [(0, 0, temp_move_line_db), (0, 0, temp_move_line_cr)]
                                     }
                self.move2_id = self.env['account.move'].create(account_move_vals)

                # Change state if all went well!
                # self.schedule_fm()
                # self.state = 'validate'
                if self.payment_request_id:
                    self.payment_request_id.is_cleared = True
                    # self.payment_request_id.un_cleared_amount = self.difference_amount

                self.at_app_id = self.env.user.id


            elif self.clearance_currency != self.env.user.company_id.currency_id:
                temp_move_line_db = {'move_id': self.move2_id.id,
                                    'name': self.clearance_no + ": Receipt of difference",
                                    'account_id': self.clearance_journal_id.default_account_id.id,
                                    'currency_id': self.clearance_currency.id,
                                    'amount_currency': self.difference_amount,
                                    'debit': self.difference_amount / self.clearance_currency.rate,
                                    # 'activity_id': line.analytic_activity_id.id,
                                    # 'location_id': line.location_id.id,
                                    #  'company_id': self.company_id.id,
                                    }
                # add credit entry
                temp_move_line_cr = {'move_id': self.move2_id.id,
                                    'name': self.clearance_no + ": Receipt of difference",
                                    'account_id': self.cr_account.id,
                                    'currency_id': self.clearance_currency.id,
                                    'amount_currency': -self.difference_amount,
                                    'credit': self.difference_amount / self.clearance_currency.rate,
                                    #'company_id': self.company_id.id,
                                    }
                account_move_vals = {'journal_id': self.clearance_journal_id.id,
                                     'date': datetime.today(),
                                     'ref': self.clearance_no,
                                    #  'CS': self.requester,
                                    #  'company_id': self.company_id.id,
                                     'line_ids': [(0, 0, temp_move_line_db), (0, 0, temp_move_line_cr)]
                                     }

                self.move2_id = self.env['account.move'].create(account_move_vals)

                # Change state if all went well!
                # self.schedule_fm()
                # self.state = 'validate'
                if self.payment_request_id:
                    self.payment_request_id.is_cleared = True
                    # self.payment_request_id.un_cleared_amount = self.difference_amount
                self.at_app_id = self.env.user.id
               
            else:
                raise Warning(_("An issue was faced when validating difference!"))
        # difference less
        elif self.difference_amount < 0:
            # account move entry
            if self.clearance_currency == self.env.user.company_id.currency_id:
                temp_move_line_db = {'move_id': self.move2_id.id,
                                    'name': str(self.clearance_no) + ": Payment of difference",
                                    'account_id': self.cr_account.id,
                                    'debit': abs(self.difference_amount),
                                    # 'activity_id': line.analytic_activity_id.id,
                                    # 'location_id': line.location_id.id,
                                    #'company_id': self.company_id.id,
                                    }
                # add credit entry
                temp_move_line_cr = {'move_id': self.move2_id.id,
                                    'name': str(self.clearance_no) + ": Payment of difference",
                                    'account_id': self.clearance_journal_id.default_account_id.id,
                                    'credit': abs(self.difference_amount),
                                    #'company_id': self.company_id.id,
                                     }

                account_move_vals = {'journal_id': self.clearance_journal_id.id,
                                    'date': datetime.today(),
                                    'ref': self.clearance_no,
                                    #'company_id': self.company_id.id,
                                    'line_ids': [(0, 0, temp_move_line_db), (0, 0, temp_move_line_cr)]
                                     }
                self.move2_id = self.env['account.move'].create(account_move_vals)

                # Change state if all went well!
                # self.schedule_fm()
                # self.state = 'validate'
                if self.payment_request_id:
                    self.payment_request_id.is_cleared = True
                self.at_app_id = self.env.user.id

                
            elif self.clearance_currency != self.env.user.company_id.currency_id:
                temp_move_line_db = {'move_id': self.move2_id.id,
                                    'name': str(self.clearance_no) + ": Payment of difference",
                                    'account_id': self.cr_account.id,
                                    'currency_id': self.clearance_currency.id,
                                    'amount_currency': abs(self.difference_amount),
                                    'debit': abs(self.difference_amount) / self.clearance_currency.rate,
                                    # 'activity_id': line.analytic_activity_id.id,
                                    # 'location_id': line.location_id.id,
                                    #  'company_id': self.company_id.id,
                                     }
                # add credit entry
                temp_move_line_cr = {'move_id': self.move2_id.id,
                                     'name': str(self.clearance_no) + ": Payment of difference",
                                     'account_id': self.clearance_journal_id.default_account_id.id,
                                     'currency_id': self.clearance_currency.id,
                                     'amount_currency': -(abs(self.difference_amount)),
                                     'credit': abs(self.difference_amount) / self.clearance_currency.rate,
                                    #  'company_id': self.company_id.id,
                                     }
                account_move_vals = {'journal_id': self.clearance_journal_id.id,
                                     'date': datetime.today(),
                                     'ref': self.clearance_no,
                                    #  'company_id': self.company_id.id,
                                     'line_ids': [(0, 0, temp_move_line_db), (0, 0, temp_move_line_cr)]
                                     }
                self.move2_id = self.env['account.move'].create(account_move_vals)

                # Change state if all went well!
                # self.schedule_fm()
                # self.state = 'validate'
                if self.payment_request_id:
                    self.payment_request_id.is_cleared = True
                self.at_app_id = self.env.user.id

        else:
            raise Warning(_("An issue was faced when validating!"))
        self.move_id.post()
        if self.move2_id:
            self.move2_id.post()

class custody_clearance_line(models.Model):
    _name = 'payment.request.clearance.lines'
   

    custody_clearance_id = fields.Many2one('custody.clearance', string='Custody Clearance', ondelete="cascade")
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, store=True)
    donor_id = fields.Many2one('res.partner', string='Donor', required=True)
    project_id = fields.Many2one('account.analytic.account',string='Project', domain="[('type','=','project')]")
    account_id = fields.Many2one('account.account', string='Account',  domain="[('internal_group','in',['expense','asset'])]")
    analytic_activity_id = fields.Many2one('account.analytic.account', 'Output/Activity', domain="[('type','=','activity')]")
    payment_request_id = fields.Many2one('payment.request', string='Payment Request')
    payment_currency = fields.Many2one(related='payment_request_id.request_currency')
    request_amount = fields.Monetary('Requested Amount', currency_field = "payment_currency", required=True)
    budget_balance = fields.Monetary(string='Budget Balance', store=True)
    location_id = fields.Many2one('account.analytic.account', domain="[('type','=','location')]")
    crossovered_budget_id = fields.Many2one('crossovered.budget', readonly=True)

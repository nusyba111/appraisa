# Copyright (C) 2019 Open Source Integrators
# <https://www.opensourceintegrators.com>
# Copyright (C) 2011 NovaPoint Group LLC (<http://www.novapointgroup.com>)
# Copyright (C) 2004-2010 OpenERP SA (<http://www.openerp.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import time

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
from operator import itemgetter
from odoo.tools.float_utils import float_round


class BankAccRecStatement(models.Model):
    _name = "bank.acc.rec.statement"
    _description = "Bank Acc Rec Statement"
    _order = "ending_date desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

<<<<<<< HEAD
=======
    name = fields.Char('Name', required=True, size=64, states={'done': [('readonly', True)]}, help="This is a unique name identifying the statement (e.g. Bank X January 2012).")
    account_id = fields.Many2one('account.account', 'Account', required=True, states={'done': [('readonly', True)]}, domain="[('company_id', '=', company_id)]", help="The Bank/Gl Account that is being reconciled.")
    ending_date = fields.Date('Ending Date', required=True, states={'done': [('readonly', True)]}, default=time.strftime('%Y-%m-%d'), help="The ending date of your bank statement.")
    last_ending_date = fields.Date('Last Stmt Date', help="The previous statement date of your bank statement.")
    starting_balance = fields.Float('Starting Balance', required=True, digits=dp.get_precision('Account'), help="The Starting Balance on your bank statement.", states={'done': [('readonly', True)]})
    ending_balance = fields.Float('Ending Balance', required=True, digits=dp.get_precision('Account'), help="The Ending Balance on your bank statement.", states={'done': [('readonly', True)]})
    company_id = fields.Many2one('res.company', 'Company', required=True, readonly=True, default= lambda self: self.env.company, help="The Company for which the deposit ticket is made to")
    notes = fields.Text('Notes')
    prepared_date = fields.Date('Prepared Date', readonly=True)
    prepared_by_user_id = fields.Many2one('res.users', 'Prepared By', readonly=True)
    validated_date = fields.Date('Validated Date', readonly=True)
    validated_by_user_id = fields.Many2one('res.users', 'Validated By', readonly=True)
    reviewed_date = fields.Date('Reviewed Date', readonly=True, copy=False,help="Date in which Deposit Ticket was verified.")
    reviewed_by_user_id = fields.Many2one('res.users', 'Reviewed By', readonly=True, copy=False, help="Entered automatically by the “last user” who saved it. System generated.")
    approved_date = fields.Date('Approved Date', readonly=True)
    approved_date_by_user_id = fields.Many2one('res.users', 'Approved By', readonly=True)
    credit_move_line_ids = fields.One2many('bank.acc.rec.statement.line', 'statement_id', 'Credits', copy=False, domain=[('type', '=', 'cr')], states={'done': [('readonly', True)]})
    debit_move_line_ids = fields.One2many('bank.acc.rec.statement.line', 'statement_id', 'Debits', copy=False, domain=[('type','=','dr')], states={'done': [('readonly', True)]})
    cleared_balance = fields.Float(compute='_compute_get_balance', string='Cleared Balance', digits=dp.get_precision('Account'), help="Total Sum of the Deposit Amount Cleared – Total Sum of Checks, Withdrawals, Debits, and Service Charges Amount Cleared")
    difference = fields.Float(compute='_compute_get_balance', string='Difference', digits=dp.get_precision('Account'), help="(Ending Balance – Beginning Balance) - Cleared Balance.")
    cleared_balance_cur = fields.Float(compute='_compute_get_balance', string='Cleared Balance (Cur)', digits=dp.get_precision('Account'), help="Total Sum of the Deposit Amount Cleared – Total Sum of Checks, Withdrawals, Debits, and Service Charges Amount Cleared")
    difference_cur = fields.Float(compute='_compute_get_balance', string='Difference (Cur)', digits=dp.get_precision('Account'), help="(Ending Balance – Beginning Balance) - Cleared Balance.")
    uncleared_balance = fields.Float(compute='_compute_get_balance', string='Uncleared Balance', digits=dp.get_precision('Account'), help="Total Sum of the Deposit Amount Uncleared – Total Sum of Checks, Withdrawals, Debits, and Service Charges Amount Uncleared")
    uncleared_balance_cur = fields.Float(compute='_compute_get_balance', string='Unleared Balance (Cur)', digits=dp.get_precision('Account'), help="Total Sum of the Deposit Amount Uncleared – Total Sum of "
                                              "Checks, Withdrawals, Debits, "
                                              "and Service Charges "
                                              "Amount Uncleared")
    sum_of_credits = fields.Float(compute='_compute_get_balance',
                                  string='Checks, Withdrawals, Debits, and'
                                         ' Service Charges Amount',
                                  digits=dp.get_precision('Account'),
                                  type='float',
                                  help="Total SUM of Amts of lines with"
                                       " Cleared = True")
    sum_of_debits = fields.Float(compute='_compute_get_balance',
                                 string='Deposits, Credits, and '
                                        'Interest Amount',
                                 digits=dp.get_precision('Account'),
                                 help="Total SUM of Amts of lines with "
                                      "Cleared = True")
    sum_of_credits_cur = fields.Float(compute='_compute_get_balance',
                                      string='Checks, Withdrawals, Debits, and'
                                             ' Service Charges Amount (Cur)',
                                      digits=dp.get_precision('Account'),
                                      help="Total SUM of Amts of lines "
                                           "with Cleared = True")
    sum_of_debits_cur = fields.Float(compute='_compute_get_balance',
                                     string='Deposits, Credits, and '
                                            'Interest Amount (Cur)',
                                     digits=dp.get_precision('Account'),
                                     help="Total SUM of Amts of lines "
                                          "with Cleared = True")
    sum_of_credits_lines = fields.Integer(compute='_compute_get_balance',
                                          string='''Checks, Withdrawals,
                                          Debits, and Service Charges # of
                                          Items''',
                                          help="Total of number of lines with "
                                          "Cleared = True")
    sum_of_debits_lines = fields.Integer(compute='_compute_get_balance',
                                         string='''Deposits, Credits, and
                                         Interest # of Items''',
                                         help="Total of number of lines with"
                                         " Cleared = True")
    sum_of_ucredits = fields.Float(compute='_compute_get_balance',
                                   string='Uncleared - Checks, Withdrawals, '
                                          'Debits, and Service Charges Amount',
                                   digits=dp.get_precision('Account'),
                                   help="Total SUM of Amts of lines with "
                                        "Cleared = False")
    sum_of_udebits = fields.Float(compute='_compute_get_balance',
                                  string='Uncleared - Deposits, Credits, '
                                         'and Interest Amount',
                                  digits=dp.get_precision('Account'),
                                  help="Total SUM of Amts of lines with "
                                       "Cleared = False")
    sum_of_ucredits_cur = fields.Float(compute='_compute_get_balance',
                                       string='Uncleared - Checks, '
                                              'Withdrawals, Debits, and '
                                              'Service Charges Amount (Cur)',
                                       digits=dp.get_precision('Account'),
                                       help="Total SUM of Amts of lines "
                                            "with Cleared = False")
    sum_of_udebits_cur = fields.Float(compute='_compute_get_balance',
                                      string='Uncleared - Deposits, Credits, '
                                             'and Interest Amount (Cur)',
                                      digits=dp.get_precision('Account'),
                                      help="Total SUM of Amts of lines with"
                                           " Cleared = False")
    sum_of_ucredits_lines = fields.Integer(compute='_compute_get_balance',
                                           string='Uncleared - Checks, '
                                           'Withdrawals, Debits, and '
                                           'Service Charges # of Items',
                                           help="Total of number of lines with"
                                           " Cleared = False")
    sum_of_udebits_lines = fields.Integer(compute='_compute_get_balance',
                                          string='''Uncleared - Deposits,
                                          Credits, and Interest # of Items''',
                                          help="Total of number of lines "
                                          "with Cleared = False")
    suppress_ending_date_filter = fields.Boolean('Remove Ending Date Filter',
                                                 help="If this is checked then"
                                                      " the Statement End Date"
                                                      " filter on the "
                                                      "transactions below will"
                                                      " not occur. All "
                                                      "transactions would "
                                                      "come over.")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('finance_officer','Finance Officer'),
        ('validate','Financial Director'),
        ('to_be_reviewed', 'Internal Auditor'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], 'State', index=True, readonly=True, default='draft')

    account_ending_balance = fields.Float(string='Account Ending Balance', compute='get_account_balance')

    reason = fields.Char('reason', track_visibility='onchange')
    journal_id = fields.Many2one('account.journal', string='Journal')
    account_id = fields.Many2one('account.account', 'Account', required=True, readonly=False,
                                 compute='get_bank_account_id',
                                 states={'done': [('readonly', True)]},
                                 domain="[('company_id', '=', company_id)]",
                                 help="The Bank/Gl Account that is being "
                                      "reconciled.", store=True)


    # new fields
    total_debit_amount = fields.Float(compute='call_total_debit_amount', string="Total In Debit")
    total_credit_amount = fields.Float(compute='call_total_credit_amount', string="Total In Credit")
    total_for_differance = fields.Float(compute='_compute_total_amount', string='Totals')

    @api.depends('debit_move_line_ids')
    def call_total_debit_amount(self):
        sum = 0.0
        for rec in self.debit_move_line_ids:
            if rec.not_in_system == True:
                sum += rec.amount
            self.total_debit_amount = sum

    @api.depends('credit_move_line_ids')
    def call_total_credit_amount(self):
        sum = 0.0
        for res in self.credit_move_line_ids:
            if res.not_in_system == True:
                sum += res.amount
            self.total_credit_amount = sum

    @api.depends('total_debit_amount', 'total_credit_amount')
    def _compute_total_amount(self):
        self.total_for_differance = self.total_debit_amount - self.total_credit_amount
        
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
    def check_group(self):
        """Check if following security constraints are implemented for groups:
        Bank Statement Preparer– they can create, view and delete any of the
        Bank Statements provided the Bank Statement is not in the DONE state,
        or the Ready for Review state.
        Bank Statement Verifier – they can create, view, edit, and delete any
        of the Bank Statements information at any time.
        NOTE: DONE Bank Statements  are only allowed to be deleted by a
        Bank Statement Verifier."""
<<<<<<< HEAD
        # model_data_obj = self.env['ir.model']
        res_groups_obj = self.user_has_groups('account_banking_reconciliation.group_bank_stmt_verifier')
        # group_verifier_id = model_data_obj._get_id(
        #     'group_bank_stmt_verifier')
        print('__________________\n \n',res_groups_obj)
        for statement in self:
            if statement.state != 'draft' and not res_groups_obj:
                print('22222222222\n \n',res_groups_obj)
=======
        res_groups_obj = self.user_has_groups('account_banking_reconciliation.group_bank_stmt_verifier')
        for statement in self:
            if statement.state != 'draft' and not res_groups_obj:
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
                raise UserError(_("Only a member of  "
                                "group may delete/edit "
                                "bank statements when not in draft "
                                "state!"))
            else:
                print('+++++++++++++++++++++++\n \n',res_groups_obj)
                pass
<<<<<<< HEAD
                # res_id = model_data_obj.browse(group_verifier_id).res_id
                # group_verifier = res_groups_obj.browse([res_id])
                # group_user_ids = [user.id for user in res_groups_obj.users]
                # if statement.state != 'draft' \
                #         and self.env.uid not in res_groups_obj:
                #     raise UserError(_("Only a member of '%s' "
                #                       "group may delete/edit "
                #                       "bank statements when not in draft "
                #                       "state!" % (res_groups_obj.name)))
            #
=======
               
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
        return True

    def write(self, vals):
        # Check if the user is allowed to perform the action
        self.check_group()
        return super(BankAccRecStatement, self).write(vals)

    def unlink(self):
        """Check if the user is allowed to perform the action"""
        self.check_group()
        return super(BankAccRecStatement, self).unlink()

    def check_difference_balance(self):
        # Check if difference balance is zero or not.
        for statement in self:
<<<<<<< HEAD

=======
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
            if statement.cleared_balance_cur:
                if statement.difference_cur != 0.0:
                    raise UserError(_("Prior to reconciling a statement, "
                                      "all differences must be accounted for "
                                      "and the Difference balance must be "
                                      "zero. Please review "
                                      "and make necessary changes."))
            else:
                if statement.difference != 0.0:
                    raise UserError(_("Prior to reconciling a statement, "
                                      "all differences must be accounted for "
                                      "and the Difference balance must "
                                      "be zero. Please review "
                                      "and make necessary changes."))
        return True

    def action_cancel(self):
        """Cancel the the statement."""
        self.write({'state': 'cancel'})
        return True
    
<<<<<<< HEAD
    def action_prepared(self):
        """Prepared the the statement."""
=======
    @api.depends('account_id', 'ending_date')
    def get_lines(self):
        cr_line_ids = []
        dr_line_ids = []
        account_move_line_obj = self.env['account.move.line']
        if self.ending_date and self.account_id:
            for statement in self:
                statement.credit_move_line_ids.unlink()
                statement.debit_move_line_ids.unlink()
            domain = [('account_id', '=', self.account_id.id),
                      ('move_id.state', '=', 'posted'),
                      ('cleared_bank_account', '=', False),('date', '<=', self.ending_date)]
            for line in account_move_line_obj.search(domain):
                amount_currency = (line.amount_currency < 0) and (
                    -1 * line.amount_currency) or line.amount_currency
                res = {
                    'date': line.date,
                    'ref': line.ref,
                    'not_in_system':line.move_id.not_in_system,
                    'check_no': line.Check_no,
                    'currency_id': line.currency_id.id,
                    'amount': line.credit or line.debit,
                    'amountcur': amount_currency,
                    'name': line.name,
                    'statement_id': self.id,
                    'move_line_id': line.id,
                    'type': line.credit and 'cr' or 'dr'}
                if res['type'] == 'cr':
                    cr_line_ids.append((0,0,res))
                if res['type'] == 'dr':
                    dr_line_ids.append((0,0,res))
            self.update({'credit_move_line_ids': cr_line_ids})
            self.update({'debit_move_line_ids': dr_line_ids})
                        
    def action_prepared(self):
        """Prepared the the statement lines."""
        self.get_lines()
        ending_balance = 0
        credit_amount = 0
        debit_amount = 0
        # get starting balance for the account
        statement_obj = self.env['bank.acc.rec.statement']
        domain = [('account_id', '=', self.account_id.id), ('state', '=', 'done')]
        # get all statements for this account in the past
        for statement in statement_obj.search(domain):
            if statement.ending_date < self.ending_date:
                ending_balance += statement.ending_balance
        self.starting_balance = ending_balance
        for cr in self.credit_move_line_ids:
            credit_amount += cr.amount
        for cr in self.debit_move_line_ids:
            debit_amount += cr.amount
        self.ending_balance =   debit_amount - credit_amount
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
        self.write({'state': 'finance_officer',
                    'prepared_date':time.strftime('%Y-%m-%d'),
                    'prepared_by_user_id':self.env.uid})
        return True

    def action_validate(self):
        """validate the the statement."""
        self.write({'state': 'validate',
                    'validated_date':time.strftime('%Y-%m-%d'),
                    'validated_by_user_id':self.env.uid})
        return True

    def action_review(self):
        """Change the status of statement from 'draft' to 'to_be_reviewed'."""
        # If difference balance not zero prevent further processing
        self.check_difference_balance()
        #add internal auditor
        self.write({'state': 'to_be_reviewed',
                    'reviewed_by_user_id': self.env.uid,
                    'reviewed_date': time.strftime('%Y-%m-%d')})
        return True

    def action_process(self):
        """Set the account move lines as 'Cleared' and
        Assign 'Bank Acc Rec Statement ID'
        for the statement lines which are marked as 'Cleared'."""
        # If difference balance not zero prevent further processing
        self.check_difference_balance()
        for statement in self:
            statement_lines = \
                statement.credit_move_line_ids + statement.debit_move_line_ids
            for statement_line in statement_lines:
                # Mark the move lines as 'Cleared'mand assign
                # the 'Bank Acc Rec Statement ID'
                statement_id = \
                    statement_line.cleared_bank_account and \
                    statement.id or False
                cleared_bank_account = \
                    statement_line.cleared_bank_account
                statement_line.move_line_id.write({
                    'cleared_bank_account': cleared_bank_account,
                    'bank_acc_rec_statement_id': statement_id})
            #add seretary general
            statement.write({'state': 'done',
                             'approved_date_by_user_id': self.env.uid,
                             'approved_date': time.strftime('%Y-%m-%d')})
        return True

    def action_cancel_draft(self):
        """Reset the statement to draft and perform resetting operations."""
        for statement in self:
            statement_lines = \
                statement.credit_move_line_ids + statement.debit_move_line_ids
            line_ids = []
            for statement_line in statement_lines:
                if statement_line.move_line_id:
                    # Find move lines related to statement lines
                    line_ids.append(statement_line.move_line_id.id)
            # Reset 'Cleared' and 'Bank Acc Rec Statement ID' to False
            self.env['account.move.line'].browse(line_ids).write(
                {'cleared_bank_account': False,
                 'bank_acc_rec_statement_id': False})

            # Reset 'Cleared' in statement lines
            statement_lines.write({'cleared_bank_account': False,
                                   'research_required': False})
            # Reset statement
            statement.write({'state': 'draft'})
        return True

    def action_select_all(self):
        """Mark all the statement lines as 'Cleared'."""
        for statement in self:
            statement_lines = \
                statement.credit_move_line_ids + statement.debit_move_line_ids
            statement_lines.write({'cleared_bank_account': True})
        return True

    def action_unselect_all(self):
        """Reset 'Cleared' in all the statement lines."""
        for statement in self:
            statement_lines = \
                statement.credit_move_line_ids + statement.debit_move_line_ids
            statement_lines.write({'cleared_bank_account': False})
        return True

    def _compute_get_balance(self):
        """Computed as following:
        A) Deposits, Credits, and Interest Amount:
        Total SUM of Amts of lines with Cleared = True
        Deposits, Credits, and Interest # of Items:
        Total of number of lines with Cleared = True
        B) Checks, Withdrawals, Debits, and Service Charges Amount:
        Checks, Withdrawals, Debits, and Service Charges Amount # of Items:
        Cleared Balance (Total Sum of the Deposit Amount Cleared (A) –
        Total Sum of Checks Amount Cleared (B))
        Difference= (Ending Balance – Beginning Balance) - cleared balance =
        should be zero.
        """
        account_precision = self.env['decimal.precision'].precision_get(
            'Account')
        for statement in self:
            for line in statement.credit_move_line_ids:
                statement.sum_of_credits += \
                    line.cleared_bank_account and \
                    float_round(line.amount, account_precision) or 0.0
                statement.sum_of_credits_cur += \
                    line.cleared_bank_account and \
                    float_round(line.amountcur, account_precision) or 0.0
                statement.sum_of_credits_lines += \
                    line.cleared_bank_account and 1 or 0
                statement.sum_of_ucredits += \
                    (not line.cleared_bank_account) and \
                    float_round(line.amount, account_precision) or 0.0
                statement.sum_of_ucredits_cur += \
                    (not line.cleared_bank_account) and \
                    float_round(line.amountcur, account_precision) or 0.0
                statement.sum_of_ucredits_lines += \
                    (not line.cleared_bank_account) and 1 or 0
            for line in statement.debit_move_line_ids:
                statement.sum_of_debits += \
                    line.cleared_bank_account and \
                    float_round(line.amount, account_precision) or 0.0
                statement.sum_of_debits_cur += \
                    line.cleared_bank_account and \
                    float_round(line.amountcur, account_precision) or 0.0
                statement.sum_of_debits_lines += \
                    line.cleared_bank_account and 1 or 0
                statement.sum_of_udebits += \
                    (not line.cleared_bank_account) and \
                    float_round(line.amount, account_precision) or 0.0
                statement.sum_of_udebits_cur += \
                    (not line.cleared_bank_account) and \
                    float_round(line.amountcur, account_precision) or 0.0
                statement.sum_of_udebits_lines += \
                    (not line.cleared_bank_account) and 1 or 0
            statement.cleared_balance = float_round(
                statement.sum_of_debits - statement.sum_of_credits,
                account_precision)
            statement.cleared_balance_cur = float_round(
                statement.sum_of_debits_cur - statement.sum_of_credits_cur,
                account_precision)
            statement.difference = \
                float_round((statement.ending_balance -
                             statement.starting_balance) -
                            statement.cleared_balance, account_precision)
            statement.difference_cur = \
                float_round((statement.ending_balance -
                             statement.starting_balance) -
                            statement.cleared_balance_cur, account_precision)
            statement.uncleared_balance = float_round(
                statement.sum_of_udebits - statement.sum_of_ucredits,
                account_precision)
            statement.uncleared_balance_cur = float_round(
                statement.sum_of_udebits_cur - statement.sum_of_ucredits_cur,
                account_precision)

<<<<<<< HEAD
    # refresh data
=======
    #refresh data
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
    def refresh_record(self):
        retval = True
        refdict = {}
        # get current state of moves in the statement
        for statement in self:
            if statement.state == 'draft':
                for cr_item in statement.credit_move_line_ids:
                    if cr_item.move_line_id and cr_item.cleared_bank_account:
                        refdict[cr_item.move_line_id.id] = \
                            cr_item.cleared_bank_account
                for dr_item in statement.debit_move_line_ids:
                    if dr_item.move_line_id and dr_item.cleared_bank_account:
                        refdict[dr_item.move_line_id.id] = \
                            dr_item.cleared_bank_account
<<<<<<< HEAD

        # for the statement
        for statement in self:
            # process only if the statement is in draft state
            if statement.state == 'draft':
                vals = statement.onchange_account_id()

                # list of credit lines
                outlist = []
                for cr_item in vals['value']['credit_move_line_ids']:
                    # cr_item['cleared_bank_account'] = refdict and refdict.get(
                    #     cr_item['move_line_id'], False) or False
                    # cr_item['research_required'] = False
                    item = [(0, 0, cr_item)]
                    outlist.append(cr_item)
                # list of debit lines
                inlist = []
                for dr_item in vals['value']['debit_move_line_ids']:
                    # dr_item['cleared_bank_account'] = refdict and refdict.get(
                    #     dr_item['move_line_id'], False) or False
                    # dr_item['research_required'] = False
                    item = [(0, 0, dr_item)]
                    inlist.append(dr_item)
                # write it to the record so it is visible on the form
                x=[(0, 0, line_vals) for line_vals in outlist]
                y=[(0, 0, line_vals) for line_vals in inlist]
                print('outlist',outlist)
                print('outlist',vals['value']['credit_move_line_ids'])
                retval = self.write(
                    {'last_ending_date': vals['value']['last_ending_date'],
                     'starting_balance': vals['value']['starting_balance'],
                     'credit_move_line_ids': outlist,
                     'debit_move_line_ids': inlist})
        return retval

    # get starting balance for the account
    def get_starting_balance(self, account_id, ending_date):
        result = (False, 0.0)
        reslist = []
        statement_obj = self.env['bank.acc.rec.statement']
        domain = [('account_id', '=', account_id), ('state', '=', 'done')]
        # get all statements for this account in the past
        for statement in statement_obj.search(domain):
            if statement.ending_date < ending_date:
                reslist.append(
                    (statement.ending_date, statement.ending_balance))
        # get the latest statement value
        if len(reslist):
            reslist = sorted(reslist, key=itemgetter(0))
            result = reslist[len(reslist) - 1]
        return result

    @api.onchange('account_id', 'ending_date', 'suppress_ending_date_filter')
    def onchange_account_id(self):
        cr_line_ids = []
        dr_line_ids = []
        account_move_line_obj = self.env['account.move.line']
        statement_line_obj = self.env['bank.acc.rec.statement.line']
        val = {
            'value': {'credit_move_line_ids': [], 'debit_move_line_ids': []}}
        if self.ending_date and self.account_id:
            for statement in self:
                statement_line_ids = statement_line_obj.search(
                    [('statement_id', '=', statement.id)])
                print(statement_line_ids,'statement_line_ids')
                # call unlink method to reset and
                # remove existing statement lines and
                # mark reset field values in related move lines
                statement.credit_move_line_ids.unlink()
                statement.debit_move_line_ids.unlink()

            # Apply filter on move lines to allow
            # 1. credit and debit side journal items in posted state of
            # the selected GL account
            # 2. Journal items which are not cleared in
            # previous bank statements
            # 3. Date less than or equal to ending date provided the
            # 'Suppress Ending Date Filter' is not check
            domain = [('account_id', '=', self.account_id.id),
                      ('move_id.state', '=', 'posted'),
                      ('cleared_bank_account', '=', False)]
            if not self.suppress_ending_date_filter:
                domain += [('date', '<=', self.ending_date)]
            for line in account_move_line_obj.search(domain):
                amount_currency = (line.amount_currency < 0) and (
                    -1 * line.amount_currency) or line.amount_currency
                res = {
                    'date': line.date,
                    'in_system': True,
                    'check_no':line.Check_no,
                    'ref': line.ref,
                    'currency_id': line.currency_id.id,
                    'amount': line.credit or line.debit,
                    'amountcur': amount_currency,
                    'name': line.name,
                    'statement_id': self.id,
                    'move_line_id': line.id,
                    'type': line.credit and 'cr' or 'dr'}
                if res['type'] == 'cr':
                    cr_line_ids.append(res)
                    # val['value']['credit_move_line_ids'].append(res)
                    # val['value']['credit_move_line_ids'] = [(0,0,res)]
                    print(val['value']['credit_move_line_ids'],'credit')

                if res['type'] == 'dr':
                    dr_line_ids.append(res)
                    # val['value']['debit_move_line_ids'] = [(0,0,res)]
                    print(val['value']['debit_move_line_ids'],'debuit')

            val['value']['debit_move_line_ids'] = [(0, 0, line_vals) for line_vals in dr_line_ids]
            val['value']['credit_move_line_ids'] = [(0, 0, line_vals) for line_vals in cr_line_ids]
            # look for previous statement for the account to
            # pull ending balance as starting balance
            prev_stmt = self.get_starting_balance(self.account_id.id,
                                                  self.ending_date)
            val['value']['last_ending_date'] = prev_stmt[0]
            val['value']['starting_balance'] = prev_stmt[1]
        return val

    def get_default_company_id(self):
        return self.env['res.users'].browse([self.env.uid]).company_id.id

    name = fields.Char('Name', required=True, size=64,
                       states={'done': [('readonly', True)]},
                       help="This is a unique name identifying "
                            "the statement (e.g. Bank X January 2012).")
    account_id = fields.Many2one('account.account', 'Account', required=True,
                                 states={'done': [('readonly', True)]},
                                 domain="[('company_id', '=', company_id)]",
                                 help="The Bank/Gl Account that is being "
                                      "reconciled.")
    ending_date = fields.Date('Ending Date', required=True,
                              states={'done': [('readonly', True)]},
                              default=time.strftime('%Y-%m-%d'),
                              help="The ending date of your bank statement.")
    last_ending_date = fields.Date('Last Stmt Date',
                                   help="The previous statement date "
                                        "of your bank statement.")
    starting_balance = fields.Float('Starting Balance', required=True,
                                    digits=dp.get_precision('Account'),
                                    help="The Starting Balance on your "
                                         "bank statement.",
                                    states={'done': [('readonly', True)]})
    ending_balance = fields.Float('Ending Balance', required=True,
                                  digits=dp.get_precision('Account'),
                                  help="The Ending Balance on your "
                                       "bank statement.",
                                  states={'done': [('readonly', True)]})
    company_id = fields.Many2one('res.company', 'Company', required=True,
                                 readonly=True, default=get_default_company_id,
                                 help="The Company for which the "
                                      "deposit ticket is made to")
    notes = fields.Text('Notes')

    prepared_date = fields.Date('Prepared Date')
    prepared_by_user_id = fields.Many2one('res.users', 'Prepared By')
    
    validated_date = fields.Date('Validated Date')
    validated_by_user_id = fields.Many2one('res.users', 'Validated By')

    reviewed_date = fields.Date('Reviewed Date',
                                states={'done': [('readonly', True)]},
                                copy=False,
                                help="Date in which Deposit "
                                     "Ticket was verified.")
    reviewed_by_user_id = fields.Many2one('res.users', 'Reviewed By',
                                          states={
                                              'done': [('readonly', True)]},
                                          copy=False,
                                          help="Entered automatically by "
                                               "the “last user” who saved it. "
                                               "System generated.")
    approved_date = fields.Date('Approved Date')
    approved_date_by_user_id = fields.Many2one('res.users', 'Approved By')
        
    
    credit_move_line_ids = fields.One2many('bank.acc.rec.statement.line',
                                           'statement_id', 'Credits',
                                           copy=False,
                                           domain=[('type', '=', 'cr')],

                                           states={
                                               'done': [('readonly', True)]})
    debit_move_line_ids = fields.One2many('bank.acc.rec.statement.line',
                                          'statement_id', 'Debits',
                                          copy=False,
                                          domain=[('type','=','dr')],
                                          states={
                                              'done': [('readonly', True)]})
    cleared_balance = fields.Float(compute='_compute_get_balance',
                                   string='Cleared Balance',
                                   digits=dp.get_precision('Account'),
                                   help="Total Sum of the Deposit Amount "
                                        "Cleared – Total Sum of Checks, "
                                        "Withdrawals, Debits, and Service "
                                        "Charges Amount Cleared")
    difference = fields.Float(compute='_compute_get_balance',
                              string='Difference',
                              digits=dp.get_precision('Account'),
                              help="(Ending Balance – Beginning Balance) - "
                                   "Cleared Balance.")
    cleared_balance_cur = fields.Float(compute='_compute_get_balance',
                                       string='Cleared Balance (Cur)',
                                       digits=dp.get_precision('Account'),
                                       help="Total Sum of the Deposit "
                                            "Amount Cleared – Total Sum of "
                                            "Checks, Withdrawals, Debits, and"
                                            " Service Charges Amount Cleared")
    difference_cur = fields.Float(compute='_compute_get_balance',
                                  string='Difference (Cur)',
                                  digits=dp.get_precision('Account'),
                                  help="(Ending Balance – Beginning Balance)"
                                       " - Cleared Balance.")
    uncleared_balance = fields.Float(compute='_compute_get_balance',
                                     string='Uncleared Balance',
                                     digits=dp.get_precision('Account'),
                                     help="Total Sum of the Deposit "
                                          "Amount Uncleared – Total Sum of "
                                          "Checks, Withdrawals, Debits, and"
                                          " Service Charges Amount Uncleared")
    uncleared_balance_cur = fields.Float(compute='_compute_get_balance',
                                         string='Unleared Balance (Cur)',
                                         digits=dp.get_precision('Account'),
                                         help="Total Sum of the Deposit Amount"
                                              " Uncleared – Total Sum of "
                                              "Checks, Withdrawals, Debits, "
                                              "and Service Charges "
                                              "Amount Uncleared")
    sum_of_credits = fields.Float(compute='_compute_get_balance',
                                  string='Checks, Withdrawals, Debits, and'
                                         ' Service Charges Amount',
                                  digits=dp.get_precision('Account'),
                                  type='float',
                                  help="Total SUM of Amts of lines with"
                                       " Cleared = True")
    sum_of_debits = fields.Float(compute='_compute_get_balance',
                                 string='Deposits, Credits, and '
                                        'Interest Amount',
                                 digits=dp.get_precision('Account'),
                                 help="Total SUM of Amts of lines with "
                                      "Cleared = True")
    sum_of_credits_cur = fields.Float(compute='_compute_get_balance',
                                      string='Checks, Withdrawals, Debits, and'
                                             ' Service Charges Amount (Cur)',
                                      digits=dp.get_precision('Account'),
                                      help="Total SUM of Amts of lines "
                                           "with Cleared = True")
    sum_of_debits_cur = fields.Float(compute='_compute_get_balance',
                                     string='Deposits, Credits, and '
                                            'Interest Amount (Cur)',
                                     digits=dp.get_precision('Account'),
                                     help="Total SUM of Amts of lines "
                                          "with Cleared = True")
    sum_of_credits_lines = fields.Integer(compute='_compute_get_balance',
                                          string='''Checks, Withdrawals,
                                          Debits, and Service Charges # of
                                          Items''',
                                          help="Total of number of lines with "
                                          "Cleared = True")
    sum_of_debits_lines = fields.Integer(compute='_compute_get_balance',
                                         string='''Deposits, Credits, and
                                         Interest # of Items''',
                                         help="Total of number of lines with"
                                         " Cleared = True")
    sum_of_ucredits = fields.Float(compute='_compute_get_balance',
                                   string='Uncleared - Checks, Withdrawals, '
                                          'Debits, and Service Charges Amount',
                                   digits=dp.get_precision('Account'),
                                   help="Total SUM of Amts of lines with "
                                        "Cleared = False")
    sum_of_udebits = fields.Float(compute='_compute_get_balance',
                                  string='Uncleared - Deposits, Credits, '
                                         'and Interest Amount',
                                  digits=dp.get_precision('Account'),
                                  help="Total SUM of Amts of lines with "
                                       "Cleared = False")
    sum_of_ucredits_cur = fields.Float(compute='_compute_get_balance',
                                       string='Uncleared - Checks, '
                                              'Withdrawals, Debits, and '
                                              'Service Charges Amount (Cur)',
                                       digits=dp.get_precision('Account'),
                                       help="Total SUM of Amts of lines "
                                            "with Cleared = False")
    sum_of_udebits_cur = fields.Float(compute='_compute_get_balance',
                                      string='Uncleared - Deposits, Credits, '
                                             'and Interest Amount (Cur)',
                                      digits=dp.get_precision('Account'),
                                      help="Total SUM of Amts of lines with"
                                           " Cleared = False")
    sum_of_ucredits_lines = fields.Integer(compute='_compute_get_balance',
                                           string='Uncleared - Checks, '
                                           'Withdrawals, Debits, and '
                                           'Service Charges # of Items',
                                           help="Total of number of lines with"
                                           " Cleared = False")
    sum_of_udebits_lines = fields.Integer(compute='_compute_get_balance',
                                          string='''Uncleared - Deposits,
                                          Credits, and Interest # of Items''',
                                          help="Total of number of lines "
                                          "with Cleared = False")
    suppress_ending_date_filter = fields.Boolean('Remove Ending Date Filter',
                                                 help="If this is checked then"
                                                      " the Statement End Date"
                                                      " filter on the "
                                                      "transactions below will"
                                                      " not occur. All "
                                                      "transactions would "
                                                      "come over.")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('finance_officer','Finance Officer'),
        ('validate','Financial Director'),
        ('to_be_reviewed', 'Internal Auditor'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], 'State', index=True, readonly=True, default='draft')

    account_ending_balance = fields.Float(string='Account Ending Balance', compute='get_account_balance')

    # state = fields.Selection([
    #     ('draft', 'Draft'),
    #     ('to_be_reviewed', 'Wait Account SH Approval'),
    #     ('done', 'Done'),
    #     ('cancel', 'Cancelled')
    # ], 'State', index=True, readonly=True, default='draft')
    # user_id = fields.Many2one('res.users',default=lambda self: self.env.uid)
    # job_id = fields.Many2one('hr.job', string='Job Position',related='user_id.employee_id.job_id')

   
    reason = fields.Char('reason', track_visibility='onchange')
    journal_id = fields.Many2one('account.journal', string='Journal')
    account_id = fields.Many2one('account.account', 'Account', required=True, readonly=False,
                                 compute='get_bank_account_id',
                                 states={'done': [('readonly', True)]},
                                 domain="[('company_id', '=', company_id)]",
                                 help="The Bank/Gl Account that is being "
                                      "reconciled.", store=True)

=======
        self.get_lines()

        

   

    
   
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
    @api.depends('journal_id')
    def get_bank_account_id(self):
        for rec in self:
            rec.account_id = rec.journal_id.default_account_id.id

    @api.depends('ending_date', 'account_id')
    def get_account_balance(self):
<<<<<<< HEAD

=======
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
        for record in self:
            move_ids = record.env['account.move.line'].search([
                ('date', '<=', record.ending_date),
                ('account_id', '=', record.account_id.id),
                ('move_id.state', '=', 'posted')])
<<<<<<< HEAD

            record.account_ending_balance = sum(move.balance for move in move_ids)

    def create_entry(self):
        new_entry = self.env['account.move'].create({'journal_id': self.journal_id.id, 'ref': self.name,
                                                     'reconsile_id': self.id})
=======
            record.account_ending_balance = sum(move.balance for move in move_ids)

    def create_entry(self):
        new_entry = self.env['account.move'].create(
                    {'journal_id': self.journal_id.id,'not_in_system': True,
                    'ref': self.name,'reconsile_id': self.id})
        
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'target': 'new',
            'res_id': new_entry.id,
            'view_type': 'form',
<<<<<<< HEAD

=======
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
        }

    _sql_constraints = [
        ('name_company_uniq', 'unique (name, company_id, account_id)',
         'The name of the statement must be unique per '
         'company and G/L account!')
    ]

    def copy(self, default=None):
        for rec in self:
            if default is None:
                default = {}
            if 'name' not in default:
                default['name'] = _("%s (copy)") % rec.name
        return super(BankAccRecStatement, self).copy(default=default)


class BankAccRecStatementLine(models.Model):
    _name = "bank.acc.rec.statement.line"
    _description = "Statement Line"

<<<<<<< HEAD
    name = fields.Char('Name', size=64,
                       help="Derived from the related Journal Item.",
                      )
=======
    name = fields.Char('Name', size=64, help="Derived from the related Journal Item.")
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
    ref = fields.Char('Reference', size=64,
                      help="Derived from related Journal Item.")
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 help="Derived from related Journal Item.")
    amount = fields.Float('Amount',
                          help="Derived from the 'debit' amount from "
                               "related Journal Item.")
    amountcur = fields.Float('Amount in Currency',

                             help="Derived from the 'amount currency' "
                                  "amount from related Journal Item.")
    date = fields.Date('Date',
                       help="Derived from related Journal Item.")
    statement_id = fields.Many2one('bank.acc.rec.statement', 'Statement', ondelete='cascade')
    move_line_id = fields.Many2one('account.move.line', 'Journal Item',
                                   help="Related Journal Item.")
    cleared_bank_account = fields.Boolean('Cleared? ',
                                          help='Check if the transaction has '
                                               'cleared from the bank')
    research_required = fields.Boolean('Research Required? ',
                                       help='Check if the transaction should '
                                            'be researched by '
                                            'Accounting personal')
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  help="The optional other currency if "
                                       "it is a multi-currency entry.")
    type = fields.Selection([('dr', 'Debit'), ('cr', 'Credit')], 'Cr/Dr')
<<<<<<< HEAD
    in_system = fields.Boolean('In system')
    check_no = fields.Char('Check NO')

    @api.model
    def create(self, vals):
        res = super(BankAccRecStatementLine, self).create(vals)
        account_move_line_obj = self.env['account.move.line']
        # Prevent manually adding new statement line.
        # This would allow only onchange method to pre-populate statement lines
        # based on the filter rules.
        if  not res.move_line_id:
            print('hi')
            raise UserError(_(
                "You cannot add any new bank statement line manually "
                "as of this revision!"))
        account_move_line_obj.browse(res.move_line_id.id).write(
            {'draft_assigned_to_statement': True})
        return res
=======
    not_in_system = fields.Boolean('Not In System')
    check_no = fields.Char('Check NO')

    # @api.model
    # def create(self, vals):
    #     res = super(BankAccRecStatementLine, self).create(vals)
    #     account_move_line_obj = self.env['account.move.line']
    #     # Prevent manually adding new statement line.
    #     # This would allow only onchange method to pre-populate statement lines
    #     # based on the filter rules.
    #     # if  not res.move_line_id:
    #     #     print('hi')
    #     #     raise UserError(_(
    #     #         "You cannot add any new bank statement line manually "
    #     #         "as of this revision!"))
    #     account_move_line_obj.browse(res.move_line_id.id).write(
    #         {'draft_assigned_to_statement': True})
    #     return res
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44

    def unlink(self):
        account_move_line_obj = self.env['account.move.line']
        move_line_ids = [x.move_line_id.id for x in self if x.move_line_id]
        # map(lambda x: x.move_line_id.id if x.move_line_id,
        # self.browse(cr, uid, ids, context=context))
        # Reset field values in move lines to be added later
        account_move_line_obj.browse(move_line_ids).write(
            {'draft_assigned_to_statement': False,
             'cleared_bank_account': False,
             'bank_acc_rec_statement_id': False})
        return super(BankAccRecStatementLine, self).unlink()
<<<<<<< HEAD
=======

    @api.onchange('move_line_id')
    def _onchange_move_line_id(self):
        if self.move_line_id.account_id.id == self.statement_id.account_id.id:
            
            if self.move_line_id.debit > 0:
                self.type = 'dr'
                self.name = self.move_line_id.name
                self.amount = self.move_line_id.debit
                self.amountcur = self.move_line_id.amount_currency
                self.currency_id = self.move_line_id.currency_id.id
                self.statement_id = self.statement_id.id
                self.date = self.move_line_id.date
                self.partner_id = self.move_line_id.partner_id.id
            
            if self.move_line_id.credit > 0:
                self.type = 'cr'
                self.name = self.move_line_id.name
                self.amount = self.move_line_id.credit
                self.amountcur = self.move_line_id.amount_currency
                self.currency_id = self.move_line_id.currency_id.id
                self.statement_id = self.statement_id.id
                self.date = self.move_line_id.date
                self.partner_id = self.move_line_id.partner_id.id
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44

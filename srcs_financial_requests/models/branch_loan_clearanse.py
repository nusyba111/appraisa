from odoo import fields, api, models,_ 

class BranchClearanse(models.Model):
    _name = "branch.loan.clearanse"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    rec_name = 'name'
    
    name = fields.Char('Clearance No.', help='Auto-generated Clearance No. for custody clearances')
    branch_laons_id = fields.Many2one('cash.request', 'Branch Loan', domain="[('is_branch_loans','=',True),('state', '=', 'payment'),('user_id','=',requester),('is_cleared','=',False)]")
    cc_date = fields.Date('Date', default=fields.Date.today(), )
    requester = fields.Char('Requester', required=True, default=lambda self: self.env.user.name)
    # is_partially_clearance = fields.Boolean(string="Partially Clearance")
    # is_branch_loans = fields.Boolean('Is Branch Loans')
    state = fields.Selection([
        ('draft','Draft'),
        ('branch_finance', 'Branch Finance Director'),
        ('branch_director','Branch Director'),
        ('secratry_general','Secretary General '),
        ('finance_department','Finance Department'),
        ('program_department','Program Department'),
        ('internal_auditor','Internal Auditor'),
        ('secratry_general_two','Secretary General '),
        ('payment','Payment'),
    ],default="draft", string='Status')
    un_cleared_amount = fields.Float('Uncleared Amount', readonly=True, store=True)
    clearance_amount = fields.Float('Clearance Total Amount')
    clearance_currency = fields.Many2one('res.currency', 'Currency')
    difference_amount = fields.Float('Difference Amount', readonly=True, store=True)
    # clearance_amount_words = fields.Char(string='Amount in Words', readonly=True, default=False, copy=False,translate=True)
    reason = fields.Char('Reason')
    clearance_amount_new = fields.Float(compute='approval_reference', string='Requested Amount', store=True, )
    clearance_journal_id = fields.Many2one('account.journal', 'Clearance Journal', help='Clearance Journal')
    journal_id = fields.Many2one('account.journal', 'Bank/Cash Journal', help='Payment journal.', domain=[('type', 'in', ['bank', 'cash'])])
    # cr_account = fields.Many2one('account.account', string="Credit Account")
    internal_transfer_id = fields.Many2one('account.payment', string='Clearance Internal Transfer',readonly=True)
    budget_line_id = fields.Many2one('crossovered.budget.lines', string='Budget Line', related='branch_laons_id.budget_line_id', required=True)
    
   
    @api.onchange('difference_amount','branch_laons_id')
    def onchange_un_cleared_amount(self):
        if self.difference_amount == 0:
            if not self.branch_laons_id.is_partially_clearance:
                self.un_cleared_amount = self.clearance_amount_new
            if self.branch_laons_id.is_partially_clearance:
                self.un_cleared_amount = self.branch_laons_id.un_cleared_amount
        else:
            self.un_cleared_amount = self.difference_amount 

    @api.depends('branch_laons_id')
    def approval_reference(self):
        for rec in self:
            rec.clearance_amount_new = 0.0
            branch_loan_obj = rec.branch_laons_id
            if branch_loan_obj:
                rec.clearance_amount_new = rec.branch_laons_id.requested_amount


    @api.onchange('branch_laons_id')
    def _onchange_branch_laons_id(self):
        for rec in self:
            if rec.branch_laons_id:
                rec.journal_id = rec.branch_laons_id.source_bank.id
                rec.clearance_journal_id = rec.branch_laons_id.dest_bank.id
                rec.clearance_currency = rec.branch_laons_id.budget_currency.id
                if not rec.branch_laons_id.is_partially_clearance:
                    rec.difference_amount = rec.branch_laons_id.requested_amount
                
                
    # # Return clearance amount in words
    # @api.depends('clearance_amount', 'clearance_currency')
    # def _compute_text(self):
    #     from . import money_to_text_en
    #     self.clearance_amount_words = ''
    #     self.clearance_amount_words = money_to_text_en.amount_to_text(self.clearance_amount, self.clearance_currency)

    @api.model
    def create(self, vals):
        res = super(BranchClearanse, self).create(vals)
        # get branch loan clearance sequence no.
        next_seq = self.env['ir.sequence'].get('branch.loan.clearance')
        res.update({'name': next_seq})
        return res

    def confrim_finance(self):
        self.state = "branch_finance"

    def confirm_branch_dir(self):
        self.state = "branch_director"
    
    def approve_secratry(self):
        self.state = "secratry_general"

    def confirm_finance_department(self):
        self.state = "finance_department"

    def approve_program_department(self):
        self.state = "program_department"
        
    def cash_request_internal_auditor(self):
        self.state = "internal_auditor"

    def branch_loan_internal_auditor(self):
        self.state = "internal_auditor"
    
    def second_approve_secretary(self):
        self.state = "secratry_general_two"

    def validate_clearance(self):
        for rec in self:
            if not rec.journal_id:
                raise UserError(_('Source Bank should be entered .'))
            if not rec.clearance_journal_id:
                raise UserError(_('Clearance Bank should be entered .'))
            else: 
                internal_transfer = self.env['account.payment'].create({
                        'is_internal_transfer':True,
                        'type_internal_transfer':'branch',
                        'payment_type':'outbound',
                        'project_id':rec.branch_laons_id.budget_id.id,
                        'journal_id':rec.clearance_journal_id.id,
                        'destination_journal_id':rec.journal_id.id,
                        'amount':rec.clearance_amount,
                        'date':rec.cc_date,
                        'currency_id':rec.clearance_currency.id,
                        'ref':rec.name,
                        'branch_id':rec.clearance_journal_id.branch_id.id,
                        'transfer_to':rec.journal_id.branch_id.id,
                        
                    })

            if internal_transfer:
                rec.difference_amount =  rec.un_cleared_amount - rec.clearance_amount 
               
                if rec.difference_amount == 0:
                    rec.branch_laons_id.is_cleared = True
                    rec.branch_laons_id.un_cleared_amount = 0
                else:
                    rec.branch_laons_id.is_partially_clearance = True
                    rec.branch_laons_id.un_cleared_amount = rec.un_cleared_amount

                internal_transfer.action_post()
                rec.internal_transfer_id = internal_transfer.id

                rec.state = "payment"


    
            

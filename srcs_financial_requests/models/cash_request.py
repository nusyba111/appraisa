from odoo import fields, api, models, _
from datetime import date
from odoo.exceptions import UserError, ValidationError

class SrcsCashRequest(models.Model):
    _name = "cash.request"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', readonly=True, default=lambda self: 'New')
    sequence = fields.Char('Sequence', readonly=True, default=lambda self: 'New')
    date = fields.Date('Request Date',default=fields.Date.today())
    user_id = fields.Many2one('res.users', string='Requestor', default=lambda self: self.env.user)
    project_id = fields.Many2one('account.analytic.account', string='Project', domain="[('type','=','project')]")
<<<<<<< HEAD
    donor_id = fields.Many2one('res.partner', string='Donor',readonly=True,store=True)
    source_bank = fields.Many2one('account.journal', string='Source Bank', required=True)
    dest_bank = fields.Many2one('account.journal', string='Destination Bank',required=True)
    budget_line_id = fields.Many2one('crossovered.budget.lines', string='Budget Line', required=True)
    budget_currency = fields.Many2one(related='budget_line_id.currency_budget_line')
=======
   
    donor_id = fields.Many2one('res.partner', string='Donor',readonly=True,store=True)
    source_bank = fields.Many2one('account.journal', string='Source Bank')
    dest_bank = fields.Many2one('account.journal', string='Destination Bank',required=True)
    budget_line_id = fields.Many2one('crossovered.budget.lines', string='Budget Line')
    budget_currency = fields.Many2one('res.currency')
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
    residual_amount = fields.Monetary('Residual amount ', currency_field='budget_currency',readonly=True,store=True)
    company_currency_id = fields.Many2one('res.currency', string='Company Currency', default=lambda self: self.env.company.currency_id.id)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id.id)
    requested_amount = fields.Monetary('Total Amount', compute="_compute_requested_amount", currency_field='budget_currency')
    requested_amount_sdg = fields.Monetary(compute='_compute_requested_amount_sdg', string='Requested Amount SDG', currency_field='company_currency_id', store=True )
    description = fields.Html('Description',compute='_compute_description')
    amount_in_words = fields.Char('Amount In Words')
    amount_in_words_sdg = fields.Char('Amount In Words SDG')
    user_lang_id = fields.Selection(related='user_id.lang', string='Lang')
    is_branch_loans = fields.Boolean('Is Branch Loans')
    internal_transfer_id = fields.Many2one('account.payment', string='Internal Transfer',readonly=True)
    is_cleared = fields.Boolean(string="Cleared", readonly=True, copy=False)
    is_partially_clearance = fields.Boolean(string="Partially Clearance", readonly=True)
    budget_id = fields.Many2one('crossovered.budget',domain="[('budget_type','=','core')]")
    tot_cleared_amount = fields.Float(string="Cleared Amount", required=False, readonly=True, copy=False)
    un_cleared_amount = fields.Float(string="Uncleared Amount", required=False, copy=False)
    cash_request_line_ids = fields.One2many('cash.reuqest.line', 'cash_request_id', string='Cash Request Line')
    state = fields.Selection([
        ('draft','Draft'),
        ('branch_finance', 'Branch Finance Director'),
        ('branch_director','Branch Director'),
        ('secratry_general','Finance Director'),
        ('finance_department','Finance Officer'),
        ('program_department','Program Department'),
        ('internal_auditor','Internal Auditor'),
        ('secratry_general_two','Secretary General '),
        ('payment','Payment'),
    ],default="draft", string='Status')

    def name_get(self):
        res = []
        for record in self:
            if record.is_branch_loans:
                name = '%s' % (record.sequence)
            else:
                name = '%s' % (record.name)
            res.append((record.id,name))
        return res
   
    @api.onchange('project_id')
    def onchange_budget_currency(self):
        for rec in self:
            if rec.project_id:
                budget_records = self.env['crossovered.budget'].search([('project_id','=',rec.project_id.id)])
                if budget_records:
                    rec.budget_currency = budget_records.currency_id.id
                    rec.donor_id = budget_records.donor_id.id

    @api.depends('cash_request_line_ids')
    def _compute_requested_amount(self):
        total = 0
        self.requested_amount = 0
        for line in self.cash_request_line_ids:
            total += line.amount
            print('__________________________total',total)
        self.requested_amount = total 
    
    @api.onchange('budget_id','project_id')
    def _onchange_budget_line_id(self):
        if self.budget_id:
            budget_line_ids = self.env['crossovered.budget.lines'].search([('crossovered_budget_id','=',self.budget_id.id),('crossovered_budget_id.budget_type','=','core')]).ids
            return{'domain':{'budget_line_id':[('id','in',budget_line_ids)]}}
        if self.project_id:
            project_ids = self.env['crossovered.budget.lines'].search([('crossovered_budget_id.budget_type','=','project'),('analytic_account_id','=',self.project_id.id)]).ids
            return{'domain':{'budget_line_id':[('id','in',project_ids)]}}
            
    @api.depends('project_id','donor_id','budget_line_id')
    def _compute_description(self):
        for desc in self:
            if desc.project_id and desc.budget_line_id:
                month = desc.budget_line_id.date_from.strftime("%B")
                day = desc.budget_line_id.date_from.day
                year = desc.budget_line_id.date_from.year
<<<<<<< HEAD
                print('_________________month',month,day)
=======
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
                desc.description = "Khartoum-Sudan "+ " \n \n" + "With refrence to the project Agreement that was signed between the Sudanese Red Crescent Society and the" + " " + str(desc.donor_id.name) + " " + "the project" + " " + str(desc.project_id.name) + " " + "as of " + month + "," + str(day) + "," + str(year)+ " " + "we here by request the following payment for the quartor one in the amount of:"
            else:
                desc.description = " "
                
    @api.depends('requested_amount')
    def _compute_requested_amount_sdg(self):
        for rec in self:
            if rec.requested_amount:
                if self.budget_currency == self.company_currency_id:
                    rec.requested_amount_sdg = rec.requested_amount
                else:
                    rec.requested_amount_sdg = rec.requested_amount / rec.budget_currency.rate
                rec.un_cleared_amount = rec.requested_amount
            else:
                rec.requested_amount_sdg = 0

    @api.onchange('budget_line_id')
    def onchange_budget_line(self):
        self.residual_amount = self.budget_line_id.balance_budget_currency
        

    @api.model
    def create(self, vals):
        if vals.get('is_branch_loans') == False:
            if vals.get('name', 'NEW') == 'NEW':
                vals['name'] = self.env['ir.sequence'].next_by_code('cash_request') or 'NEW'
        if vals.get('is_branch_loans') == True:
            if vals.get('sequence', 'NEW') == 'NEW':
                vals['sequence'] = self.env['ir.sequence'].next_by_code('branch_loan') or 'NEW'
        result = super(SrcsCashRequest, self).create(vals)
        return result

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

    def submit_payment(self):
        if self.is_branch_loans:
            refrence = self.sequence
        else:
            refrence = self.name
        if not self.source_bank:
            raise UserError(_('Source Bank should be entered .'))
<<<<<<< HEAD
        else:    
            internal_transfer = self.env['account.payment'].create({
                    'is_internal_transfer':True,
                    'type_internal_transfer':'branch',
                    'payment_type':'outbound',
                    'project_id':self.project_id.id,
                    'journal_id':self.source_bank.id,
                    'destination_journal_id':self.dest_bank.id,
                    'amount':self.requested_amount,
                    'date':self.date,
                    'currency_id':self.currency_id.id,
                    'ref':self.name,
                    'branch_id':self.source_bank.branch_id.id,
                    'transfer_to':self.dest_bank.branch_id.id,
                })
            print('_______________________',internal_transfer)
=======
        
        else: 
            if self.project_id:   
                internal_transfer = self.env['account.payment'].create({
                        'is_internal_transfer':True,
                        'type_internal_transfer':'branch',
                        'payment_type':'outbound',
                        'project_id':self.project_id.id,
                        'journal_id':self.source_bank.id,
                        'destination_journal_id':self.dest_bank.id,
                        'amount':self.requested_amount,
                        'date':self.date,
                        'currency_id':self.budget_currency.id,
                        'ref':refrence,
                        'branch_id':self.source_bank.branch_id.id,
                        'transfer_to':self.dest_bank.branch_id.id,
                        
                    })
            else:
                internal_transfer = self.env['account.payment'].create({
                        'is_internal_transfer':True,
                        'type_internal_transfer':'branch',
                        'payment_type':'outbound',
                        'project_id':self.budget_id.project_id.id,
                        'journal_id':self.source_bank.id,
                        'destination_journal_id':self.dest_bank.id,
                        'amount':self.requested_amount,
                        'date':self.date,
                        'currency_id':self.budget_currency.id,
                        'ref':refrence,
                        'branch_id':self.source_bank.branch_id.id,
                        'transfer_to':self.dest_bank.branch_id.id,
                        
                    })

>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
            if internal_transfer:
                internal_transfer.action_post()
                self.internal_transfer_id = internal_transfer.id

                self.state = "payment"


    def reset_to_draft(self):
        self.state = "draft"

    @api.onchange('requested_amount', 'currency_id')
    def _compute_amount_in_words(self):
        from . import money_to_text_en
        from . import money_to_text_ar
        for r in self:
            if r.requested_amount:
                if r.user_lang_id == 'en_US':
                    r.amount_in_words = money_to_text_en.amount_to_text(r.requested_amount, r.budget_currency.name)
                    r.amount_in_words_sdg =  money_to_text_en.amount_to_text(r.requested_amount_sdg, r.company_currency_id.name)
                if r.user_lang_id == 'ar_001':
                    r.amount_in_words = money_to_text_ar.amount_to_text_arabic(r.requested_amount, r.budget_currency.name)
                    r.amount_in_words_sdg =  money_to_text_ar.amount_to_text_arabic(r.requested_amount_sdg, r.company_currency_id.name)

<<<<<<< HEAD
    @api.constrains('requested_amount')
    def _check_requested_amount(self):
        for rec in self:
            if rec.currency_id.id == rec.budget_currency.id:
                print('hreeeeeeeeeeeeeeeeeeeeeeeeeeee')
                print("\n\n\n\n\n\n\n\n ddddddddddddresidual amount",rec.residual_amount,rec.requested_amount)
                if rec.requested_amount > rec.residual_amount:
                    print('________________________________requested_amount',rec.requested_amount)
                    raise ValidationError(_('Requested Amount should be less than or equal to Bugdet Residual Amount here'))  
            if rec.currency_id.id != rec.budget_currency.id:
                print("\n\n\n\n\n\n\n\n")
                print("rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
                print("\n\n\n\n\n\n\n\n residual amount",rec.residual_amount,rec.requested_amount)
                request_amount = 0
                budget_amount_company_currency = 0
                request_amount = rec.requested_amount / rec.currency_id.rate 
                budget_amount_company_currency = rec.residual_amount / rec.budget_currency.rate
                print('_____________________xxxxx',budget_amount_company_currency,rec.residual_amount,rec.budget_currency.rate)
                if request_amount > budget_amount_company_currency:
                    print('________________________________total_currency',budget_amount_company_currency)
                    raise ValidationError(_('Requested Amount should be less than or equal to Bugdet Residual Amount'))
=======
    # @api.constrains('requested_amount')
    # def _check_requested_amount(self):
    #     for rec in self:
    #         # if rec.company_currency_id.id == rec.budget_currency.id:
    #         if rec.requested_amount > rec.residual_amount:
    #             raise ValidationError(_('Requested Amount should be less than or equal to Bugdet Residual Amount'))  
    #         # if rec.company_currency_id.id != rec.budget_currency.id:
    #         #     request_amount = 0
    #         #     budget_amount_company_currency = 0
    #         #     request_amount = rec.requested_amount / rec.budget_currency.rate 
    #         #     budget_amount_company_currency = rec.residual_amount / rec.budget_currency.rate
    #         #     if request_amount > budget_amount_company_currency:
    #         #         raise ValidationError(_('Requested Amount should be less than or equal to Bugdet Residual Amount'))

class SrcsCashRequestLine(models.Model):
    _name = "cash.reuqest.line"

    cash_request_id = fields.Many2one('cash.request', string='Cash Request')
    project_id = fields.Many2one(related='cash_request_id.project_id')
    budget_line = fields.Many2one('crossovered.budget.lines', string='Budget Line')
    cash_request_line_currency = fields.Many2one('res.currency', related='budget_line.currency_budget_line')
    budget_line_limit = fields.Monetary('Budget Line Balance',currency_field="cash_request_line_currency")
    amount = fields.Monetary('Requested Amount',currency_field="cash_request_line_currency")  

    @api.onchange('budget_line')
    def _onchange_budget_line(self):
        for rec in self:
            if rec.project_id:
                rec.budget_line_limit = rec.budget_line.balance_budget_currency
                budget_line_per_project = self.env['crossovered.budget.lines'].search([('crossovered_budget_id.project_id','=',rec.project_id.id)]).ids
                if budget_line_per_project:
                    return{'domain':{'budget_line':[('id','in',budget_line_per_project)]}}
               

    
    @api.constrains('amount','budget_line')
    def _check_request_amount(self):
        for line in self:
            if line.amount > line.budget_line_limit:
                print('________________________________total',line.amount)
                raise ValidationError(_('Requested Amount should be less than or equal to Bugdet Line Balance'))  


   
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44

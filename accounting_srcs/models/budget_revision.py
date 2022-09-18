from odoo import api, models, fields, _ 
from odoo.exceptions import ValidationError


class SrcsBudgetRevison(models.Model):
    _name = "budget.revision"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    rec_name = "name"

    name = fields.Char(string='Sequence', readonly=True, copy=False, index=True, default=lambda self: 'New Revision')
    requested_date = fields.Date('Requested Date',default= fields.Date.today())
    budget_id = fields.Many2one('crossovered.budget', string='Budget',domain="[('state','=','validate')]")
    currency_id = fields.Many2one('res.currency','Currency',related='budget_id.currency_id',readonly=True)
    budget_line_ids = fields.One2many('budget.revision.line', 'budget_revision', string='Budget Lines')
    transfer_amount_line_ids = fields.One2many('budget.transfer.amount', 'budget_revision_amount', string='Budget TransferLines')
    modify_budget_line_total_ids = fields.One2many('modify.budget.line.total', 'budget_revision_amount', string='Modify Budget Lines Total')
    budget_currency = fields.Many2one(related='budget_id.currency_id')
    budget_change = fields.Selection([
        ('basic_info', 'Basic Information'),('transfer_amount','Transfer Amount'),('add_budget_line','Add Budget Lines'),('modify_line','Modify Budget Total'),
    ], default="basic_info", string='Budget Change')
    user_id = fields.Many2one('res.users', 'Responsible')
    date_from = fields.Date('Start Date')
    date_to = fields.Date('End Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Finance Officer'),
        ('finance_manager','Finance Manager '),
        ('cancel', 'Cancelled'),
        ('validate', 'Validated'),
        ], 'Status', default='draft',readonly=True)

    @api.onchange('budget_id')
    def _onchange_budget_id(self):
        self.date_from = self.budget_id.date_from
        self.date_to = self.budget_id.date_to
        self.user_id = self.budget_id.user_id.id
        budget_lines = self.env['crossovered.budget.lines'].search([('crossovered_budget_id','=',self.budget_id.id)]).ids
        print('_____________________\n\n\n\n\n\n onchange',budget_lines)
        if budget_lines:
            return{'domain':{'budget_line_ids':[('id','in',budget_lines)]}}

    def change_budget_data(self):
        budget = self.env['crossovered.budget'].search([('id','=',self.budget_id.id)])
        for rec in self:
            # if rec.state == 'confirm':
            if rec.budget_change == 'basic_info':
                budget.update({'date_from':rec.date_from, 'date_to':rec.date_to, 'user_id':rec.user_id.id})
                print('_______________________basic_info',budget)
            if rec.budget_change == 'transfer_amount':
                for line in rec.transfer_amount_line_ids:
                    if line.transfered_from_limit > 0:
                        line.from_limit = line.transfered_from_limit - line.requeted_amount
                        line.to_limit = line.transfered_to_limit + line.requeted_amount
                        line.transfer_from.total_budget = line.from_limit
                        line.transfer_to.total_budget = line.to_limit
                        print('_______________________transfer_amount')
                    else:
                        raise ValidationError(_('Budget Balance is not enough'))
            if rec.budget_change == 'add_budget_line':
                for line in rec.budget_line_ids:
                    self.env['crossovered.budget.lines'].create({
                    'date_from': rec.budget_id.date_from,
                    'date_to': rec.budget_id.date_to,
                    'general_budget_id': line.general_budget_id.id,
                    'analytic_activity_id': line.analytic_activity_id.id,
                    'description': line.description,
                    'location_id': line.location_id.id,
                    'unit_of_measure': line.unit_of_measure,
                    'quantity': line.quantity,
                    'frequency': line.frequency,
                    'unit_cost': line.unit_cost,
                    'currency_budget_line': line.currency_budget_line.id,
                    'total_budget': line.total_budget,
                    'planned_amount': line.planned_amount,
                    'crossovered_budget_id':self.budget_id.id,
                    })
                    print('_______________________add_budget_line')
            if rec.budget_change == 'modify_line':
                for record in rec.modify_budget_line_total_ids:
                    if record.requeted_amount:
                        record.budget_line.total_budget = record.requeted_amount
                        print('___________________________________modify',record.budget_line.total_budget)
            self.state = 'validate'
                          


    @api.model
    def create(self, vals):
        if vals.get('name', 'NEW') == 'NEW':
            vals['name'] = self.env['ir.sequence'].next_by_code('budget.revison') or 'NEW'
        result = super(SrcsBudgetRevison, self).create(vals)
        return result


    def confirm_officer(self):
        self.state = 'confirm'

    def confirm_manager(self):
        self.state = 'finance_manager'

    # def validate(self):
    #     self.change_budget_data()
    #     self.state = 'validate'

    def cancel(self):
        self.state = 'cancel'

    
class SrcsModifyBudgetLineTotal(models.Model):
    _name = "modify.budget.line.total"
    
    budget_revision_currency = fields.Many2one('res.currency', related='budget_revision_amount.currency_id')
    budget_revision_amount = fields.Many2one('budget.revision', string='Budget Revision')
    budget_id = fields.Many2one(related='budget_revision_amount.budget_id')
    budget_line = fields.Many2one('crossovered.budget.lines', string='Budget Line',domain="[('crossovered_budget_id','=',budget_id)]")
    budget_line_limit = fields.Monetary('Budget Line Balance',currency_field="budget_revision_currency")
    requeted_amount = fields.Monetary('Modified Total Amount',currency_field="budget_revision_currency")  

    @api.onchange('budget_line')
    def _onchange_budget_line(self):
        for rec in self:
            if rec.budget_revision_amount.budget_id:
                rec.budget_line_limit = rec.budget_line.balance_budget_currency


class SrcsBudgetRevisontransfer(models.Model):
    _name = "budget.transfer.amount"

    budget_revision_currency = fields.Many2one('res.currency', related='budget_revision_amount.currency_id')
    budget_revision_amount = fields.Many2one('budget.revision', string='Budget Revision')
    budget_id = fields.Many2one(related='budget_revision_amount.budget_id')
    transfer_from = fields.Many2one('crossovered.budget.lines', string='Transfer From Line',domain="[('crossovered_budget_id','=',budget_id)]")
    transfered_from_limit = fields.Monetary('Amount Before',currency_field="budget_revision_currency")
    from_limit = fields.Monetary('Amount After',default=0 ,readonly=True,currency_field="budget_revision_currency")
    transfer_to = fields.Many2one('crossovered.budget.lines', string='Transfer To Line',domain="[('crossovered_budget_id','=',budget_id)]")
    transfered_to_limit = fields.Monetary('Amount Before',currency_field="budget_revision_currency")
    to_limit = fields.Monetary('Amount After',default=0 ,readonly=True,currency_field="budget_revision_currency")
    requeted_amount = fields.Monetary('Requested Amount',currency_field="budget_revision_currency")  

    @api.onchange('transfer_from','transfer_to')
    def _onchange_transfer_lines(self):
        for rec in self:
            if rec.budget_revision_amount.budget_id:
                rec.transfered_from_limit = rec.transfer_from.balance_budget_currency
                rec.transfered_to_limit = rec.transfer_to.balance_budget_currency
    
    @api.constrains('requeted_amount','transfer_from')
    def _check_request_amount(self):
        for line in self:
            if line.requeted_amount > line.transfered_from_limit:
                print('________________________________total',line.requeted_amount)
                raise ValidationError(_('Requested Amount should be less than or equal to Bugdet Line Balance'))  
           

class SrcsBudgetRevisonLine(models.Model):
    _name = "budget.revision.line"

    budget_revision = fields.Many2one('budget.revision', string='Budget Revision')
    budget_id = fields.Many2one('crossovered.budget', string='Budget')
    budget_revision_currency = fields.Many2one('res.currency', related='budget_revision.currency_id')
    currency_budget_line = fields.Many2one('res.currency', compute="compute_currency", string="Bugdet Currency",store=True)
    # analytic_account_id = fields.Many2one('account.analytic.account',store=True)
    analytic_activity_id = fields.Many2one('account.analytic.account', 'Output/Activity')
    location_id = fields.Many2one('account.analytic.account', string='Location', domain="[('type','=','location')]")
    description = fields.Char(related='analytic_activity_id.description')
    unit_of_measure = fields.Many2one('uom.uom', string='UOM')
    quantity = fields.Float('Quantity')
    frequency = fields.Float('Frequency')
    unit_cost = fields.Float('Unit Cost')
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account',compute="_compute_analytic_account_id")
    general_budget_id = fields.Many2one('account.budget.post', 'Budgetary Position')
    date_from = fields.Date('Start Date', required=True)
    date_to = fields.Date('End Date', required=True)
    total_budget = fields.Monetary(compute='_compute_total_budget', string='Total budget (Budget Currency)',currency_field='currency_budget_line', readonly=False,store=True)
    planned_amount = fields.Monetary(string='Total budget ',currency_field='budget_revision_currency')
    
    # @api.model
    # def create(self, vals):
    #     res = super(SrcsBudgetRevisonLine, self).create(vals)
    #     res.update({'budget_id':self.budget_revision.budget_id.id})
    #     print('__________________\n\n\n',res)
    #     return res

    @api.depends('budget_revision.currency_id')
    def compute_currency(self):
        for record in self:
            if record.budget_revision.currency_id:
                record.currency_budget_line = record.budget_revision.currency_id.id
            
    @api.depends('budget_revision.budget_id.budget_type')
    def _compute_analytic_account_id(self):
        for rec in self:
            rec.analytic_account_id = rec.budget_revision.budget_id.analytic_account_id.id

    @api.depends('unit_of_measure','quantity','frequency','unit_cost')
    def _compute_total_budget(self):
        for rec in self:
            if rec.quantity and rec.frequency and rec.unit_cost:
                rec.total_budget = rec.quantity * rec.frequency * rec.unit_cost
            if rec.quantity and rec.unit_cost:
                rec.total_budget = rec.quantity * rec.unit_cost
            else:
                rec.total_budget = rec.total_budget
    
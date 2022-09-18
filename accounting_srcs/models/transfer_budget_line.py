from odoo import api, models, fields, _ 
from odoo.exceptions import ValidationError


class SrcsBudgetLineTransfer(models.Model):
    _name = "budget.line.transfer"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    rec_name = "sequence"

    sequence = fields.Char(string='Sequence', readonly=True, copy=False, index=True, default=lambda self: 'New Transfer')
    requested_date = fields.Date('Requested Date',default= fields.Date.today())
    requeted_amount = fields.Monetary('Requested Amount',currency_field="currency_id")
    budget_id = fields.Many2one('crossovered.budget', string='Budget',domain="[('state','=','validate')]")
    currency_id = fields.Many2one('res.currency','Currency',related='budget_id.currency_id',readonly=False)
    transfer_from = fields.Many2one('crossovered.budget.lines', string='Transfer From Line',domain="[('crossovered_budget_id','=',budget_id)]")
    transfered_from_limit = fields.Monetary('Amount Before',currency_field="budget_currency")
    from_limit = fields.Monetary('Amount After',default=0 ,readonly=True)
    transfer_to = fields.Many2one('crossovered.budget.lines', string='Transfer To Line',domain="[('crossovered_budget_id','=',budget_id)]")
    transfered_to_limit = fields.Monetary('Amount Before',currency_field="budget_currency")
    to_limit = fields.Monetary('Amount After',default=0 ,readonly=True)
    budget_currency = fields.Many2one(related='budget_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Finance Officer'),
        ('finance_manager','Finance Manager '),
        ('cancel', 'Cancelled'),
        ('validate', 'Validated'),
        ], 'Status', default='draft',readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'NEW') == 'NEW':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('payment.request') or 'NEW'
        result = super(SrcsBudgetLineTransfer, self).create(vals)
        return result

    @api.onchange('transfer_from','transfer_to')
    def _onchange_transfer_lines(self):
        if self.budget_id:
            self.transfered_from_limit = self.transfer_from.balance_budget_currency
            self.transfered_to_limit = self.transfer_to.balance_budget_currency

    @api.depends('requeted_amount')
    def transfer_amount(self):
        self.to_limit = 0
        self.from_limit = 0
        if self.transfered_from_limit > 0:
            self.from_limit = self.transfered_from_limit - self.requeted_amount
            print('_____________________________from limt',self.from_limit)
            self.to_limit = self.transfered_to_limit + self.requeted_amount
            print('_____________________________to limt',self.to_limit)
            transfer_from_line = self.env['crossovered.budget.lines'].search([('crossovered_budget_id','=',self.budget_id.id),('id','=',self.transfer_from.id)])
            transfer_to_line = self.env['crossovered.budget.lines'].search([('crossovered_budget_id','=',self.budget_id.id),('id','=',self.transfer_to.id)])
            if transfer_from_line:
                print('\n\n\n\n',transfer_from_line)
                transfer_from_line.total_budget = self.from_limit
                transfer_to_line.total_budget = self.to_limit
                print('\n\n\n\n',transfer_from_line.total_budget)
            self.state = 'finance_manager'
        else:
            raise ValidationError(_('Budget Balance is not enough'))

    def confirm_officer(self):
        self.state = 'confirm'

    # def confirm_manager(self):
    #     self.state = 'finance_manager'

    def validate(self):
        self.state = 'validate'

    def cancel(self):
        self.state = 'cancel'

    @api.constrains('requeted_amount','transfer_from')
    def _check_request_amount(self):
        for line in self:
            if line.budget_currency.id == line.currency_id.id:
                print('hreeeeeeeeeeeeeeeeeeeeeeeeeeee')
                if line.requeted_amount > line.transfered_from_limit:
                    print('________________________________total',line.requeted_amount)
                    raise ValidationError(_('Requested Amount should be less than or equal to Bugdet Line Balance'))  
            if line.budget_currency.id != line.currency_id.id:
                print("\n\n\n\n\n\n\n\n")
                print("rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
                request_amount = 0
                budget_amount_company_currency = 0
                request_amount = line.requeted_amount / line.currency_id.rate
                print('\n\n\n\n request_amount',request_amount) 
                budget_amount_company_currency = line.transfered_from_limit / line.budget_currency.rate
                print('\n\n\n\n',budget_amount_company_currency) 
                if request_amount > budget_amount_company_currency:
                    print('________________________________total_currency',budget_amount_company_currency)
                    raise ValidationError(_('Requested Amount should be less than or equal to Bugdet Balance'))

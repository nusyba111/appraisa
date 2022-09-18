from odoo import api, fields, models,_
from odoo.exceptions import ValidationError

class AccountSrcs(models.Model):
    _inherit = "account.move"
    
    state = fields.Selection([
        ('draft', 'Draft'),('finance_direct','Finance Director '),
        ('secratry_general','Secretary General  '),
        ('posted','Posted'),('cancel','cancelled'),
    ],default='draft', string='state')
    expensse_asset = fields.Boolean('Expensse Asset')
<<<<<<< HEAD
=======

    def approve_entry_pr(self):
        for record in self:
            if record.move_type =='entry':
                for rec in record.line_ids:
                    if rec.debit != 0:
                        if rec.analytic_account_id:
                            budget_lines = self.env['crossovered.budget.lines'].search([('date_from','<=',rec.date),('date_to','>=',rec.date),
                                                ('crossovered_budget_state','=','validate'),('analytic_activity_id','=',rec.activity_id.id),
                                                ('analytic_account_id','=',rec.analytic_account_id.id),
                                                ('general_budget_id.account_ids','in', rec.account_id.id)])
                            for line in budget_lines:
                                if line.location_id:
                                    budget_line = self.env['crossovered.budget.lines'].search([('date_from','<=',rec.date),('date_to','>=',rec.date),
                                                ('location_id','=',rec.location_id.id),
                                                ('crossovered_budget_state','=','validate'),('analytic_activity_id','=',rec.activity_id.id),
                                                ('analytic_account_id','=',rec.analytic_account_id.id),
                                                ('general_budget_id.account_ids','in', rec.account_id.id)])
                                else:
                                    budget_line = self.env['crossovered.budget.lines'].search([('date_from','<=',rec.date),('date_to','>=',rec.date),
                                                ('crossovered_budget_state','=','validate'),('analytic_activity_id','=',rec.activity_id.id),
                                                ('analytic_account_id','=',rec.analytic_account_id.id),
                                                ('general_budget_id.account_ids','in', rec.account_id.id)])

                        if not rec.analytic_account_id:
                            budget_lines = self.env['crossovered.budget.lines'].search([('date_from','<=',rec.date),('date_to','>=',rec.date),
                                                ('crossovered_budget_state','=','validate'),('analytic_activity_id','=',rec.activity_id.id),
                                                ('analytic_account_id','=',rec.branch_id_line.location_id.id),
                                                ('general_budget_id.account_ids','in', rec.account_id.id)])
                            for line in budget_lines:
                                if line.location_id:
                                    budget_line = self.env['crossovered.budget.lines'].search([('date_from','<=',rec.date),('date_to','>=',rec.date),
                                                ('location_id','=',rec.location_id.id),('crossovered_budget_state','=','validate'),('analytic_activity_id','=',rec.activity_id.id),
                                                ('analytic_account_id','=',rec.branch_id_line.location_id.id),
                                                ('general_budget_id.account_ids','in', rec.account_id.id)])
                                else:
                                    budget_line = self.env['crossovered.budget.lines'].search([('date_from','<=',rec.date),('date_to','>=',rec.date),
                                                ('crossovered_budget_state','=','validate'),('analytic_activity_id','=',rec.activity_id.id),
                                                ('analytic_account_id','=',rec.branch_id_line.location_id.id),
                                                ('general_budget_id.account_ids','in', rec.account_id.id)])
                        if budget_line:
                            invoice_total = rec.debit
                            print('__________________________________________________________invoicetotal',invoice_total)
                            conversion_amount = 0
                            rec.amount_from_conversion = 0
                            rec.amount_in_company_currency = 0
                            for line in budget_line:
                                if line.crossovered_budget_id.currency_id.id != record.company_id.currency_id.id:
                                    currency_conversion = self.env['currency.conversion'].search([('budget_id','=',line.crossovered_budget_id.id),('remain_amount','!=',0),('state','=','confirm')], order='id asc')                    
                                    if currency_conversion:
                                        for conversion in currency_conversion :
                                            conversion_amount += (conversion.remain_amount / conversion.rate)
                                            print('_______________before', conversion_amount)
                                        if conversion_amount >= invoice_total:
                                            for conversion in currency_conversion :
                                                record_amount = (conversion.remain_amount / conversion.rate)
                                                if invoice_total >= record_amount:
                                                    rec.amount_from_conversion += conversion.remain_amount
                                                    rec.amount_in_company_currency += (conversion.remain_amount * conversion.rate)
                                                    print('__________________________________________________amount in  company',rec.amount_in_company_currency) 
                                                    invoice_total -= record_amount
                                                    conversion.remain_amount = 0
                                                elif invoice_total < record_amount:
                                                    rec.amount_from_conversion += (invoice_total * conversion.rate)
                                                    rec.amount_in_company_currency += invoice_total
                                                    print('hgfdslkjhgfds',invoice_total)
                                                    print('++++++++++++++++++++++++amount in  company',rec.amount_in_company_currency)
                                                    conversion.remain_amount = conversion.remain_amount - (invoice_total * conversion.rate)
                                                    invoice_total = 0
                                        else:
                                            raise ValidationError(_('Conversion is less than the Expensses you have to make currency conversion .'))
                                    else:
                                        raise ValidationError(_('There is no converted amount to cover this bill.'))
                                else:
                                    if line.balance_budget_currency < invoice_total:
                                        raise ValidationError(_('Budget line balance is not enough.')) 
                                    else:
                                        print('________________________fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff',invoice_total)
                        else:
                            raise ValidationError(_('No budget line found for this move .'))

>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
    def approve_finance(self):
        for record in self:
            if record.move_type == 'in_invoice':
                for rec in record.invoice_line_ids:
                    if rec.analytic_account_id:
                        budget_lines = self.env['crossovered.budget.lines'].search([('date_from','<=',rec.date),('date_to','>=',rec.date),
                                            ('crossovered_budget_state','=','validate'),('analytic_activity_id','=',rec.activity_id.id),
                                            ('analytic_account_id','=',rec.analytic_account_id.id),
                                            ('general_budget_id.account_ids','in', rec.account_id.id)])
                        for line in budget_lines:
                            if line.location_id:
                                budget_line = self.env['crossovered.budget.lines'].search([('date_from','<=',rec.date),('date_to','>=',rec.date),
                                            ('location_id','=',rec.location_id.id),
                                            ('crossovered_budget_state','=','validate'),('analytic_activity_id','=',rec.activity_id.id),
                                            ('analytic_account_id','=',rec.analytic_account_id.id),
                                            ('general_budget_id.account_ids','in', rec.account_id.id)])
                            else:
                                budget_line = self.env['crossovered.budget.lines'].search([('date_from','<=',rec.date),('date_to','>=',rec.date),
                                            ('crossovered_budget_state','=','validate'),('analytic_activity_id','=',rec.activity_id.id),
                                            ('analytic_account_id','=',rec.analytic_account_id.id),
                                            ('general_budget_id.account_ids','in', rec.account_id.id)])

                    if not rec.analytic_account_id:
                        budget_lines = self.env['crossovered.budget.lines'].search([('date_from','<=',rec.date),('date_to','>=',rec.date),
                                            ('crossovered_budget_state','=','validate'),('analytic_activity_id','=',rec.activity_id.id),
                                            ('analytic_account_id','=',rec.branch_id_line.location_id.id),
                                            ('general_budget_id.account_ids','in', rec.account_id.id)])
                        for line in budget_lines:
                            if line.location_id:
                                budget_line = self.env['crossovered.budget.lines'].search([('date_from','<=',rec.date),('date_to','>=',rec.date),
                                            ('location_id','=',rec.location_id.id),('crossovered_budget_state','=','validate'),('analytic_activity_id','=',rec.activity_id.id),
                                            ('analytic_account_id','=',rec.branch_id_line.location_id.id),
                                            ('general_budget_id.account_ids','in', rec.account_id.id)])
                            else:
                                budget_line = self.env['crossovered.budget.lines'].search([('date_from','<=',rec.date),('date_to','>=',rec.date),
                                            ('crossovered_budget_state','=','validate'),('analytic_activity_id','=',rec.activity_id.id),
                                            ('analytic_account_id','=',rec.branch_id_line.location_id.id),
                                            ('general_budget_id.account_ids','in', rec.account_id.id)])
                    if budget_line:
                        invoice_total = rec.price_subtotal + ((rec.tax_ids.amount) / 100 * rec.price_subtotal)
                        print('_________________xxxxxx',invoice_total)
                        conversion_amount = 0
                        rec.amount_from_conversion = 0
                        rec.amount_in_company_currency = 0
                        for line in budget_line:
                            if line.crossovered_budget_id.currency_id.id != record.company_id.currency_id.id:
                                currency_conversion = self.env['currency.conversion'].search([('budget_id','=',line.crossovered_budget_id.id),('branch_id','=',rec.branch_id_line.id),('remain_amount','!=',0),('state','=','confirm')], order='id asc')                    
                                if currency_conversion:
                                    for conversion in currency_conversion :
                                        conversion_amount += (conversion.remain_amount / conversion.rate)
                                    if conversion_amount >= invoice_total:
                                        record.state = 'finance_direct'
                                    else:
                                        raise ValidationError(_('Conversion is less than the Expensses you have to make currency conversion .'))
                                else:
                                    raise ValidationError(_('There is no converted amount to cover this bill.'))
                            else:
                                if line.balance_budget_currency >= invoice_total:
                                    record.state = 'finance_direct'
                                else:
                                    print('_____________________dddd',line.balance_budget_currency)
                                    raise ValidationError(_('Budget line balance is not enough.')) 
                    else:
                        raise ValidationError(_('No budget line found for this move .'))
            else:
                record.state = 'finance_direct'

    def approve_secratry(self):
        self.state = "secratry_general"

    def _post(self, soft=True):
        for record in self:
            if record.move_type == 'in_invoice':
                for rec in record.invoice_line_ids:
<<<<<<< HEAD
                    changed_deffernce = abs(rec.credit - rec.debit)
                    fixed_deffernce = abs(rec.credit - rec.debit)
                    amount = 0
                    rec.amount_from_conversion = 0
                    budget_line = self.env['crossovered.budget.lines'].search([('date_from','<=',rec.date),('date_to','>=',rec.date),
                                        ('location_id','=',rec.location_id.id),
                                        ('crossovered_budget_state','=','validate'),('analytic_activity_id','=',rec.activity_id.id),
                                        ('analytic_account_id','=',rec.analytic_account_id.id),
                                        ('general_budget_id.account_ids','in', rec.account_id.id)])
                    print('_____________________budget line',budget_line)
=======
                    if rec.analytic_account_id:
                        budget_lines = self.env['crossovered.budget.lines'].search([('date_from','<=',rec.date),('date_to','>=',rec.date),
                                            ('crossovered_budget_state','=','validate'),('analytic_activity_id','=',rec.activity_id.id),
                                            ('analytic_account_id','=',rec.analytic_account_id.id),
                                            ('general_budget_id.account_ids','in', rec.account_id.id)])
                        for line in budget_lines:
                            if line.location_id:
                                budget_line = self.env['crossovered.budget.lines'].search([('date_from','<=',rec.date),('date_to','>=',rec.date),
                                            ('location_id','=',rec.location_id.id),
                                            ('crossovered_budget_state','=','validate'),('analytic_activity_id','=',rec.activity_id.id),
                                            ('analytic_account_id','=',rec.analytic_account_id.id),
                                            ('general_budget_id.account_ids','in', rec.account_id.id)])
                            else:
                                budget_line = self.env['crossovered.budget.lines'].search([('date_from','<=',rec.date),('date_to','>=',rec.date),
                                            ('crossovered_budget_state','=','validate'),('analytic_activity_id','=',rec.activity_id.id),
                                            ('analytic_account_id','=',rec.analytic_account_id.id),
                                            ('general_budget_id.account_ids','in', rec.account_id.id)])

                    if not rec.analytic_account_id:
                        budget_lines = self.env['crossovered.budget.lines'].search([('date_from','<=',rec.date),('date_to','>=',rec.date),
                                            ('crossovered_budget_state','=','validate'),('analytic_activity_id','=',rec.activity_id.id),
                                            ('analytic_account_id','=',rec.branch_id_line.location_id.id),
                                            ('general_budget_id.account_ids','in', rec.account_id.id)])
                        for line in budget_lines:
                            if line.location_id:
                                budget_line = self.env['crossovered.budget.lines'].search([('date_from','<=',rec.date),('date_to','>=',rec.date),
                                            ('location_id','=',rec.location_id.id),('crossovered_budget_state','=','validate'),('analytic_activity_id','=',rec.activity_id.id),
                                            ('analytic_account_id','=',rec.branch_id_line.location_id.id),
                                            ('general_budget_id.account_ids','in', rec.account_id.id)])
                            else:
                                budget_line = self.env['crossovered.budget.lines'].search([('date_from','<=',rec.date),('date_to','>=',rec.date),
                                            ('crossovered_budget_state','=','validate'),('analytic_activity_id','=',rec.activity_id.id),
                                            ('analytic_account_id','=',rec.branch_id_line.location_id.id),
                                            ('general_budget_id.account_ids','in', rec.account_id.id)])
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
                    if budget_line:
                        invoice_total = rec.price_subtotal + ((rec.tax_ids.amount) / 100 * rec.price_subtotal)
                        print('________________________________________________\n\n\n\n\n\n\n\n\n\ninoice total',invoice_total)
                        conversion_amount = 0
                        rec.amount_from_conversion = 0
                        rec.amount_in_company_currency = 0
                        for line in budget_line:
                            if line.crossovered_budget_id.currency_id.id != record.company_id.currency_id.id:
                                currency_conversion = self.env['currency.conversion'].search([('budget_id','=',line.crossovered_budget_id.id),('branch_id','=',rec.branch_id_line.id),('remain_amount','!=',0),('state','=','confirm')], order='id asc')                    
                                if currency_conversion:
                                    # if rec.move_id.currency_id == record.company_id.currency_id.id:
                                    #case of bill in company currency
                                    for conversion in currency_conversion :
                                        conversion_amount += (conversion.remain_amount / conversion.rate)
                                    if conversion_amount >= invoice_total:
                                        for conversion in currency_conversion :
                                            record_amount = (conversion.remain_amount / conversion.rate)
                                            if invoice_total >= record_amount:
                                                rec.amount_from_conversion += conversion.remain_amount
                                                rec.amount_in_company_currency += (conversion.remain_amount * conversion.rate)
                                                print('__________________________________________________amount in  company',rec.amount_in_company_currency) 
                                                invoice_total -= record_amount
                                                conversion.remain_amount = 0
                                            elif invoice_total < record_amount:
                                                rec.amount_from_conversion += (invoice_total * conversion.rate)
                                                rec.amount_in_company_currency += invoice_total
                                                print('++++++++++++++++++++++++amount in  company',rec.amount_in_company_currency)
                                                conversion.remain_amount = conversion.remain_amount - (invoice_total * conversion.rate)
                                                invoice_total = 0
                                    else:
                                        raise ValidationError(_('Conversion is less than the Expensses you have to make currency conversion .'))
                                    # else:
                                    #to do
                                    #case of bill not in company currency

                                else:
                                    raise ValidationError(_('There is no converted amount to cover this bill.'))
                            else:
<<<<<<< HEAD
                                raise ValidationError(_('You have to make currency conversion to cover Expensses.'))
                    else:
                        raise ValidationError(_('No budget line found for this move .'))

=======
                                if line.balance_budget_currency < invoice_total:
                                    raise ValidationError(_('Budget line balance is not enough.')) 
                    else:
                        raise ValidationError(_('No budget line found for this move .'))
        res = super(AccountSrcs, self)._post(soft=True)
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
        return res

        
class SrcChartofAccount(models.Model):
    _inherit = "account.account" 

    account = fields.Boolean('Account') 
    project = fields.Boolean('Project') 
    activity = fields.Boolean('Activity')
    donor = fields.Boolean('Donor')
    location = fields.Boolean('Location')


class SrcBudgte(models.Model):
    _inherit = "crossovered.budget"

    currency_conversion_ids = fields.One2many('currency.conversion', 'budget_id', string='Currency Conversion')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Finance Officer'),
        ('finance_manager','Finance Manager '),
        ('cancel', 'Cancelled'),
        ('validate', 'Validated'),
        ('done', 'Done')
        ], 'Status', default='draft', index=True, required=True, readonly=True, copy=False, tracking=True)
    budget_type = fields.Selection([
        ('core', 'Core'),('project','Project'),
    ],default='core', required=True, string='Budget Type')
<<<<<<< HEAD

    donor_id = fields.Many2one('res.partner', string='Donor', default=lambda self: self.company_id.partner_id.id)
=======
    date_from = fields.Date('Start Date', states={'done': [('readonly', True)]}, required=True)
    date_to = fields.Date('End Date', states={'done': [('readonly', True)]}, required=True)
    donor_id = fields.Many2one('res.partner', string='Donor', default=lambda self: self.env.company.partner_id.id)
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
    currency_id = fields.Many2one('res.currency', string='Currency')
    site = fields.Char('Site')
    situation = fields.Char('Situation')
    goal = fields.Char('Goal')
    project_id = fields.Many2one('account.analytic.account',string='Project', domain="[('type','=','project')]")
    site_boolean = fields.Boolean(related="project_id.site",store=True)
    situation_boolean = fields.Boolean(related="project_id.situation",store=True)
    goal_boolean = fields.Boolean(related="project_id.goal",store=True)
    unit_of_measure_boolean = fields.Boolean(related="project_id.unit_m",store=True)
    unit_cost_boolean = fields.Boolean(related="project_id.unit_cost",store=True)
    frequency_boolean = fields.Boolean(related="project_id.frequent",store=True)
    quantity_boolean = fields.Boolean(related="project_id.quantity",store=True)
    conversion_count = fields.Float(compute="compute_conversion_count")
    add_budget_lines  = fields.Boolean('Add Budget Line')


    @api.onchange('project_id')
    def _onchange_donor_id(self):
        if self.budget_type == 'project':
            self.donor_id = self.project_id.partner_id.id
<<<<<<< HEAD
            print('______________donor',self.donor_id,self.project_id.partner_id.id)
        

=======
        
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
    def confirm_manager(self):
        self.state = 'finance_manager'

    def get_currnecy_conversion(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Currency Conversions'),
            'view_mode': 'tree,form',
            'res_model': 'currency.conversion',
            'domain': [('budget_id', '=', self.id)],
            'context': "{'create': False}"
        } 

    def compute_conversion_count(self):
        for record in self:
            record.conversion_count = self.env['currency.conversion'].search_count([('budget_id', '=', self.id)])

class SrcBudgetLine(models.Model):
    _inherit = "crossovered.budget.lines"

<<<<<<< HEAD
    currency_budget_line = fields.Many2one('res.currency', string="Bugdet Currency",related='crossovered_budget_id.currency_id',store=True)
    analytic_account_id = fields.Many2one('account.analytic.account',store=True)
    analytic_activity_id = fields.Many2one('account.analytic.account', 'Output/Activity')
=======
    budget_revision = fields.Many2one('budget.revision', string='Budget Revision')
    currency_budget_line = fields.Many2one('res.currency', compute="compute_currency", string="Bugdet Currency",store=True)
    analytic_account_id = fields.Many2one('account.analytic.account',compute='_compute_analytic_account_id',store=True)
    analytic_activity_id = fields.Many2one('account.analytic.account', 'Output/Activity',required=True)
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
    location_id = fields.Many2one('account.analytic.account', string='Location', domain="[('type','=','location')]")
    description = fields.Char(related='analytic_activity_id.description',store=True)
    unit_of_measure = fields.Many2one('uom.uom', string='UOM')
    quantity = fields.Float('Quantity')
    frequency = fields.Float('Frequency')
    unit_cost = fields.Float('Unit Cost')
<<<<<<< HEAD
    practical_amount_bu_currency = fields.Monetary(compute='_compute_practical_budget_currency', currency_field='currency_budget_line',string='Practical Amount(Budget Currency)',store=True)
    balance_SDG = fields.Monetary(compute='_compute_balance_SDG', string='Balance SDG',currency_field='currency_id',store=True)
    balance_budget_currency = fields.Monetary(compute='_compute_balance_budegt_currency', string='Balance budget currency',currency_field='currency_budget_line',store=True)
    total_budget = fields.Monetary(compute='_compute_total_budget', string='Total budget (Budget Currency)',currency_field='currency_budget_line',store=True, readonly=False)
    planned_amount = fields.Monetary(string='Total budget ',currency_field='currency_id',store=True)
    
    @api.depends('crossovered_budget_id.budget_type')
    def _compute_analytic_account_id(self):
        for rec in self:
            if rec.crossovered_budget_id.project_id:
                rec.analytic_account_id = rec.crossovered_budget_id.project_id.id
            else:
                rec.analytic_account_id = rec.location_id.id
=======
    practical_amount_bu_currency = fields.Monetary(compute='_compute_practical_amount', currency_field='currency_budget_line',string='Practical Amount(Budget Currency)')
    balance_SDG = fields.Monetary(compute='_compute_balance_SDG', string='Balance SDG',currency_field='currency_id')
    balance_budget_currency = fields.Monetary(compute='_compute_balance_budegt_currency', string='Balance budget currency',currency_field='currency_budget_line')
    total_budget = fields.Monetary(compute='_compute_total_budget', string='Total budget (Budget Currency)',currency_field='currency_budget_line', readonly=False,store=True)
    planned_amount = fields.Monetary(string='Total budget ',currency_field='currency_id')
    
    @api.depends("analytic_activity_id","crossovered_budget_id", "general_budget_id", "analytic_account_id")
    def _compute_line_name(self):
        #just in case someone opens the budget line in form view
        for record in self:
            computed_name = record.analytic_activity_id.name+' - ' + record.crossovered_budget_id.name
            if record.general_budget_id:
                computed_name += ' - ' + record.general_budget_id.name
            if record.analytic_account_id:
                computed_name += ' - ' + record.analytic_account_id.name
            record.name = computed_name

    @api.depends('crossovered_budget_id.currency_id')
    def compute_currency(self):
        for record in self:
            if record.crossovered_budget_id.currency_id:
                record.currency_budget_line = record.crossovered_budget_id.currency_id.id
            
    @api.depends('crossovered_budget_id.budget_type')
    def _compute_analytic_account_id(self):
        for rec in self:
            if rec.crossovered_budget_id.budget_type == 'project':
                rec.analytic_account_id = rec.crossovered_budget_id.project_id.id
            else:
                rec.analytic_account_id = rec.crossovered_budget_id.branch_id.location_id.id
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44

    @api.depends('unit_of_measure','quantity','frequency','unit_cost')
    def _compute_total_budget(self):
        for rec in self:
            if rec.quantity and rec.frequency and rec.unit_cost:
                rec.total_budget = rec.quantity * rec.frequency * rec.unit_cost
<<<<<<< HEAD
                print('__________________________________________','\n',rec.currency_budget_line.rate)
    
    @api.onchange('total_budget')
    def _onchange_planned_amount(self):
        if self.currency_budget_line:
            if self.currency_budget_line.id == self.company_id.currency_id.id:
                self.planned_amount = self.total_budget
            if self.currency_budget_line.id != self.company_id.currency_id.id:
                self.planned_amount = self.total_budget / self.currency_budget_line.rate
        else:
            self.planned_amount = 0
=======
            if rec.quantity and rec.unit_cost:
                rec.total_budget = rec.quantity * rec.unit_cost
            else:
                rec.total_budget = rec.total_budget
            
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
            
    @api.onchange('total_budget')
    def _onchange_planned_amount(self):
        for rec in self:
            if rec.crossovered_budget_id.currency_id.id:
                if rec.currency_budget_line.id == rec.company_id.currency_id.id:
                    rec.planned_amount = rec.total_budget
                if rec.currency_budget_line.id != rec.company_id.currency_id.id:
                    rec.planned_amount = rec.total_budget / rec.crossovered_budget_id.currency_id.rate
                       
    
    def _compute_practical_amount(self):
<<<<<<< HEAD
        # res = super(SrcBudgetLine, self)._compute_practical_amount()
        self.practical_amount = 0
        for record in self:
            date_to = record.date_to
            date_from = record.date_from
            print('________________________dldlfflfl',record.practical_amount)
            # if record.analytic_account_id and record.analytic_activity_id and record.location_id and record.general_budget_id.account_ids:
            aml_obj = self.env['account.move.line']
            domain = []
            print('________________________gkgkhkhkhkkkhllhlhlllhh',domain)
            for line in record.general_budget_id.account_ids:
                if line.user_type_id.internal_group == 'expense': 
                
                    domain = [('account_id', 'in',
                            record.general_budget_id.account_ids.ids),
                            ('date', '>=', date_from),
                            ('date', '<=', date_to),
                            ('move_id.state', '=', 'posted'),
                            ('analytic_account_id','=',record.analytic_account_id.id),
                            ('activity_id','=',record.analytic_activity_id.id),
                            ('location_id','=',record.location_id.id),
                            # ('partner_id','=',record.crossovered_budget_id.donor_id.id),
                            ]
                    print('________________________domain parctical',domain)
                # elif line.internal_group == 'income':
                #     # aml_obj = self.env['account.move.line']
                #     domain = [('account_id', 'in',
                #             record.general_budget_id.account_ids.ids),
                #             ('date', '>=', date_from),
                #             ('date', '<=', date_to),
                #             ('move_id.state', '=', 'posted'),
                #             ('analytic_account_id','=',record.analytic_account_id.id),
                #             ('activity_id','=',record.analytic_activity_id.id),
                #             ('location_id','=',record.location_id.id),
                #             ('partner_id','=',record.crossovered_budget_id.donor_id.id),
                #             ]
                    where_query = aml_obj._where_calc(domain)
                    aml_obj._apply_ir_rules(where_query, 'read')
                    from_clause, where_clause, where_clause_params = where_query.get_sql()
                    select = "SELECT sum(credit)-sum(debit) from " + from_clause + " where " + where_clause

                    self.env.cr.execute(select, where_clause_params)
                    record.practical_amount = self.env.cr.fetchone()[0] or 0.0
                    print('========',record.practical_amount)
        # return res
    
    def _compute_practical_budget_currency(self):
        self.practical_amount_bu_currency = 0
        print('_____________________ssss\n \n \n \n')
        for res in self:
            if res.practical_amount != 0:
                # if res.currency_budget_line != res.currency_id:
                date_to = res.date_to
                date_from = res.date_from
                # move_line = self.env['account.move.line'].search([('account_id', 'in',
                #     res.general_budget_id.account_ids.ids),
                #     ('date', '>=', date_from),
                #     ('date', '<=', date_to),
                #     ('move_id.state', '=', 'posted'),
                #     ('analytic_account_id','=',res.analytic_account_id.id),
                #     ('activity_id','=',res.analytic_activity_id.id),
                #     ('location_id','=',res.location_id.id),
                #     ('partner_id','=',res.crossovered_budget_id.donor_id.id),])
                print('__________________________keofffffffffffff',res.practical_amount)
                move_line_exp = self.env['account.move.line'].search([('account_id', 'in',
                    res.general_budget_id.account_ids.ids),
                    ('date', '>=', date_from),
                    ('date', '<=', date_to),
                    ('move_id.state', '=', 'posted'),
                    ('analytic_account_id','=',res.analytic_account_id.id),
                    ('activity_id','=',res.analytic_activity_id.id),
                    ('location_id','=',res.location_id.id),
                    # ('partner_id','=',res.crossovered_budget_id.donor_id.id),
                    ])
                print('__________________________move_line_exp',move_line_exp)
                amount = 0
                if move_line_exp:
                    for exp in move_line_exp:
                        # if res.general_budget_id.account_ids.internal_group == 'expense':                        
                        if exp.move_id.move_type == 'in_invoice':
                            amount += exp.amount_from_conversion
                            res.practical_amount_bu_currency = -(amount)
                            print('__________________________practical',amount)
                # if move_line:
                #     for line in move_line:
                #         # elif res.general_budget_id.account_ids.internal_group == 'income':
                #         if line.move_id.move_type == 'out_invoice':
                #             if line.currency_id == res.currency_budget_line:
                #                 res.practical_amount_bu_currency += abs(line.amount_currency)
                #                 print('+++++++++++++++++++++practical',res.practical_amount_bu_currency)
                        
                #             else:
                #                 currency_obj = self.env['res.currency.rate'].search([('currency_id','=',res.currency_budget_line.id),('name','=',line.date)])
                #                 for currency in currency_obj:
                #                     res.practical_amount_bu_currency += line.credit * currency.company_rate
                #                     print('___+++++++++++++++++practical',res.practical_amount_bu_currency)
                # else:
                #     res.practical_amount_bu_currency = 0
                else:
                    print('________________________________________res.practical_amount_bu_currency',res.practical_amount_bu_currency)
                    res.practical_amount_bu_currency = 0
            else:
                print('________________________fffffffffffffff',res.practical_amount_bu_currency)
                res.practical_amount_bu_currency = 0
        
=======
        self.practical_amount = 0
        self.practical_amount_bu_currency = 0
        for res in self:
            date_to = res.date_to
            date_from = res.date_from
            if res.crossovered_budget_id.currency_id.id != res.company_id.currency_id.id:
                if res.location_id:
                    if res.crossovered_budget_id.budget_type == 'project':
                        move_line_exp = self.env['account.move.line'].search([('account_id', 'in',
                            res.general_budget_id.account_ids.ids),
                            ('date', '>=', date_from),
                            ('date', '<=', date_to),
                            ('move_id.state', '=', 'posted'),
                            ('analytic_account_id','=',res.analytic_account_id.id),
                            ('activity_id','=',res.analytic_activity_id.id),
                            ('location_id','=',res.location_id.id),
                            ])
                        amount = 0
                        amount_company = 0
                        if move_line_exp:
                            for exp in move_line_exp:
                                # if exp.move_id.move_type == 'entry':
                                #     amount += exp.debit
                                #     res.practical_amount_bu_currency = -(amount)
                                #     res.practical_amount = -(amount)
                                # if exp.move_id.move_type == 'in_invoice':
                                amount += exp.amount_from_conversion
                                res.practical_amount_bu_currency = -(amount)
                                amount_company += exp.amount_in_company_currency
                                res.practical_amount = -(amount_company)
                        else:
                            res.practical_amount_bu_currency = 0
                            res.practical_amount = 0
                    else:
                        move_line_exp = self.env['account.move.line'].search([('account_id', 'in',
                            res.general_budget_id.account_ids.ids),
                            ('date', '>=', date_from),
                            ('date', '<=', date_to),
                            ('move_id.state', '=', 'posted'),
                            ('activity_id','=',res.analytic_activity_id.id),
                            ('location_id','=',res.location_id.id),
                            ])
                        amount = 0
                        amount_company = 0
                        if move_line_exp:
                            for exp in move_line_exp:
                                if exp.move_id.move_type == 'entry':
                                    amount += exp.debit
                                    res.practical_amount_bu_currency = -(amount)
                                    res.practical_amount = -(amount)
                                if exp.move_id.move_type == 'in_invoice':
                                    amount += exp.amount_from_conversion
                                    res.practical_amount_bu_currency = -(amount)
                                    amount_company += exp.amount_in_company_currency
                                    res.practical_amount = -(amount_company)
                    
                        else:
                            res.practical_amount_bu_currency = 0
                            res.practical_amount = 0
                
                else:
                    if res.crossovered_budget_id.budget_type == 'project':
                        move_line_exp = self.env['account.move.line'].search([('account_id', 'in',
                            res.general_budget_id.account_ids.ids),
                            ('date', '>=', date_from),
                            ('date', '<=', date_to),
                            ('move_id.state', '=', 'posted'),
                            ('analytic_account_id','=',res.analytic_account_id.id),
                            ('activity_id','=',res.analytic_activity_id.id),
                            ])
                        amount = 0
                        amount_company = 0
                        if move_line_exp:
                            for exp in move_line_exp:
                                amount += exp.amount_from_conversion
                                res.practical_amount_bu_currency = -(amount)
                                amount_company += exp.amount_in_company_currency
                                res.practical_amount = -(amount_company)
                        else:
                            res.practical_amount_bu_currency = 0
                            res.practical_amount = 0
                    else:
                        move_line_exp = self.env['account.move.line'].search([('account_id', 'in',
                            res.general_budget_id.account_ids.ids),
                            ('date', '>=', date_from),
                            ('date', '<=', date_to),
                            ('move_id.state', '=', 'posted'),
                            ('activity_id','=',res.analytic_activity_id.id)])
                        amount = 0
                        amount_company = 0
                        if move_line_exp:
                            for exp in move_line_exp:
                                amount += exp.amount_from_conversion
                                res.practical_amount_bu_currency = -(amount)
                                amount_company += exp.amount_in_company_currency
                                res.practical_amount = -(amount_company)
                
                        else:
                            res.practical_amount_bu_currency = 0
                            res.practical_amount = 0
            else:
                if res.location_id:
                    if res.crossovered_budget_id.budget_type == 'project':
                        move_line_exp = self.env['account.move.line'].search([('account_id', 'in',
                            res.general_budget_id.account_ids.ids),
                            ('date', '>=', date_from),
                            ('date', '<=', date_to),
                            ('move_id.state', '=', 'posted'),
                            ('analytic_account_id','=',res.analytic_account_id.id),
                            ('activity_id','=',res.analytic_activity_id.id),
                            ('location_id','=',res.location_id.id),
                            ])
                        amount = 0
                        if move_line_exp:
                            for exp in move_line_exp:
                                if exp.move_id.move_type == 'entry':
                                    amount += exp.debit
                                    res.practical_amount_bu_currency = -(amount)
                                    res.practical_amount = -(amount)
                                if exp.move_id.move_type == 'in_invoice':
                                    amount += exp.price_subtotal + ((exp.tax_ids.amount) / 100 * exp.price_subtotal)
                                    res.practical_amount_bu_currency = -(amount)
                                    res.practical_amount = -(amount)
                        else:
                            res.practical_amount_bu_currency = 0
                            res.practical_amount = 0
                    else:
                        move_line_exp = self.env['account.move.line'].search([('account_id', 'in',
                            res.general_budget_id.account_ids.ids),
                            ('date', '>=', date_from),
                            ('date', '<=', date_to),
                            ('move_id.state', '=', 'posted'),
                            ('activity_id','=',res.analytic_activity_id.id),
                            ('location_id','=',res.location_id.id),
                            ('analytic_account_id','=',False),
                            ])
                        amount = 0
                        if move_line_exp:
                            for exp in move_line_exp:
                                if exp.move_id.move_type == 'entry':
                                    amount += exp.debit
                                    res.practical_amount_bu_currency = -(amount)
                                    res.practical_amount = -(amount)
                                if exp.move_id.move_type == 'in_invoice':
                                    amount += exp.price_subtotal + ((exp.tax_ids.amount) / 100 * exp.price_subtotal)
                                    res.practical_amount_bu_currency = -(amount)
                                    res.practical_amount = -(amount)
                    
                        else:
                            res.practical_amount_bu_currency = 0
                            res.practical_amount = 0
                else:
                    if res.crossovered_budget_id.budget_type == 'project':
                        move_line_exp = self.env['account.move.line'].search([('account_id', 'in',
                            res.general_budget_id.account_ids.ids),
                            ('date', '>=', date_from),
                            ('date', '<=', date_to),
                            ('move_id.state', '=', 'posted'),
                            ('analytic_account_id','=',res.analytic_account_id.id),
                            ('activity_id','=',res.analytic_activity_id.id),
                            ])
                        amount = 0
                        if move_line_exp:
                            for exp in move_line_exp:
                                if exp.move_id.move_type == 'entry':
                                    amount += exp.debit
                                    res.practical_amount_bu_currency = -(amount)
                                    res.practical_amount = -(amount)
                                if exp.move_id.move_type == 'in_invoice':
                                    amount += exp.price_subtotal + ((exp.tax_ids.amount) / 100 * exp.price_subtotal)
                                    res.practical_amount_bu_currency = -(amount)
                                    res.practical_amount = -(amount)
                        else:
                            res.practical_amount_bu_currency = 0
                            res.practical_amount = 0
                    else:
                        move_line_exp = self.env['account.move.line'].search([('account_id', 'in',
                            res.general_budget_id.account_ids.ids),
                            ('date', '>=', date_from),
                            ('date', '<=', date_to),
                            ('move_id.state', '=', 'posted'),
                            ('activity_id','=',res.analytic_activity_id.id),
                            ('analytic_account_id','=',False),
                            ])
                        amount = 0
                        if move_line_exp:
                            for exp in move_line_exp:
                                if exp.move_id.move_type == 'entry':
                                    amount += exp.debit
                                    res.practical_amount_bu_currency = -(amount)
                                    res.practical_amount = -(amount)
                                if exp.move_id.move_type == 'in_invoice':
                                    amount += exp.price_subtotal + ((exp.tax_ids.amount) / 100 * exp.price_subtotal)
                                    res.practical_amount_bu_currency = -(amount)
                                    res.practical_amount = -(amount)
                    
                        else:
                            res.practical_amount_bu_currency = 0
                            res.practical_amount = 0

>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
    @api.depends('practical_amount_bu_currency','total_budget')
    def _compute_balance_budegt_currency(self):
        for rec in self:
            rec.balance_budget_currency = rec.total_budget - abs(rec.practical_amount_bu_currency)    

    @api.depends('practical_amount','planned_amount')
    def _compute_balance_SDG(self):
        for rec in self:
            rec.balance_SDG = rec.planned_amount - abs(rec.practical_amount)
        
    def action_open_budget_entries(self):
        if self.analytic_account_id and self.analytic_activity_id and self.crossovered_budget_id.donor_id and self.location_id:
            action = self.env['ir.actions.act_window']._for_xml_id('account.action_account_moves_all_a')
            action['domain'] = [('account_id', 'in',
                                    self.general_budget_id.account_ids.ids),
                                ('activity_id','=', self.analytic_activity_id.id),
                                ('location_id','=', self.location_id.id),
                                ('analytic_account_id','=', self.analytic_account_id.id),
                                ('date', '>=', self.date_from),
                                ('date', '<=', self.date_to)
                                ]
            return action

        if self.analytic_account_id and self.analytic_activity_id and self.crossovered_budget_id.donor_id:
            action = self.env['ir.actions.act_window']._for_xml_id('account.action_account_moves_all_a')
            action['domain'] = [('account_id', 'in',
                                    self.general_budget_id.account_ids.ids),
                                ('activity_id','=', self.analytic_activity_id.id),
                                ('analytic_account_id','=', self.analytic_account_id.id),
                                ('date', '>=', self.date_from),
                                ('date', '<=', self.date_to)
                                ]
            return action
           

class SrcsActivityHierarchy(models.Model):
    _inherit = "account.analytic.group"

    project_id = fields.Many2one('account.analytic.account', string='Project', domain="[('type','=','project')]")


class srcAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"
   
    name = fields.Char('Name')
    description = fields.Char('Description')
    code = fields.Char('Code')
    type = fields.Selection([
        ('project', 'Project'),('activity','Activity'),('location','Location'),('core','Core Activity')
    ], string='Type')
    core_activity_id = fields.Many2one('account.analytic.account', string='Core Activity',domain="[('type','=','core')]")
    unit_m = fields.Boolean('Unit of Measure')
    quantity = fields.Boolean('Quantity')
    frequent = fields.Boolean('Frequency')
    unit_cost = fields.Boolean('unit cost')
    site = fields.Boolean('Site')
    situation = fields.Boolean('Situation')
    goal = fields.Boolean('Goal')
    partner_id = fields.Many2one('res.partner', string='Donor', auto_join=True, tracking=True, check_company=True)
    currency_id = fields.Many2one(related="company_id.currency_id", string="Currency",store=True ,readonly=False)
<<<<<<< HEAD
    
=======
    project_id = fields.Many2one('account.analytic.account', string='Project', domain="[('type','=','project')]")

>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
    def name_get(self):
        res = []
        for analytic in self:
            name = analytic.name
            if analytic.group_id and analytic.group_id.parent_id:
                name = '%s / %s / %s' % (analytic.group_id.parent_id.name, analytic.group_id.name, analytic.name)
            elif analytic.group_id and not analytic.group_id.parent_id:
                name = '%s / %s ' % (analytic.group_id.name, analytic.name)
            elif not analytic.group_id:
                name = '%s' % (analytic.name)
            res.append((analytic.id,name))
        return res
    

class Donor(models.Model):    
    _inherit = "res.partner"

    donor_code = fields.Char('Donor Code')

class SrcCurrency(models.Model):
    _inherit = 'res.currency'

    name = fields.Char(string='Currency', size=10,required=True, help="Currency Code (ISO 4217)")
    bank_id = fields.Many2one('res.bank', string='Bank')

class SrcAccountLine(models.Model):
    _inherit = "account.move.line"

    donor_bool = fields.Boolean(related="account_id.donor",store=True)
    activity_id = fields.Many2one('account.analytic.account', string='Activity',domain="[('type','=','activity')]")
    location_id = fields.Many2one('account.analytic.account', string='Location',domain="[('type','=','location')]")
    project = fields.Boolean(related="account_id.project",store=True)
    activity = fields.Boolean(related="account_id.activity",store=True)
    location = fields.Boolean(related="account_id.location",store=True)
    amount_from_conversion = fields.Float(default=0, string='Amount From Conversion')
    amount_in_company_currency = fields.Float(default=0, string='Amount in Company Currency')
    
                    
class Conversion(models.Model):
    _name = "currency.conversion"

    name = fields.Char(string='Name', required=True, default=lambda self: _('New'))
    source_bank = fields.Many2one('account.journal', string='Source Bank', required=True)
    dest_bank = fields.Many2one('account.journal', string='Destination Bank',required=True)
    budget_id = fields.Many2one('crossovered.budget', string='Budget', required=True)
    company_currency = fields.Many2one('res.currency', string='Currency', default= lambda self: self.env.company.currency_id.id)
    currency_id = fields.Many2one('res.currency', string='Currency',readonly=True,store=True)
    budget_limit = fields.Monetary('Budget Balance',currency_field='currency_id')
    date = fields.Date('Date', required=True, default= fields.Date.today())
    rate = fields.Float('Rate',compute="_compute_rate", digits=(12, 6), store=True)
    amount = fields.Monetary('Amount', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),('confirm','confirmed')
    ],default="draft", string='status')
    internal_transfer_id = fields.Many2one('account.payment', string='Internal Transfer', readonly=True)
    remain_amount = fields.Monetary('Remain Amount',readonly=True)
<<<<<<< HEAD
    remain_amount_sdg = fields.Monetary('Remain Amount SDG', currency_field='company_currency',digits=(12, 6),readonly=True)
=======
    remain_amount_sdg = fields.Monetary('Remaining SDG', compute="_compute_remain_sdg", currency_field='company_currency',digits=(12, 6),readonly=True,store=True)

    @api.depends('currency_id')
    def _compute_rate(self):
        for rec in self:
            rec.rate = rec.budget_id.currency_id.rate
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44

    @api.onchange('budget_id')
    def _onchange_budget(self):
        sum_balance = 0
        for record in self:
            if record.budget_id:
                record.currency_id = record.budget_id.currency_id.id
                for line in record.budget_id.crossovered_budget_line:
                    sum_balance += line.balance_budget_currency
                record.budget_limit = sum_balance
           
    @api.onchange('amount')
    def _onchange_remain_amount(self):
        for rec in self:
            rec.remain_amount = rec.amount

    @api.depends('remain_amount')
    def _compute_remain_sdg(self):
        self.remain_amount_sdg = 0
        for res in self:
            if res.rate:
                res.remain_amount_sdg = res.remain_amount / res.rate
        
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('currency.conversion') or _('New')
        res = super(Conversion, self).create(vals)
        return res

    def confirm(self):
        for rec in self:
            if rec.currency_id:
                internal_transfer = self.env['account.payment'].create({
                    'is_internal_transfer':True,
                    'payment_type':'outbound',
                    'type_internal_transfer':'inernal',
                    'journal_id':rec.source_bank.id,
                    'destination_journal_id':rec.dest_bank.id,
                    'amount':rec.amount,
                    'date':rec.date,
                    'currency_id':rec.currency_id.id,
                    'ref':rec.name,
                })
                rec.internal_transfer_id = internal_transfer.id
                rec.state = "confirm"

    @api.constrains('amount','budget_limit')
    def _constrains_amount(self):
        for rec in self:
            print(rec.amount)
            print(rec.budget_limit)
            if rec.amount > rec.budget_limit:
                raise ValidationError(_('You can not convert amount more then budget limit'))


class SrcsPayment(models.Model):
    _inherit = "account.payment"

    project_id = fields.Many2one('account.analytic.account',string="Project", domain="[('type','=','project')]")
    type_internal_transfer = fields.Selection([
        ('inernal', 'Internal Transfer'),
        ('branch', 'Transfer To Branch'),
    ], default='inernal', string='Internal Transfer Type')
    
    # Modify internal transfer receipt payment be in draft state not posted in case send to branch
    def _create_paired_internal_transfer_payment(self):
        for payment in self:
            if payment.type_internal_transfer == 'branch':
                paired_payment = payment.copy({
                    'journal_id': payment.destination_journal_id.id,
                    'destination_journal_id': payment.journal_id.id,
                    'payment_type': payment.payment_type == 'outbound' and 'inbound' or 'outbound',
                    'move_id': None,
                    'ref': payment.ref,
                    'paired_internal_transfer_payment_id': payment.id
                })
                payment.paired_internal_transfer_payment_id = paired_payment

                body = _('This payment has been created from <a href=# data-oe-model=account.payment data-oe-id=%d>%s</a>') % (payment.id, payment.name)
                paired_payment.message_post(body=body)
                body = _('A second payment has been created: <a href=# data-oe-model=account.payment data-oe-id=%d>%s</a>') % (paired_payment.id, paired_payment.name)
                payment.message_post(body=body)

                lines = (payment.move_id.line_ids + paired_payment.move_id.line_ids).filtered(
                    lambda l: l.account_id == payment.destination_account_id and not l.reconciled)

            if payment.type_internal_transfer == 'inernal':
                paired_payment = payment.copy({
                    'journal_id': payment.destination_journal_id.id,
                    'destination_journal_id': payment.journal_id.id,
                    'payment_type': payment.payment_type == 'outbound' and 'inbound' or 'outbound',
                    'move_id': None,
                    'ref': payment.ref,
                    'paired_internal_transfer_payment_id': payment.id
                })
                paired_payment.move_id._post(soft=False)
                payment.paired_internal_transfer_payment_id = paired_payment

                body = _('This payment has been created from <a href=# data-oe-model=account.payment data-oe-id=%d>%s</a>') % (payment.id, payment.name)
                paired_payment.message_post(body=body)
                body = _('A second payment has been created: <a href=# data-oe-model=account.payment data-oe-id=%d>%s</a>') % (paired_payment.id, paired_payment.name)
                payment.message_post(body=body)

                lines = (payment.move_id.line_ids + paired_payment.move_id.line_ids).filtered(
                    lambda l: l.account_id == payment.destination_account_id and not l.reconciled)
                lines.reconcile()
       


    
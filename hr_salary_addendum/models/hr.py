# -*- coding: utf-8 -*-

from odoo import api, fields, models,_
from odoo.exceptions import ValidationError, UserError, Warning


class SalaryAddendum(models.Model):
    _name = 'hr.salary.addendum'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'

    date = fields.Date(string="Date")
    employee_id = fields.Many2one('hr.employee',string="To",domain="[('branch_id','=',branch_id)]")
    job_id = fields.Many2one('hr.job',related="employee_id.job_id",string="Job Title")
    branch_id = fields.Many2one("res.branch",string="Branch",readonly=True,default=lambda self: self.env.user.current_branch)
    current_grade = fields.Many2one('hr.grade',related="employee_id.grade_id",string="Current Grade")
    current_level = fields.Many2one('hr.level',related="employee_id.level_id",string="Current Level")
    grade_id = fields.Many2one('hr.grade',string="Grade",domain="[('branch_id','=',branch_id)]")
    level_id = fields.Many2one('hr.level',string="Degree",domain="[('grade_id','=',grade_id),('branch_id','=',branch_id)]")
    state = fields.Selection([('draft','Employee Approve'),
                            ('employee','Head Of HR Section'),
                            ('hr_head_section','Approved'),
                            ('finance_approve','Finance Approve')]
                            ,default='draft',string="State")
    plan_id = fields.One2many('salary.plan.addendum','addendum_id',string="Coverage Salary Addendum")
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.user.company_id.currency_id)



    def action_submit(self):
        self.write({'state':'employee'})

    def action_hr_approve(self):
        self.write({'state':'hr_head_section'})
        


    def action_finance_approve(self):
        for line in self.plan_id:
            if self.currency_id == line.currency_id.id:
                if line.percentage_of_covering > line.budget_balance:
                    raise ValidationError(_('Requested Amount should be less than or equal to Bugdet Balance'))  
        if self.grade_id:
            self.employee_id.grade_id = self.grade_id.id
            self.employee_id.level_id = self.level_id.id
        self.write({'state':'finance_approve'})            
                



        



class SalaryPlanaddendum(models.Model):
    _name = 'salary.plan.addendum'

    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, compute="_compute_buget_balance", store=True)
    addendum_id = fields.Many2one('hr.salary.addendum',string="Salary Addendum")
    project = fields.Many2one('account.analytic.account',string="Project",domain="[('type','=','project')]")
    percentage_of_covering = fields.Float(string="Percentage Of Covering")
    activity = fields.Many2one('account.analytic.account',domain="[('type','=','activity')]",string="Activity")
    location = fields.Many2one('account.analytic.account',domain="[('type','=','location')]",string="Location")
    donor_id = fields.Many2one('res.partner',string="Doner")
    account_id = fields.Many2one('account.account',string="Account",domain="[('internal_group','=','expense')]")
    budget_balance = fields.Monetary(compute="_compute_buget_balance", string='Budget Balance', store=True)

    @api.depends('donor_id','project','account_id','activity')
    def _compute_buget_balance(self):
        for rec in self:
            rec.budget_balance = 0
            if rec.donor_id and rec.project and rec.account_id and rec.activity:
                budget_line = self.env['crossovered.budget.lines'].search([('crossovered_budget_id.donor_id','=', rec.donor_id.id),
                                                                            ('analytic_activity_id','=',rec.activity.id),
                                                                            ('analytic_account_id','=',rec.project.id),
                                                                            ('general_budget_id.account_ids','in', rec.account_id.id),
                                                                            ('date_from','<=',rec.addendum_id.date),('date_to','>=',rec.addendum_id.date),
                                                                            ('crossovered_budget_id.state','=','validate')])
                if budget_line:
                    rec.budget_balance = budget_line.balance_budget_currency
                    rec.currency_id = budget_line.currency_budget_line.id
                else:
                    raise ValidationError(_('There is No Budget for this %s and %s and %s and %s')%(rec.account_id.name,rec.project.name,rec.activity.name,rec.donor_id.name))
            else:
                rec.budget_balance = 0


    

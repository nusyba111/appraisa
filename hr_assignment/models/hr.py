# -*- coding: utf-8 -*-

from odoo import api, fields, models,_
from odoo.exceptions import ValidationError, UserError, Warning


class HRAssignment(models.Model):
    _name = 'hr.assigment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'

    date = fields.Date(string="Date")
    employee_id = fields.Many2one('hr.employee',string="Dear /",domain="[('branch_id','=',branch_id)]")
    branch_id = fields.Many2one("res.branch",string="Branch",readonly=True,default=lambda self: self.env.user.current_branch)
    state = fields.Selection([('draft','HR Manager Approve'),
                            ('hr_approve','Employee Approve'),
                            ('approve','Approved')]
                            ,default='draft',string="State")


    def action_submit(self):
        self.write({'state':'hr_approve'})

    def action_employee_approve(self):
        self.write({'state':'approve'})
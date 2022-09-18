# -*- coding: utf-8 -*-
###############################################################################
#
#    IATL International Pvt. Ltd.
#    Copyright (C) 2020-TODAY Tech-Receptives(<http://www.iatl-sd.com>).
#
###############################################################################
from odoo import models, fields, api, _


class HrMissionTicket(models.Model):
    _name = 'hr.mission.ticket'
    
    travel_agency = fields.Many2one('res.partner',string="Travel Agency")
    date_from = fields.Date(string= "Date From")
    date_to = fields.Date(string= "Date To")
    ticket_amount = fields.Float(string="Ticket Amount")
    account_id = fields.Many2one('account.account',string="Ticket Account")
    doner = fields.Many2one('res.partner',string="Doner",required=True)
    project = fields.Many2one('account.analytic.account',required=True, domain="[('type','=','project')]",string="Project")
    activity = fields.Many2one('account.analytic.account',required=True,domain="[('type','=','activity')]",string="Activity")
    location = fields.Many2one('account.analytic.account',required=True,domain="[('type','=','location')]",string="Location")
    state = fields.Selection([('draft','Draft'),('approve','Approved')],default='draft')
    payment_request_id = fields.Many2one('payment.request',string="Payment Request")

    def action_approve(self):
        self.write({'state':'approve'})
        line_list = []
        request_line = {
          'project_id':self.project.id,
          'analytic_activity_id':self.activity.id,
          'donor_id':self.doner.id,
          'request_amount':self.ticket_amount,
        }
        line_list.append((0, 0, request_line))
        payment_request = self.env['payment.request'].create({
            'journal_id':self.journal_id.id,
            'reason':'Annual Leave Allowance',
            'budget_line_ids':line_list
            })
        self.payment_request_id = payment_request.id    
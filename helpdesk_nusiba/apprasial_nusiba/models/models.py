# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HelpDeskTicket(models.Model):
    _name = 'hd.ticket'
    _rec_name = 'ticket_id'
    _inherit = ['mail.thread', 'mail.activity.mixin', ]
    _description = 'Help Desk Ticket'
    #
    date = fields.Date(string='Date')
    ticket_id = fields.Char(string='Ticket ID', copy=False)
    customer_id = fields.Many2one('res.partner', string='Customer')
    name = fields.Char(string='Name', )
    time_submitted = fields.Float(string='Time submitted', readonly=True)
    description = fields.Text(string='Description', required=True)
    team_id = fields.Many2one('hd.team', string='Team')
    assign_to_id = fields.Many2one('res.users', string='Assigned to')
    priority = fields.Selection([('0', 'all'),('1', 'low'), ('2', 'medium'), ('3', 'high') ])
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    # all info are related to customer
    partner_name = fields.Char(string='Customer Name', compute='_compute_partner_name', store=True, readonly=False)
    partner_email = fields.Char(string='Customer Email', compute='_compute_partner_email', store=True, readonly=False)
    customer_phone = fields.Char(string='Customer Phone')
    tags_ids = fields.Many2many('hd.tags', 'ticket_tag_rel', string='Tags')
    hosting_type = fields.Selection([('on-premise', 'On-Premise'), ('cloud', 'Cloud')], required=True,
                                    string='Hosting Type')
    server_url = fields.Char(string='Server URL')
    # resolution_time=fields.Float(compute='')
    state = fields.Selection(string='State',
                             selection=[('draft', 'Draft'),
                                        ('new', 'New'),
                                        ('in_progress', 'In Progress'),
                                        ('solved', 'Solved'),
                                        ('cancel', 'Cancelled'),
                                        ],
                             readonly=True, copy=False, index=True, tracking=3, default='draft')
    all_tickets = fields.Integer('All Tickets')
    my_tickets = fields.Integer('My Tickets')
     # tickets = fields.Integer('Tickets')


    # @api.depends('partner_id')
    # def _compute_partner_name(self):
    #     for ticket in self:
    #         if ticket.partner_id:
    #             ticket.partner_name = ticket.partner_id.name

    @api.depends('partner_id')
    def _compute_partner_name(self):
        for rec in self:
            if rec.partner_id:
                rec.partner_name = rec.partner_id.name

    @api.depends('partner_id')
    def _compute_partner_email(self):
        for rec in self:
            if rec.partner_id:
                rec.partner_email = rec.partner_id.email


    @api.model
    def assign_ticket_to_self(self):
        self.ensure_one()
        self.user_id = self.env.user

    # # sequence function for doc_num
    # # @api.model
    # # def create(self, vals):
    # #     vals['doc_num'] = self.env['ir.sequence'].next_by_code(
    # #         'hd.ticket.seq') or 'New'
    # #     return super(HelpDeskTicket, self).create(vals)
    # @api.model_create_multi
    # def create(self, list_value):
    #     now = fields.Datetime.now()
        # determine user_id and stage_id if not given. Done in batch.
        # teams = self.env['helpdesk.team'].browse([vals['team_id'] for vals in list_value if vals.get('team_id')])
        # team_default_map = dict.fromkeys(teams.ids, dict())
        # for team in teams:
        #     team_default_map[team.id] = {
        #         'stage_id': team._determine_stage()[team.id].id,
        #         'user_id': team._determine_user_to_assign()[team.id].id
        #     }

        # Manually create a partner now since 'generate_recipients' doesn't keep the name. This is
        # to avoid intrusive changes in the 'mail' module
        # for vals in list_value:
        #     partner_id = vals.get('partner_id', False)
        #     partner_name = vals.get('partner_name', False)
        #     partner_email = vals.get('partner_email', False)
        #     if partner_name and partner_email and not partner_id:
        #         try:
        #             vals['partner_id'] = self.env['res.partner'].find_or_create(
        #                 tools.formataddr((partner_name, partner_email))
        #             ).id
        #         except UnicodeEncodeError:
        #             # 'formataddr' doesn't support non-ascii characters in email. Therefore, we fall
        #             # back on a simple partner creation.
        #             vals['partner_id'] = self.env['res.partner'].create({
        #                 'name': partner_name,
        #                 'email': partner_email,
        #             }).id

    #     @api.depends('team_id')
    # def _compute_user_and_stage_ids(self):
    #     for ticket in self.filtered(lambda ticket: ticket.team_id):
    #         if not ticket.user_id:
    #             ticket.user_id = ticket.team_id._determine_user_to_assign()[ticket.team_id.id]
    #         if not ticket.stage_id or ticket.stage_id not in ticket.team_id.stage_ids:
    #             ticket.stage_id = ticket.team_id._determine_stage()[ticket.team_id.id]

    def action_draft(self):
        return self.write({'state': 'draft'})

    def action_cancel(self):
        return self.write({'state': 'cancel'})

    def action_new(self):
        return self.write({'state': 'new'})

    def action_in_progress(self):
        return self.write({'state': 'in_progress'})

    def action_solved(self):
        return self.write({'state': 'solved'})


        # , ('4', 'excellent')




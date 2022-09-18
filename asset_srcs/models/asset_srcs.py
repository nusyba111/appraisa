from odoo import api, fields, models,_

class SrcsAsset(models.Model):
    _inherit = "account.asset"

    location_id = fields.Many2one('account.analytic.account', string='Location',domain="[('type','=','location')]")
    owner = fields.Many2one('res.users', string='User', default= lambda self: self.env.user)
    donor_id = fields.Many2one('res.partner', string='Donor')
    project_id = fields.Many2one('account.analytic.account', string='Project',domain="[('type','=','project')]")
    office = fields.Char('Office')
    description = fields.Char('Description')
    mark = fields.Char('Mark')
    serial_num = fields.Char('Serial Number')
    code = fields.Char('Code')
    photo = fields.Binary('Photo')
    state = fields.Selection([('model', 'Model'), ('draft', 'Draft'), ('open', 'Asset Manager'),('finance','Finance Director'),('sg','Secretary General'),('paused', 'On Hold'), ('close', 'Closed')], 'Status', copy=False, default='draft',
        help="When an asset is created, the status is 'Draft'.\n"
            "If the asset is confirmed, the status goes in 'Running' and the depreciation lines can be posted in the accounting.\n"
            "The 'On Hold' status can be set manually when you want to pause the depreciation of an asset for some time.\n"
            "You can manually close an asset when the depreciation is over. If the last line of depreciation is posted, the asset automatically goes in that status.")

    def action_finance(self):
        self.state = 'finance'

    def action_sg(self):
        self.state = 'sg'
        
class SrcsAssetOpertaion(models.Model):
    _name = "asset.opertaion"

    name = fields.Char('Operation Name', required=True, readonly=True, default=lambda self: 'New')
    donor_id = fields.Many2one('res.partner', string='Donor', required=True)
    project_id = fields.Many2one('account.analytic.account', string='Project',domain="[('type','=','project')]", required=True)
    location_id = fields.Many2one('account.analytic.account', string='Location',domain="[('type','=','location')]", required=True)
    type = fields.Selection([
        ('donation', 'Donation In Kind'),('transfer','Transfer Between Branches'),('transfer_asset','Transfer From Donor'),
    ], string='Type')
    acquistion_date = fields.Date('Acquisition Date')
    asset_id = fields.Many2one('account.asset', string='Asset', domain="[('state','!=','model')]")
    asset_type_id = fields.Many2one('account.asset', string='Asset Type', domain="[('state','=','model')]")
    currency_id = fields.Many2one('res.currency',related='asset_id.currency_id')
    net_value = fields.Monetary('Net Value',related='asset_id.original_value', currency_field="currency_id")
    debit = fields.Many2one('account.account', string='Debit Account')
    credit = fields.Many2one('account.account', string='Credit Account')
    state = fields.Selection([
        ('darft','Draft'),
        ('project', 'Project/Fleet'),
        ('asset_manager','Asset Manager'),
        ('finance_director','Finance Director'),
        ('secratry_general','Secretary General  '),
    ], default="darft", string='State')
    move_id = fields.Many2one('account.move', string="Journal Entry", readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'NEW') == 'NEW':
            vals['name'] = self.env['ir.sequence'].next_by_code('asset.operation') or 'NEW'
        result = super(SrcsAssetOpertaion, self).create(vals)
        return result

    @api.onchange('asset_id')
    def _onchange_asset_id(self):
        for rec in self:
            rec.asset_type_id = rec.asset_id.model_id.id
            rec.project_id = rec.asset_id.project_id.id
            rec.location_id = rec.asset_id.location_id.id
            rec.donor_id = rec.asset_id.donor_id.id

    def confirm(self):
        self.state = "project"

    def submit_manager(self):
        self.state = "asset_manager"

    def approve_director(self):
        move = {
            'name': self.name,
            'date': self.acquistion_date,
            'partner_id': self.donor_id.id,
            'move_type': 'entry',
            'state': 'draft',
            'line_ids': [(0, 0, {
                'name': self.name,
                'partner_id': self.donor_id.id,
                'account_id': self.debit.id,
                'analytic_account_id': self.project_id.id,
                'location_id': self.location_id.id,
                'debit': self.net_value}),
                (0, 0, {
                'name': self.name,
                'partner_id': self.donor_id.id,
                'account_id': self.credit.id,
                'analytic_account_id': self.project_id.id,
                'location_id': self.location_id.id,
                'credit': self.net_value})]
            }
        move_id = self.env['account.move'].create(move)
        # move_id.post()
        if self.type == 'transfer':
            self.asset_id.branch_id = self.transfer_to.id
        if move_id:
            self.move_id = move_id.id
        self.state = "finance_director"

    def done_secratry(self):
        self.state = "secratry_general"

    def reset_draft(self):
        self.state = "darft"

    
class AccountAsset(models.Model):
    _inherit = "account.move"

    #to be reviewed
    def create_asset(self):
        # vals=[]
        expense_account = self.line_ids.filtered(lambda line: line.account_id.user_type_id.internal_group == "expense")
        if expense_account:
<<<<<<< HEAD
            print('________________________________________________expense_account',expense_account)
=======
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
            for line in expense_account: 
                vals = {
                    'state': 'draft',
                    'company_id': line.company_id.id,
                    'name': line.name,
                    'original_value': line.price_subtotal,
                    'acquisition_date': self.date,
                    'currency_id': self.currency_id.id,
                    'method': 'linear',
                    'original_move_line_ids': [(6, False, line.ids)],
                    }  
                model_id = line.account_id.asset_model
                if model_id:
                    vals.update({
                        'model_id': model_id.id,
                    })
<<<<<<< HEAD
                print('_______________________________',vals)
=======
>>>>>>> 38c8c1b6423fa61a6ac1a666891c83c6440bdb44
                self.env['account.asset'].create(vals)
                self.expensse_asset = True
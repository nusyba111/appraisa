from odoo import fields, models,api,_


class reason_wiz(models.TransientModel):

    _name = 'reason.wiz'

    description = fields.Text(string='Reason', required=True)

    def add_reason(self,data):
        current_reconsile=self.env['bank.acc.rec.statement'].search([('id','=',data['active_id'])])

        current_reconsile.reason = self.description
        current_reconsile.action_cancel()
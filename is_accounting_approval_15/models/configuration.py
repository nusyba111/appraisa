##############################################################################
#    Description: Accounting Approval                                        #
#    Author: IntelliSoft Software                                            #
#    Date: Aug 2015 -  Till Now                                              #
##############################################################################

from odoo import models, fields, api, _
from odoo.tools.misc import format_date
from odoo.tools import image_process


# inherit to add manager for approvals
class res_users(models.Model):
    _inherit = 'res.users'

    approval_manager = fields.Many2one('res.users', 'Manager for Approval(s)')
    user_signature = fields.Binary('Signature')
    resized_user_signature = fields.Binary('Resized Signature')

    @api.depends('user_signature')
    def _get_image(self):
        if self.user_signature:
            self.resized_user_signature = self.user_signature

    def resize_signature(self):
        if self.user_signature:
            self.resized_user_signature = image_process(self.user_signature, size=(100, 50))


#################################################################################################
# inherit
class ResCurrency(models.Model):
    _inherit = 'res.currency'

    narration_ar_un = fields.Char('Arabic Narration Main')
    narration_ar_cn = fields.Char('Arabic Narration Denomination')


# inherit to add F.M Limit to approve finance approval request
class TResCompany(models.Model):
    _inherit = 'res.company'

    f_limit = fields.Float('FC Manager Limit')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    fn_req_gm_approval = fields.Boolean(string="GM Approval",
                                        config_parameter='is_accounting_approval_15.fn_req_gm_approval', readonly=False)
    fn_req_gm_approval_amount = fields.Float(string="Minimum Amount", required=False,
                                             config_parameter='is_accounting_approval_15.fn_req_gm_approval_amount',
                                             readonly=False)

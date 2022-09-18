from odoo import fields, api, models,_
from odoo.osv import expression

class SrcsEmployee(models.Model):
    _inherit="hr.employee"

    emp_code = fields.Char(string='Employee Code')

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|',('name', operator, name), ('emp_code', operator, name)]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

    # def name_get(self):
    #     result = []
    #     for emp in self:
    #         name = emp.emp_code + ' ' + emp.name
    #         result.append((emp.id, name))
    #     return result
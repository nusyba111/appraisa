from dateutil.relativedelta import relativedelta
from openerp import fields, models, api, tools, _
import xlsxwriter
import base64
from io import StringIO, BytesIO
from openerp.exceptions import Warning as UserError
from odoo.tools import *

class PINReport(models.Model):
    _name = 'pin.card'
    _description = 'Print all Product'

    location=fields.Many2one('stock.location',string='To Location' ,domain=[('usage','=','internal')])
    date_from=fields.Datetime('Date From',required=True)
    date_to=fields.Datetime('Date To',required=True)
    product_id=fields.Many2one('product.product',string='Product',required=True)

    def print_report(self):
        # data = {}
        # data['ids'] = self.env.context.get('active_ids', [])
        # data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        # data['form'] = self.read(['date_from', 'date_to', 'location', 'product_id'])location

        return True

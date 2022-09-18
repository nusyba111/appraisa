# -*- coding: utf-8 -*-
###########
from dateutil.relativedelta import relativedelta
from openerp import fields, models, api, tools, _
import xlsxwriter
import base64
from io import StringIO, BytesIO
from openerp.exceptions import Warning as UserError
from odoo.tools import *

class WarehouseReport(models.Model):
    _name = 'warehouse.report'
    _description = 'Print all Warehouse Products'

    location=fields.Many2one('stock.location',string='From Location' ,domain=[('usage','=','internal')])
    date_from=fields.Datetime(string='Date From',required=True)
    date_to=fields.Datetime(string='Date To',required=True)

    def print_report(self):
        for report in self:
            a = 1
            logo = report.env.user.company_id.logo
            company_id = report.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
            file_name = _('Warehouse Report.xlsx')
            fp = BytesIO()
            workbook = xlsxwriter.Workbook(fp)
            excel_sheet = workbook.add_worksheet('Warehouse Report')
            report_title = 'Warehouse Report For SRCS Purchase '
            report_second_title =  self.location.name
            header_format = workbook.add_format(
                {'bold': True, 'font_color': 'white', 'bg_color': '#0080ff', 'border': 1})
            header_format_sequence = workbook.add_format(
                {'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1})
            header_format.set_align('center')
            header_format.set_align('vertical center')
            header_format.set_text_wrap()
            format = workbook.add_format(
                {'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1, 'font_size': '10'})
            title_format = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': 'white', 'border': 1})
            title_format.set_align('center')
            format.set_align('center')
            header_format_sequence.set_align('center')
            format.set_text_wrap()
            format.set_num_format('#,##0.000')
            sequence_format = workbook.add_format(
                {'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1})
            sequence_format.set_align('center')
            sequence_format.set_text_wrap()
            total_format = workbook.add_format(
                {'bold': True, 'font_color': 'black', 'bg_color': '#808080', 'border': 1, 'font_size': '10'})

            excel_sheet.merge_range('A1:G1', report_title, title_format)
            excel_sheet.merge_range('A2:G2', report_second_title, title_format)

            col = 0
            row = 3
            excel_sheet.set_column(col, col, 25)
            excel_sheet.write(row, col, 'No', header_format)
            col += 1
            excel_sheet.set_column(col, col, 25)
            excel_sheet.write(row, col, 'Supplier Part#', header_format)
            col += 1
            excel_sheet.set_column(col, col, 25)
            excel_sheet.write(row, col, 'Item Description', header_format)
            col += 1
            excel_sheet.set_column(col, col, 25)
            excel_sheet.write(row, col, 'Item Description in Arabic', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'UM (Unit of Measure)', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Opening Stock Quantity in '+self.location.name, header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Current Stock', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Last Purchase Price(USD)', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Stock Value(USD)', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Last Purchase Price(SDG)', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Stock Value(SDG)', header_format)
            col += 1
            excel_sheet.write(row, col, 'Last Purchase Price(CHF)', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Stock Value(CHF)', header_format)
            col += 1
            excel_sheet.write(row, col, 'Last Purchase Price(EURO)', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Stock Value(EURO)', header_format)
            col += 1
            procs = self.env['stock.quant'].search([('location_id','=',self.location.id)])
            col = 0
            row += 1
            for pro in procs:
                excel_sheet.write(row, col, a, format)
                a = a + 1
                col += 1
                excel_sheet.write(row, col, pro.product_id.default_code, format)
                col += 1
                excel_sheet.write(row, col,  pro.product_id.name, format)
                col += 1
                excel_sheet.write(row, col,  pro.product_id.item_description, format)
                col += 1
                excel_sheet.write(row, col, pro.product_id.uom_id.name, format)
                col += 1
                quant = pro.product_id.with_context({'location': self.location.id, 'to_date': self.date_from}).qty_available
                excel_sheet.write(row, col, quant, format)
                col += 1
                excel_sheet.write(row, col, pro.available_quantity, format)
                col += 1
                curr_usd = self.env.ref('base.USD')
                print('cccccccccc', curr_usd, curr_usd.rate)
                cost_usd = pro.product_id.standard_price * curr_usd.rate
                value_usd = pro.value * curr_usd.rate
                excel_sheet.write(row, col, cost_usd, format)
                col += 1
                excel_sheet.write(row, col, value_usd, format)
                col += 1
                excel_sheet.write(row, col, pro.product_id.standard_price, format)
                col += 1
                excel_sheet.write(row, col, pro.value, format)
                col += 1
                curr_chf = self.env.ref('base.CHF')
                print('cccccccccc', curr_chf, curr_chf.rate)
                cost_chf = pro.product_id.standard_price * curr_chf.rate
                value_chf = pro.value * curr_chf.rate
                excel_sheet.write(row, col, cost_chf, format)
                col += 1
                excel_sheet.write(row, col, value_chf, format)
                col += 1
                curr_euro = self.env.ref('base.EUR')
                print('cccccccccc', curr_euro, curr_euro.rate)
                cost_euro = pro.product_id.standard_price * curr_euro.rate
                value_euro = pro.value * curr_euro.rate
                excel_sheet.write(row, col, cost_euro, format)
                col += 1
                excel_sheet.write(row, col, value_euro, format)
                col += 1

                col = 0
                row += 1

            workbook.close()
            file_download = base64.b64encode(fp.getvalue())
            fp.close()
            wizardmodel = self.env['warehouse.report.excel']
            res_id = wizardmodel.create({'name': file_name, 'file_download': file_download})
            return {
                'name': 'Files to Download',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'warehouse.report.excel',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': res_id.id,
            }

class Warehouse(models.TransientModel):
    _name = 'warehouse.report.excel'

    name = fields.Char('File Name', size=256, readonly=True)
    file_download = fields.Binary('File to Download', readonly=True)

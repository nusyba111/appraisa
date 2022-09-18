# -*- coding: utf-8 -*-
###########
from dateutil.relativedelta import relativedelta
from openerp import fields, models, api, tools, _
import xlsxwriter
import base64
from io import StringIO, BytesIO
from openerp.exceptions import Warning as UserError
from odoo.tools import *

class HealthReport(models.Model):
    _name = 'health.report'
    _description = 'Print all Warehouse Products'

    location=fields.Many2one('stock.location',string='From Location', required=True ,domain=[('usage','=','internal')])
    date_from=fields.Datetime(string='Date From' , required=True)
    date_to=fields.Datetime(string='Date To', required=True)

    def print_report(self):
        for report in self:
            a = 1
            logo = report.env.user.company_id.logo
            company_id = report.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
            file_name = _('Health Report.xlsx')
            fp = BytesIO()
            workbook = xlsxwriter.Workbook(fp)
            excel_sheet = workbook.add_worksheet('Health Report')
            report_title = 'Health Report For SRCS Inventory '
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
            excel_sheet.write(row, col, 'Date', header_format)
            col += 1
            excel_sheet.set_column(col, col, 25)
            excel_sheet.write(row, col, 'Item', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'No of Units', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Donor', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'The beneficiary', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Car No', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Driver Name', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Policy No', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Approval', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Remarks', header_format)
            col += 1
            self._cr.execute('SELECT move.id, ' \
                             'move.state, '
                             'min(move.state),' \
                             'min(move.date) ' \
                             'FROM stock_move move ' \
                             'where move.location_id =' + str(
                self.location.id)+ ' GROUP BY move.id ' \
                                  'ORDER BY move.id ASC')
            move_ids = self._cr.fetchall()
            move_ids = move_ids and [x[0] for x in move_ids] or []
            for res in self.env['stock.move'].browse(move_ids):
                print('lllllllllllllllllllllllllllllll',res)
                if res.state == 'done' and res.date.strftime("%Y-%m-%d") >= self.date_from.strftime("%Y-%m-%d")\
                        and res.date.strftime("%Y-%m-%d") <= self.date_to.strftime("%Y-%m-%d") and \
                        res.location_dest_id.usage in ('customer','internal') :
                    print('eeeeeeeeeeeeeeeee', res)
                    col = 0
                    row += 1
                    excel_sheet.write(row, col, a, format)
                    a = a + 1
                    col += 1
                    excel_sheet.write(row, col, str(res.date), format)
                    col += 1
                    excel_sheet.write(row, col, res.product_id.name, format)
                    col += 1
                    excel_sheet.write(row, col, res.product_uom_qty, format)
                    col += 1
                    excel_sheet.write(row, col, res.product_id.donor_id.name, format)
                    col += 1
                    excel_sheet.write(row, col, res.picking_id.partner_id.name, format)
                    col += 1
                    excel_sheet.write(row, col, res.picking_id.truck_number, format)
                    col += 1
                    excel_sheet.write(row, col, res.picking_id.driver.name, format)
                    col += 1
                    excel_sheet.write(row, col, res.picking_id.bill_leading, format)
                    col += 1
                    excel_sheet.write(row, col, '', format)
                    col += 1
                    excel_sheet.write(row, col, '', format)
                    col += 1


            workbook.close()
            file_download = base64.b64encode(fp.getvalue())
            fp.close()
            wizardmodel = self.env['health.report.excel']
            res_id = wizardmodel.create({'name': file_name, 'file_download': file_download})
            return {
                'name': 'Files to Download',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'health.report.excel',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': res_id.id,
            }

class Health(models.TransientModel):
    _name = 'health.report.excel'

    name = fields.Char('File Name', size=256, readonly=True)
    file_download = fields.Binary('File to Download', readonly=True)

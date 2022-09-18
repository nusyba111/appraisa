# -*- coding: utf-8 -*-
###########
from dateutil.relativedelta import relativedelta
from openerp import fields, models, api, tools, _
import xlsxwriter
import base64
from io import StringIO, BytesIO
from openerp.exceptions import Warning as UserError
from odoo.tools import *

class ReceivedReport(models.Model):
    _name = 'received.report'
    _description = 'Print all Warehouse Products'

    location=fields.Many2one('stock.location',string='To Location' ,domain=[('usage','=','internal')])
    date_from=fields.Datetime('Date From',required=True)
    date_to=fields.Datetime('Date To',required=True)

    def print_report(self):
        for report in self:
            a = 1
            logo = report.env.user.company_id.logo
            company_id = report.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
            file_name = _('Recieved Report.xlsx')
            fp = BytesIO()
            workbook = xlsxwriter.Workbook(fp)
            excel_sheet = workbook.add_worksheet('Received Report')
            report_title = 'Received Report For SRCS Inventory '
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
            excel_sheet.write(row, col, 'Description', header_format)
            col += 1
            excel_sheet.set_column(col, col, 25)
            excel_sheet.write(row, col, 'No of Units', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Units Type', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Donor', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Vendor', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Destination', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Stock Location', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'GRN', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Date', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Remarks', header_format)
            col += 1
            recieved = self.env['stock.picking'].search([('scheduled_date','>=',self.date_from),('scheduled_date','<=',self.date_to),
                                                      ('location_dest_id','=',self.location.id)])
            print('tttttttttt',recieved)
            for rec in recieved:
                col = 0
                row += 1
                excel_sheet.write(row, col, a, format)
                a = a + 1
                col += 1
                for line in rec.move_ids_without_package:
                    excel_sheet.write(row, col, line.product_id.name, format)
                    col += 1
                    excel_sheet.write(row, col, line.quantity_done, format)
                    col += 1
                    excel_sheet.write(row, col, line.product_id.uom_id.name, format)
                    col += 1
                    excel_sheet.write(row, col, line.product_id.donor_id.name, format)
                    col += 1
                    excel_sheet.write(row, col, line.picking_id.partner_id.name, format)
                    col += 1
                    excel_sheet.write(row, col, self.location.name, format)
                    col += 1
                    excel_sheet.write(row, col, " ", format)
                    col += 1
                    excel_sheet.write(row, col, '', format)
                    col += 1
                    excel_sheet.write(row, col, line.picking_id.date_done, format)
                    col += 1
                    excel_sheet.write(row, col, "", format)
                    col = 1
                    row += 1
                col = 0
                row += 1

            workbook.close()
            file_download = base64.b64encode(fp.getvalue())
            fp.close()
            wizardmodel = self.env['received.report.excel']
            res_id = wizardmodel.create({'name': file_name, 'file_download': file_download})
            return {
                'name': 'Files to Download',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'received.report.excel',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': res_id.id,
            }

class Received(models.TransientModel):
    _name = 'received.report.excel'

    name = fields.Char('File Name', size=256, readonly=True)
    file_download = fields.Binary('File to Download', readonly=True)

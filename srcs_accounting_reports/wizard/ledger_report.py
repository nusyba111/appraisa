# -*- coding: utf-8 -*-
###########
from dateutil.relativedelta import relativedelta
from openerp import fields, models, api, tools, _
import datetime
import xlsxwriter
import base64
from io import StringIO, BytesIO
from dateutil.relativedelta import relativedelta
from openerp.exceptions import Warning as UserError
from odoo.tools import *


class LedgerReport(models.Model):
    _name = 'ledger.report'
    _description = 'ledger'

    from_date = fields.Date('From Date', required=True)
    to_date = fields.Date('To Date', required=True)
    project_id = fields.Many2one('account.analytic.account', string="Project", required=True, domain="[('type','=','project')]")
    account_id = fields.Many2one('account.account', string="Account", required=True)

    def print_report(self):
        for report in self:
            a = 1
            logo = report.env.user.company_id.logo
            company_id = report.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
            file_name = _('Ledger report.xlsx')
            fp = BytesIO()
            workbook = xlsxwriter.Workbook(fp)
            excel_sheet = workbook.add_worksheet('Ledger report')
            report_title = 'South Sudan'
            report_title1 = 'Sudanese Red Crescent Society - PPA#972'
            report_title2 = 'For the period From ' + str(report.from_date) + ' To ' + str(report.to_date)
            project_name = 'For ' + str(report.project_id.name) + ' Project'
            name = 'Opening Balance'

            header_format = workbook.add_format(
                {'bold': True, 'font_color': 'white', 'bg_color': '#ccccff', 'border': 1})
            header_format_sequence = workbook.add_format(
                {'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1})
            header_format.set_align('center')
            header_format.set_align('vertical center')
            header_format.set_text_wrap()
            format = workbook.add_format(
                {'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1, 'font_size': '10'})
            title_format = workbook.add_format(
                {'bold': True, 'font_color': 'red', 'bg_color': 'Light Blue2', 'border': 1})
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
                {'bold': True, 'font_color': 'black', 'bg_color': '#ccccff', 'border': 1, 'font_size': '10'})
            report_title4 = workbook.add_format(
                {'bold': True, 'font_color': 'black', 'bg_color': '#99CCFF', 'border': 1, 'font_size': '12'})
            report_title4.set_align('center')
            col = 0
            row = 1
            excel_sheet.merge_range(row, col, row + 1, col + 14, report_title, report_title4)
            col = 0
            row = 3
            excel_sheet.merge_range(row, col, row + 1, col + 14, report_title1, report_title4)
            col = 0
            row = 5
            excel_sheet.merge_range(row, col, row + 1, col + 14, report_title2, report_title4)
            col = 0
            row = 7
            excel_sheet.merge_range(row, col, row + 1, col + 14, project_name, report_title4)
            col = 0
            row = 9
            excel_sheet.set_column(col, col, 25)
            excel_sheet.write(row, col, 'Number', header_format)
            col += 1
            excel_sheet.set_column(col, col, 25)
            excel_sheet.write(row, col, 'date', header_format)
            col += 1
            excel_sheet.set_column(col, col, 25)
            excel_sheet.write(row, col, 'Location', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Goal', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Site', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Situation', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Budget Code/Out-put', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Account Code ', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Cheque Number', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Payee', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Particulars/Descriptions', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'DR Amount', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'CR Amount', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Balance', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Remarks if any', header_format)
            col += 1

            budget = self.env['account.move.line'].search(
                [('move_id.date', '>=', str(report.from_date)), ('move_id.date', '<=', str(report.to_date)),
                 ('account_id', '=', self.account_id.id),
                 ('analytic_account_id', '=', self.project_id.id)
                 ], order='date asc')
            get_balance = self.env['account.move.line'].search([
                ('date', '<=', self.from_date + relativedelta(days=-1)),
                ('account_id', '=', self.account_id.id),
                ('analytic_account_id', '=', self.project_id.id)
            ])
            counter = 0
            intial_balance = 0
            for line in get_balance:
                print('_______________getbalance', line)
                intial_balance += line.balance
            
            col = 1
            row += 1
            get_balance = self.env['account.move.line'].search([
                ('date', '<=', self.from_date + relativedelta(days=-1)),
                ('account_id', '=', self.account_id.id),
                ('analytic_account_id', '=', self.project_id.id)
            ],limit =1, order="date desc")
            excel_sheet.write(row, col, str(get_balance.date), format)
            col += 9
            
            # excel_sheet.write(row, col, name, format)
            col += 3
            excel_sheet.write(row, col, intial_balance, format)
            row += 1
            col = 0
            sequence = 0
            total_debits = total_credits = total_balance = 0.0
            for rec in budget:
                counter += 1
                sequence += 1
                excel_sheet.write(row, col, str(sequence), format)
                col += 1
                excel_sheet.write(row, col, str(rec.move_id.date), format)
                col += 1
                excel_sheet.write(row, col, rec.location_id.name, format)
                col += 1
                project = rec.analytic_account_id.crossovered_budget_line.crossovered_budget_id
                excel_sheet.write(row, col, project.goal, format)
                col += 1
                excel_sheet.write(row, col, project.site, format)
                col += 1
                excel_sheet.write(row, col, project.situation, format)
                col += 1
                excel_sheet.write(row, col, rec.analytic_account_id.code, format)
                col += 1
                excel_sheet.write(row, col, rec.account_id.code, format)
                col += 1
                excel_sheet.write(row, col, rec.Check_no, format)
                col += 1
                excel_sheet.write(row, col, rec.partner_id.name, format)
                col += 1
                excel_sheet.write(row, col, rec.name, format)
                col += 1
                excel_sheet.write(row, col, rec.debit, format)
                col += 1
                excel_sheet.write(row, col, rec.credit, format)
                col += 1
                if counter == 1:
                    total = intial_balance + rec.credit - rec.debit
                else:
                    total += rec.credit - rec.debit
                excel_sheet.write(row, col, total, format)
                col += 1
                excel_sheet.write(row, col, rec.ref, format)
                col += 1
                col = 0
                row += 1
            counter = 0.0
            workbook.close()
            file_download = base64.b64encode(fp.getvalue())
            fp.close()
            wizardmodel = self.env['ledger.report.excel']
            res_id = wizardmodel.create({'name': file_name, 'file_download': file_download})
            return {
                'name': 'Files to Download',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'ledger.report.excel',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': res_id.id,
            }


class ledger_Report_Excel(models.TransientModel):
    _name = 'ledger.report.excel'
    name = fields.Char('File Name', size=256, readonly=True)
    file_download = fields.Binary('File to Download', readonly=True)

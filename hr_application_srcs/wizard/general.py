# -*- coding: utf-8 -*-
###########
from dateutil.relativedelta import relativedelta
from openerp import fields, models, api, tools, _
import xlsxwriter
import base64
from io import StringIO, BytesIO
from openerp.exceptions import Warning as UserError
from odoo.tools import *

class position(models.Model):
    _name = 'donor.donation.report'
    _description = 'donor.donation.report'

    from_date=fields.Date('From Date', required=True)
    to_date=fields.Date('To Date' , required=True)


    def print_report(self):
        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'start_date': self.from_date, 'expiration_date': self.to_date,
            },
        }
        for report in self:
            from_date = report.from_date
            to_date = report.to_date

            if self.from_date > self.to_date:
                raise UserError(_("You must be enter start date less than end date."))

            # report_title = 'Salaries must Pay by SRCS in Different Currency and number of Emplyees '
            file_name = _('Donor Donation in USD.xlsx')
            a = 1
            # logo = report.env.user.company_id.logo
            # company_id = report.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
            # file_name = _('Preventive Maintainance.xlsx')
            # file_name = _('Job Position.xlsx')
            fp = BytesIO()
            workbook = xlsxwriter.Workbook(fp)
            excel_sheet = workbook.add_worksheet('Donor Donation in USD')
            report_title = 'Donor Donation Report'
            header_format = workbook.add_format(
                {'bold': True, 'font_color': 'black', 'bg_color': '#FFFFFF', 'border': 1})
            bg_format = workbook.add_format(
                {'bold': True, 'font_color': 'black', 'bg_color': '#DE3163', 'border': 1})
            header_format_sequence = workbook.add_format(
                {'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1})
            heading = workbook.add_format(
                {'bold': True, 'font_color': 'black', 'bg_color': 'white', 'border': 1})
            heading.set_align('left')
            header_format.set_align('center')
            header_format.set_align('vertical center')
            header_format.set_text_wrap()
            format = workbook.add_format(
                {'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1, 'font_size': '20'})
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
            col = 3
            row = 3

            excel_sheet.set_column(col, col, 50)
            excel_sheet.write(row, col, 'Donors', header_format)
            col += 1
            excel_sheet.set_column(col, col, 50)
            excel_sheet.write(row, col, 'USD', header_format)
            col += 1

            # sequence_id = 0
            # col = 0
            # excel_sheet.write(row, col, 'Donor Donation in USD', header_format)
            excel_sheet.merge_range('D1:E1', '', bg_format)
            excel_sheet.merge_range('D2:E2', 'Salaries Percentage covered by donors in USD', heading)
            excel_sheet.merge_range('D3:E3', '', bg_format)
            excel_sheet.merge_range('A1:C100', ' ', bg_format)
            excel_sheet.merge_range('F1:Z100', ' ', bg_format)

            # excel_sheet.merge_range('A3:C300', ' ', heading)



            # excel_sheet.write_blank(0, 0, None)
            # excel_sheet.write('A8', 'Some hidden rows.')

            # employee_list =[]
            # employees = self.env['hr.contract'].search([])
            # for rec in employees:
            #     if rec.state == 'open':
            #         employee_list.append({
            #             'name': rec.employee_id,
            #             'job_position': rec.job_id.name,
            #             # 'work_location_id': rec.work_location_id.name,

                        

            #             })

            # employees_contract_ids = self.env['cash.request'].search([])

            # counter = 0
            # row = 6
            # col = 0
            # for rec in employees_contract_ids:
                
            #     counter += 1
                
            #     excel_sheet.write(row, col, str(counter), format)
            #     col += 1 
                # excel_sheet.write(row, col, fleet.registration_start, format)
                # col += 1
                # excel_sheet.write(row, col, fleet.registration_end, format)
                # col += 1
                # excel_sheet.write(row, col, fleet.local_insurance_policy_number, format)
                # col += 1
                # excel_sheet.write(row, col, fleet.insurance_start, format)
                # col += 1
                # excel_sheet.write(row, col, fleet.insurance_end, format)
                # col += 1
                # excel_sheet.write(row, col, fleet.cost_third_party_local, format)
                # col += 1
                # excel_sheet.write(row, col, fleet.registration_plate_type, format)
                # col += 1
                # excel_sheet.write(row, col, fleet.model_id.name, format)
                # col += 1
                # col = 0
                # row += 1

            workbook.close()
            download_file = base64.b64encode(fp.getvalue())
            fp.close()
            wizardmodel = self.env['donor.donation.report.excel']
            res_id = wizardmodel.create({'name': file_name, 'download_file': download_file})
            return {
                'name': 'Files to Download',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'donor.donation.report.excel',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': res_id.id,
            }

class FleetMaintainance_Report_Excel(models.TransientModel):
    _name = 'donor.donation.report.excel'

    name = fields.Char('File Name', size=256, readonly=True)
    download_file = fields.Binary('File to Download', readonly=True)


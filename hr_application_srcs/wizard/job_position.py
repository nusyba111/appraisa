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
    _name = 'position.position.report'
    _description = 'job.position'

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

            report_title = 'Salaries must Pay by SRCS in Different Currency and number of Emplyees '
            file_name = _('Monitoring Report.xlsx')
            a = 1
            # logo = report.env.user.company_id.logo
            # company_id = report.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
            # file_name = _('Preventive Maintainance.xlsx')
            # file_name = _('Job Position.xlsx')
            fp = BytesIO()
            workbook = xlsxwriter.Workbook(fp)
            excel_sheet = workbook.add_worksheet('Monitoring Report')
            report_title = 'Monitoring Report'
            header_format = workbook.add_format(
                {'bold': True, 'font_color': 'black', 'bg_color': '#FFFFFF', 'border': 1})
            bg_format = workbook.add_format(
                {'bold': True, 'font_color': 'black', 'bg_color': '#FF90FF', 'border': 1})
            header_format_sequence = workbook.add_format(
                {'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1})
            heading = workbook.add_format(
                {'bold': False, 'font_color': 'white', 'bg_color': '#000080 ', 'border': 3})
            heading.set_align('left')
            header_format.set_align('center')
            header_format.set_align('vertical center')
            header_format.set_text_wrap()
            format = workbook.add_format(
                {'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1, 'font_size': '5px'})
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
            col = 1
            row = 3

            excel_sheet.set_column(col, col, 10)
            excel_sheet.write(row, col, 'Donors', header_format)
            col += 1
            excel_sheet.set_column(col, col, 10)
            excel_sheet.write(row, col, 'USD', header_format)
            col += 1
            excel_sheet.set_column(col, col, 10)
            excel_sheet.write(row, col, 'SDG', header_format)
            col += 1
            excel_sheet.set_column(col, col, 10)
            excel_sheet.write(row, col, ' ', header_format)
            col += 1
            excel_sheet.set_column(col, col, 10)
            excel_sheet.write(row, col, 'State', header_format)
            col += 1
            excel_sheet.set_column(col, col, 10)
            excel_sheet.write(row, col, 'USD', header_format)
            col += 1
            excel_sheet.set_column(col, col, 10)
            excel_sheet.write(row, col, 'SDG', header_format)
            col += 1
            excel_sheet.set_column(col, col, 10)
            excel_sheet.write(row, col, 'SDG', header_format)
            col += 1
            excel_sheet.set_column(col, col, 10)
            excel_sheet.write(row, col, 'USD', header_format)
            col += 1
            excel_sheet.set_column(col, col, 10)
            excel_sheet.write(row, col, 'Number of Staff', header_format)
            col += 1
            # excel_sheet.set_column(col, col, 20)
            # excel_sheet.write(row, col, 'Donor 2 Percentage', header_format)
            # col += 1
            # 

            # sequence_id = 0
            # col = 0
            excel_sheet.write(row, col, 'Monitoring Report', header_format)
            excel_sheet.merge_range('A1:A1000', ' ', bg_format)
            excel_sheet.merge_range('E1:E1000', ' ', bg_format)
            excel_sheet.merge_range('B1:L1', '', bg_format)
            excel_sheet.merge_range('B2:D2', 'Salaries must Pay by SRCS in Different Currency and number of Emplyees', heading)
            excel_sheet.merge_range('B3:L3', '', bg_format)
            excel_sheet.merge_range('F2:L2', 'Salaries must Pay by SRCS in Different Currency and number of Emplyees', heading)
            excel_sheet.merge_range('M1:Z1000', ' ', bg_format)
            



# employees_contract_ids = self.env['cash.request'].search([])

#             counter = 0
#             row = 6
#             col = 0
#             for rec in employees_contract_ids:
                
#                 counter += 1
                
#                 excel_sheet.write(row, col, str(counter), format)
#                 col += 1 
                # excel_sheet.write(row, col,rec.employee_id.work_location_id.name, format)
                # col += 1
                # excel_sheet.write(row, col, rec.employee_id.name, format)
                # col += 1
                # excel_sheet.write(row, col, rec.employee_id.job_id.name, format)
                # col += 1
                # excel_sheet.write(row, col, str(rec.wage), format)
                # col += 1
                # excel_sheet.write(row, col, rec.employee_id.name, format)
                # col += 1
            
            # counter = 0
            # row += 1
            # col = 1
            # for rec in employees:

                # serv=self.env['fleet.service'].search([('vehicle_id','=',fleet.id)])
                # serv=self.env['fleet.service'].search([('vehicle_id','=',fleet.id),('minimum_odometer','<=',fleet.odometer),('maximum_odometer','>=',fleet.odometer)])
                # excel_sheet.write(row, col, rec.frist_name, format)
                # excel_sheet.write(row, col, a, format)
                # a = a + 1
                # col += 1
                
                # counter += 2
                # sequence += 1
                # excel_sheet.write(row, col, str(sequence), format)
                # col = 1 
                # excel_sheet.write(row, col, str
                #     (rec.employee_id.address_id.name), format)
                # col += 1
                # excel_sheet.write(row, col, rec.gosi_no, format)
                # col += 1
                # excel_sheet.write(row, col, rec.gosi_no, format)
                # col += 1

                # col += 1
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
            wizardmodel = self.env['position.position.job.report.excel']
            res_id = wizardmodel.create({'name': file_name, 'download_file': download_file})
            return {
                'name': 'Files to Download',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'position.position.job.report.excel',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': res_id.id,
            }

class FleetMaintainance_Report_Excel(models.TransientModel):
    _name = 'position.position.job.report.excel'

    name = fields.Char('File Name', size=256, readonly=True)
    download_file = fields.Binary('File to Download', readonly=True)


# -*- coding: utf-8 -*-

from odoo import models, fields, api,tools, _
from odoo.exceptions import ValidationError
import datetime
import xlsxwriter
import base64
import datetime
import pandas as pd


from io import StringIO
from datetime import *
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import os

from odoo.exceptions import Warning as UserError
from dateutil import relativedelta
from io import BytesIO
from odoo.tools import float_round

class maindataReportwizard(models.TransientModel):
    _name = "main.data.report"
    _description ="Main Data Report wizard"


    # user_id = fields.Many2many('res.users',string="User")
    date_from = fields.Date(string="Date From",required=True)
    date_to = fields.Date(string="Date To",required=True)
    # company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.user.company_id)

    def print(self):
        for report in self:
            date_from = report.date_from
            date_to = report.date_to
            # company_id = report.company_id
            # user_id = report.user_id.ids

            if self.date_from > self.date_to:
                raise UserError(_("You must be enter start date less than end date."))

            report_title = 'تقرير من ' + str(date_from) + ' إلي ' + str(date_to)
            file_name = _('Main Data Report.xlsx')
            fp = BytesIO()
            workbook = xlsxwriter.Workbook(fp)
            date_style = workbook.add_format({'text_wrap': True,'border': 1,'num_format': 'dd-mm-yyyy HH-MM:SS'})
            excel_sheet = workbook.add_worksheet('Main Data Report')
            header_format = workbook.add_format(
                {'bold': True, 'font_color': 'black', 'bg_color': '#FFFFFF', 'border': 4})
            header_format_sequence = workbook.add_format(
                {'bold': False, 'font_color': 'black', 'bg_color': 'black', 'border': 1 ,'font_size': '3'})
            format = workbook.add_format({'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1})
            title_format = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': '#cbcbcb'})
            title_format.set_align('center')
            format.set_align('center')
            header_format_sequence.set_align('left')
            header_format.set_align('center')
            header_format.set_text_wrap()
            # excel_sheet.set_row(5, 20)
            # excel_sheet.set_column('F:U', 20, )
            # excel_sheet.left_to_right()
            format.set_text_wrap()
            format.set_num_format('#,##0.00')
            format_details = workbook.add_format()
            format_details.set_num_format('#,##0.00')
            sequence_id = 0
            col = 0

            # employee_list =[]
            # employees = self.env['hr.contract'].search([])
            # for rec in employees:
            #     if rec.state == 'open':
            #         employee_list.append({
            #             'name': rec.employee_id,
            #             'job_position': rec.job_id.name,
                        # 'work_location_id': rec.work_location_id.name,

                        

                        # })
            
            employees = self.env['hr.contract'].search([('date_start', '>=', date_from),('date_start', '<=', date_to)])

            # if employees.employee_id:
            row = 5
            # first_row = 4
            # seq = 0

            excel_sheet.write(row, col, 'SIN', header_format)
            col += 1
            excel_sheet.write(row, col, 'State', header_format)
            col += 1
            excel_sheet.write(row, col, 'Name', header_format)
            col += 1
            excel_sheet.write(row, col, 'Position', header_format)
            col += 1
            excel_sheet.write(row, col, 'Gross Salary', header_format)
            col += 1
            excel_sheet.write(row, col, 'Sate Percentage', header_format)
            col += 1
            # excel_sheet.write(row, col, 'Total Percentage', header_format)
            # col += 1
            
            excel_sheet.write(row, col, 'Currency', header_format)
            col += 1
            excel_sheet.write(row, col, 'Start', header_format)
            col += 1
            excel_sheet.write(row, col, 'End', header_format)
            col += 1
            excel_sheet.write(row, col, 'No Of Month', header_format)
            col += 1
            excel_sheet.write(row, col, 'Cost of Salary', header_format)
            col += 1
            # if seq >=1:
                
            # excel_sheet.write(row, col, 'Covered By SRCS', header_format)
            # col += 1
            # excel_sheet.write(row, col, 'Donor 1 name2', header_format)
            # col += 1
            # excel_sheet.write(row, col, 'Donor 2 name22', header_format)
            # col += 1



            excel_sheet.set_column(0, 4, 25)
            excel_sheet.set_row(1, 25)
            excel_sheet.merge_range(0, 0, 1, 5, 'Main Data Report ', title_format)
            excel_sheet.merge_range(2, 0, 3, 5, report_title, title_format)
            excel_sheet.merge_range(3, 0, 4, 50, '', title_format)
            # excel_sheet = sum( line.percentage_of_covering for usd in rec.salary_plan)
            # excel_sheet.write(2, 1,=sum('B0': 'B2''))
            # excel_sheet.write_formula('AK7', '{=SUM('rec.salary_plan','percentage_of_covering')}')

            counter = 0

            
            row +=1
            col =0
            sequence = 0

            for rec in employees:
                
                counter += 1
                sequence +=1
                
                excel_sheet.write(row, col, str(sequence), format)
                col += 1 
                excel_sheet.write(row, col,rec.employee_id.work_location_id.name, format)
                col += 1
                excel_sheet.write(row, col, rec.employee_id.name, format)
                col += 1
                excel_sheet.write(row, col, rec.employee_id.job_id.name, format)
                col += 1
                excel_sheet.write(row, col, str(rec.wage), format)
                col += 1
                # excel_sheet.write(row, col, rec.employee_id.name, format)
                # col += 1
                excel_sheet.write(row, col, rec.employee_id.name, format)
                col += 1
                # print("*******************",rec.salary_plan)
                # 
                
                # excel_sheet.write(row, col, rec.employee_id.name, format)
                # col += 1
                # excel_sheet.write(row, col, rec.employee_id.name, format)
                # col += 1 
                excel_sheet.write(row, col, rec.forgin_currency_id.name, format)
                col += 1 
                if rec.date_start :
                    excel_sheet.write(row, col, rec.date_start.strftime("%Y-%m-%d"), format)
                    col += 1
                else:
                    excel_sheet.write(row, col, "", format)
                    col+=1
                if rec.date_end:
                    excel_sheet.write(row, col, rec.date_end.strftime("%Y-%m-%d"), format)
                    col += 1
                else:
                    excel_sheet.write(row, col, "", format)
                    col+=1
                if rec.date_end and rec.date_start:
                    date = pd.Timestamp(rec.date_end)
                    month = (rec.date_end.year - rec.date_start.year) * 12 + (rec.date_end.month - rec.date_start.month)
                    if date.is_month_end:
                        month+=1
                if month:
                    excel_sheet.write(row, col, str(month), format)
                    col+=1
                else:
                    excel_sheet.write(row, col, "0", format)
                    col+=1
                cost = month * rec.wage
                excel_sheet.write(row, col, cost, format)
                col += 1
                col = 0
                row +=1
            

            row = 5
            col = 11
            
            y = 0
            
            row1 = 6
            for rec in employees:       
                col1 = 11
                for line in rec.salary_plan :
                    if len(rec.salary_plan) >= y :
                        y = len(rec.salary_plan)

               
                for line in rec.salary_plan :

                    print("***********************",line.location.name)
                    excel_sheet.write(row1, col1, line.location.name, format)
                    col1 += 1
                    print("$$$$$$$$$$$$$$$$$$$$$$$",line.percentage_of_covering)
                    excel_sheet.write(row1, col1, str(line.percentage_of_covering), format)
                    col1 += 1
                    print("#######################",line.doner_id.name)
                    excel_sheet.write(row1, col1, line.doner_id.name, format)
                    col1 += 1
                    excel_sheet.write(row1, col1, line.coverage_in_usd * month, format)
                    col1 += 1
                    print("&&&&&&&&&&&&&&&&&&&&&&&")
                row1 += 1
                   
            
            for x in range(y):
                excel_sheet.write(row, col, 'State', header_format)
                col += 1
                excel_sheet.write(row, col, 'Donor  Percentage', header_format)
                col += 1
                excel_sheet.write(row, col, 'Donor  name', header_format)
                col +=1
                excel_sheet.write(row, col, 'Covered in USD', header_format)
                col +=1
            excel_sheet = sum(line.percentage_of_covering for line in rec.salary_plan)
            col += 1

            # excel_sheet.write_column(0, 0, rec.salary_plan)
            # chart = workbook.add_chart({'type': 'column'})
            # chart.add_series({'values': '=Sheet1!$A$1:$A$7'})
            # worksheet.insert_chart('C1', chart)


            # d = 0
                
            # row2 = 6
            # for rec in employees:
            #     col2 = y+1
            #     for donor in rec.salary_plan :
            #         if len(rec.salary_plan) >= d :
            #             d = len(rec.salary_plan)

               
            #     for donor in rec.salary_plan :

            #         print("***********************",donor.coverage_in_usd)
            #         excel_sheet.write(row2, col2, donor.location.name, format)
            #         col2 += 1
            #         print("$$$$$$$$$$$$$$$$$$$$$$$",donor.percentage_of_covering)
            #         excel_sheet.write(row2, col2, str(donor.percentage_of_covering), format)
            #         col2 += 1
            #         print("#######################",donor.doner_id.name)
            #         excel_sheet.write(row2, col2, donor.doner_id.name, format)
            #         col2 += 1
            #         print("&&&&&&&&&&&&&&&&&&&&&&&")
            #     row1 += 1
                   
            
            # for z in range(d):
            #     excel_sheet.write(row, col, 'covered by SRCS', header_format)
            #     col += 1
            #     excel_sheet.write(row, col, 'covered by', header_format)
            #     col += 1
            #     excel_sheet.write(row, col, 'Donor  name', header_format)
            #     col +=1





            workbook.close()
            file_download = base64.b64encode(fp.getvalue())
            fp.close()
            wizardmodel = self.env['data.report.wiz.excel']
            res_id = wizardmodel.create({'name': file_name, 'file_download': file_download})
            return {
                'name': 'Files to Download',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'data.report.wiz.excel',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': res_id.id,
            }


class PurchaseReportWizexel(models.TransientModel):
    _name = 'data.report.wiz.excel'

    name = fields.Char('File Name', size=256, readonly=True)
    file_download = fields.Binary('File to Download', readonly=True)
# -*- coding: utf-8 -*-
###############################################################################
#
#    IATL-Intellisoft International Pvt. Ltd.
#    Copyright (C) 2021 Tech-Receptives(<http://www.iatl-intellisoft.com>).
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import xlsxwriter
import base64
import datetime

from io import StringIO
from datetime import *
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import os

from odoo.exceptions import Warning as UserError
from dateutil import relativedelta
from io import BytesIO

class HolidayPlanningReport(models.Model):
    _name = "leave.planning.report"

    state = fields.Selection([('approved','Approved'),('not','Not Approved')],required=True,string="Status")


    
    def print_report(self):
        for report in self:
            logo = report.env.user.company_id.logo
            
            
            company_id = report.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
            address1 = company_id.street
            address2 = company_id.street2
            country = company_id.country_id.name
            phone = company_id.phone
            website = company_id.website
            
            file_name = None
            fp = BytesIO()
            workbook = xlsxwriter.Workbook(fp)
            excel_sheet = workbook.add_worksheet('Secretary General Office')
            image_data = BytesIO(base64.b64decode(logo))  
            # excel_sheet.insert_image('A1', 'logo.png', {'image_data': image_data})
            
            header_format = workbook.add_format(
                {'bold': True, 'font_color': 'black', 'bg_color': '#a4f3dd', 'border': 1})
            header_format_sequence = workbook.add_format(
                {'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1})
            format = workbook.add_format({'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1})
            title_format = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': 'white'})
            header_format.set_align('center')
            header_format.set_align('vertical center')
            header_format.set_text_wrap()
            format = workbook.add_format(
                {'bold': True, 'font_color': 'black', 'bg_color': 'white', 'border': 0, 'font_size': '10'})
            format1 = workbook.add_format(
                {'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1, 'font_size': '10'})
            title_format = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': '#f4e350', 'border': 1})
            title_format.set_align('center')
            format.set_align('center')
            format1.set_align('center')
            header_format_sequence.set_align('center')
            format.set_text_wrap()
            format1.set_text_wrap()
            format.set_num_format('#,##0.000')
            format1.set_num_format('#,##0.000')
            date_format = workbook.add_format({'num_format': 'dd/mm/yy','border': 0, 'font_size': '10'})
            date_format.set_align('center')
            date_time_format = workbook.add_format({'num_format': 'dd/mm/yy :H:M:S','border': 0, 'font_size': '10'})
            date_time_format.set_align('center')

            format_details = workbook.add_format()
            sequence_format = workbook.add_format(
                {'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1})
            sequence_format.set_align('center')
            sequence_format.set_text_wrap()
            total_format = workbook.add_format(
                {'bold': True, 'font_color': 'black', 'bg_color': '#e18ce0', 'border': 1, 'font_size': '10'})
            total_format2 = workbook.add_format(
                {'bold': True, 'font_color': 'black', 'bg_color': '#aacbf1', 'border': 1, 'font_size': '10'}) 
            total_format.set_align('center')
            total_format.set_text_wrap()
            total_format2.set_align('center')
            total_format2.set_text_wrap()
            format_details.set_num_format('#,##0.00')
            sequence_id = 0
            col = 0
            row = 3
            first_row = 9
            # total1 = 0.0
            # total_owner = 0.0
            # count = 0.0
            # tot = 0.0
            # own = 0.0
            # con = 0
            top_row = 3
            bottom_row = 2
            left_column = 2
            right_column = 3

            report_title = 'Secretary General Office'
            file_name = _('Secretary General Office.xlsx')
            
            excel_sheet.merge_range(0, 1, 1, 51, report_title, title_format)
            excel_sheet.merge_range(2, 1, 3, 1,'الإسم', header_format)
            excel_sheet.merge_range(2, 2, 3, 2,'المستحق', header_format)
            excel_sheet.merge_range(2, 3, 3, 3,'الرصيد الحالي', header_format)
            excel_sheet.merge_range(2, 4, 2, 7,'ياناير', header_format)
            excel_sheet.write(3, 4,'1', header_format)
            excel_sheet.write(3, 5,'2', header_format)
            excel_sheet.write(3, 6,'3', header_format)
            excel_sheet.write(3, 7,'4', header_format)
            excel_sheet.merge_range(2, 8, 2, 11,'فبراير', header_format)
            excel_sheet.write(3, 8,'1', header_format)
            excel_sheet.write(3, 9,'2', header_format)
            excel_sheet.write(3, 10,'3', header_format)
            excel_sheet.write(3, 11,'4', header_format)
            excel_sheet.merge_range(2, 12, 2, 15,'مارس', header_format)
            excel_sheet.write(3, 12,'1', header_format)
            excel_sheet.write(3, 13,'2', header_format)
            excel_sheet.write(3, 14,'3', header_format)
            excel_sheet.write(3, 15,'4', header_format)
            excel_sheet.merge_range(2, 16, 2, 19,'أبريل', header_format)
            excel_sheet.write(3, 16,'1', header_format)
            excel_sheet.write(3, 17,'2', header_format)
            excel_sheet.write(3, 18,'3', header_format)
            excel_sheet.write(3, 19,'4', header_format)
            excel_sheet.merge_range(2, 20, 2, 23,'مايو', header_format)
            excel_sheet.write(3, 20,'1', header_format)
            excel_sheet.write(3, 21,'2', header_format)
            excel_sheet.write(3, 22,'3', header_format)
            excel_sheet.write(3, 23,'4', header_format)
            excel_sheet.merge_range(2, 24, 2, 27,'يونيو', header_format)
            excel_sheet.write(3, 24,'1', header_format)
            excel_sheet.write(3, 25,'2', header_format)
            excel_sheet.write(3, 26,'3', header_format)
            excel_sheet.write(3, 27,'4', header_format)
            excel_sheet.merge_range(2, 28, 2, 31,'يوليو', header_format)
            excel_sheet.write(3, 28,'1', header_format)
            excel_sheet.write(3, 29,'2', header_format)
            excel_sheet.write(3, 30,'3', header_format)
            excel_sheet.write(3, 31,'4', header_format)
            excel_sheet.merge_range(2, 32, 2, 35,'أغسطس', header_format)
            excel_sheet.write(3, 32,'1', header_format)
            excel_sheet.write(3, 33,'2', header_format)
            excel_sheet.write(3, 34,'3', header_format)
            excel_sheet.write(3, 35,'4', header_format)
            excel_sheet.merge_range(2, 36, 2, 39,'سبتمبر', header_format)
            excel_sheet.write(3, 36,'1', header_format)
            excel_sheet.write(3, 37,'2', header_format)
            excel_sheet.write(3, 38,'3', header_format)
            excel_sheet.write(3, 39,'4', header_format)
            excel_sheet.merge_range(2, 40, 2, 43,'أكتوبر', header_format)
            excel_sheet.write(3, 40,'1', header_format)
            excel_sheet.write(3, 41,'2', header_format)
            excel_sheet.write(3, 42,'3', header_format)
            excel_sheet.write(3, 43,'4', header_format)
            excel_sheet.merge_range(2, 44, 2, 47,'نوفمبر', header_format)
            excel_sheet.write(3, 44,'1', header_format)
            excel_sheet.write(3, 45,'2', header_format)
            excel_sheet.write(3, 46,'3', header_format)
            excel_sheet.write(3, 47,'4', header_format)
            excel_sheet.merge_range(2, 48, 2, 51,'ديسمبر', header_format)
            excel_sheet.write(3, 48,'1', header_format)
            excel_sheet.write(3, 49,'2', header_format)
            excel_sheet.write(3, 50,'3', header_format)
            excel_sheet.write(3, 51,'4', header_format)
            excel_sheet.set_column(1,1, 20)
            # excel_sheet.merge_range(top_row, bottom_row, left_column + 2 , right_column+2, 'المستحق', header_format)
            # excel_sheet.write(row, col+3, 'الررصيد الحالي', header_format)
            planns = self.env['hr.leave.planning'].search([])
            current = 0.0
            acutal_current = 0.0
            acutal = 0.0
            for plan in planns:
                for line in plan.leaves:
                    if line.state == 'validate':
                        acutal_current += line.number_of_days
                current_allocation = self.env['hr.leave.allocation'].search([('employee_id','=',plan.employee_id.id),
                    ('date_from','<=',plan.date_from),('date_to','>=',plan.date_to),
                    ('holiday_status_id','=',plan.leave_type.id),('state','=','validate')])
                for allocation in current_allocation:
                    if allocation:
                        current += allocation.number_of_days_display 
                acutal = current - acutal_current        
                row += 1
                excel_sheet.write(row,col+1,plan.employee_id.name,format1)
                excel_sheet.write(row,col+2,current,format1)
                excel_sheet.write(row,col+3,acutal,format1)


            


            # excel_sheet.write(row, col+4, 'No Of Transaction', header_format)
            # excel_sheet.write(row, col+5, 'Total Of Amount', header_format)
            # excel_sheet.write(row, col+6, 'Total Fees', header_format)
            # excel_sheet.write(row, col+7, 'Agent Commision 20%', header_format)
            # excel_sheet.write(row, col+8, 'E-connect Net Commision', header_format)
      
            # excel_sheet.set_column(col+1, col+4, 20)
            # excel_sheet.set_column(col+2, col+4, 20)
            # excel_sheet.set_column(col+3, col+4, 20)
            # excel_sheet.set_column(col+4, col+4, 20)
            # excel_sheet.set_column(col+5, col+5, 20)
            # excel_sheet.set_column(col+7, col+7, 20)
            # excel_sheet.set_column(col+8, col+8, 20)
            

            # objects = self.env['agent.fees'].search([])
            # for name in objects:
            #       row+=1
            #       excel_sheet.write(row,col+1,name.agent_name,format1)
            #       excel_sheet.write(row,col+2,name.location,format1)
            #       excel_sheet.write(row,col+3,name.terminal_id,format1)
            #       excel_sheet.write(row,col+4,name.number_of_transaction,format1)
            #       excel_sheet.write(row,col+5,name.total_of_amount,format1)
            #       excel_sheet.write(row,col+6,name.total_fees,format1)
            #       excel_sheet.write(row,col+7,name.agent_commision,format1)
            #       excel_sheet.write(row,col+8,name.connect_net_commision,format1)

                        

                                                    

            workbook.close()
            file_download = base64.b64encode(fp.getvalue())
            fp.close()
            wizardmodel = self.env['leave.planning.report.excel']
            res_id = wizardmodel.create({'name': file_name, 'file_download': file_download})
            return {
                'name': 'Files to Download',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'leave.planning.report.excel',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': res_id.id,
            }


class LeavePlanningReportExcel(models.TransientModel):
    _name = 'leave.planning.report.excel'

    name = fields.Char('File Name', size=256, readonly=True)
    file_download = fields.Binary('File to Download', readonly=True)
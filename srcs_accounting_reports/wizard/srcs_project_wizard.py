from odoo import api, fields, models, _
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta


class SRCSProjectReport(models.TransientModel):
    _name = "project.report.wizard"

    branch_id = fields.Many2one('res.branch', string='Branch')
    date_from = fields.Date('Date From', required=True)
    date_to= fields.Date('Date To', required=True)
    project_id = fields.Many2one('account.analytic.account',string='Project', required=True, domain="[('type','=','project')]")
    bank_id = fields.Many2one('account.journal',domain="[('type','=','bank')]", string="Bank")
    cash_id = fields.Many2one('account.journal',domain="[('type','=','cash')]", string="Cash")
    
    def print_excel_project(self):
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'project_id': self.project_id.id,
            'bank_id':  self.bank_id.id,
            'cash_id': self.cash_id.id,
            'branch_id': self.branch_id.id,
        }
        return self.env.ref('srcs_accounting_reports.action_report_project').report_action(self, data=data)
  

class ProjectXlsx(models.AbstractModel):
    _name = 'report.srcs_accounting_reports.project_report_excel_template'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):

        # passing data from wizard
        date_from = data['date_from']
        date_to = data['date_to']
        project = data['project_id']
        print('kgkgkhkhkhkhkhkhk',project)
        bank = data['bank_id']
        cash = data['cash_id']
        branch = data['branch_id']
        #project period from budget info
        budget = self.env['crossovered.budget'].search([('project_id','=',project)])
        # excel sheet format
        sheet = workbook.add_worksheet('Expenditure Report')
        bold = workbook.add_format({'bold': True})
        branch_format = workbook.add_format({'font_size': '13','bold': True ,'bg_color':'yellow'})
        title_format = workbook.add_format({'font_size': '18','bold': True ,'bg_color':'yellow'})
        border = workbook.add_format({ 'border': 1})
        bold_border = workbook.add_format({ 'border': 1,'bold': True ,'font_size': '11'})
        cash_header_format = workbook.add_format({'bg_color':'#D9D9D9','border': 1,'font_size': '15','bold': True })
        cash_format = workbook.add_format({'bg_color':'#D9D9D9','border': 1,'bold': True,'font_size': '11'})
        format = workbook.add_format({'bg_color':'#D9D9D9'})
        format_format = workbook.add_format({'bg_color':'yellow','border': 1,'font_size': '15','bold': True })
        bank_format = workbook.add_format({'bg_color':'yellow','border': 1,'bold': True})
        details_format = workbook.add_format({'bg_color':'yellow','border': 1})
        signature_format = workbook.add_format({'font_size': '13','bold': True })
        title_format.set_align('center')
        bold_border.set_align('center')
        format.set_align('center')
        format_format.set_align('center')
        bank_format.set_align('center')
        cash_format.set_align('center')
        cash_header_format.set_align('center')
        sheet.merge_range(0,0,1,1,'Sudanese Red Crescent Society', title_format)
        sheet.merge_range(1,0,2,1,' ', title_format)
        branch = 'Branch Name:' + ' ' + str(partners.branch_id.name) 
        sheet.merge_range(3,0,4,1,branch,branch_format)
        name = 'Project Name:' +' ' + ' '+ str(partners.project_id.name)
        sheet.merge_range(5,0,6,1,name,branch_format)
        #######################
        project_sart_date = budget.date_from
        project_end_date =budget.date_to
        project_period = 'Project Duration:' + ' ' +' ' + 'From:' + ' ' +' ' + str(project_sart_date) +' '+ ' ' +'TO:' + ' '+' ' + str(project_end_date)
        sheet.merge_range(7,0,8,1,project_period, branch_format)
        date_1 = partners.date_from.strftime("%d/%m/%Y")
        date_2 = partners.date_to.strftime("%d/%m/%Y")
        period = 'Report Period:' + ' ' + ' ' + 'From' + ' '+' ' + str(date_1) + ' ' + ' ' +'To' + ' ' + ' ' +str(date_2)
        sheet.merge_range(9,0,10,1,period, branch_format)
        sheet.set_column(1,1,60)
        sheet.set_column('A:A',25)
        sheet.set_column('E:F',25)
        sheet.set_column('D:D',60)
        sheet.set_column('H:O',25)
        sheet.write(13,0,'Entry Date',bold_border)
        sheet.write(14,0,'DD-MM-YY',format)
        sheet.write(13,1,'Entry',bold_border)
        sheet.write(14,1,'NO',format)
        sheet.write(13,2,'Check',bold_border)
        sheet.write(14,2,'Payee',format)
        sheet.write(13,3,'Description',bold_border)
        sheet.write(14,3,' ',format)
        sheet.write(13,4,'Account',bold_border)
        sheet.write(14,4,'code',format)
        sheet.write(13,5,'Project ',bold_border)
        sheet.write(14,5,'code',format)
        sheet.write(13,6,'Activity ',bold_border)
        sheet.write(14,6,'code',format)
        sheet.write(13,7,'Donor ',bold_border)
        sheet.write(14,7,'code',format)
        sheet.write(13,8,'Location ',bold_border)
        sheet.write(14,8,'code',format)
        sheet.write(13,9,'Credit ',bank_format)
        sheet.write(14,9,'Income',bank_format)
        sheet.merge_range('J12:L13','SDG Bank Account No',format_format)
        # sheet.write(10,)
        sheet.write(13,10,'Debit',bank_format)
        sheet.write(14,10,'Expenditure',bank_format)
        sheet.write(13,11,'Balance',bank_format)
        sheet.write(14,11,' ',bank_format)
        sheet.merge_range('M12:O13','SDG-Petty Cash Acount',cash_header_format)
        # sheet.write(10,)
        sheet.write(13,12,'Credit ',cash_format)
        sheet.write(14,12,'Income',cash_format)
        sheet.write(13,13,'Debit',cash_format)
        sheet.write(14,13,'Expenditure',cash_format)
        sheet.write(13,14,'Balance',cash_format)
        sheet.write(14,14,' ',cash_format)
        row = 15
        col = 0
        move_line_d = self.env['account.move.line'].search([('account_id.user_type_id.internal_group','=','expense'),('analytic_account_id','=',project),
                                                        ('move_id.date','>=',date_from),('move_id.date','<=',date_to)
                                                        ])
        print('____________move_line_d\n\n\n\n\n',move_line_d)
        bank_data = move_line_d.filtered(lambda move: move.move_id.journal_id.id == bank or move.move_id.journal_id.id == cash)
        print('____________bank_data\n\n\n\n\n',bank_data)
        # get_balance = self.env['account.move.line'].search([
        #         ('move_id.date', '<=', date_from + relativedelta(days=-1)),
        #         ('account_id', '=', bank or cash),
        #         ('analytic_account_id', '=', project)
        #     ])
        # print('___________________date',date_from + relativedelta(days=-1))
        # print('____________beforeget_balance\n\n\n\n\n',get_balance)
        # counter = 0
        # intial_balance = 0
        # for line in get_balance:
        #     print('_______________getbalance', line)
        #     intial_balance += line.balance

        payment = []
        for line in bank_data:
            date1 = line.date.strftime("%d/%m/%y")
            print('\n\n\n\n\n\n\n\n\n line', line)
            sheet.write(row,col,date1,border)
            sheet.write(row,col+1,line.move_id.name,border)
            sheet.write(row,col+3,line.name,border)
            if line.account_id:
                sheet.write(row,col+4,line.account_id.code,border)
            else:
                sheet.write(row,col+4,' ',border)
            if line.analytic_account_id:
                sheet.write(row,col+5,line.analytic_account_id.code,border)
            else:
                sheet.write(row,col+5,' ',border)
            if line.activity_id:
                sheet.write(row,col+6,line.activity_id.code,border)
            else:
                sheet.write(row,col+6,' ',border)
            if line.partner_id:
                sheet.write(row,col+7,line.partner_id.name,border)
            else:
                sheet.write(row,col+7,' ',border)
            if line.location_id:
                sheet.write(row,col+8,line.location_id.code,border)
            else:
                sheet.write(row,col+8,' ',border)
             
            if line.move_id.move_type == 'entry':
                if line.move_id.journal_id.type == 'bank':
                    for rec in line.move_id.line_ids:
                        if rec.account_id.id == line.move_id.journal_id.default_account_id.id:
                            if rec.credit > 0:
                                sheet.write(row,col+9,rec.credit,details_format)
                                sheet.write(row,col+10,0,details_format)
                            if rec.debit > 0:
                                sheet.write(row,col+10,rec.debit,details_format)
                                sheet.write(row,col+9,0,details_format)
                        else:
                            sheet.write(row,col+9,0,details_format)
                            sheet.write(row,col+10,0,details_format)
                    # sheet.write(row,col+11,line.balance,details_format)
                else:
                    sheet.write(row,col+9,0,details_format)
                    sheet.write(row,col+10,0,details_format)
                if line.move_id.journal_id.type == 'cash':
                    for rec in line.move_id.line_ids:
                        if rec.account_id.id == line.move_id.journal_id.default_account_id.id:
                            if rec.credit > 0 :
                                sheet.write(row,col+12,rec.credit,border)
                                sheet.write(row,col+13,0,border)
                            if rec.debit > 0 :
                                sheet.write(row,col+13,rec.debit,border)
                                sheet.write(row,col+12,0,border)
                        else:
                            sheet.write(row,col+12,0,border)
                            sheet.write(row,col+13,0,border)
                    # sheet.write(row,col+14,line.balance,border)
                else:
                    sheet.write(row,col+12,0,border)
                    sheet.write(row,col+13,0,border)
                # payment.append(line.move_id.name)

                print('_________________________________________________entry\n\n\n\n\n\n',line.move_id.journal_id.type,'\n\n\n\n\n',line.move_id.name)

            elif line.move_id.move_type == 'in_invoice':
                
                # print('_________________________________________________\n\n\n\n\n\n',line.move_id.name)
                payment = self.env['account.payment'].search([('ref','=',line.move_id.name)])
                for pay in payment:
                    if pay.name == pay.move_id.name:
                        if line.move_id.journal_id.type == 'bank':
                            for rec in line.move_id.line_ids:
                                if rec.account_id.id == line.move_id.journal_id.default_account_id.id:
                                    if rec.credit > 0:
                                        sheet.write(row,col+9,rec.credit,details_format)
                                        sheet.write(row,col+10,0,details_format)
                                    if rec.debit > 0:
                                        sheet.write(row,col+10,rec.debit,details_format)
                                        sheet.write(row,col+9,0,details_format)
                                else:
                                    sheet.write(row,col+9,0,details_format)
                                    sheet.write(row,col+10,0,details_format)
                            # sheet.write(row,col+11,line.balance,details_format)
                        if line.move_id.journal_id.type == 'cash':
                            for rec in line.move_id.line_ids:
                                if rec.account_id.id == line.move_id.journal_id.default_account_id.id:
                                    if rec.credit > 0 :
                                        sheet.write(row,col+12,rec.credit,border)
                                        sheet.write(row,col+13,0,border)
                                    if rec.debit > 0 :
                                        sheet.write(row,col+13,rec.debit,border)
                                        sheet.write(row,col+12,0,border)
                                else:
                                    sheet.write(row,col+9,0,border)
                                    sheet.write(row,col+10,0,border)
                    
                    print('_________________________________________________\n\n\n\n\n\n',payment)
            row += 1
       
        sheet.write(row+3,col+3,'Project Coordinator',signature_format)
        sheet.write(row+5,col+3,'Signature',signature_format)
        sheet.write(row+7,col+3,'Date',signature_format)
        sheet.write(row+3,col+5,'Finance Director',signature_format)
        sheet.write(row+5,col+5,'Signature',signature_format)
        sheet.write(row+7,col+5,'Date',signature_format)
        sheet.write(row+3,col+7,'Project Accountant',signature_format)
        sheet.write(row+5,col+7,'Signature',signature_format)
        sheet.write(row+7,col+7,'Date',signature_format)

            
from odoo import api, fields, models, _
from datetime import datetime, timedelta, date

class SrcsBudgetReportWizard(models.TransientModel):
    _name = "budget.report.wizard"

    branch_id = fields.Many2one('res.branch', string='Branch')
    date_from = fields.Date('Date From', required=True)
    date_to= fields.Date('Date To', required=True)
    project_id = fields.Many2one('account.analytic.account',string='Project', required=True, domain="[('type','=','project')]")

    def print_excel_project(self):
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'project_id': self.project_id.id,
            'branch_id': self.branch_id.id,
        }
        return self.env.ref('srcs_accounting_reports.action_budget_report').report_action(self, data=data)


class BudgetXlsx(models.AbstractModel):
    _name = 'report.srcs_accounting_reports.budget_report_excel_template'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):

        start_date = data['date_from']
        end_date = data['date_to']
        project = data['project_id']
        # excel sheet format
        sheet = workbook.add_worksheet('Budget Report')
        bold = workbook.add_format({'bold': True})
        Header_format = workbook.add_format({'font_size': '20','bold': True , 'font_color': 'white', 'bg_color':'Light Teal 4'})
        Header_format.set_align('center')
        body_format = workbook.add_format({'font_size': '13','bold': True })
        # body_format.set_align('center')
        sheet.merge_range(0,0,1,5,'Sudanese Red Crescent Society', Header_format)
        sheet.merge_range(4,3,5,11,partners.project_id.name, Header_format)
        sheet.merge_range(0,0,1,9,'Sudanese Red Crescent Society', Header_format)
        output_activity = self.env['account.analytic.account'].search([('project_id','=',project)])
        if output_activity:
            for rec in output_activity:
                activity_ids = self.env['account.analytic.group'].search([('project_id','=',project),('id','=',output_activity.id)])

        print('______________________________________herracy',activity_ids)
        row = 10
        col = 0
        # if activity_ids:
        #     for herarcy_activity in activity_ids:
        #         # zzz = len(herarcy_activity.parent_id.parent_id.name)
        #         # y = sheet.set_column(row,col+3,zzz)
        #         sheet.write(row,col+3,herarcy_activity.name,body_format)
        #         print('_________________________________parnet',herarcy_activity.parent_id.parent_id)
        #         activity_child_ids = self.env['account.analytic.group'].search([('project_id','=',project),('parent_id','in',herarcy_activity.id)])
        #         if activity_child_ids:
        #             for rec in activity_child_ids:  
        #                 sheet.write(row+1,col+3,rec.name,body_format)
        #                 print('_________________________________herracyparnet',rec)
        #                 output_activity = self.env['account.analytic.account'].search([('project_id','=',project),('group_id','=',rec.id)])

        #                 if output_activity:
        #                     for active in output_activity:
        #                         sheet.write(row+3,col,active.name)
        #                         row = 13
        #                         row += 1
        #                         print('-----------------------------output_activity\n\n\n\n',output_activity)
        
        #     sheet.write(row+7,col,'       ',body_format)
        #     row += 1  
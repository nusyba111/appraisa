# -*- coding: utf-8 -*-
import calendar

from dateutil.relativedelta import relativedelta
from odoo import api, models, fields, _
# import calendar
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class TicketReportWiz(models.TransientModel):
    _name = 'hd.ticket.wiz'

    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    team_name = fields.Char(string='Team Name')

# -*- coding: utf-8 -*-
from odoo import fields, models, api,_
from random import randint

class HdTeam(models.Model):
    _name = 'hd.team'
    _description = 'Help desk team'
    _rec_name = 'team_name'

    team_name = fields.Char(string='Team Name')


class HdTags(models.Model):
    _name = 'hd.tags'
    _description = 'Help desk tags'
    _rec_name = 'tag_name'


    def _get_default_color(self):
             return randint(1, 11)

    tag_name = fields.Char(string='Tags')
    color = fields.Integer('Color', default=_get_default_color)

# def _get_default_color(self):
#         return randint(1, 11)
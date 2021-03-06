# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class TbdResPartner(models.Model):
    """Adds last name and first name; name becomes a stored function field."""

    _inherit = "res.partner"

    select_sector = [
        ('public', 'Public'),
        ('private', 'Privée')
    ]
    mymob_sector = fields.Selection(select_sector, string='Res Users sector')
    mymob_contract = fields.Many2many('contract.contract', string='market')

    select_partner_company_type = [
        ('society', 'Societé (Client)'),
        ('school', 'Etablissement scolaire')
    ]
    select_partner_individual_type = [
        ('customer', 'Client'),
        ('student', 'Eleve'),
        ('tutor', 'Tuteur')
    ]
    select_partner_type = select_partner_company_type + select_partner_individual_type
    mymob_partner_type = fields.Selection(select_partner_type, string='Res Users type')

    # TODO Remplir
    select_student_condition = [
        ('WIP', '[WIP] Student')
    ]
    mymob_student_condition = fields.Selection(select_student_condition, string='Condition')

    # TODO Remplir
    select_school_type = [
        ('WIP', '[WIP] School')
    ]
    mymob_school_type = fields.Selection(select_school_type, string='School type')

    select_vacancy_area = [
        ('a', 'Zone A'),
        ('b', 'Zone B'),
        ('c', 'Zone C')
    ]
    mymob_vacancy_area = fields.Selection(select_vacancy_area, string='Zone de vacance')
    # TODO a definir
    mymob_school_holidays = fields.Char(default="[WIP]")

    mymob_school = fields.Many2one('res.partner', string='Related School', index=True,
                                   domain=[('mymob_partner_type', '=', 'school')])

    mymob_lots = fields.Many2one('project.project', string='Lots')

    # @api.onchange(mymob_partner_type)
    # def on_change_mymob_partner_type(self):
    #     """ """
    #     if self.mymob_partner_type in self.select_partner_company_type:
    #         self.is_company = True
    #         self.company_type = 'company'
    #     else:
    #         self.is_company = False
    #         self.company_type = 'person'


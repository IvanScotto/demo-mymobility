# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class TbdResPartner(models.Model):
    """

    """

    _inherit = "res.partner"

    select_sector = [
        ('public', 'Public'),
        ('private', 'Private')
    ]
    mymob_sector = fields.Selection(select_sector, string='Res Users sector')
    mymob_contract = fields.Many2many('contract.contract', string='Market')

    select_partner_company_type = [
        ('society', 'Society (Client)'),
        ('school', 'Educational establishment')
    ]
    select_partner_individual_type = [
        ('customer', 'Client'),
        ('student', 'Student'),
        ('tutor', 'Tutor')
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
    mymob_vacancy_area = fields.Selection(select_vacancy_area, string='Vacancy area')
    # TODO a definir
    mymob_school_holidays = fields.Char(default="[WIP]")
    mymob_school = fields.Many2one('res.partner', string='Related School', index=True,
                                   domain=[('mymob_partner_type', '=', 'school')])
    mymob_lots = fields.Many2one('project.project', string='Lots')
    mymob_street3 = fields.Char()
    mymob_street4 = fields.Char()
    mymob_GESCAR_reference = fields.Char()
    mymob_siren = fields.Char(string='SIREN', size=9, domain=[('mymob_partner_type', '=', 'society')])
    mymob_siret = fields.Char(string='SIRET', size=14, domain=[('mymob_partner_type', '=', 'society')])
    mymob_uai_code = fields.Char(string='Code UAI', size=50)
    mymob_birthday_date = fields.Date(string='Birthday date',domain=[('mymob_partner_type', '=', 'student')])

    select_gender_type = [
            ('Mr', 'Mister'),
            ('Ms', 'Miss')
        ]
    mymob_gender_type = fields.Selection(select_gender_type, string='Gender type',domain=[('mymob_partner_type', '=', 'student')])
    mymob_stop_duration = fields.Integer(string='Durée de l\'arrêt',domain=[('mymob_partner_type', '=', 'student')])
    #default values for res.partner
    @api.model
    def default_get(self, fields):
        result = super(TbdResPartner, self).default_get(fields)
        mymob_partner_type_context = self._context.get('mymob_partner_type')
        company_type_context = self._context.get('company_type')

        if 'mymob_partner_type' in fields and mymob_partner_type_context:
            result['mymob_partner_type'] = mymob_partner_type_context

        if 'company_type' in fields and company_type_context:
            result['company_type'] = company_type_context

        lot_id_context = self._context.get('lot_id')
        if 'lot_id' in fields and lot_id_context:
            result['lot_id'] = lot_id_context

        return result

    def action_show_markets(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Market'),
            'view_mode': 'tree,form',
            'res_model': 'contract.contract',
            'context': "{'create': True}"
        }

# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class TbdHrEmployee(models.Model):
    _inherit = "hr.employee"

    mymob_number_securite_social = fields.Char("N° de Securite sociale", size=15)

    mymob_phone = fields.Char(string="Telehpone2")
    mymob_mobile = fields.Char(string="Mobile2")
    mymob_email = fields.Char(string="Courriel2")
    mymob_activity_TPMR = fields.Boolean('Activité de TPMR', default=False)
    mymob_number_driver_license = fields.Char(string='Numero de permis de conduire')
    mymob_date_obtain_driver_license = fields.Date()
    mymob_matricule = fields.Char(string='Matricule')
    mymob_start_point_address = fields.Many2one('res.partner', string='Start point')


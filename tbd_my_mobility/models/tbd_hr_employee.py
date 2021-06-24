# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class TbdHrEmployee(models.Model):
    _inherit = "hr.employee"

    mymob_number_securite_social = fields.Char("Social Security number", size=15)

    mymob_phone = fields.Char(string="Phone2")
    mymob_mobile = fields.Char(string="Mobile2")
    mymob_email = fields.Char(string="Email2")

    mymob_activity_TPMR = fields.Boolean('TPMR activity', default=False)
    mymob_number_driver_license = fields.Char(string='Driver\'s license number')
    mymob_date_obtain_driver_license = fields.Date()
    mymob_matricule = fields.Char(string='Registration number')
    mymob_start_point_address = fields.Many2one('res.partner', string='Start point')


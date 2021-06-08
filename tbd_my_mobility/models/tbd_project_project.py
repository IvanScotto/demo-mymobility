# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class TbdProjectProject(models.Model):
    _inherit = "project.project"

    mymob_school = fields.Many2many('res.partner', string='Etablissement scolaire',
                                    domain=[('mymob_partner_type', '=', 'school'), ])
    mymob_agency = fields.Many2one('hr.department', string='Etablissement d\'agence')
    mymob_market = fields.Many2one('contract.contract', string='Marché', readonly=True)

    @api.model
    def create(self, vals):
        contract_contract = self.env['contract.contract'].search_read([('id', '=', vals['mymob_market'])])
        if contract_contract:
            vals['partner_id'] = contract_contract[0]['partner_id'][0]
        return super(TbdProjectProject, self).create(vals)

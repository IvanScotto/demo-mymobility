# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class TbdProjectProject(models.Model):
    _inherit = "project.project"

    mymob_agency = fields.Many2many('hr.department', string='Etablissement d\'agence')
    # mymob_client = fields.Many2one('res.partner', string='Client', required=True, readonly=True)
    mymob_client = fields.Many2one('contract.contract', string='Client', required=True, readonly=True)
    mymob_market = fields.Many2one('contract.contract', string='Marché', required=True, readonly=True)
    # mymob_client = fields.One2many(comodel_name='contract.contract', inverse_name='partner_id', string='Client')

    @api.onchange('partner_id')
    def onchange_parner_id(self):
        if not self.partner_id:
            self.update({
                'mymob_client': False,
                'mymob_market': False
            })
            return
        # values = {
        #     'mymob_client': addr['invoice']
        # }
        # self.update(values)
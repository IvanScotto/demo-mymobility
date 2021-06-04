# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class TbdProjectProject(models.Model):
    _inherit = "project.project"

    mymob_agency = fields.Many2many('hr.department', string='Etablissement d\'agence')
    mymob_client = fields.Many2one('res.partner', string='Client', readonly=True)
    mymob_market = fields.Many2one('contract.contract', string='Marché', readonly=True)

    @api.model
    def create(self, vals):
        if self.mymob_market.partner_id:
            vals['mymob_client'] = self.mymob_market.partner_id
            vals['partner_id'] = self.mymob_market.partner_id
        return super(TbdProjectProject, self).create(vals)

    # @api.onchange('partner_id')
    # def onchange_parner_id(self):
    #     if not self.partner_id:
    #         self.update({
    #             'mymob_client': False,
    #             'mymob_market': False
    #         })
    #         return
        # values = {
        #     'mymob_client': addr['invoice']
        # }
        # self.update(values)

    # @api.onchange('name')
    # def onchange_name(self):
    #     if not self.mymob_market:
    #         self.update({'mymob_client': False})
    #
    #     _logger.critical("TBD ON CHANGE TOTO  NAME %s" % self.mymob_market.partner_id)
        # values = {
        #     'mymob_client': self.mymob_market.partner_id.id,
        #     'partner_id': self.mymob_market.partner_id.id
        # }
        # _logger.critical(values)
        # self.update(values)

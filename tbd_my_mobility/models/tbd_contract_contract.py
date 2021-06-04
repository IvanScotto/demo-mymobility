# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class TbdContractContract(models.Model):

    _inherit = "contract.contract"

    mymob_partner_invoice_id = fields.Many2one(
        'res.partner', string='Invoice Address')
    contract_line_ids = fields.One2many(
        string="Contract lines",
        comodel_name="contract.line",
        inverse_name="contract_id",
        copy=True,
    )
    mymob_lots = fields.One2many(comodel_name='project.project', inverse_name='mymob_market', string='Lots')
    mymob_client = fields.One2many(comodel_name='project.project', inverse_name='mymob_client', string='Client')

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if not self.partner_id:
            self.update({
                'mymob_partner_invoice_id': False,
                'mymob_client': False
            })
            return

        addr = self.partner_id.address_get(['invoice'])
        values = {
            'mymob_partner_invoice_id': addr['invoice'],
            'mymob_client': self.partner_id
        }
        self.update(values)

        # TBD Filter
        # readonly=True, required=True,
        # states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'sale': [('readonly', False)]},
        # domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]"


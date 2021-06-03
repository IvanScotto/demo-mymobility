# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class TbdContractContract(models.Model):

    _inherit = "contract.contract"

    mymob_partner_invoice_id = fields.Many2one(
        'res.partner', string='Invoice Address')


    # @api.depends('partner_id')
    # def _compute_partner_invoice_adress(self):
    #     for contract in self:
    #         contract.mymob_partner_invoice_id = contract.partner_id.address_get(['invoice'])

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if not self.partner_id:
            self.update({
                'mymob_partner_invoice_id': False
            })
            return

        addr = self.partner_id.address_get(['invoice'])
        values = {
            'mymob_partner_invoice_id': addr['invoice']
        }
        self.update(values)

        # TBD Filter
        # readonly=True, required=True,
        # states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'sale': [('readonly', False)]},
        # domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]"

    # mymob_lots = fields.One2many('contract.contract', 'id', string='Lots')
# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class TbdContractContract(models.Model):

    _inherit = "contract.contract"

    mymob_partner_invoice_id = fields.Many2one(
        'res.partner', string='Invoice Address')


        # TBD Filter
        # readonly=True, required=True,
        # states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'sale': [('readonly', False)]},
        # domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]"

    # mymob_lots = fields.One2many('contract.contract', 'id', string='Lots')
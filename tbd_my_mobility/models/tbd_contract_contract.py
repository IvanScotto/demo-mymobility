# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class TbdContractContract(models.Model):

    _inherit = "contract.contract"

    mymob_partner_invoice_id = fields.Many2one('res.partner', string='Invoice Address')
    mymob_lots = fields.One2many(comodel_name='project.project', inverse_name='mymob_market', string='Lots')
    mymob_agency_count = fields.Integer(default=1)

    mymob_lots_count = fields.Integer(compute="_compute_lots_count")

    def _compute_lots_count(self):
        for rec in self:
            rec.mymob_lots_count = self.env['project.project'].search_count([('mymob_market', '=', self.id)])

    def action_show_agency(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Agency'),
            'view_mode': 'tree',
            'res_model': 'hr.department',
            'context': "{'create': False}"
        }

    def action_show_lots(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Lots'),
            'view_mode': 'tree',
            'res_model': 'project.project',
            'domain': [('mymob_market', '=', self.id)],
            'context': "{'create': False}"
        }

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


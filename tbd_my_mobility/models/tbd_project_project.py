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
    mymob_map = fields.Many2one('res.partner', string='map address')
    label_tasks = fields.Char(string='Use Tasks as', default='Lots',
                              help="Label used for the tasks of the project.", translate=True)

    test_long = fields.Float(default=47.115983)
    test_lat = fields.Float(default=2.782795)

    @api.onchange('user_id')
    def onchange_partner_id(self):
        if not self.partner_id:
            self.update({
                'mymob_map': False
            })
            return

        addr = self.partner_id.address_get()
        values = {
            'mymob_map': addr['default']
        }
        self.update(values)

    @api.model
    def create(self, vals):
        contract_contract = self.env['contract.contract'].search_read([('id', '=', vals['mymob_market'])])
        if contract_contract:
            vals['partner_id'] = contract_contract[0]['partner_id'][0]
        return super(TbdProjectProject, self).create(vals)

    def action_show_school(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('School'),
            'view_mode': 'tree',
            'res_model': 'res.partner',
            'domain': [('mymob_partner_type', '=', 'school')],
            'context': "{'create': True}"
        }

    def action_show_student(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Student'),
            'view_mode': 'tree',
            'res_model': 'res.partner',
            'domain': [('mymob_partner_type', '=', 'student')],
            'context': "{'create': True}"
        }
# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class TbdImport(models.TransientModel):
    _inherit = "base_import.import"

    def do(self, fields, columns, options, dryrun):
        import_result = super(TbdImport, self).do(fields, columns, options, dryrun)

        mymob_partner_type_context = self._context.get('mymob_partner_type')
        lot_id = self._context.get('lot_id')

        if mymob_partner_type_context and lot_id and not dryrun:
            records_partner = self.env['res.partner'].search([('id', 'in', import_result['ids'])])
            record_lot = self.env['project.project'].search([('id', '=', lot_id)])

            if mymob_partner_type_context == 'student':
                for record in records_partner:
                    record.update({'mymob_lots': lot_id})
                    record_lot[0].update({'mymob_student': [(4, record.id, 0)]})

            if mymob_partner_type_context == 'school':
                for record in records_partner:
                    record_lot[0].update({'mymob_school': [(4, record.id, 0)]})
        return import_result

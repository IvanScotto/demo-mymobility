# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class TbdProjectTask(models.Model):
    """

    """
    _inherit = "project.task"

    select_task_type = [
        ('segment', 'Segment'),
        ('route', 'Itinéraire'),
        ('driver', 'Tache conducteur')
    ]

    mymob_type = fields.Selection(select_task_type, string='Type de task')

    # TODO Completer
    # mymob_exclusion_calendar = fields.
    # mymob_status = fields.

    mymob_starting_date_validity = fields.Datetime('Date de début de validité')
    mymob_ending_date_validity = fields.Datetime('Date de fin de validité')
    mymob_activity_TPMR = fields.Boolean('Activité de TPMR', default=False)

    # TODO Remplir
    select_cycle = [
        ('wip', '[WIP]')
    ]
    mymob_cycle = fields.Selection(select_cycle, 'Cycle')

    select_nbr_cycle = [
        ('every_week', 'Toutes les semaines'),
        ('even_week', 'Semaine paire'),
        ('odd_week', 'Semaine impaire')
    ]
    mymob_nbr_cycle = fields.Selection(select_nbr_cycle, 'Nombre de cycle')

    select_category_vehicle = [
        ('wip', '[WIP]')
    ]
    mymob_category_vehicle = fields.Selection(select_category_vehicle, 'Category de vehicule')

    mymob_start_time = fields.Datetime('Horaire de début')
    mymob_end_time = fields.Datetime('Horaire de fin')

    mymob_partner_invoice_id = fields.Many2one('res.partner', string='Invoice Address')
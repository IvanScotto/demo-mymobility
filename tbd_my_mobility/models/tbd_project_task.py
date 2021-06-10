# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class TbdDays(models.Model):
    _name = 'tbd.weekdays'
    _description = 'Day of the week'

    select_day = [
        ('monday', 'Lundi'),
        ('tuesday', 'Mardi'),
        ('wednesday', 'Mercredi'),
        ('thursday', 'Jeudi'),
        ('friday', 'Vendredi'),
        ('saturday', 'Samedi'),
        ('sunday', 'Dimanche'),
    ]
    mymob_days = fields.Selection(select_day, string="Jour de la semaine")


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

    select_cycle = [
        ('week', 'Week'),
        ('month', 'Month'),
        ('year', 'Year')
    ]
    mymob_cycle = fields.Selection(select_cycle, 'Cycle')

    select_nbr_cycle = [
        ('every_week', 'Toutes les semaines'),
        ('even_week', 'Semaine paire'),
        ('odd_week', 'Semaine impaire')
    ]
    mymob_nbr_cycle = fields.Selection(select_nbr_cycle, 'Nombre de cycle')

    #TODO Remplir
    select_category_vehicle = [
        ('wip', '[WIP]')
    ]
    mymob_category_vehicle = fields.Selection(select_category_vehicle, 'Category de vehicule')

    mymob_start_time = fields.Datetime('Horaire de début')
    mymob_end_time = fields.Datetime('Horaire de fin')

    mymob_partner_invoice_id = fields.Many2one('res.partner', string='Invoice Address')

    select_direction = [
        ('go', 'Aller'),
        ('return', 'Retour')
    ]
    mymob_direction = fields.Selection(select_direction, string='Sens du trajet')

    mybmob_days = fields.Many2many('tbd.weekdays', string='Jour de la semaine')

    mymob_stop_duration = fields.Integer(string='Durée de l\'arrêt')
    mymob_stage_time_hour = fields.Integer(string='Heure de l\'étape')
    mymob_stage_time_minute = fields.Integer(string='Minute de l\'étape')
    mymob_distance_between_stage = fields.Float(string='Distance entre étape')

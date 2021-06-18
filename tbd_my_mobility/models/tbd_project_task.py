# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class TbdDays(models.Model):
    _name = 'tbd.weekdays'
    _description = 'Day of the week'

    select_day = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    mymob_days = fields.Selection(select_day, string="Day of the week")


class TbdProjectTask(models.Model):
    """

    """
    _inherit = "project.task"

    select_task_type = [
        ('segment', 'Segment'),
        ('route', 'Route'),
        ('driver', 'Driver task')
    ]

    mymob_type = fields.Selection(select_task_type, string='Type of task')

    # TODO Completer
    # mymob_exclusion_calendar = fields.
    # mymob_status = fields.

    mymob_starting_date_validity = fields.Date('Starting date of validity')
    mymob_ending_date_validity = fields.Date('Expiration date')
    mymob_activity_TPMR = fields.Boolean('TPMR activity', default=False)

    select_cycle = [
        ('week', 'Week'),
        ('month', 'Month'),
        ('year', 'Year')
    ]
    mymob_cycle = fields.Selection(select_cycle, 'Cycle', default='week')

    select_nbr_cycle = [
        ('every_week', 'Every week'),
        ('even_week', 'Even week'),
        ('odd_week', 'Odd week')
    ]
    mymob_nbr_cycle = fields.Selection(select_nbr_cycle, 'Number of cycles')

    #TODO Remplir
    select_category_vehicle = [
        ('wip', '[WIP]')
    ]
    mymob_category_vehicle = fields.Selection(select_category_vehicle, 'Vehicle category')

    mymob_start_time = fields.Datetime('Start time')
    mymob_end_time = fields.Datetime('End time')

    mymob_partner_invoice_id = fields.Many2one('res.partner', string='Invoice Address',
                                               domain=[('mymob_partner_type', 'in', ('student', 'tutor')), ])
    mymob_student = fields.Many2one('res.partner', string='Student')

    select_direction = [
        ('go', 'Go'),
        ('return', 'Return')
    ]
    mymob_direction = fields.Selection(select_direction, string='Sens du trajet')

    mybmob_days = fields.Many2many('tbd.weekdays', string='Day of the week')

    mymob_stop_duration = fields.Integer(string='Duration of the shutdown')
    mymob_stage_time_hour = fields.Integer(string='Hour of the Stage (H)')
    mymob_stage_time_minute = fields.Integer(string='Minute of the Stage (M)')
    mymob_distance_between_stage = fields.Float(string='Distance between stages')

    mymob_child_ids = fields.One2many('project.task', 'parent_id', string="Child Task")
    mymob_sequence = fields.Integer(string="Sequence")

    @api.onchange('mymob_student')
    def onchange_partner_id(self):
        if not self.mymob_student:
            self.update({
                'mymob_partner_invoice_id': False
            })
            return

        addr = self.mymob_student.address_get(['invoice'])
        values = {
            'mymob_partner_invoice_id': addr['invoice']
        }
        self.update(values)

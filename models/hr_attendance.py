# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import fields, models


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    attendance_request = fields.Boolean(
        string='Attendance Request',
    )
    
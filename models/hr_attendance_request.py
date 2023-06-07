# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class HrAttendanceRequest(models.Model):
    _name = 'hr.attendance.request'
    _description = 'Attendance Request'

    _rec_name = 'employee_id'
    # _order = 'name ASC'

    #inheritance
    _inherit = ['mail.thread', 'mail.activity.mixin']

    #get employee
    def _get_employee_id(self):
        employee_rec = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        return employee_rec.id
    
    # -- fields
    attendance_date = fields.Date(
        string='Attendance Date',
        required=True,
        default=fields.Date.context_today,
        help='Attendance date',
    )
    
    clock_in = fields.Float(
        string='Clock In',
        required=True,
        help='Clock In',
    )

    clock_out = fields.Float(
        string='Clock Out',
        required=True,
        help='Clock Out',
    )
    
    work_note = fields.Text(
        string='Work Note',
        required=True,
        help='Work Note/Reason'
    )
    
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee',
        default=_get_employee_id,
        readonly=True,
        required=True,
        ondelete='restrict',
    )
    
    state_request = fields.Selection(
        string='Status',
        selection=[('draft', 'Draft'), ('requested', 'Requested'), ('rejected', 'Rejected'), ('approved', 'Approved')],
        default='draft',
        track_visibility='onchange',
        help='Status'
    )
    # -- end fields

    # -- constraints 
    # validate attendance date (cannot future)
    def _check_attendance_date(self):
        for record in self:
            if record.attendance_date > fields.Date.today():
                raise ValidationError(_('The attendance date cannot be set in the future'))
    
    # set unique employee & date
    _sql_constraints = [
        (
            'unique_attendance_request',
            'unique(employee_id, attendance_date)',
            _('Data already exists for this date!')
        )
    ]
    # -- end contraints
    
    # -- methods  
    # @api.multi
    def unlink(self):
        for record in self:
            if record.state_request not in ('draft'):
                raise UserError(
                    'You cannot delete a document which is not draft!'
                )
        return super(HrAttendanceRequest, self).unlink()
          
    # @api.multi
    def submit_req(self):
        _clock_in = datetime.combine(self.attendance_date, datetime.min.time())
        _clock_out = datetime.combine(self.attendance_date, datetime.max.time())

        _count = self.env['hr.attendance'].search_count([
                ('employee_id', '=', self.env.uid),
                ('check_in', '>=', _clock_in),
                ('check_in', '<=', _clock_out)
            ],
            limit=1
        )
        if _count > 0:
            raise ValidationError(_('Data already exists for this date!'))

        self.ensure_one()
        # self.sudo().write({
        #     'state_request': 'requested'
        # })
        self._set_state('requested')
        return
    
    # @api.multi
    def approve_req(self):
        self.ensure_one()

        _f_check_in = '{0:02.0f}:{1:02.0f}'.format(*divmod(self.clock_in * 60, 60))
        _time_check_in = datetime.strptime(_f_check_in, '%H:%M').time()
        _check_in = datetime.combine(self.attendance_date, _time_check_in)

        _f_check_out = '{0:02.0f}:{1:02.0f}'.format(*divmod(self.clock_out * 60, 60))
        _time_check_out = datetime.strptime(_f_check_out, '%H:%M').time()
        _check_out = datetime.combine(self.attendance_date, _time_check_out)

        data = {
            'check_in': _check_in,
            'check_out': _check_out,
            'employee_id': self.employee_id.id,
            'attendance_request': True
        }
        
        self._set_state('approved')
        self.env['hr.attendance'].sudo().create(data)
        return
    
    # @api.multi
    def reject_req(self):
        self.ensure_one()
        self._set_state('rejected')
        return
    
    def _set_state(self, new_state):
        self.write({
            'state_request': new_state
        })
        return
    # -- end mothods
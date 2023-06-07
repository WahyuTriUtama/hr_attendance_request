# -*- coding: utf-8 -*-
###############################################################################
#
#    Wahyu Tri Utomo<wahyutriutama@gmail.com>
#
#    Copyright (c) All rights reserved:
#        (c) 2023  Balelabs
#
###############################################################################

{
    'name': 'Attendance Request',
    'version': '16.0.1.0.0',
    'summary': 'Employees Attendance Request',
    'description': 'Employees Attendance Request',
    'category': 'Human Resources',
    'author': 'Wahyu',
    'company': 'PT Bale Lab Indonesia',
    'website': 'https://www.balelabs.id',
    'depends': ['base', 'hr', 'hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/hr_attendance_request_view.xml'
    ],
    'images': ['static/img/icon.png'],
    'license': 'LGPL-3',
    'installable': True,
    'application': True
}

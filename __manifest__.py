# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Employee Evaluate',
    'version': '1.0',
    'category': 'Human Resources/Evaluate',
    'sequence': 335,
    'description': """
Add all information on the employee form to manage Evaluate.
=============================================================


You can assign several Evaluate per employee.
    """,
    'website': 'https://www.odoo.com/page/employees',
    'depends': ['hr', 'sale'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'data/cron.xml',
        'views/hr_evaluate_views.xml',
        'views/hr_evaluate_form_views.xml',
        'views/hr_evaluate_config_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}

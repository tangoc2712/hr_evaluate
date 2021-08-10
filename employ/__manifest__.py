# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Employ',
    'version': '1.1',
    'author': 'Ta Quang Ngoc',
    'summary': 'Employee Manage System',
    'sequence': 10,
    'description': "",
    'category': 'Employee',
    'website': 'https://www.odoo.com',
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'views/employ_view.xml',
    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

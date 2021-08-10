from odoo import api, fields, models


class EmployProfile(models.Model):
    _name = "employ.profile"

    name = fields.Char(string="Full Name")
    age = fields.Integer(string="Age")
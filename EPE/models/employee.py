from odoo import api, models, fields


class EmployeeProfile(models.Model):
    _name = "employee.profile"

    name = fields.Char(string="Full Name")

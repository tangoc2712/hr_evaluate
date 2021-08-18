from odoo import models, api, fields
from odoo.exceptions import UserError


class HrEvaluateForm(models.Model):
    _name = "hr.evaluate.form"

    baby = fields.Char(string='BaBY')
    shark = fields.Char(string='SHAKILA')




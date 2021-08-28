from odoo import models, api, fields
from odoo.exceptions import UserError


class HrEvaluateConfig(models.Model):
    _name = 'hr.evaluate.config'
    _description = "Config Table to get default value"

    criteria = fields.Char(string="Tiêu chí đánh giá")
    percentage = fields.Integer(string="Trọng số")
    rank = fields.Selection(selection=[
        ('A+', 'A+'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D')
    ], string="Rank")
    rank_str = fields.Char(string="Loại")
    type = fields.Selection(selection=[
        ('conclusion', 'conclusion'),
        ('discipline', 'discipline'),
        ('sum', 'sum'),
    ], string="Configuration type")




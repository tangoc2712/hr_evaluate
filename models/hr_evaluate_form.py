from odoo import models, api, fields
from odoo.exceptions import UserError


class HrEvaluateForm(models.Model):
    _name = "hr.evaluate.form"

    employee_id = fields.Many2one('hr.evaluate', string="Employee Id")
    job_des = fields.Text(string='Job Description')
    par_level = fields.Text(string='Participation Level')
    comp_level = fields.Integer(string="Completion Level (%)")
    quantity = fields.Selection(
        [('excellent', 'Xuất Sắc'),
         ('good', 'Tốt'),
         ('kha', 'Khá'),
         ('mid', 'Trung Bình'),
         ('fail', 'Chưa Đạt')])
    des = fields.Char(string='Description')
    manager_des = fields.Char(string='Manager Description')
    self_eval = fields.Integer(string='Self Evaluate')
    manager_eval = fields.Integer(string='Manager Evaluate')


class HrEvaluateForm2(models.Model):
    _name = "hr.evaluate.form2"

    employee_id2 = fields.Many2one('hr.evaluate', string="Form Id 2")
    criteria = fields.Char(string='Criteria ')
    weight_num = fields.Integer(string='Weight (%)')
    self_evaluate = fields.Integer(string='Self evaluate')
    dl_evaluate = fields.Integer(string='DL/PM evaluate')


class HrEvaluate(models.Model):
    _inherit = "hr.evaluate"

    form_list = fields.One2many('hr.evaluate.form', 'employee_id', string="Form Question List")
    form_list2 = fields.One2many('hr.evaluate.form2', 'employee_id2', string="Form2 Question List")

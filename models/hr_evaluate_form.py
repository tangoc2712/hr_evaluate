from odoo import models, api, fields
from odoo.exceptions import UserError


class HrEvaluateForm(models.Model):
    _name = "hr.evaluate.form"

    employee_id = fields.Many2one('hr.evaluate', string="Employee Id")
    job_des = fields.Char(string='Nội dung công việc')
    par_level = fields.Char(string='Mức độ tham gia')
    comp_level = fields.Integer(string="Mức độ hoàn thành (%)")
    quantity = fields.Selection(
        [('excellent', 'Xuất Sắc'),
         ('good', 'Tốt'),
         ('kha', 'Khá'),
         ('mid', 'Trung Bình'),
         ('fail', 'Chưa Đạt')])
    des = fields.Char(string='Ghi chú')
    manager_eval = fields.Integer(string='Quản lý đánh giá ')

    manager_edit = fields.Boolean(string='Manage can edit')


class HrEvaluateForm2(models.Model):
    _name = "hr.evaluate.form2"

    employee_id2 = fields.Many2one('hr.evaluate', string="Form Id 2")
    criteria = fields.Char(string='Tiêu chí đánh giá')
    weight_num = fields.Char(string='Trọng số (%)')
    self_evaluate = fields.Float(string='Cá nhân đánh giá')
    self_evaluate_edit = fields.Boolean(string="Employee can edit")
    dl_evaluate = fields.Float(string='Quản lý đánh giá')
    dl_evaluate_edit = fields.Boolean(string="PM/DL can edit")
    des = fields.Char(string="Ghi chú")


class HrEvaluate(models.Model):
    _inherit = "hr.evaluate"

    form_list = fields.One2many('hr.evaluate.form', 'employee_id', string="Form Question List")
    form_list2 = fields.One2many('hr.evaluate.form2', 'employee_id2', string="Form2 Question List")

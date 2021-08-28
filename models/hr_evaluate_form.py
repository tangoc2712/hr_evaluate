from odoo import models, api, fields
from odoo.exceptions import UserError


class HrEvaluateForm(models.Model):
    _name = "hr.evaluate.form"
    _description = "Performance Form"
    employee_id = fields.Many2one('hr.evaluate', string="Employee Id")
    job_des = fields.Char(string='Nội dung công việc', required=True)
    par_level = fields.Char(string='Mức độ tham gia', required=True)
    comp_level = fields.Integer(string="Mức độ hoàn thành (%)", required=True)
    quantity = fields.Selection(
        [('excellent', 'Xuất Sắc'),
         ('good', 'Tốt'),
         ('kha', 'Khá'),
         ('mid', 'Trung Bình'),
         ('fail', 'Chưa Đạt')], required=True)
    des = fields.Char(string='Ghi chú')
    manager_eval = fields.Integer(string='Quản lý đánh giá ')

    manager_edit = fields.Boolean(string="DL can edit", default=False, readonly=True)


class HrEvaluateForm2(models.Model):
    _name = "hr.evaluate.form2"
    _description = "Discipline Form"

    evaluate_config_id = fields.Many2one('hr.evaluate.config', string="Config ID")
    employee_id2 = fields.Many2one('hr.evaluate', string="Form Id 2")
    criteria = fields.Char(string='Tiêu chí đánh giá')
    weight_num = fields.Float(string='Trọng số (%)')
    self_evaluate = fields.Float(string='Cá nhân đánh giá')
    self_evaluate_edit = fields.Boolean(string="Employee can edit")
    dl_evaluate = fields.Float(string='Quản lý đánh giá', digits=0)
    dl_evaluate_edit = fields.Boolean(string="PM/DL can edit")
    des = fields.Char(string="Ghi chú")

    point_self = fields.Float(compute="_calculate_point")
    point_dl = fields.Float(compute="_calculate_point")

    # total = fields.Float(compute='_compute_sum')

    @api.depends('self_evaluate', 'weight_num', )
    def _compute_sum(self):
        total = 0
        for re in self:
            re.self_evaluate = re.self_evaluate * re.weight_num
            total += re.self_evaluate
            print(total)


class HrEvaluateForm3(models.Model):
    _name = "hr.evaluate.form3"
    _description = "Conclusion Form"

    evaluate_config_id = fields.Many2one('hr.evaluate.config', string="Config ID")
    employee_id3 = fields.Many2one('hr.evaluate', string="Form Id 3")
    manager_rank = fields.Boolean(string="Quản lý đánh giá", readonly=True)
    self_rank = fields.Boolean(string="Cá nhân đánh giá đánh giá", readonly=True)
    rank = fields.Char(string="Loại")


class HrEvaluate(models.Model):
    _inherit = "hr.evaluate"

    form_list = fields.One2many('hr.evaluate.form', 'employee_id', string="Form Question List")
    form_list2 = fields.One2many('hr.evaluate.form2', 'employee_id2', string="Form2 Question List")

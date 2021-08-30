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
         ('fail', 'Chưa Đạt')], required=True, string="Chất lượng")
    des = fields.Char(string='Ghi chú')
    manager_eval = fields.Text(string='Quản lý đánh giá ')

    manager_edit = fields.Boolean(string="DL can edit", compute="_change_state", readonly=True)

    @api.onchange('job_des', 'employee_id.state')
    def _change_state(self):
        for re in self:
            print(re.manager_edit)
            if re.employee_id.state != 'draft':
                re.manager_edit = True


class HrEvaluateForm2(models.Model):
    _name = "hr.evaluate.form2"
    _description = "Discipline Form"

    evaluate_config_id = fields.Many2one('hr.evaluate.config', string="Config ID")
    employee_id2 = fields.Many2one('hr.evaluate', string="Form Id 2")
    criteria = fields.Char(string='Tiêu chí đánh giá')
    weight_num = fields.Integer(string='Trọng số (%)')
    self_evaluate = fields.Integer(string='Cá nhân đánh giá')
    self_evaluate_edit = fields.Boolean(string="Employee can edit", compute="_change_state", default=True)
    dl_evaluate = fields.Integer(string='Quản lý đánh giá', digits=0)
    dl_evaluate_edit = fields.Boolean(string="PM/DL can edit", compute="_change_state", default=True)
    des = fields.Char(string="Ghi chú")

    @api.onchange('criteria', 'employee_id2.state')
    def _change_state(self):
        for re in self:
            print(re.self_evaluate_edit)
            if re.employee_id2.state == 'draft':
                re.self_evaluate_edit = True
                re.dl_evaluate_edit = False
            else:
                re.self_evaluate_edit = False
                re.dl_evaluate_edit = True



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

from odoo import models, api, fields
from odoo.exceptions import UserError


class HrEvaluateForm(models.Model):
    _name = "hr.evaluate.form"
    _description = "Performance Form"
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

    manager_edit = fields.Boolean(string='Manage can edit', default=False, readonly=True)

    def write(self, values):
        """Override default Odoo write function and extend."""
        check = super(HrEvaluateForm, self).write(values)
        if check is None:
            raise UserError("Please choose 1 hobby at least!!!")
        return check

    @api.onchange('employee_id')
    def _onchange_contract_id(self):
        statee = self.env['hr.evaluate'].sudo().search([('employee_id', '=', self.employee_id.id),
                                                        ('state', '!=', 'draft')])
        if statee:
            self.manager_edit = True


class HrEvaluateForm2(models.Model):
    _name = "hr.evaluate.form2"
    _description = "Discipline Form"

    evaluate_config_id = fields.Many2one('hr.evaluate.config', string="Config ID")
    employee_id2 = fields.Many2one('hr.evaluate', string="Form Id 2")
    criteria = fields.Char(string='Tiêu chí đánh giá')
    weight_num = fields.Char(string='Trọng số (%)')
    self_evaluate = fields.Float(string='Cá nhân đánh giá')
    self_evaluate_edit = fields.Boolean(string="Employee can edit")
    dl_evaluate = fields.Float(string='Quản lý đánh giá')
    dl_evaluate_edit = fields.Boolean(string="PM/DL can edit")
    des = fields.Char(string="Ghi chú")


class HrEvaluateForm3(models.Model):
    _name = "hr.evaluate.form3"
    _description = "Conclusion Form"

    evaluate_config_id = fields.Many2one('hr.evaluate.config', string="Config ID")
    employee_id3 = fields.Many2one('hr.evaluate', string="Form Id 3")
    manager_rank = fields.Boolean(string="Quản lý đánh giá")
    self_rank = fields.Boolean(string="Cá nhân đánh giá đánh giá")
    rank = fields.Char(string="Loại")

































































class HrEvaluate(models.Model):
    _inherit = "hr.evaluate"

    form_list = fields.One2many('hr.evaluate.form', 'employee_id', string="Form Question List")
    form_list2 = fields.One2many('hr.evaluate.form2', 'employee_id2', string="Form2 Question List")

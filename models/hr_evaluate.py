from odoo import api, fields, models, tools


class HrEvaluate(models.Model):
    _name = "hr.evaluate"
    _description = 'Employee Evaluate'

    name = fields.Char(string="Name")
    employee_id = fields.Many2one('hr.employee', string='Employee', tracking=True)
    department_id = fields.Many2one('hr.department', compute='_compute_employee_evaluate', store=True, readonly=True,
                                    string="Department")
    job_id = fields.Many2one('hr.job', compute='_compute_employee_evaluate', store=True, readonly=True,
                             string='Job Position')
    start_date = fields.Date(string='Start Date', readonly=True)
    job_des = fields.Text(string='Job Description')
    par_level = fields.Text(string='Participation Level')
    comp_level = fields.Integer(string="Completion Level (%)")
    quantity = fields.Selection(
        [('excellent', 'Xuất Sắc'), ('good', 'Tốt'), ('kha', 'Khá'), ('mid', 'Trung Bình'), ('fail', 'Chưa Đạt')])
    des = fields.Text(string='Description')
    manager_des = fields.Text(string='Manager Description')
    self_eval = fields.Integer(string='Self Evaluate')
    manager_eval = fields.Integer(string='Manager Evaluate')

    @api.depends('employee_id')
    def _compute_employee_evaluate(self):
        for evaluate in self.filtered('employee_id'):
            evaluate.job_id = evaluate.employee_id.job_id
            evaluate.department_id = evaluate.employee_id.department_id


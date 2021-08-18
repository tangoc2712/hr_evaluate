from odoo import api, fields, models, tools


class HrEvaluate(models.Model):
    _name = "hr.evaluate"
    _description = 'Employee Evaluate'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char('No.', default='/')

    # on create method
    @api.model
    def create(self, vals):
        obj = super(HrEvaluate, self).create(vals)
        if obj.name == '/':
            number = self.env['ir.sequence'].get('sequence.code') or '/'
            obj.write({'name': number})
        return obj

    employee_id = fields.Many2one('hr.employee', string='Employee', tracking=True)
    user_id = fields.Many2one('res.users', string='Account', store=True)
    department_id = fields.Many2one('hr.department', compute='_compute_employee_evaluate', store=True, readonly=True,
                                    string="Department")
    job_id = fields.Many2one('hr.job', compute='_compute_employee_evaluate', store=True, readonly=True,
                             string='Job Position')
    start_date = fields.Date(string='Start Date', readonly=True)
    job_des = fields.Text(string='Job Description')
    par_level = fields.Text(string='Participation Level')
    comp_level = fields.Integer(string="Completion Level (%)")
    quantity = fields.Selection(
        [('excellent', 'Xuất Sắc'),
         ('good', 'Tốt'),
         ('kha', 'Khá'),
         ('mid', 'Trung Bình'),
         ('fail', 'Chưa Đạt')])
    des = fields.Text(string='Description')
    manager_des = fields.Text(string='Manager Description')
    self_eval = fields.Integer(string='Self Evaluate')
    manager_eval = fields.Integer(string='Manager Evaluate')

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('pm', 'PM Review'),
        ('dl', 'DL Review'),
        ('approve', 'Approved')
    ], default='draft')

    @api.depends('employee_id')
    def _compute_employee_evaluate(self):
        for evaluate in self.filtered('employee_id'):
            evaluate.job_id = evaluate.employee_id.job_id
            evaluate.department_id = evaluate.employee_id.department_id

    def user_confirm(self):
        for record in self:
            record.status = 'pm'

    def pm_confirm(self):
        for record in self:
            record.status = 'dl'

    def dl_confirm(self):
        for record in self:
            record.status = 'approve'

    def cancel_user_confirm(self):
        for record in self:
            record.status = 'draft'

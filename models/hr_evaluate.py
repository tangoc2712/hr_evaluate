from odoo import api, fields, models, tools


class HrEvaluate(models.Model):
    _name = "hr.evaluate"
    _description = 'Employee Evaluate'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('No.', default='/')
    # form_id = fields.Many2many('hr.evaluate.form')
    employee_id = fields.Many2one('hr.employee', string='Employee', tracking=True)
    user_id = fields.Many2one('res.users', string='Account', store=True)
    department_id = fields.Many2one('hr.department', compute='_compute_employee_evaluate', store=True, readonly=True,
                                    string="Department")
    job_id = fields.Many2one('hr.job', compute='_compute_employee_evaluate', store=True, readonly=True,
                             string='Job Position')

    petition = fields.Html()
    remark = fields.Html()
    start_date = fields.Date(string='Start Date', default=fields.Date.today(), readonly=True)

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('pm', 'PM Review'),
        ('dl', 'DL Review'),
        ('approve', 'Approved')
    ], default='draft')

    # on create method ==> auto generate contract name
    @api.model
    def create(self, vals):
        obj = super(HrEvaluate, self).create(vals)
        if obj.name == '/':
            number = self.env['ir.sequence'].get('sequence.code') or '/'
            obj.write({'name': number})
        return obj

    @api.depends('employee_id')
    def _compute_employee_evaluate(self):
        for evaluate in self.filtered('employee_id'):
            evaluate.job_id = evaluate.employee_id.job_id
            evaluate.department_id = evaluate.employee_id.department_id

    def user_confirm(self):
        for record in self:
            record.state = 'pm'

    def pm_confirm(self):
        for record in self:
            record.state = 'dl'

    def dl_confirm(self):
        for record in self:
            record.state = 'approve'

    def cancel_user_confirm(self):
        for record in self:
            record.state = 'draft'

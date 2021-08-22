from odoo import api, fields, models, tools


class HrEvaluate(models.Model):
    _name = "hr.evaluate"
    _description = 'Employee Evaluate'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # contract_id = fields.Many2one('hr.contract', string="Hợp đồng thử việc")

    # start_date = fields.Date(compute='_compute_date_evaluate', string="Ngày bắt đầu", readonly=True)
    # end_date = fields.Date(compute='_compute_date_evaluate', string="Ngày kết thúc", readonly=True)

    employee_id = fields.Many2one('hr.employee', string='Người được đánh giá', tracking=True)
    department_id = fields.Many2one('hr.department', compute='_compute_employee_evaluate', store=True, readonly=True,
                                    string="Department")
    job_id = fields.Many2one('hr.job', compute='_compute_employee_evaluate', store=True, readonly=True,
                             string='Chức vụ')
    company_id = fields.Many2one('res.company', required=True)
    petition = fields.Html()
    remark = fields.Html()
    pm_assign = fields.Many2one('hr.employee', string='PM assigned', tracking=True)
    dl_assign = fields.Many2one('hr.employee', string='Người đánh giá', tracking=True)
    dl_assign_job_id = fields.Many2one('hr.job', compute='_compute_dl_evaluate', store=True, readonly=True,
                                       string='Chức vụ')

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('pm', 'PM Review'),
        ('dl', 'DL Review'),
        ('approve', 'Approved')
    ], default='draft', tracking=True)

    @api.depends('employee_id')
    def _compute_employee_evaluate(self):
        for evaluate in self.filtered('employee_id'):
            evaluate.company_id = evaluate.employee_id.company_id
            evaluate.job_id = evaluate.employee_id.job_id
            evaluate.department_id = evaluate.employee_id.department_id
            # evaluate.contract_id = evaluate.employee_id.name


    @api.depends('dl_assign')
    def _compute_dl_evaluate(self):
        for evaluate in self.filtered('dl_assign'):
            evaluate.dl_assign_job_id = evaluate.dl_assign.job_id

    # @api.depends('contract_id')
    # def _compute_date_evaluate(self):
    #     for evaluate in self.filtered('contract_id'):
    #         evaluate.start_date = evaluate.contract_id.date_start
    #         evaluate.end_date = evaluate.contract_id.date_end

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

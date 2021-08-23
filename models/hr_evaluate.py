from odoo import api, fields, models, tools


class HrEvaluate(models.Model):
    _name = "hr.evaluate"
    _description = 'Employee Evaluate'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    account = fields.Char(string='Account')
    # contract_id = fields.Many2one('hr.contract', string="Hợp đồng thử việc")
    start_date = fields.Date(string="Ngày bắt đầu", readonly=True)
    end_date = fields.Date(string="Ngày kết thúc", readonly=True)

    employee_id = fields.Many2one('hr.employee', string='Người được đánh giá', tracking=True)
    department_id = fields.Many2one('hr.department', compute='_compute_employee_evaluate', store=True, readonly=True,
                                    string="Department")
    job_id = fields.Many2one('hr.job', compute='_compute_employee_evaluate', store=True, readonly=True,
                             string='Chức vụ')
    company_id = fields.Many2one('res.company', required=True)
    petition = fields.Html()
    remark = fields.Html()
    pm_assign = fields.Many2one('hr.employee', string='PM assigned',store=True,tracking=True)
    dl_assign = fields.Many2one('hr.employee', compute="_compute_employee_evaluate", store=True, readonly=True)
    dl_assign_job_id = fields.Many2one('hr.job', compute='_compute_dl_evaluate', store=True, readonly=True,
                                       string='Chức vụ')
    notes = fields.Char()
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('pm', 'PM Review'),
        ('dl', 'DL Review'),
        ('approve', 'Approved')
    ], default='draft', tracking=True)

    employee_can_submit = fields.Boolean(default=True)
    pm_can_submit = fields.Boolean()
    dl_can_submit = fields.Boolean()
    dl_can_assign = fields.Boolean(default=False)
    can_retain = fields.Boolean()

    form_evaluate_ids = fields.One2many('hr.evaluate.form', 'employee_id', string='Performance Evaluate')
    form2_evaluate_ids = fields.One2many('hr.evaluate.form2', 'employee_id2', string='Discipline Evaluate')

    @api.depends('employee_id')
    def _compute_employee_evaluate(self):
        for evaluate in self.filtered('employee_id'):
            evaluate.company_id = evaluate.employee_id.company_id
            evaluate.job_id = evaluate.employee_id.job_id
            evaluate.department_id = evaluate.employee_id.department_id
            evaluate.dl_assign = evaluate.employee_id.parent_id
            # evaluate.contract_id = evaluate.employee_id.name

    @api.depends('dl_assign')
    def _compute_dl_evaluate(self):
        for evaluate in self.filtered('dl_assign'):
            evaluate.dl_assign_job_id = evaluate.dl_assign.job_id

    @api.onchange('employee_id')
    def _onchange_account(self):
        self.account = str(self.employee_id).upper()

    @api.onchange('employee_id')
    def _onchange_contract_id(self):
        contract = self.env['hr.contract'].sudo().search([('employee_id', '=', self.employee_id.id),
                                                          ('state', '=', 'open')])
        if contract:
            self.start_date = contract[0].date_start
            self.end_date = contract[0].date_end

    # @api.depends('contract_id')
    # def _compute_date_evaluate(self):
    #     for evaluate in self.filtered('contract_id'):
    #         evaluate.start_date = evaluate.contract_id.date_start
    #         evaluate.end_date = evaluate.contract_id.date_end

    def action_employee_submit(self):
        self.dl_can_assign = True
        self.dl_can_submit = True
        self.employee_can_submit = False
        self.state = 'dl'

    def action_pm_submit(self):
        self.pm_can_submit = False
        self.dl_can_submit = True
        self.state = 'dl'

    def action_dl_submit(self):
        self.dl_can_submit = False
        self.state = 'approve'

    def cancel_user_confirm(self):
        self.state = 'draft'

    def action_dl_assign(self):
        self.form_evaluate_ids.manager_edit = True
        self.pm_can_submit = True
        self.dl_can_submit = False
        self.dl_can_assign = False
        self.state = 'pm'

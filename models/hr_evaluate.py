from odoo import api, fields, models, tools
from odoo.exceptions import UserError


class HrEvaluate(models.Model):
    _name = "hr.evaluate"
    _description = 'Employee Evaluate'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    account = fields.Char(related='employee_id.work_email', string='Tài khoản')
    contract_id = fields.Char(string="Hợp đồng")
    start_date = fields.Date(string="Ngày bắt đầu", readonly=True)
    end_date = fields.Date(string="Ngày kết thúc", readonly=True)

    trail_contract_id = fields.Many2one('hr.contract', string='Hợp đồng thử việc', tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Người được đánh giá', tracking=True)
    department_id = fields.Many2one('hr.department', compute='_compute_employee_evaluate', store=True, readonly=True,
                                    string="Phòng ban")
    job_id = fields.Many2one('hr.job', compute='_compute_employee_evaluate', store=True, readonly=True,
                             string='Chức vụ')
    company_id = fields.Many2one('res.company', required=True)
    petition = fields.Text()
    remark = fields.Text()
    pm_assign = fields.Many2one('hr.employee', string='PM assigned', store=True, tracking=True)
    dl_assign = fields.Many2one('hr.employee', compute="_compute_employee_evaluate", store=True, readonly=True)
    dl_assign_job_id = fields.Many2one('hr.job', compute='_compute_dl_evaluate', store=True, readonly=True,
                                       string='Chức vụ')
    notes = fields.Text(string="Message", tracking=True)
    mess = fields.Text(compute='_update_note')

    @api.depends('dl_assign', 'pm_assign')
    def _update_note(self):
        for re in self:
            re.mess = "Status: DL " + str(re.dl_assign.name) + " assigned to PM " + str(
                re.pm_assign.name) + "\n" + "Note: " + str(re.notes)
            print(re.mess)

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('pm', 'PM Review'),
        ('dl', 'DL Review'),
        ('approve', 'Approved')
    ], default='draft', tracking=True, string="Trạng thái")

    employee_confirm = fields.Selection(selection=[
        ('yes', 'Có'),
        ('no', 'Không'),
    ], store=True, string="Nhân viên xác nhận ký tiếp hợp đồng (*)")
    dl_confirm = fields.Selection(selection=[
        ('yes', 'Có'),
        ('no', 'Không'),
    ], store=True, string="	DL xác nhận ký tiếp hợp đồng (*)")
    employee_reason = fields.Text(string="Lý do của nhân viên")
    dl_reason = fields.Text(string="Lý do của DL")
    hrm_reason = fields.Text(string="Lý do của HRM")

    employee_can_submit = fields.Boolean(default=True)
    pm_can_submit = fields.Boolean()
    dl_can_submit = fields.Boolean()
    dl_can_assign = fields.Boolean(default=False)
    can_retain = fields.Boolean()

    form_evaluate_ids = fields.One2many('hr.evaluate.form', 'employee_id', string='Performance Evaluate', required=True)
    form2_evaluate_ids = fields.One2many('hr.evaluate.form2', 'employee_id2', string='Discipline Evaluate')
    form3_evaluate_ids = fields.One2many('hr.evaluate.form3', 'employee_id3', string='Conclusion Evaluate')

    @api.model
    def change_state(self):
        manage_edit = self.env['hr.evaluate.form'].sudo().search([])
        if self.state == 'draft' or self.state == 'approve':
            manage_edit.manager_edit = True

    @api.model
    def auto_generate_evaluate(self):
        print("Danh sách các nhân viên đến lúc lên thớt:")
        today = fields.Datetime.today()
        contract = self.env['hr.contract'].sudo().search([('state', '=', 'open')], order="date_end desc")
        for re in contract:
            date_end = fields.Datetime.to_datetime(re.date_end)
            if (date_end is not None) and (int((date_end - today).days) < 15) and (int((date_end - today).days) > 0):
                print(re.employee_id.id)
                vals = {
                    'employee_id': re.employee_id.id,
                    'company_id': re.employee_id.company_id.id,
                    'contract_id': re.name,
                    'start_date': re.date_start,
                    'end_date': re.date_end,
                    'dl_confirm': '',

                }
                self.env['hr.evaluate'].create(vals)

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
    def _onchange_contract_id(self):
        contract = self.env['hr.contract'].sudo().search([('employee_id', '=', self.employee_id.id),
                                                          ('state', '=', 'open')])
        if contract:
            self.start_date = contract[0].date_start
            self.end_date = contract[0].date_end
            self.contract_id = contract[0].name

    @api.model
    def default_get(self, fields):
        res = super(HrEvaluate, self).default_get(fields)
        print("testing.............")
        # evaluate_config_id_ids = self.get_discipline_evaluate()
        evaluate_config_id_ids = self.env['hr.evaluate.config'].search([])
        disciplines = []
        ranks = []
        for config_id in evaluate_config_id_ids:
            if config_id.type == 'conclusion':
                ranks.append((0, 0, {'evaluate_config_id': config_id.id,
                                     'rank': config_id.rank_str
                                     }))
            elif config_id.type == 'discipline':
                disciplines.append((0, 0, {'evaluate_config_id': config_id.id,
                                           'criteria': config_id.criteria,
                                           'weight_num': config_id.percentage,
                                           'self_evaluate': 0,
                                           'dl_evaluate': 0}))
            elif config_id.type == 'sum':
                disciplines.append((0, 0, {'evaluate_config_id': config_id.id,
                                           }))

        res.update({'form2_evaluate_ids': disciplines,
                    'form3_evaluate_ids': ranks})
        return res

    def action_employee_submit(self):
        # template_id = self.env.ref("hr_evaluate.email_template_evaluate_em_to_dl").id
        # print(template_id)
        # self.env['mail.template'].browse(template_id).send_mail(self.id)

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
        self.dl_can_assign = False
        self.state = 'approve'

    def cancel_user_confirm(self):
        self.state = 'draft'

    def action_dl_assign(self):
        # self.form_evaluate_ids.manager_edit = True
        self.pm_can_submit = True
        self.dl_can_submit = False
        self.dl_can_assign = False
        self.state = 'pm'

    def action_dl_to_pm(self):
        form_view = self.env.ref('hr_evaluate.dl_assign_view_form')
        return {
            'name': 'Form DL Assign',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': form_view.id,
            'res_model': 'hr.evaluate',
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'new'
        }

    # # validate function
    # @api.constrains('form_evaluate_ids', 'state', 'employee_confirm', 'petition', 'remark')
    # def _onchange_value(self):
    #     if (not self.form_evaluate_ids) and (self.employee_can_submit is True):
    #         raise UserError("Chọn ít nhất một nội dung công việc")
    #     if (not self.petition) and (self.employee_can_submit is True):
    #         raise UserError("Hãy điền vào phần Ý kiến, kiến nghị")
    #
    #     # if not self.remark:
    #     #     if self.state == 'pm':
    #     #         raise UserError("Hãy điền vào phần Ý kiến nhận xét")
    #     if (not self.employee_confirm) and (self.employee_can_submit is True):
    #         raise UserError("Nhân viên hãy chọn có tiếp tục hợp đồng không")

        # if not self.dl_confirm:
        #     if self.state == 'approve' and self.dl_can_assign is False:
        #         raise UserError("DL hãy chọn có tiếp tục hợp đồng không")

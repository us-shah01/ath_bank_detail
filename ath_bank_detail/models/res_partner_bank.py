from odoo import models, fields, api


class ResPartnerBank(models.Model):
    _name = 'res.bank'
    _inherit = ['res.bank','mail.thread','mail.activity.mixin']

    branch_name = fields.Char(string="Branch Name", required=True,tracking=True)
    name = fields.Char(tracking=True)
    bic = fields.Char(tracking=True)
    street = fields.Char(tracking=True)
    city = fields.Char(tracking=True)
    state = fields.Many2one('res.country.state',tracking=True)
    street2 = fields.Char(tracking=True)
    bank_display_name = fields.Char(string="Bank Name", compute="_compute_display_name")
    ifsc_code = fields.Char(string="IFSC Code", required=True,tracking=True)
    _sql_constraints = [
        ('unique_ifsc_code', 'unique(ifsc_code)', 'The IFSC Code must be unique!')
    ]

    @api.depends('name', 'ifsc_code', 'branch_name')
    def _compute_display_name(self):
        for bank in self:
            name_part = bank.name or ''
            branch_part = f" ({bank.branch_name})" if bank.branch_name else ''
            ifsc_part = f" - {bank.ifsc_code}" if bank.ifsc_code else ''
            bank.display_name = f"{name_part}{branch_part}{ifsc_part}"
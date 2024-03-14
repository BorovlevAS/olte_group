from odoo import api, fields, models


class StandardProtection(models.Model):
    _name = "standard.protection"

    record_number = fields.Char(string="Record number", default=lambda self: ("New"))
    name = fields.Char(string="Name")
    code = fields.Char(string="Code")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["record_number"] = self.env["ir.sequence"].next_by_code(
                "standard.protection"
            )
        return super().create(vals_list)

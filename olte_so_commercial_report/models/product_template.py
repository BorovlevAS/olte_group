from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    standard_protection = fields.Many2many(
        comodel_name="standard.protection", string="Standard for protection"
    )
    description = fields.Text(string="Description")

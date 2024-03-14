from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    standard_protection = fields.Many2many(
        comodel_name="standard.protection", string="Standard for protection"
    )
    model_description = fields.Text(string="Model description")

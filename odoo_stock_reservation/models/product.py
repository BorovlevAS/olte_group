from odoo import fields, models


class Product(models.Model):
    _inherit = "product.template"

    is_reservation = fields.Boolean(default=False, string="Is Reserved")

    reserver_id = fields.Many2one("res.users")

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    commercial_proposal_name = fields.Char()

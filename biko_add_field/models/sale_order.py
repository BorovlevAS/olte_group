from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    biko_payment_type_id = fields.Many2one(
        "biko.payment.type",
        string="Payment type",
    )

    biko_percentage_prepayment = fields.Integer("Percentage of partial prepayment")

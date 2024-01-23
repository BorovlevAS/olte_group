from odoo import fields, models


class PurchaseRequest(models.Model):
    _inherit = "purchase.request"

    sale_order_id = fields.Many2one(comodel_name="sale.order")

    def action_view_sale_order(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "res_id": self.sale_order_id.id,
            "view_mode": "form",
            "target": "current",
        }

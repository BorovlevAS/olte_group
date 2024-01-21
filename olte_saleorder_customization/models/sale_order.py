from odoo import _, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    purchase_request_id = fields.One2many("purchase.request", "sale_order_id")
    purchase_request_count = fields.Integer(
        string="Purchase request count", compute="_compute_purchase_request_count"
    )

    def create_purchase_request(self):
        create_vals = {
            "requested_by": self.env.user.id,
            "date_start": fields.Date.today(),
            "sale_order_id": self.id,
            "line_ids": [],
            "origin": self.name,
        }

        for line in self.order_line:
            create_vals["line_ids"].append(
                [
                    0,
                    0,
                    {
                        "product_id": line.product_id.id,
                        "name": line.name,
                        "product_qty": line.product_uom_qty,
                        "product_uom_id": line.product_uom.id,
                        "date_required": fields.Date.today(),
                    },
                ]
            )

        return self.env["purchase.request"].create(create_vals)

    def action_view_purchase_request(self, purchase_request_id):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "purchase_request.purchase_request_form_action"
        )

        action["views"] = [
            (self.env.ref("purchase_request.view_purchase_request_form").id, "form")
        ]
        action["res_id"] = purchase_request_id
        return action

    def action_create_purchase_request(self):
        purchase_request_id = self.create_purchase_request()

        return self.action_view_purchase_request(purchase_request_id.id)

    def _compute_purchase_request_count(self):
        for rec in self:
            rec.purchase_request_count = self.env["purchase.request"].search_count(
                [("sale_order_id", "=", rec.id)]
            )

    def action_purchase_request_count(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Purchase request"),
            "res_model": "purchase.request",
            "context": {"default_origin": self.id},
            "domain": [("sale_order_id", "=", [self.id])],
            "view_mode": "tree,form",
            "target": "current",
        }

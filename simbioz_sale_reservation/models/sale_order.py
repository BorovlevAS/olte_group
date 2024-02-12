from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    reserve_days = fields.Integer(
        string="Number of days",
        default=0,
    )

    state = fields.Selection(
        selection_add=[
            ("reserve", "In reserve"),
            ("sent",),
        ],
        ondelete={
            "reserve": "set default",
        },
    )

    def create_reservation(self):
        reservation_id = self.env["stock.reservation"].create(
            [{"sale_order_id": self.id}]
        )
        for line_id in self.order_line:
            self.env["stock.reservation.line"].create(
                [
                    {
                        "reservation_id": reservation_id.id,
                        "order_line_id": line_id.id,
                        "product_id": line_id.product_id.id,
                        "product_qty": line_id.product_uom_qty,
                        "uom_id": line_id.product_uom.id,
                        "stock_reservation_qty": line_id.product_uom_qty,
                    }
                ]
            )
        reservation_id.action_create_reservation()
        return True

    def _action_reserve(self):
        self.create_reservation()
        self.write({"state": "reserve"})

    def action_reserve(self):
        self._action_reserve()

    def action_draft(self):
        result = super().action_draft()
        for order_id in self:
            if order_id.state == "reserve":
                order_id.action_cancel_stock_reservation()
                order_id.write({"state": "draft"})
        return result

    def action_cancel_stock_reservation(self):
        result = super().action_cancel_stock_reservation()
        self.state = "draft"
        return result

    def schedule_action_cancel_reservation(self):
        date_obj = fields.datetime.now()
        reservations = self.env["stock.move.reservation"].search(
            [
                ("reserv_due_date", "<=", date_obj),
                ("reserv_due_date", "!=", False),
                ("state", "!=", "cancel"),
            ]
        )

        for reserve in reservations:
            reserve.custome_sale_order_id.action_cancel_stock_reservation()

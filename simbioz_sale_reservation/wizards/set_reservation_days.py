from odoo import _, fields, models
from odoo.exceptions import UserError


class SetReservationDays(models.TransientModel):
    _name = "set.reservation.days"

    order_id = fields.Many2one(
        "sale.order",
        string="Sale Order",
        readonly=True,
    )
    number_of_days = fields.Integer(string="Days of the reservation", default=0)

    def action_set_reserve(self):
        if self.number_of_days < 0:
            raise UserError(_("Please enter a valid number of days"))
        self.order_id.write({"reserve_days": self.number_of_days})
        return self.order_id._action_reserve()

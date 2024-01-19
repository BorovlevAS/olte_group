from odoo import api, fields, models


class SalesOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_image = fields.Image(compute="_compute_product_image")

    @api.depends("product_id.image_128")
    def _compute_product_image(self):
        for line in self:
            line.product_image = line.product_id.image_128

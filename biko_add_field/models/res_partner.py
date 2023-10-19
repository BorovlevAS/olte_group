# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    biko_brand_purchased_ids = fields.Many2many(
        "biko.brand.purchased",
        "biko_brand_purchased_res_partner_rel",
        "res_partner_id",
        "biko_brands_purchased_id",
        string="What brands do you buy?",
    )

    biko_work_before_ids = fields.Many2many(
        "res.partner",
        "biko_work_before_res_partner_rel",
        "res_partner_id",
        "biko_work_before_id",
        string="Who did you work with before?",
    )

    biko_amount_emploees = fields.Integer("Amount emploees")

    biko_budget_id = fields.Many2one(
        "biko.budget",
        string="Budget",
    )

    biko_agent_ids = fields.Many2many(
        "res.partner",
        "biko_agent_res_partner_rel",
        "res_partner_id",
        "biko_agent_id",
        string="Agent",
    )

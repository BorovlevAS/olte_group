from odoo import _, api, fields, models
from odoo.exceptions import UserError


class CrmLead(models.Model):
    _inherit = "crm.lead"

    biko_brand_purchased_ids = fields.Many2many(
        "biko.brand.purchased",
        "biko_brand_purchased_rel",
        "lead_id",
        "biko_brands_purchased_id",
        # compute="_compute_biko_brand_purchased_ids",
        # inverse="_inverse_biko_brand_purchased_ids",
        # store=True,
        string="What brands do you buy?",
    )

    biko_deal_type_id = fields.Many2one(
        "biko.deal.type",
        string="Type of deal",
    )

    biko_work_before_ids = fields.Many2many(
        "res.partner",
        "biko_work_before_rel",
        "lead_id",
        "biko_work_before_id",
        compute="_compute_biko_work_before_ids",
        inverse="_inverse_biko_work_before_ids",
        store=True,
        string="Who did you work with before?",
    )

    biko_amount_emploees = fields.Integer(
        "Amount emploees",
        # compute="_compute_biko_amount_emploees",
        # inverse="_inverse_biko_amount_emploees",
        # store=True,
    )

    biko_traffic_source_id = fields.Many2one(
        "biko.traffic.source",
        string="Traffic source",
    )

    biko_who_get_percentage_ids = fields.Many2many(
        "hr.employee",
        "biko_who_get_rel",
        "lead_id",
        "biko_who_get_percentage_id",
        string="Who get %?",
    )

    biko_requirement = fields.Char("For what need have you gone wild?")

    biko_feedback = fields.Char("Feedback")

    biko_brand_ids = fields.Many2many(
        "biko.brand",
        "biko_brand_rel",
        "lead_id",
        "biko_brands_id",
        string="Brand/analogue",
    )

    biko_budget_id = fields.Many2one(
        "biko.budget",
        string="Budget",
        # compute="_compute_biko_budget_id",
        # inverse="_inverse_biko_budget_id",
        # store=True,
    )

    biko_agent_ids = fields.Many2many(
        "res.partner",
        "biko_agent_rel",
        "lead_id",
        "biko_agent_id",
        string="Agent",
        # compute="_compute_biko_agent_ids",
        # inverse="_inverse_biko_agent_ids",
        # store=True,
    )

    biko_link_tender = fields.Char(string="Link to the tender/documentation")

    biko_tender_offer_number = fields.Char(string="Tender offer number")

    biko_submission_deadline = fields.Datetime(string="Submission deadline")

    biko_auction_date = fields.Datetime(string="Auction date")

    biko_deliveries_date = fields.Datetime(string="Delivery date")

    biko_resume = fields.Char(string="Summary of this agreement")

    biko_who_find_tender = fields.Many2one(
        "hr.employee",
        string="Who found the tender",
    )

    biko_payment_type_id = fields.Many2one(
        "biko.payment.type",
        string="Payment type",
    )

    biko_percentage_prepayment = fields.Integer("Percentage of partial prepayment")

    biko_head = fields.Many2one(
        "hr.employee",
        string="Head",
    )

    biko_rop = fields.Many2one(
        "hr.employee",
        string="ROP",
    )

    biko_financial_director = fields.Many2one(
        "hr.employee",
        string="Financial director",
    )

    biko_manage_director = fields.Many2one(
        "hr.employee",
        string="Manage director",
    )

    biko_interested_in = fields.Char(
        string="What kind of in-service training are you interested in?"
    )
    biko_best_result = fields.Char(string="What is the best outcome for you")

    biko_execution_of_date = fields.Datetime(string="The term of execution of")
    biko_execution_to_date = fields.Datetime(string="Deadline until")

    biko_checklist_link = fields.Char(
        string="Link to the checklist from the client's words"
    )

    def _prepare_customer_values(self, partner_name, is_company=False, parent_id=False):
        values = super()._prepare_customer_values(
            partner_name, is_company=is_company, parent_id=parent_id
        )

        values.update(
            {
                "biko_brand_purchased_ids": self.biko_brand_purchased_ids.ids,
                "biko_work_before_ids": self.biko_work_before_ids.ids,
                "biko_amount_emploees": self.biko_amount_emploees,
                "biko_budget_id": self.biko_budget_id.id,
                "biko_agent_ids": self.biko_agent_ids.ids,
            }
        )

        return values

    @api.depends(
        "email_from",
        "phone",
        "partner_id",
        "biko_brand_purchased_ids",
        "biko_work_before_ids",
        "biko_amount_emploees",
        "biko_budget_id",
        "biko_agent_ids",
    )
    def _compute_ribbon_message(self):
        for lead in self:
            tracking_fields = {
                "phone": lead._get_partner_email_update(),
                "email": lead._get_partner_phone_update(),
                # _("What brands do you buy?"): lead._get_partner_field_update(
                #     "biko_brand_purchased_ids"
                # ),
                _("Who did you work with before?"): lead._get_partner_field_update(
                    "biko_work_before_ids"
                ),
                # _("Amount emploees"): lead._get_partner_field_update(
                #     "biko_amount_emploees"
                # ),
                # _("Budget"): lead._get_partner_field_update("biko_budget_id"),
                # _("Agent"): lead._get_partner_field_update("biko_agent_ids"),
            }

            msg = ""
            for key, value in tracking_fields.items():
                if value:
                    msg += f"{key.capitalize()}, "

            lead.ribbon_message = (
                _("By saving this change, the customer's fields: ")
                + msg.format(msg=msg[:-2])
                + _("will also be updated.")
                if msg
                else False
            )

    def _get_partner_field_update(self, name_field):
        """Calculate if we should write the name_field on the related partner. When
        name_field of the lead / partner is an empty string, we force it to False
        to not propagate a False on an empty string.

        Done in a separate method so it can be used in both ribbon and inverse
        and compute of name_field update methods.
        """
        self.ensure_one()
        if self.partner_id and self[name_field] != self.partner_id[name_field]:
            lead_name_field_formatted = (
                self[name_field].ids if ("ids" in name_field) else self[name_field]
            )
            partner_name_field_formatted = (
                self.partner_id[name_field].ids
                if ("ids" in name_field)
                else self.partner_id[name_field]
            )
            return lead_name_field_formatted != partner_name_field_formatted
        return False

    def inverse_name_field(self, name_field):
        for lead in self:
            if lead._get_partner_field_update(name_field):
                lead.partner_id[name_field] = lead[name_field]

    @api.depends("partner_id")
    def _compute_biko_brand_purchased_ids(self):
        for lead in self:
            lead.update(
                {"biko_brand_purchased_ids": lead.partner_id.biko_brand_purchased_ids}
            )

    def _inverse_biko_brand_purchased_ids(self):
        self.inverse_name_field("biko_brand_purchased_ids")

    @api.depends("partner_id")
    def _compute_biko_work_before_ids(self):
        for lead in self:
            lead.update({"biko_work_before_ids": lead.partner_id.biko_work_before_ids})

    def _inverse_biko_work_before_ids(self):
        self.inverse_name_field("biko_work_before_ids")

    @api.depends("partner_id")
    def _compute_biko_amount_emploees(self):
        for lead in self:
            lead.update({"biko_amount_emploees": lead.partner_id.biko_amount_emploees})

    def _inverse_biko_amount_emploees(self):
        self.inverse_name_field("biko_amount_emploees")

    @api.depends("partner_id")
    def _compute_biko_budget_id(self):
        for lead in self:
            lead.update({"biko_budget_id": lead.partner_id.biko_budget_id})

    def _inverse_biko_budget_id(self):
        self.inverse_name_field("biko_budget_id")

    @api.depends("partner_id")
    def _compute_biko_agent_ids(self):
        for lead in self:
            lead.update({"biko_agent_ids": lead.partner_id.biko_agent_ids})

    def _inverse_biko_agent_ids(self):
        self.inverse_name_field("biko_agent_ids")

    def action_create_quotation(self):
        if self.partner_id:
            vals = {
                "default_partner_id": self.partner_id.id,
                "default_team_id": self.team_id.id,
                "default_campaign_id": self.campaign_id.id,
                "default_medium_id": self.medium_id.id,
                "default_source_id": self.source_id.id,
                "default_opportunity_id": self.id,
                "default_biko_payment_type_id": self.biko_payment_type_id.id,
                "default_biko_percentage_prepayment": self.biko_percentage_prepayment,
                # 'default_order_line': order_lines, # created by onchange method on field 'opportunity_id' on model 'sale.order'
            }
        else:
            raise UserError(
                _("In order to create sale order, Customer field should not be empty!")
            )

        return {
            "name": "Create Sale Quotation",
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "sale.order",
            "target": "current",
            "context": vals,
        }

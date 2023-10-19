from odoo import fields, models


class BikoBrandPurchased(models.Model):
    _name = "biko.brand.purchased"
    _description = "Brands purchased"

    name = fields.Char(string="Name", required=True, translate=True)


class BikoDealType(models.Model):
    _name = "biko.deal.type"
    _description = "Type of deal"

    name = fields.Char(string="Name", required=True, translate=True)


class BikoTrafficSource(models.Model):
    _name = "biko.traffic.source"
    _description = "Traffic source"

    name = fields.Char(string="Name", required=True, translate=True)


class BikoBrand(models.Model):
    _name = "biko.brand"
    _description = "Brand/analogue"

    name = fields.Char(string="Name", required=True, translate=True)


class BikoBudget(models.Model):
    _name = "biko.budget"
    _description = "Budget"

    name = fields.Char(string="Name", required=True, translate=True)


class BikoPaymentType(models.Model):
    _name = "biko.payment.type"
    _description = "Payment type"

    name = fields.Char(string="Name", required=True, translate=True)

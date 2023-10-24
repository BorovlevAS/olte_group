{
    "name": "BIKO: add field in objects",
    "version": "14.0.1.0.0",
    "author": "Zhmyhova T.N.",
    "company": "BIKO Solutions",
    "depends": [
        "crm",
        "sale",
        "hr",
        "crm_opportunity_product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/crm_lead_view.xml",
        "views/res_partner_view.xml",
        "views/sale_order_views.xml",
        "views/biko_add_field_view.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
    "application": True,
    "auto_install": False,
}

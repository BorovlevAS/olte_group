{
    "name": "BIKO: olte_so_commercial_report",
    "version": "14.0.1.0.0",
    "author": "Yevdokimova A.Y.",
    "company": "BIKO Solutions",
    "depends": [
        "sales_team",
        "sale",
        "product",
        "stock",
        "web",
        "res_partner_telegram",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "views/standard_protection_view.xml",
        "views/product_template.xml",
        "views/product_product.xml",
        "views/sale_order.xml",
        "reports/report.xml",
        "reports/report_printed_fields.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
    "application": True,
    "auto_install": False,
}

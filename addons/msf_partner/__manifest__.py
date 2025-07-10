{
    "name": "MSF Partner",
    "version": "18.0.1.0.0",
    "category": "",
    "summary": "Port of partner extension modules from Unifield",
    "author": "TeMPO Consulting",
    "website": "https://tempo-consulting.fr",
    "license": "LGPL-3",
    "depends": ["uom"],
    "data": [
        "security/ir.model.access.csv",

        "views/res_partner_views.xml",

        "menus/partner_menus.xml",
    ],
    "installable": True,
    "auto_install": False,
}

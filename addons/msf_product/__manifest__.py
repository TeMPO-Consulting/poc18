{
    "name": "MSF Product",
    "version": "18.0.1.0.0",
    "category": "",
    "summary": "Port of product modules from Unifield",
    "author": "TeMPO Consulting",
    "website": "https://tempo-consulting.fr",
    "license": "LGPL-3",
    "depends": ["uom"],
    "data": [
        "security/ir.model.access.csv",

        "views/product_nomenclature_views.xml",
        "views/product_product_views.xml",
        "views/uom_views.xml",

        "menus/supply_configuration_menus.xml",
        "menus/product_menus.xml",
    ],
    "installable": True,
    "auto_install": False,
}

# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#################################################################################

{
    'name'          : "Odoo Map Widget",

    'summary'       : """
    The module offers an ease to the customers to add map widget in core Odoo forms as well as custom.
    """,

    'description'   : """
    Odoo Map Widget allows you to add the map widget in any of the form views in Odoo. 
    You can simply mark the location in the map by adding its longitude along with its latitude.
    The module offers an ease to the customers to add map widget in core Odoo forms as well as custom.
""",

     'author'       : "Webkul Software Pvt. Ltd.",
    "license"       :  "Other proprietary",
    'website'       : "https://www.webkul.com",
    'live_test_url' : 'http://odoodemo.webkul.com/?module=odoo_map_widget',

    'category'      : 'Utility',
    'version'       : '1.0.3',

    'depends'       : ['base_geolocalize'],

    'data'          : [
                        'security/ir.model.access.csv',
                        'views/assets.xml',
                        'views/views.xml',
                        'views/templates.xml',
                        ],

    "images"        :  ['static/description/banner.png'],
    "price"         :  59,
    "currency"      :  "USD",
    'sequence'      :   1,
}

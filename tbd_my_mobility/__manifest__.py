# -*- coding: utf-8 -*-
{
    'name': "My Mobility by TBD",
    'version': '14.0.0.3',
    'author': "Agence TBD",
    'website': "https://www.agence-tbd.com",
    'category': 'Website',
    'summary':
        """
            My Mobility base
        """,
    'description':
        """
            * 14.0.0.3 Add addons OCA contract
            * 14.0.0.2 Add addons OCA partner_firstname
            * 14.0.0.1 Installateur TBD
        """,
    'depends': [
        'base',
        'timesheet_grid',
        'hr',
        'sale',
        'account',
        'hr_holidays',
        'helpdesk',
        'contacts',
        'fleet',
        'website',
        'website_sale',
        'partner_firstname',
        'contract',
        'project',
        'odoo_map_widget'
    ],
    'data': [
        'views/res_partner_view.xml',
        'views/project_task_view.xml',
        'views/project_project_view.xml',
        'views/contract_contract_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
        'static/src/xml/import_button.xml'
    ],
    'application': True,
    'installable': True,
    'active': True
}

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Innoving Solde Progressive',
    'version': '1.0.0',
    'category': 'Invoicing Management',
    'summary': 'Innoving Accounting Solde Progressive Reports',
    'sequence': '40',
    'author': 'Innoving',
    'company': 'Innoving',
    'maintainer': 'Innoving',
    'support': 'innoving2021@gmail.com',
    'website': '',
    'depends': ['account',],
    'live_test_url': '',
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'wizards/innoving_solde_progressive.xml',
        #'wizards/innoving_partner_ledger.xml',
        #'wizards/innoving_account_ledger.xml',
        #'reports/innoving_report.xml',
        #'reports/innoving_report_partner_ledger.xml',
        #'reports/innoving_report_account_ledger.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': ['static/description/banner.gif'],
    'qweb': [],
}

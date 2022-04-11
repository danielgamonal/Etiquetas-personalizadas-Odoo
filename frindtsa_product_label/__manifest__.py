# -*- coding: utf-8 -*-
# @author: Daniel Gamonal (daniel.gamonal@frindtsa.cl)
# @author: Esteban Almonacid (esteban.almonacid@gfrindtsa.cl)
{
    
    'name': 'Fleje Personalizado',
    'category': 'Extra Tools',
    'author': 'Frindt s.a',
    'website': 'https://ferreteriafrindt.cl',
    'license': 'LGPL-3',
    'summary': 'imprimir flejes personalizados',
    'depends': [
        'product',
    ],
    'data': [
        'wizard/print_product_label_views.xml',
        'report/product_label_reports.xml',
        'report/product_label_templates.xml',
    ],
    'external_dependencies': {
    },
    'support': 'soporte@frindtsa.cl',
    'application': False,
    'installable': True,
    'auto_install': False,
}
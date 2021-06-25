# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################

{
    'name': 'Horas Extras',
    'version': '1.0',
    'category': 'Modulos Generales/RRHH',
    'description': """
    Calculo de horas extras
    """,
    'author': 'Mario Chogllo',
    'website': 'http://www.goberp.com',
    'depends': ['gt_hr_base'],
    'init_xml': [],
    'update_xml': [
        'extras_view.xml',
#        'security/ir.model.access.csv',
        ],
    'demo_xml': [],
    'installable': True,
    'active': True,
}

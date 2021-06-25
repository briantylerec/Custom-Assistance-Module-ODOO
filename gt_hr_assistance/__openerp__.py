# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################

{
    'name': 'Asistencia',
    'version': '1.0',
    'category': 'Modulos Generales/RRHH',
    'description': """
    cargar las asistencias
    """,
    'author': 'Mario Chogllo',
    'website': 'http://www.goberp.com',
    'depends': ['gt_hr_base'],
    'init_xml': [],
    'update_xml': [
        'asistencia_view.xml',
#        'security/ir.model.access.csv',
        ],
    'demo_xml': [],
    'installable': True,
    'active': True,
}

{
    'name': 'reader_carte',
    'version': '1.0',
    'author': 'Votre Nom',
    'category': 'Human Resources',
    'summary': 'Module to create employees using RFID cards',
    'description': """
    This module allows creating employees by reading RFID cards. The card number is saved as the employee ID.
    """,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/carte.xml',
        'views/historique.xml',
        'views/liste_passager.xml',



    ],
'assets': {
        'web.assets_backend': [
            'reader_carte/static/src/css/style.css',

        ],

    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
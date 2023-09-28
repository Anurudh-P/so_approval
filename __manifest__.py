{
    'name': 'SO Approval',
    'version': '16.0.1.0.0',
    'sequence': 16,
    'summary': 'Sale order approval',
    'depends': [
        'base_setup',
        'sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/so_approval_user_groups.xml',
        'views/so_approval_view.xml',
        'wizards/warning_wizard_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}

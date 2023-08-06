{
    'name': "Odoo Biba Ardoak customizations",
    'version': '14.0.0.0.5',
    'depends': [
        'base',
        'sale_stock',
        'stock_picking_batch',
    ],
    'author': "Coopdevs Treball SCCL",
    'website': 'https://coopdevs.org',
    'category': "Cooperative management",
    'description': """
    Odoo Biba Ardoak customizations.
    """,
    "license": "AGPL-3",
    'data': [
        "data/ir_config_parameter.xml",
        "report/account_invoice_report_view.xml",
        "report/delivery_note_mail_template.xml",
        "report/report_picking_batch_delivery_note.xml",
        "report/stock_picking_batch_report_views.xml",
        "views/report_view.xml",
        "wizards/stock_picking_batch/stock_picking_batch.xml"
    ],
}

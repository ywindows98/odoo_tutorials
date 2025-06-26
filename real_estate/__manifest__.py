

{
    'name': 'Real Estate',
    'depends': ['base'],
    'version': '0.1',
    'summary': 'Store real estate listings and control offers.',
    'author': 'ywindows98',
    'application': True,
    'category': 'Real Estate',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
        'data/estate.property.tag.csv',
        'demo/estate.property.xml'
    ],
}
from odoo import models, fields, api

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    bedrooms = fields.Integer(string='Bedrooms')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Float(string='Gargen Area (sqm)', digits=(8,2))
    living_area = fields.Float(string='Living Area (sqm)', digits=(8,2))
    expected_price = fields.Float(string='Expected Price', digits=(16,2), required=True)
    date_availability = fields.Date(string='Available From')
    garden_orientation = fields.Selection(string='Garden Orientation', selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])


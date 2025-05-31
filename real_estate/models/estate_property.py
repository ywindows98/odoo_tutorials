from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    property_type_id = fields.Many2one(string='Property Type', comodel_name='estate.property.type')
    postcode = fields.Char(string='Postcode')
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Float(string='Gargen Area (sqm)', digits=(8,2))
    living_area = fields.Float(string='Living Area (sqm)', digits=(8,2))
    total_area = fields.Float(string='Total Area (sqm)', digits=(10,2), compute='_compute_total_area')
    expected_price = fields.Float(string='Expected Price', digits=(16,2), required=True)
    selling_price = fields.Float(string='Selling Price', digits=(16, 2), readonly=True, copy=False)
    best_price = fields.Float(string='Best Price', digits=(16,2), compute='_compute_best_price')
    availability_date = fields.Date(string='Available From', copy=False, default=date.today() + relativedelta(months=3))
    garden_orientation = fields.Selection(string='Garden Orientation', selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])

    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(string='State', default='new', selection=[
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ])

    user_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    client_id = fields.Many2one('res.partner', string='Buyer')

    tag_ids = fields.Many2many('estate.property.tag', string='Tags')


    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")



    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)
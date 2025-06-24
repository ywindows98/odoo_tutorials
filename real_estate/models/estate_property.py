from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

from datetime import date
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    # 1. Private attributes (_name, _description, _inherit, _sql_constraints, …)
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = 'id desc'

    # 2. Default method and default_get

    # 3. Field declarations
    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    property_type_id = fields.Many2one(string='Property Type', comodel_name='estate.property.type')
    postcode = fields.Char(string='Postcode')
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Float(string='Garden Area (sqm)', digits=(8,2))
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
    partner_id = fields.Many2one('res.partner', string='Buyer')

    tag_ids = fields.Many2many('estate.property.tag', string='Tags')


    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price of the property must be strictly positive.'),

        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price of the property must be positive.')
    ]

    # 4. Compute, inverse and search methods in the same order as field declaration
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    # 5. Selection method (methods used to return computed values for selection fields)

    # 6. Constrains methods (@api.constrains) and onchange methods (@api.onchange)
    @api.constrains('selling_price', 'expected_price')
    def check_selling_price(self):
        for record in self:
            if (not float_is_zero(record.selling_price, precision_digits=2)
                    and record.expected_price > record.selling_price):
                if record.selling_price < record.expected_price * 0.9:
                    raise ValidationError('The selling price must be at least 90% of the expected price! '
                                          'You have to lower the expected price to accept this offer.')

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None
            return {'warning': {
                'title': _("Warning"),
                'message': ('The garden option is removed from this property.')}}

    # Implemented in the offer CRUD methods
    # @api.onchange('offer_ids')
    # def _onchange_offer_ids(self):
    #     if len(self.offer_ids)>0 and self.state not in ['offer_received', 'offer_accepted', 'sold', 'canceled']:
    #         self.state = 'offer_received'

    # 7. CRUD methods (ORM overrides)
    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_canceled(self):
        allowed_delete_states = ['new', 'canceled']
        if not all(record.state in allowed_delete_states for record in self):
            raise UserError('An estate property can\'t be deleted if it is not New or not Canceled.')

    # 8. Action methods
    def action_sell_estate_property(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError('A canceled property can\'t be sold.')
            else:
                record.state = 'sold'

        return True

    def action_cancel_estate_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('A sold property can\'t be canceled.')
            else:
                record.state = 'canceled'

        return True

    # 9. And finally, other business methods.
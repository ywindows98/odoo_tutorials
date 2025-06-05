from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    # name = fields.Char(string='Name', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    price = fields.Float(string='Price', digits=(16,2))
    status = fields.Selection(string='Status', copy=False, selection=[
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ])

    property_type_id = fields.Many2one(string='Property Type', related='property_id.property_type_id', store=True)

    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'The offer price must be strictly positive.')
    ]

    # CRUD methods
    @api.model
    def create(self, vals):
        property_id = self.env['estate.property'].browse(vals['property_id'])
        max_price = max(property_id.offer_ids.mapped('price'), default=0)

        if vals['price'] < max_price:
            raise UserError(_('A new offer can only have a price higher or equal to the highest existing offer (%s).',
                              max_price))
        else:
            if property_id.state not in ['offer_accepted', 'sold', 'canceled']:
                property_id.state = 'offer_received'

        # The parent method
        return super().create(vals)

    # Compute/Onchange
    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (record.create_date or fields.Date.today()) + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    # Utility
    def _check_for_accepted_offers(self):
        related_property = self.property_id
        if 'accepted' in related_property.offer_ids.mapped('status'):
            return True

        return False

    # Actions
    def accept_estate_property_offer_action(self):
        if not self._check_for_accepted_offers():
            self.status = 'accepted'
            related_property = self.property_id
            related_property.selling_price = self.price
            related_property.partner_id = self.partner_id
            if related_property.state not in ['offer_accepted', 'sold', 'canceled']:
                related_property.state = 'offer_accepted'
        else:
            raise UserError('Multiple offers can\'t be accepted at the same time.')

        return True

    def refuse_estate_property_offer_action(self):
        if self.status == 'accepted':
            related_property = self.property_id
            related_property.selling_price = None
            related_property.partner_id = None

        self.status = 'refused'


        return True


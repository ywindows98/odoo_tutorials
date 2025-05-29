from odoo import models, fields, api

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    # name = fields.Char(string='Name', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    price = fields.Float(string='Price', digits=(16,2))
    status = fields.Selection(string='Status', copy=False, selection=[
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ])

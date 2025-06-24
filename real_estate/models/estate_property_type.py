from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')

    sequence = fields.Integer(string='Sequence', default=1, help='Used to order types. Lower is better.')

    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(string='Offers Count', compute='_compute_offer_count')

    _sql_constraints = [
        ('unique_name', 'unique (name)', 'This type already exists!')
    ]

    # 4. Compute, inverse and search methods in the same order as field declaration
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)

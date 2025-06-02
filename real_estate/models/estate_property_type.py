from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')

    sequence = fields.Integer(string='Sequence', default=1, help='Used to order types. Lower is better.')

    _sql_constraints = [
        ('unique_name', 'unique (name)', 'This type already exists!')
    ]
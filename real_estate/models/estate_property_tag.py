from odoo import models, fields, api

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name'

    name = fields.Char(string='Name', required=True)

    _sql_constraints = [
        ('unique_name', 'unique (name)', 'This tag already exists!')
    ]
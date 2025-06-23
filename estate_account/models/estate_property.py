from odoo import models, fields, api, _, Command
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

from datetime import date
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _inherit = 'estate.property'



    def sell_estate_property_action(self):
        journal = self.env['account.journal'].search([
            ('type', '=', 'sale'),
            ('company_id', '=', self.env.company.id)
        ], limit=1)

        if not journal:
            raise UserError("No Sales Journal found.")

        invoice_vals_list = []

        invoice_vals = {
            # 'name': f'{self.name} sell invoice',
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'journal_id': journal.id,
            'invoice_line_ids': []
        }

        invoice_line_vals = [
            Command.create({
                "name": "Service fees",
                "quantity": 1,
                "price_unit": self.selling_price * 0.06  # 6% of the selling price as a service fee
            }),
            Command.create({
                "name": "Administrative fees",
                "quantity": 1,
                "price_unit": 100  # 100 as the administrative fees
            })
        ]

        invoice_vals['invoice_line_ids'] += invoice_line_vals
        invoice_vals_list.append(invoice_vals)

        invoice = self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals_list)

        invoice.action_post()

        return super().sell_estate_property_action()
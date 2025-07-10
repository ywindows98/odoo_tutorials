# -*- coding: utf-8 -*-
from odoo import Command
from .common import RealEstateTestCommon
from odoo.tests import tagged
from odoo.tests.common import Form
from odoo.exceptions import UserError, ValidationError
from odoo.tools import mute_logger
import psycopg2
from freezegun import freeze_time


@tagged('post_install', '-at_install')
class TestEstateProperty(RealEstateTestCommon):
    def test_sell_property_with_no_offers(self):
        offer_vals = {
            'property_id': self.property_with_no_accepted_offers_sample.id,
            'partner_id': self.simple_partner.id,
            'price': 120000
        }

        offer = self.env['estate.property.offer'].create(offer_vals)

        with self.assertRaises(UserError):
            self.property_with_no_accepted_offers_sample.action_sell_estate_property()

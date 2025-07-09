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

    def test_create_offer_for_sold_property(self):
        offer_vals = {
            'property_id': self.sold_property_sample.id,
            'partner_id': self.simple_partner.id,
            'price': 150000
        }

        self.sold_property_sample = self.env['estate.property.offer'].create(offer_vals)

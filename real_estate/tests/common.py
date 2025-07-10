from odoo import fields, Command
from odoo.tests.common import TransactionCase, HttpCase, tagged, Form

import json
import time
import base64
from lxml import etree
from unittest import SkipTest


class RealEstateTestCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.simple_partner = cls.env['res.partner'].create({
            'name': 'simple partner'
        })

        cls.simple_company = cls.env['res.company'].create({
            'name': 'simple company'
        })

        cls.simple_agent = cls.env['res.users'].create({
            'name': 'simple agent',
            'login': 'simple_agent',
            'password': 'simple_agent',
            # [(6, 0, [])]
            'company_ids': [Command.set([cls.simple_company.id])],
            'company_id': cls.simple_company.id,
            'groups_id': [
                Command.link(cls.env.ref('real_estate.group_real_estate_user').id)
            ],
        })

        cls.sold_property_sample = cls.env['estate.property'].create({
            'name': 'Sold Property Test',
            'expected_price': 144000,
            'user_id': cls.simple_agent.id,
            'company_id': cls.simple_agent.company_id.id,
            'state': 'sold'
        })

        cls.property_with_no_accepted_offers_sample = cls.env['estate.property'].create({
            'name': 'Sold Property Test',
            'expected_price': 112000,
            'user_id': cls.simple_agent.id,
            'company_id': cls.simple_agent.company_id.id
        })
# -*- coding: utf-8 -*-
# © <2012> <Israel Cruz Argil, Argil Consulting>
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class AccountPayment(models.Model):
    _name = 'account.payment'
    _inherit = 'account.payment'

    advance_ids = fields.One2many(
        'tms.advance',
        'payment_id',
        string='Advances')

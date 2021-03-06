# -*- coding: utf-8 -*-
# © <2012> <Israel Cruz Argil, Argil Consulting>
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from datetime import datetime

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError

_logger = logging.getLogger(__name__)
try:
    from sodapy import Socrata
except ImportError:
    _logger.debug('Cannot `import sodapy`.')


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    driver_license = fields.Char(string="License ID")
    license_type = fields.Char(string="License Type")
    days_to_expire = fields.Integer(compute='_compute_days_to_expire')
    license_valid_from = fields.Date()
    license_expiration = fields.Date()

    @api.depends('license_expiration')
    def _compute_days_to_expire(self):
        for rec in self:
            if rec.license_expiration:
                date = datetime.strptime(rec.license_expiration, '%Y-%m-%d')
            else:
                date = datetime.now()
            now = datetime.now()
            delta = date - now
            rec.days_to_expire = delta.days if delta.days > 0 else 0

    @api.onchange('driver_license')
    def _onchange_driver_license(self):
        client = Socrata("www.datossct.gob.mx", None)
        try:
            driver_license = client.get(
                '3qhi-59v6', licencia=self.driver_license)
            license_valid_from = datetime.strptime(
                driver_license[0]['fecha_inicio_vigencia'],
                '%Y-%m-%dT%H:%M:%S.%f')
            license_expiration = datetime.strptime(
                driver_license[0]['fecha_fin_vigencia'],
                '%Y-%m-%dT%H:%M:%S.%f')
            self.license_type = driver_license[0]['categoria_de_la_licencia']
            self.license_valid_from = license_valid_from
            self.license_expiration = license_expiration
            client.close()
        except:
            client.close()
            raise ValidationError(_(
                'The driver license is not in SCT database'))

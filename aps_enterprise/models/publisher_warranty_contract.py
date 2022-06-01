# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import datetime
from datetime import timedelta
import logging

import requests
import werkzeug.urls

from ast import literal_eval

from odoo import api, release, SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.models import AbstractModel
from odoo.tools.translate import _
from odoo.tools import config, misc, ustr

_logger = logging.getLogger(__name__)

class PublisherWarrantyContract(AbstractModel):
    _name = "publisher_warranty.contract"
    _description = "Odoo Enterprise Correction"

    def update_notification(self, cron_mode=True):
        """
        Send a message to Odoo's publisher warranty server to check the
        validity of the contracts, get notifications, etc...

        @param cron_mode: If true, catch all exceptions (appropriate for usage in a cron).
        @type cron_mode: boolean
        """
        try:
            # Update expiration date
            expiration_date = datetime.datetime.now() + datetime.timedelta(days=1825)
            set_param = self.env['ir.config_parameter'].sudo().set_param
            set_param('database.expiration_date',  expiration_date)
        except Exception:
            if cron_mode:
                return False    # we don't want to see any stack trace in cron
            else:
                raise
        return True
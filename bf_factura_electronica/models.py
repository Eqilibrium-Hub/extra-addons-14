# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json
import base64

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    def get_name_invoice(self):
        aux = self.name
        #print(self.l10n_latam_document_type_id)
        if (self.l10n_latam_document_type_id.id in [3,8,13,35]):
            #print(self.ref)
            #print(self.reversed_entry_id.name)
            #name = f"{aux} ({self.invoice_origin})"
            name = f"{aux} ({self.reversed_entry_id.name})"
        else:
            name=aux
        return name

    def get_tax_details(self):
        taxs = self.env['account.tax'].search([('type_tax_use','=','sale'),('amount_type','=','percent')],order='amount desc')
        tax_data = {}
        for t in taxs:
            tax_data[t.name] = 0
        for t in self.line_ids:
            if t.tax_line_id:
                tax_data[t.tax_line_id.name] = t.price_total
            a=1
        return tax_data

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _compute_price_subtotal_vat(self):
        for line in self:
            if line.tax_ids:
                for tax_id in line.tax_ids:
                    if tax_id.tax_group_id.l10n_ar_vat_afip_code in [5,6,4,9,0,1,2,3,8]:
                        line.price_subtotal_vat = line.price_subtotal * \
                            (1 + tax_id.amount / 100)
                    else:
                        line.price_subtotal_vat = line.price_subtotal
            else:
                line.price_subtotal_vat = 0

    price_subtotal_vat = fields.Float(
        'price_subtotal_vat', compute=_compute_price_subtotal_vat)
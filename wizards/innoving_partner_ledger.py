# -*- coding: utf-8 -*-
import base64
import datetime
from email.policy import default
import hashlib
import pytz
import threading

from email.utils import formataddr
from lxml import etree

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.modules import get_module_resource
from odoo.osv.expression import get_unaccent_wrapper
from odoo.exceptions import UserError, ValidationError
from odoo.osv.orm import browse_record
from datetime import datetime
from datetime import date

from odoo.osv import expression
from odoo.tools.float_utils import float_round as round
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import html_translate



class InnovingPartnerLedger(models.TransientModel):
    _name = 'innoving.partner.ledger'
    _description = 'Innoving partner ledger'


    
    partner_id = fields.Many2one('res.partner', string='Partenaire')
    partner_name = fields.Char('Partenaire')
    account_code = fields.Char('Code')
    account_name = fields.Char('Compte')
    periode_id = fields.Many2one('periode', string='Période')
    date_from = fields.Date('Date début')
    date_to = fields.Date('date fin')
    somme_credit = fields.Float(string='Somme credit')  
    somme_debit = fields.Float(string='Somme debit')
    solde_progressif = fields.Float(string='Solde pregressif')
    selon = fields.Selection(string="Selon", selection=[
        ('Date', 'Date'),
        ('Periode', 'Période')], default='Date')
    journal_ids = fields.Many2many('account.journal', 'innoving_partner_ledger_journal_rel', 'partner_id', 'journal_id', string='Journaux', default=[])
    
    
    @api.onchange('periode_id')
    def onchange_periode_id(self):
        if self.periode_id:
            periode = self.env['periode'].search([('id','=',self.periode_id.id)])
            if periode.id:
                #self.ticket_html = self.req_ticket_html()
                self.date_from = periode.date_from
                self.date_to = periode.date_to
        return {}

    @api.onchange('date_from','date_to')
    def onchange_periode_date(self):
        if self.date_from and self.date_to:
            if self.date_from > self.date_to:
                raise UserError(_('Attention, vérifier les dates !')) 
        return {}
    
    
    
    @api.multi
    def print_report(self):        
        domain = []
        partner_id = self.partner_id.id
        partner_name = self.partner_id.name
        date_from = self.date_from
        date_to = self.date_to
        somme_credit = 0.0
        somme_debit = 0.0
        solde_progressif = 0.0
        journaux = [line.id for line in self.journal_ids]
        somme = 0.0
        
        if date_from:
            domain += [('date', '>=', date_from)]
        if date_to:
            domain += [('date', '<=', date_to)]
        if partner_id:
            domain += [('partner_id', '=', partner_id)]
        if self.journal_ids:
            domain += [('journal_id', 'in', journaux)]
        #payslips = self.env['hr.payslip'].search(domain)
        payslips = self.env['account.move.line'].search_read(domain, order='date asc')
        payslips_list =  []
        for payslip in payslips:

            somme_credit += payslip['credit']
            somme_debit += payslip['debit']
            solde_progressif = somme + (payslip['debit'] - payslip['credit'])

            if payslip['partner_id'] == False:
                partner = ""
            else:
                partner = payslip['partner_id'][1] 
            vals = {
                'account_id': payslip['account_id'],
                'date': payslip['date'],
                'piece': payslip['move_id'][1],
                'name': payslip['name'],
                'credit': payslip['credit'],
                'debit': payslip['debit'],
                'balance': solde_progressif,
                'partner_id': partner,
                'account': payslip['account_id'][1],
                'journal': payslip['journal_id'][1],
            }
            
            #raise UserError(_('%s') % (payslip['partner_id']))
            payslips_list.append(vals)
            somme = solde_progressif
            #raise UserError(_('%s') % (payslip['analytic_account_id']))
        self.partner_name = partner_name
        self.somme_credit = somme_credit
        self.somme_debit = somme_debit
        self.somme_balance = solde_progressif

        data = {
            'form_data': self.read()[0],
            'payslips': payslips_list,
        }    
        return self.env.ref('innoving_grand_livre.action_innoving_partner_ledger').report_action(self, data=data)
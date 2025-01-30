from odoo import models, fields, api

class CarteRFIDHistorique(models.Model):
    _name = 'altex.rfid.historique'
    _description = 'Historique des montants ajoutés aux cartes RFID'


    rfid_id = fields.Many2one('altex.rfid', string='Carte RFID', required=True, ondelete='cascade')
    montant_ajoute = fields.Monetary(string='Montant ajouté', required=True, currency_field='currency_id')
    date_ajout = fields.Datetime(string="Date d'ajout", default=fields.Datetime.now, readonly=True)
    currency_id = fields.Many2one('res.currency', string='Devise', required=True,
                                  default=lambda self: self.env.company.currency_id.id)

    @api.model
    def create(self, vals):

        record = super(CarteRFIDHistorique, self).create(vals)


        if record.rfid_id:
            record.rfid_id.montant += record.montant_ajoute

        return record

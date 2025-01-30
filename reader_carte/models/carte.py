from odoo import models, fields, api,re
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
import logging

# Initialiser un logger
_logger = logging.getLogger(__name__)

class CarteRFID(models.Model):
    _name = 'altex.rfid'
    _description = 'Carte RFID'

    rfid_id = fields.Integer(string='ID de la carte', required=True)
    qr_name = fields.Char(string='Le QR code', required=True)
    montant = fields.Monetary(string='Montant associé à la carte RFID', required=True, currency_field='currency_id')
    partner_id = fields.Many2one('res.partner', string='Contact')
    prix_carte = fields.Float(string='Prix de la carte', required=True, default=10.0)
    partner_name = fields.Char(string='Nom ', compute='_compute_partner_name', store=True)
    create_date = fields.Datetime(string="Date de création", default=fields.Datetime.now, readonly=True)
    currency_id = fields.Many2one('res.currency', string='Devise', required=True,
                                  default=lambda self: self.env.company.currency_id.id)
    historique_ids = fields.One2many('altex.rfid.historique', 'rfid_id', string='Historique des montants')

    @api.depends('partner_id')
    def _compute_partner(self):
        for record in self:
            record.partner_name = record.partner_id.name if record.partner_id else ''

    @api.constrains('rfid_id')
    def _check_duplicate_rfid_id(self):
        for record in self:
            # Vérification des doublons pour le champ rfid_id
            duplicate = self.env['altex.rfid'].search([('rfid_id', '=', record.rfid_id), ('id', '!=', record.id)],
                                                      limit=1)
            if duplicate:
                raise ValidationError(
                    f"L'ID de la carte RFID {record.rfid_id} est déjà utilisé pour un autre enregistrement.")

    @api.constrains('qr_name')
    def _check_qr_name_exists(self):
        for record in self:
            # Extraire la portion entre les barres verticales |...|
            match = re.search(r'\|([^|]+)\|([^|]+)\|', record.qr_name)
            if match:
                qr_part = match.group(0)  # Partie extraite, par exemple |34567|89012|
                # Vérification si cette portion existe dans le champ 'code' du modèle 'res.partner'
                partner = self.env['res.partner'].search([('code', '=', qr_part)], limit=1)
                if not partner:
                    raise UserError(
                        f"Ce QR code partiel {qr_part} n'existe pas dans la base de données des partenaires.")
                else:
                    # Si le QR code existe, on peut afficher un message (optionnel)
                    _logger.info(f"Le QR code partiel {qr_part} existe dans le partenaire : {partner.name}")
            else:
                raise UserError("Le QR code ne respecte pas le format attendu.")

    @api.depends('qr_name')
    def _compute_partner_name(self):
        """
        Extrait le code du champ qr_name, recherche le partenaire associé
        dans res.partner, et met à jour le champ partner_name.
        """
        for record in self:
            if record.qr_name:
                # Extraire la partie du QR code entre les 2e et 3e pipes (|)
                match = re.search(r'\|([^|]+)\|([^|]+)\|', record.qr_name)
                if match:
                    extracted_code = f"|{match.group(1)}|{match.group(2)}|"
                    # Rechercher un partenaire correspondant au code extrait
                    partner = self.env['res.partner'].search([('code', '=', extracted_code)], limit=1)
                    if partner:
                        record.partner_name = partner.name
                    else:
                        record.partner_name = "Partenaire non trouvé"
                else:
                    record.partner_name = "Format QR invalide"
            else:
                record.partner_name = "QR code vide"

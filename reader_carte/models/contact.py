from odoo import models, fields, api
import base64
import xlrd
from datetime import datetime


class ResPartner(models.Model):
    _inherit = 'res.partner'

    numero_carte_accee = fields.Integer(string="Numéro de la carte d'accès")
    numero_billet = fields.Integer(string="Numéro du billet")
    numero_dossier = fields.Integer(string="Numéro de dossier")
    navire = fields.Char(string="Navire")
    traversee = fields.Char(string="Traversée")
    date_traversee = fields.Datetime(string="Date de la traversée")
    heure_enregistrement = fields.Char(string="Heure de l'enregistrement", default=lambda self: datetime.now().strftime('%H:%M:%S'))
    ordre = fields.Integer(string="Ordre")
    code = fields.Char(string="QR Code", compute='_compute_code', store=True)

    @api.depends('numero_carte_accee', 'numero_billet')
    def _compute_code(self):
        for record in self:
            record.code = f"|{record.numero_carte_accee}|{record.numero_billet}|"

    @api.model
    def import_from_excel(self):
        if not self.file_data:
            raise ValueError("Veuillez importer un fichier Excel.")

        file_content = base64.b64decode(self.file_data)
        book = xlrd.open_workbook(file_contents=file_content)
        sheet = book.sheet_by_index(0)

        ligne_erreurs = []  # Pour suivre les lignes avec des erreurs
        for row_idx in range(1, sheet.nrows):  # Sauter l'entête
            name = sheet.cell(row_idx, 0).value
            if not name:
                ligne_erreurs.append(row_idx + 1)  # Numéro de la ligne Excel
                continue

            try:
                vals = {
                    'name': name.strip(),  # Suppression des espaces autour du nom
                    'numero_carte_accee': int(sheet.cell(row_idx, 1).value) if sheet.cell(row_idx, 1).value else None,
                    'numero_billet': int(sheet.cell(row_idx, 2).value) if sheet.cell(row_idx, 2).value else None,
                    'numero_dossier': int(sheet.cell(row_idx, 3).value) if sheet.cell(row_idx, 3).value else None,
                    'navire': sheet.cell(row_idx, 4).value or '',
                    'traversee': sheet.cell(row_idx, 5).value or '',
                    'date_traversee': self._convert_excel_date(sheet.cell(row_idx, 6).value, book.datemode),
                    'heure_enregistrement': sheet.cell(row_idx, 7).value or '',
                    'ordre': int(sheet.cell(row_idx, 8).value) if sheet.cell(row_idx, 8).value else None,
                }
                self.create(vals)
            except Exception as e:
                ligne_erreurs.append(row_idx + 1)

        if ligne_erreurs:
            raise ValueError(f"Les lignes suivantes du fichier Excel contiennent des erreurs ou des données manquantes : {ligne_erreurs}")

        return True

    @staticmethod
    def _convert_excel_date(value, datemode):
        try:
            return datetime(*xlrd.xldate_as_tuple(value, datemode))
        except Exception:
            return None

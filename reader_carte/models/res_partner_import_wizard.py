from odoo import models, fields, api
import base64
import xlrd
from datetime import datetime


class ResPartnerImportWizard(models.TransientModel):
    _name = 'res.partner.import.wizard'
    _description = 'Wizard for importing ResPartner data from Excel'

    file = fields.Binary(string='File', required=True)

    def import_file(self):
        try:
            file_content = base64.b64decode(self.file)
            workbook = xlrd.open_workbook(file_contents=file_content)
            sheet = workbook.sheet_by_index(0)

            for row_index in range(1, sheet.nrows):  # Skip header row
                row = sheet.row(row_index)
                vals = {
                    'numero_carte_accee': int(row[0].value),
                    'numero_billet': int(row[1].value),
                    'numero_dossier': int(row[2].value),
                    'navire': row[3].value,
                    'traversee': row[4].value,
                    'date_traversee': datetime.strptime(row[5].value, '%Y-%m-%d %H:%M:%S'),
                    'heure_enregistrement': row[6].value,
                    'ordre': int(row[7].value),
                }
                self.env['res.partner'].create(vals)

        except Exception as e:
            raise models.ValidationError("Erreur lors de l'importation du fichier : %s" % e)

        return {'type': 'ir.actions.act_window_close'}
from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_date_creation = fields.Date(string="Date de création")
    x_forme_juridique = fields.Char(string="Forme juridique")
    x_rcs = fields.Char(string="Inscription au RCS")
    x_capital_social = fields.Integer(string="Capital social")
    x_dirigeants = fields.Char(string="Dirigeants")
    x_actionnaires = fields.Char(string="Actionnaires et bénéficaires")
    x_comptes_annuels = fields.Binary(string="Comptes annuels")
    x_recup_infos_bilan = fields.Char(string="Récupération infos bilan quand présente")

    def custom_button_method(self):
        print("Custom button clicked")

    def get_pappers_data(self):
        _logger.info("get_pappers_data method called")
        api_token = '9c8e5b5093e4d43b1449e17499c7e941adebb0ab1f1d8d6b'
        url = 'https://api.pappers.fr/v1/entreprise'

        for record in self:
            siren = record.siret
            if not siren:
                _logger.error("SIREN not found for record ID: %s", record.id)
                continue

            params = {
                'api_token': api_token,
                'siren': siren
            }

            try:
                response = requests.get(url, params=params)
                _logger.info(f"URL: {response.url}")
                response.raise_for_status()  # Raises error for bad responses
                data = response.json()

                updates = {}
                if 'nom_entreprise' in data:
                    updates['name'] = data['nom_entreprise']
                    _logger.info(f"Company name updated to: {data['nom_entreprise']}")

                if 'site_web' in data:
                    updates['website'] = data['site_web']
                    _logger.info(f"Website updated to: {data['site_web']}")

                if 'date_creation' in data:
                    updates['x_date_creation'] = data['date_creation']
                    _logger.info(f"Date de création updated to: {data['date_creation']}")

                if 'forme_juridique' in data:
                    updates['x_forme_juridique'] = data['forme_juridique']
                    _logger.info(f"Forme juridique updated to: {data['forme_juridique']}")

                if 'telephone' in data:
                    updates['phone'] = data['telephone']
                    _logger.info(f"Phone updated to: {data['telephone']}")

                if 'capital' in data:
                    updates['x_capital_social'] = data['capital']
                    _logger.info(f"Capital social updated to: {data['capital']}")

                if 'email' in data:
                    updates['email'] = data['email']
                    _logger.info(f"Email updated to: {data['email']}")

                if 'nom_complet' in data:
                    updates['x_actionnaires'] = data['nom_complet']
                    _logger.info(f"Actionnaires updated to: {data['nom_complet']}")

                if 'numero_rcs' in data:
                    updates['x_rcs'] = data['numero_rcs']
                    _logger.info(f"Inscription au RCS updated to: {data['numero_rcs']}")

                if 'adresse_ligne_1' in data:
                    updates['street'] = data['adresse_ligne_1']
                    _logger.info(f"Street updated to: {data['adresse_ligne_1']}")

                if 'nom_complet' in data:
                    updates['x_dirigeants'] = data['nom_complet']
                    _logger.info(f"Dirigeants updated to: {data['nom_complet']}")

                if updates:
                    record.write(updates)
                    _logger.info(f"Record ID {record.id} updated with data: {updates}")

            except requests.exceptions.RequestException as e:
                _logger.error(f"Error fetching data from Pappers API for record ID {record.id}: {e}")

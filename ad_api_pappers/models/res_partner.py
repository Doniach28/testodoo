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
        for record in self:
            siren = record.siret
            if not siren:
                _logger.error("SIREN not found for record ID: %s", record.id)
                continue
        url = 'https://api.pappers.fr/v1/entreprise'

        params = {
            'api_token': api_token,
            'siren': siren
        }

        try:
            # Envoie une requête GET à l'URL avec les paramètres spécifiés
            response = requests.get(url, params=params)
            _logger.info(f"URL: {response.url}")
            # Vérifie si la réponse HTTP indique une erreur et lève une exception si c'est le cas
            response.raise_for_status()  # Raises error for bad responses
            # Décode le contenu JSON de la réponse en un dictionnaire Python
            data = response.json()

            if 'nom_entreprise' in data:
                nom_entreprise = data['nom_entreprise']
                self.write({'name': nom_entreprise})
                _logger.info(f"Company name updated to: {nom_entreprise}")

            if 'site_web' in data:
                site_web = data['site_web']
                self.write({'website': site_web})
                _logger.info(f"Website updated to: {site_web}")

            if 'date_creation' in data:
                date_creation = data['date_creation']
                self.write({'x_date_creation': date_creation})
                _logger.info(f"Website updated to: {date_creation}")

            if 'forme_juridique' in data:
                forme_juridique = data['forme_juridique']
                self.write({'x_forme_juridique': forme_juridique})
                _logger.info(f"forme juridique  updated to: {forme_juridique}")

            if 'telephone' in data:
                telephone = data['telephone']
                self.write({'phone': telephone})
                _logger.info(f"Phone updated to: {telephone}")

            if 'capital' in data:
                capital = data['capital']
                self.write({'x_capital_social': capital})
                _logger.info(f"capitale sociale  updated to: {capital}")

            if 'email' in data:
                email = data['email']
                self.write({'email': email})
                _logger.info(f"the email updated to: {email}")

            if 'nom_complet' in data:
                nom_complet = data['nom_complet']
                self.write({'x_actionnaires': nom_complet})
                _logger.info(f"acctionnaires updated to: {nom_complet}")

            if 'numero_rcs' in data:
                numero_rcs = data['numero_rcs']
                self.write({'x_rcs': numero_rcs})
                _logger.info(f"Inscription au RCS updated to: {numero_rcs}")

            if 'adresse_ligne_1' in data:
                adresse_ligne_1 = data['adresse_ligne_1']
                self.write({'street': adresse_ligne_1})
                _logger.info(f"street updated to: {adresse_ligne_1}")
            if 'nom_complet' in data:
                nom_complet = data['nom_complet']
                self.write({'x_dirigeants': nom_complet})
                _logger.info(f"Dirigeants   updated to: {nom_complet}")


        except requests.exceptions.RequestException as e:
            # Log the error
            _logger.error(f"Error fetching data from Pappers API: {e}")

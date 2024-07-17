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
        api_token = 'f312fec8ad12a492c943b06cff6139238c20e4cab29a8df0'
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
                
        except requests.exceptions.RequestException as e:
            # Log the error
            _logger.error(f"Error fetching data from Pappers API: {e}")

    
    def button_fetch_pappers_data(self):
        _logger.info("button_fetch_pappers_data method called")
        for record in self:
            record.get_pappers_data()


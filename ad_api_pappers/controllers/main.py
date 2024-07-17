from odoo import http
from odoo.http import request, Response

class PappersController(http.Controller):
    @http.route('/pappers/get_data', auth='public', methods=['GET'], type='json')
    def get_data(self, siret):
        pappers_model = request.env['pappers.api']
        data = pappers_model.get_pappers_data(siret)
        return Response(json.dumps(data), content_type='application/json', status=200)

import json
from flask import request, jsonify
from flask.views import MethodView
from Views.viewHelper import register_view
from Controlers.company_control import CompanyControl

class LoginView(MethodView):
    def post(self):
        json = request.get_json()
        if json == None:
            return jsonify({"error": "Please provide a JSON"}), 400

        try:
            company = CompanyControl.login(json['login'] , json['password'])
            if company != None:
                return jsonify(company.as_dict()), 200
            else:
                return jsonify({"error": "Senha ou usuário inválido"}), 401
        except ValueError as error:
            return jsonify({"error": str(error)}), 500

def initialize_view(app):
    endpoint='login_view'
    methods=['POST']
    url='/login/'
    pk=''
    register_view(app,LoginView,endpoint,url,methods,pk)

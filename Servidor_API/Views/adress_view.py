import json
from flask import request, jsonify
from flask.views import MethodView
from viewHelper import register_view,app 




class AdressView(MethodView):

    def get(self,id_adress=None):
        return jsonify({"testeGet": id})
    #def post(self):
        #return jsonify({"testePost": "123"})
    def put(self,id_adress):
        return jsonify({"testePut": id})
    def delete(self,id_adress):
        return jsonify({"testeDElete": id})

endpoint='adress_view'
methods=['GET','PUT','DELETE']
url='/adress/'
pk='id_adress'
register_view(app,AdressView,endpoint,url,methods,pk)

from http import HTTPStatus

from flask import Flask, request
from flask_restful import Resource, Api 

from models import laptop

app = Flask(__name__)
api = Api(app)        

class Recommendation(Resource):

    def post(self):
        criteria = request.get_json()
        validCriteria = ['nama', 'harga', 'processor', 'ram', 'storage', 'baterai']
        laptop = laptop()

        if not criteria:
            return 'criteria is empty', HTTPStatus.BAD_REQUEST.value

        if not all([v in validCriteria for v in criteria]):
            return 'criteria is not found', HTTPStatus.NOT_FOUND.value

        recommendations = laptop.get_recs(criteria)
        results = [{"nama": laptop.laptop_data_dict[rec[0]], "skor": rec[1]} for rec in recommendations.items()]

        return {
            'alternatif': results
        }, HTTPStatus.OK.value


api.add_resource(Recommendation, '/recommendation')

if __name__ == '__main__':
    app.run(port='5005', debug=True)

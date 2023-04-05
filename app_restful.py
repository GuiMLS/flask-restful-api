from flask import Flask
from flask import request
from flask_restful import Resource, Api
import json
from roles import Roles

app = Flask(__name__)
api = Api(app)

developers = [
    {
        "id": "0",
        "name": "John",
        "role": "backend"
    },
    {
        "id": "1",
        "name": "Jane",
        "role": "frontend"
    }
]


class Developer(Resource):
    def get(self, id):
        try:
            response = developers[id]
        except IndexError:
            message = 'The ID {} doesn\'t correspond to a developer.'.format(id)
            response = {'Status': 'Error', 'Message': message}
        except Exception:
            message = 'Unknown error. Please, contact the API admin.'
            response = {'Status': 'Error', 'Message': message}
        return response

    def put(self):
        pass

    def delete(self, id):
        developers.pop(id)
        message = 'The register was deleted.'
        response = {'Status': 'Success', 'Message': message}
        return response


class DevelopersList(Resource):
    def get(self):
        return developers
    def post(self):
        data = json.loads(request.data)
        position = len(developers)
        data['id'] = position
        developers.append(data)
        return developers[position]


api.add_resource(Developer, '/dev/<int:id>/')  # Creating the route /dev
api.add_resource(DevelopersList, '/dev/')  # Creating the route /dev
api.add_resource(Roles, '/roles/')  # Creating the route /dev

if __name__ == '__main__':
    app.run(debug = True)
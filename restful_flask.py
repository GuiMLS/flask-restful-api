from flask import Flask
from flask import request
from flask_restful import Resource, Api

import json

app = Flask(__name__)

@app.route("/<int:id>", methods=['GET', 'POST'])
def people(id):
    return {'nome': 'Rafael', 'id':id}

@app.route("/soma/<int:valor1>/<int:valor2>/", methods=['GET', 'POST'])
def soma(valor1, valor2):
    return {'soma': valor1+valor2}

@app.route("/soma", methods=['POST', 'GET']) #recebendo via Body @!! PT
def soma2():
    total = 0
    if request.method == 'POST':
        dados = json.loads(request.data)
        total = sum(dados['valores'])
    elif request.method == 'GET':
        total = 100 + 10
    return {'soma': total}

if __name__ == '__main__':
    app.run(debug=True)



from flask import Flask, jsonify, request
from .db import read_food, add_food

app = Flask(__name__)

DEFAULT_RESPONSE_DATA = {
    'ok': False,
    'data': []
}

@app.route('/')
@app.route('/index')
def index():
    r = DEFAULT_RESPONSE_DATA
    r['data'] = {'message': 'Hello! Welcome to crudapp'}
    r['ok'] = True
    return jsonify(r)


@app.route('/api/food', methods=['GET', 'POST'])
def get_foods():
    method = request.method
    r = DEFAULT_RESPONSE_DATA

    if method == 'GET':
        sqlstr = 'SELECT * FROM foods'
        id = request.args.get('id')

        try:
            r['data'] = read_food(id)
        except Exception as e:
            r['data'] = {'message': str(e)}

    elif method == 'POST':
        body = request.json

        if body:
            try:
                add_food(body.get('food'))
                r['ok'] = True
                r['data'] = {'message': 'OK'}
            except Exception as e:
                r['data'] = {'message': str(e)}
        else:
            r['data'] = {'message': 'POST body must be provided'}

    return jsonify(r)

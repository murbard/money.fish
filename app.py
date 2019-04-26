import hashlib
from island import Island
import json
import os

secret = os.environ['FISH_SECRET']

from flask import Flask, request, render_template
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

app.island = Island()


class Coordinator(Resource):
    """ Used by another process to make the clock tick """

    def post(self):
        if request.form['secret'] != secret:
            return {}, 401

        if request.form['action'] == 'tick':
            if not app.island.started:
                app.island.morning()
                app.island.started = True
            else:
                app.island.evening()
                app.island.morning()
            return {'day':app.island.day}, 200

        if request.form['action'] == 'reset':
            app.island = Island()
            return {'day':app.island.day}, 200


api.add_resource(Coordinator, '/run')

class Stats(Resource):

    def post(self):
        if request.form['secret'] != secret:
            return {}, 401

        return app.island.stats, 200

api.add_resource(Stats, '/stats')



@app.route('/')
def index():
    return render_template('index.html')


class Hello(Resource):
    """ For debugging purposes """

    def get(self):
        return {'hello': 'world'}


api.add_resource(Hello, '/hello')


class Register(Resource):
    """ Register as a villager """

    def post(self):
        if app.island.started:
            return {}, 403

        name = request.form['name']
        if len(name) > 128:
            return {}, 403

        key_provided = request.form['key']
        key = hashlib.blake2b(
            name.encode('ascii'), key=secret.encode('ascii'), digest_size=20).hexdigest()
        print(key)

        if key != key_provided:
            return {}, 401

        app.island.register_villager(key)
        return {'key': key}


api.add_resource(Register, '/register')


class Info(Resource):
    """" Get information on the state of the island. """

    def get(self, key):
        if key not in app.island.villagers:
            return {}, 404
        return {
            key: {
                'fish': app.island.get_fish(key),
                'shells': app.island.get_shells(key)
            },
            'villagers': len(app.island.villagers),
            'day': app.island.day,
            'last_price': app.island.last_price,
            'last_quantity': app.island.last_quantity
        }


api.add_resource(Info, '/info/<string:key>')


class Order(Resource):
    def post(self, key):
        try:
            shells = int(request.form['shells'])
        except:
            return {}, 400
        if app.island.place_order(key, shells):
            return {'shells': request.form['shells']}
        else:
            return {}, 403


api.add_resource(Order, '/order/<string:key>')

if __name__ == '__main__':
    app.run(debug=True)

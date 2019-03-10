import hashlib
import island
import json
import os

secret = os.environ['FISH_SECRET']

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

island = island.Island()


class Coordinator(Resource):
    """ Used by another process to make the clock tick """

    def post(self):
        if request.form['secret'] != secret:
            return {}, 401

        if not island.started:
            island.morning()
            island.started = True

        island.evening()
        island.morning()
        return {}, 200


api.add_resource(Coordinator, '/tick')


class Register(Resource):
    """ Register as a villager """

    def post(self):
        if island.started:
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

        island.register_villager(key)
        return {'key': key}


api.add_resource(Register, '/register')


class Info(Resource):
    """" Get information on the state of the island. """

    def get(self, key):
        if key not in island.villagers:
            return {}, 404
        return {
            key: {
                'fish': island.get_fish(key),
                'shells': island.get_shells(key)
            },
            'villagers': len(island.villagers),
            'day': island.day,
            'last_price': island.last_price,
            'last_quantity': island.last_quantity
        }


api.add_resource(Info, '/info/<string:key>')


class Order(Resource):
    def post(self, key):
        try:
            shells = int(request.form['shells'])
        except:
            return {}, 400
        if island.place_order(key, shells):
            return {'shells': request.form['shells']}
        else:
            return {}, 403


api.add_resource(Order, '/order/<string:key>')

if __name__ == '__main__':
    app.run(debug=True)

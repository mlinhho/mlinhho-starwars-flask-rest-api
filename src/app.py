"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Person, Planet, User, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def handle_people():
    people = Person.query.all()
    people_as_dictionaries = []
    for _person in people:
        people_as_dictionaries.append(_person.to_dict())
    return jsonify(people_as_dictionaries), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def handle_one_person(people_id):
    person = Person.query.get(people_id)
    if person is None:
        return jsonify({
            "msg": "no person is found for that id"
        }), 404
    else:
        return jsonify(person.to_dict()),200
    
@app.route('/planets', methods=['GET'])
def handle_planets():
    planets = Planet.query.all()
    planets_as_dictionaries = []
    for _planet in planets:
        planets_as_dictionaries.append(_planet.to_dict())
    return jsonify(planets_as_dictionaries), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def handle_one_planet(planets_id):
    planet = Planet.query.get(planets_id)
    if planet is None:
        return jsonify({
            "msg": "no planet is found for that id"
        }), 404
    else:
        return jsonify(planet.to_dict()),200
    
@app.route('/users', methods=['GET'])
def handle_users():
    users = User.query.all()
    users_as_dictionaries = []
    for _user in users:
        users_as_dictionaries.append(_user.to_dict())
    return jsonify(users_as_dictionaries), 200

@app.route('/users/favorites', methods=['GET'])
def handle_favorites():
    favorites = Favorite.query.all()
    favorites_as_dictionaries = []
    for _favorite in favorites:
        favorites_as_dictionaries.append(_favorite.to_dict())
    return jsonify(favorites_as_dictionaries), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def handle_planet_favorite(planet_id):
    body = request.json
    if "user_id" not in body:
        return jsonify({
            "msg": "user id is required for the favorite creation"
        }),400
    if planet_id is None:
        return jsonify({
            "msg": "planet id is required for the favorite creation"
        }),400
    user = User.query.get(body["user_id"])
    if user is None:
        return jsonify({
            "msg": "user is required for the favorite creation"
        }),404
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({
            "msg": "no planet favorited for that id"
        }), 404
    favorite = Favorite.query.filter_by(
        user_id = user.id,
        planet_id = planet.id
    ).one_or_none()
    if favorite is not None:
        return jsonify({
            "msg": "you can't favorite because it's already existing"
        }),400
    planet_favorite = Favorite(
        user_id = user.id,
        planet_id = planet.id
        )
    return jsonify(planet_favorite.to_dict()), 201

@app.route('/favorite/person/<int:person_id>', methods=['POST'])
def handle_person_favorite(person_id):
    body = request.json
    if "user_id" not in body:
        return jsonify({
            "msg": "user id is required for the favorite creation"
        }),400
    if person_id is None:
        return jsonify({
            "msg": "person id is required for the favorite creation"
        }),400
    user = User.query.get(body["user_id"])
    if user is None:
        return jsonify({
            "msg": "user is required for the favorite creation"
        }),404
    person = Person.query.get(person_id)
    if person is None:
        return jsonify({
            "msg": "no person favorited for that id"
        }), 404
    favorite = Favorite.query.filter_by(
        user_id = user.id,
        person_id = person.id
    ).one_or_none()
    if favorite is not None:
        return jsonify({
            "msg": "you can't favorite because it's already existing"
        }),400
    person_favorite = Favorite(
        user_id = user.id,
        person_id = person.id
        )
    return jsonify(person_favorite.to_dict()), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite(planet_id):
    body = request.json

    if "user_id" not in body:
        return jsonify({
            "msg": "user id is required to delete the favorite"
        }),400
    if planet_id is None:
        return jsonify({
            "msg": "planet id is required to delete the favorite"
        }),400
    
    user = User.query.get(body["user_id"])
    if user is None:
        return jsonify({
            "msg": "user is required to delete the favorite"
        }),404
    
    planet = Planet.query.get(planet_id)

    if planet is None:
        return jsonify({
            "msg": "no planet favorited for that id"
        }), 404
    
    favorite = Favorite.query.filter_by(
        user_id = user.id,
        planet_id = planet.id
    ).one_or_none()

    if favorite is None:
        return jsonify({
            "msg": "you can't delete because nothing is favorited"
        }),400
    favorite.delete()
    return jsonify(""),204

@app.route('/favorite/person/<int:person_id>', methods=['DELETE'])
def delete_person_favorite(person_id):
    body = request.json

    if "user_id" not in body:
        return jsonify({
            "msg": "user id is required to delete the favorite"
        }),400
    if person_id is None:
        return jsonify({
            "msg": "person id is required to delete the favorite"
        }),400
    
    user = User.query.get(body["user_id"])
    if user is None:
        return jsonify({
            "msg": "user is required to delete the favorite"
        }),404
    
    person = Person.query.get(person_id)

    if person is None:
        return jsonify({
            "msg": "no person favorited for that id"
        }), 404
    
    favorite = Favorite.query.filter_by(
        user_id = user.id,
        person_id = person.id
    ).one_or_none()

    if favorite is None:
        return jsonify({
            "msg": "you can't delete because nothing is favorited"
        }),400
    favorite.delete()
    return jsonify(""),204

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

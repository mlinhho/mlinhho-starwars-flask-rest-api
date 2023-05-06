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
from models import db, User, Person, Planet
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

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

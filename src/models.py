import os
import sys
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def to_dict(self):
        return {
            "id":self.id,
            "username":self.username,
            "email":self.email
        }

class Planet(db.Model):
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    population = db.Column(db.Integer)
    gravity = db.Column(db.String(40))
    climate = db.Column(db.String(50))
    terrain = db.Column(db.String(50))
    surface_water = db.Column(db.Integer)
    diameter = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    edited = db.Column(db.Date)
    created = db.Column(db.Date, nullable=False)
    url = db.Column(db.String(100), unique = True)

    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "population":self.population,
            "gravity":self.gravity,
            "climate":self.climate,
            "terrain":self.terrain,
            "surface_water":self.surface_water,
            "diameter":self.diameter,
            "orbital_period":self.orbital_period,
            "rotation_period":self.rotation_period,
            "created":self.created,
            "url":self.url
        }

class Person(db.Model):
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    birth_year = db.Column(db.Date)
    eye_color = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    hair_color = db.Column(db.String(20))
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    skin_color = db.Column(db.String(30))
    edited = db.Column(db.Date)
    created = db.Column(db.Date, nullable=False)
    origin_planet_url = db.Column(db.String(100), db.ForeignKey('planet.url'))
    url = db.Column(db.String(100), unique = True)

    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "birth_year":self.birth_year,
            "eye_color":self.eye_color,
            "gender":self.gender,
            "hair_color":self.hair_color,
            "height":self.height,
            "mass":self.mass,
            "edited":self.edited,
            "created":self.created,
            "url":self.url
        }
    
    
class Favorite(db.Model):
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    def __init__(self,user_id,planet_id=None,person_id=None):
        self.planet_id = planet_id
        self.person_id = person_id
        self.user_id = user_id
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id":self.id,
            "user_id":self.user_id,
            "planet_id":self.planet_id,
            "person_id":self.person_id
        }

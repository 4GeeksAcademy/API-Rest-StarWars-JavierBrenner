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
from models import db, User, Planet, Character, Favorite
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

# -------- START User rutes -----------

@app.route('/user', methods=['GET'])
def all_users():
    user_list = db.session.query(User).all()
    users = list(map(lambda user: user.serialize(), user_list))

    response_body = {
        "users": users
    }
    return jsonify(response_body), 200
    
@app.route('/user/<int:id>')
def get_user(id):
    user = User.query.get(id)

    if user is None:
        return jsonify({"msg": "User not found"}), 404
    
    return jsonify({"user": user.serialize()}), 200

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    name = data.get('name')     
    lastname = data.get('lastname')
    email = data.get('email')
    password = data.get ('password')

    if username is None or name is None or lastname is None or email is None or password is None:
        return jsonify({"msg":"Bad request i need username, name, lastname, email and password"}), 400

    new_user = User(username=username, name=name, lastname=lastname, email=email, password=password, is_active=True)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg":"User created", "user": new_user.serialize()}), 201

@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()

    user_update = db.session.get(User, id)
    if user_update is None:
        return jsonify({"msg": "User not found"}), 404
    
    user_update.username = data.get('username', user_update.username)
    user_update.name = data.get('name', user_update.name)
    user_update.lastname = data.get('lastname', user_update.lastname)
    user_update.email = data.get('email', user_update.email)
    user_update.password = data.get('password', user_update.password)
    
    db.session.commit()
    return jsonify({"msg": "User updated", "user": user_update.serialize_update()}), 200

# -------- END User rutes -----------

# ------- START Character rutes --------

@app.route('/character', methods=['GET'])
def all_characters():
    character_list = db.session.query(Character).all()
    characters = list(map(lambda character: character.serialize(), character_list))

    response_body = {
        "characters": characters
    }
    return jsonify(response_body), 200
    
@app.route('/character/<int:id>')
def get_character(id):
    character = Character.query.get(id)

    if character is None:
        return jsonify({"msg": "Character not found"}), 404
    
    return jsonify({"character": character.serialize()}), 200

@app.route('/character', methods=['POST'])
def create_character():
    data = request.get_json()
    img = data.get('img')
    name = data.get('name')
    birth_year = data.get('birth_year')
    gender = data.get('gender')
    height = data.get('height')
    description = data.get('description')

    if img is None or name is None or birth_year is None or gender is None or height is None or description is None:
        return jsonify({"msg":"Bad request i need img url, name, birth_year, gender, height and description"}), 400
    
    new_character = Character(img=img, name=name, birth_year=birth_year, gender=gender, height=height, description=description)
    db.session.add(new_character)
    db.session.commit()
    return jsonify({"msg":"Character created", "character": new_character.serialize()}), 201

@app.route('/character/<int:id>', methods=['PUT'])
def update_character(id):
    data = request.get_json()
    character_update = db.session.get(Character, id)
    if character_update is None:
        return jsonify({"msg": "Character not found"}), 404
    
    character_update.img = data.get('img', character_update.img)
    character_update.name = data.get('name', character_update.name)
    character_update.birth_year = data.get('birth_year', character_update.birth_year)
    character_update.gender = data.get('gender', character_update.gender)
    character_update.height = data.get('height', character_update.height)
    character_update.description = data.get('description', character_update.description)
    
    db.session.commit()
    return jsonify({"msg": "Character updated", "character": character_update.serialize()}), 200

@app.route('/character/<int:id>', methods=['DELETE'])
def delete_character(id):
    character = db.session.get(Character, id)
    if character is None:
        return jsonify({"msg": "Character not found"}), 404
    
    db.session.delete(character)
    db.session.commit()

    return jsonify({"msg": f"Character {id} deleted"}), 200


# ------- END Character rutes --------

# ------- START Planet rutes --------

@app.route('/planet', methods=['GET'])
def all_planets():
    planet_list = db.session.query(Planet).all()
    planets = list(map(lambda planet: planet.serialize(), planet_list))

    response_body = {
        "planets": planets
    }
    return jsonify(response_body), 200
    
@app.route('/planet/<int:id>')
def get_planet(id):
    planet = Planet.query.get(id)

    if planet is None:
        return jsonify({"msg": "Planet not found"}), 404
    
    return jsonify({"planet": planet.serialize()}), 200

@app.route('/planet', methods=['POST'])
def create_planet():
    data = request.get_json()
    img = data.get('img')
    name = data.get('name')
    climate = data.get('climate')
    diameter = data.get('diameter')
    gravity = data.get('gravity')
    description = data.get('description')

    if img is None or name is None or climate is None or diameter is None or gravity is None or description is None:
        return jsonify({"msg": "Bad request i need img url, name, climate, diameter, gravity and description"}), 400
    
    new_planet = Planet(img=img, name=name, climate=climate, diameter=diameter, gravity=gravity, description=description)
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({"msg":"Planet created", "planet": new_planet.serialize()}), 201

@app.route('/planet/<int:id>', methods=['PUT'])
def update_planet(id):
    data = request.get_json()
    planet_update = db.session.get(Planet, id)
    if planet_update is None:
        return jsonify({"msg": "Planet not found"}), 404
    
    planet_update.img = data.get('img', planet_update.img)
    planet_update.name = data.get('name', planet_update.name)
    planet_update.climate = data.get('climate', planet_update.climate)
    planet_update.diameter = data.get('diameter', planet_update.diameter)
    planet_update.gravity = data.get('gravity', planet_update.gravity)
    planet_update.description = data.get('description', planet_update.description)
    
    db.session.commit()
    return jsonify({"msg": "Planet updated", "planet": planet_update.serialize()}), 200

@app.route('/planet/<int:id>', methods=['DELETE'])
def delete_planet(id):
    planet = db.session.get(Planet, id)
    if planet is None:
        return jsonify({"msg": "Planet not found"}), 404
    
    db.session.delete(planet)
    db.session.commit()

    return jsonify({"msg": f"Planet {id} deleted"}), 200

# ------- END Planet rutes --------

# ------- START Favorite rutes -------

@app.route('/favorite', methods=['POST'])
def create_favorite():
    data = request.get_json()
    user_id = data.get('user_id')
    character_id = data.get('character_id')
    planet_id =data.get('planet_id')

    if user_id is None:
        return jsonify({"msg": "Bad request i need user_id"}), 400
    
    new_fav = Favorite(user_id=user_id, character_id=character_id, planet_id=planet_id)
    if character_id is None and planet_id is None:
        return jsonify({"msg": "Bad request i need character_id or planet_id, or both"})
    
    db.session.add(new_fav)
    db.session.commit()

    if character_id is not None and planet_id is not None:
        favorite = new_fav.serialize()
    elif character_id is not None:
        favorite = new_fav.serialize_fav_character()
    else:
        favorite = new_fav.serialize_fav_planet()
    return jsonify({"msg":"Favorite created", "favorite": favorite}), 201

@app.route('/favorite/<int:user_id>', methods=['GET'])
def get_favorites_from_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"msg": "User not found"}), 400
    query= db.select(Favorite).where(Favorite.user_id == user_id)
    favorite_list = db.session.execute(query).scalars().all()
    favorites = list(map(lambda favorite: favorite.serialize(), favorite_list))

    return jsonify ({"user_id": user_id, "favorites": favorites})

@app.route('/favorite/<int:id>', methods=['DELETE'])
def delete_favorite(id):
    favorite = db.session.get(Favorite, id)
    if favorite is None:
        return jsonify({"msg": "Favorite not found"}), 404
    
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": f"Favorite {id} deleted"}), 200


# ------- END Favorite rutes -------


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

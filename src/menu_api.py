__version__ = '0.1.0'


from flask import Flask, request
from http import HTTPStatus as Status

from db_manager import DatabaseManager
from models import Restaurant, Food, status_json
import datetime
import os
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import logging

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'do-not-keep-your-secret-key-here'
jwt = JWTManager(app)
logger = logging.getLogger(__name__)

db = DatabaseManager()

@app.route('/', methods=["GET"])
def version():  # put application's code here
    return status_json(Status.OK, 'Request was successful.',
                       {"version": __version__, 'app_name': __name__})

@app.route('/token', methods=["GET"])
def token():
    access_token = create_access_token(identity='admin')
    return status_json(Status.OK, 'Here is your token, enjoy!', {'token': access_token})

@app.route('/restaurant/<name>', methods=["POST"])
@app.route('/restaurant/<int:id_>', methods=["PUT", "DELETE"])
@jwt_required()
def restaurant(name = None, id_ = None):
    contact = request.args.get('contact')
    opening_hours = request.args.get('opening_hours')
    address = request.args.get('address')

    if request.method == "PUT":
        name = request.args.get('name')
        put_dict: dict = {'id': id_, 'name': name, 'contact': contact, 'opening_hours': opening_hours, 'address': address}
        put_dict = {k:v for k,v in put_dict.items() if v}
        try:
            data = db.update(Restaurant, put_dict)
            return status_json(Status.CREATED, 'Restaurant was updated successfully.', data)
        except Exception as e:
            return status_json(Status.INTERNAL_SERVER_ERROR, f'Failed to add restaurant: {e}')

    if request.method == "POST":
        try:
            data = db.insert(Restaurant(name=name,
                                        contact=contact,
                                        opening_hours=opening_hours,
                                        address=address))
            return status_json(Status.CREATED, 'Restaurant was added successfully.', data)
        except Exception as e:
            return status_json(Status.INTERNAL_SERVER_ERROR, f'Failed to add restaurant: {e}')

    if request.method == "DELETE":
        try:
            data = db.delete(Restaurant, id_)
            return status_json(Status.OK, f'Restaurant with id {id_} was deleted.', data)
        except Exception as e:
            return status_json(Status.INTERNAL_SERVER_ERROR, f'Failed to delete restaurant: {e}')


@app.route('/restaurant/<int:id_>', methods=["GET"])
@app.route('/restaurants', methods=["GET"])
def restaurants(id_ = None):
    try:
        data = db.get(Restaurant, id_)
        return status_json(Status.OK, 'Data about the restaurants were fetched.', data)
    except Exception as e:
        return status_json(Status.INTERNAL_SERVER_ERROR, f'Failed to get restaurant: {e}')


@app.route('/food/<restaurant_id>/<name>', methods=["POST"])
@app.route('/food/<int:id_>', methods=["PUT", "DELETE"])
@jwt_required()
def food(name = None, restaurant_id = None, id_ = None):
    day = request.args.get('day')
    price = request.args.get('price')
    try:
        day = datetime.date.fromisoformat(request.args.get('day')) if day else None
        price = float(request.args.get('price')) if price else None
    except ValueError as e:
        return status_json(Status.BAD_REQUEST, f'Failed to add food: {e}')

    if request.method == "PUT":
        name = request.args.get('name')
        put_dict: dict = {'id': id_, 'name': name, 'day': day, 'price': price}
        put_dict = {k:v for k,v in put_dict.items() if v}
        try:
            data = db.update(Food, put_dict)
            return status_json(Status.CREATED, 'Food was updated successfully.', data)
        except Exception as e:
            return status_json(Status.INTERNAL_SERVER_ERROR, f'Failed to add food: {e}')

    if request.method == "POST":
        try:
            if not db.get(Restaurant, restaurant_id):
                raise 'No restaurant with this ID.'
            data = db.insert(Food(restaurant_id=restaurant_id,
                                  name=name,
                                  day=day,
                                  price=price))
            return status_json(Status.CREATED, 'Food was added successfully.', data)
        except Exception as e:
            return status_json(Status.INTERNAL_SERVER_ERROR, f'Failed to add food: {e}')

    if request.method == "DELETE":
        try:
            data = db.delete(Food, id_)
            return status_json(Status.OK, f'Food with id {id_} was deleted.', data)
        except Exception as e:
            return status_json(Status.INTERNAL_SERVER_ERROR, f'Failed to delete food: {e}')


@app.route('/foods/<int:restaurant_id>', methods=["GET"])
def foods(restaurant_id):
    try:
        data = db.get(Food, restaurant_id)
        return status_json(Status.OK, 'Data about the restaurant were fetched.', data)
    except Exception as e:
        return status_json(Status.INTERNAL_SERVER_ERROR, f'Failed to get food: {e}')


if __name__ == '__main__':
    app.run(debug=True)

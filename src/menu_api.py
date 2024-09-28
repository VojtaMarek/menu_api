__version__ = '0.1.0'


from flask import Flask, request
from http import HTTPStatus as Status

from database import DatabaseManager
from models import Restaurant, status_json

app = Flask(__name__)

db = DatabaseManager()


@app.route('/', methods=["GET"])
def home():
    return __name__


@app.route('/version', methods=["GET"])
def version():  # put application's code here
    return status_json(Status.OK, 'Request was successful.',
                       {"version": __version__, 'app_name': __name__})


@app.route('/restaurant/<int:id_>', methods=["GET"])
@app.route('/restaurant', methods=["GET"])
def restaurants(id_ = 0):
    try:
        data = db.get(Restaurant, id_)
        return status_json(Status.OK, 'Data about the restaurant were fetched.', data)
    except Exception as e:
        return status_json(Status.INTERNAL_SERVER_ERROR, f'Failed to get restaurant: {e}')


@app.route('/restaurant/<name>', methods=["POST"])
@app.route('/restaurant/<int:id_>', methods=["PUT"])
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

    try:
        data = db.insert(Restaurant(name=name,
                                    contact=contact,
                                    opening_hours=opening_hours,
                                    address=address))
        return status_json(Status.CREATED, 'Restaurant was added successfully.', data)
    except Exception as e:
        return status_json(Status.INTERNAL_SERVER_ERROR, f'Failed to add restaurant: {e}')


if __name__ == '__main__':
    app.run(debug=True)







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


@app.route('/restaurant_/<name>', methods=["POST", "UPDATE"])
def restaurant(name):
    if request.method == "POST":
        try:
            data = db.insert(Restaurant(name=name, active=True))
            return status_json(Status.OK, 'Restaurant was added successfully.', data)
        except Exception as e:
            status_json(500, f'Failed to add restaurant: {e}')
    if request.method == "UPDATE":
        raise NotImplemented


if __name__ == '__main__':
    app.run(debug=True)







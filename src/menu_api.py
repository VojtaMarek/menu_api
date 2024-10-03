__version__ = '0.1.0'


import os
import logging
from http import HTTPStatus as Status

from flask import Flask, request
from flask.views import MethodView
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

from db_manager import DatabaseManager
from models import Restaurant, Food
from tools import status_json, from_iso_day

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'do-not-keep-your-secret-key-here'
jwt = JWTManager(app)

logger = logging.getLogger(__name__)


class GeneralAPI(MethodView):
    @staticmethod
    def version():
        return status_json(Status.OK, 'Request was successful.',
                           {"version": __version__, 'app_name': __name__})

    @staticmethod
    def token():
        access_token = create_access_token(identity='admin')
        return status_json(Status.OK, 'Here is your token, enjoy!', {'token': access_token})


class ModelAPI(MethodView):
    init_every_request = False

    def __init__(self, model):
        self.model = model
        self.db = DatabaseManager(model)

    def get(self, id_ = None, group_id = None):
        try:
            data = self.db.get(self.model, id_, group_id)
            return status_json(Status.OK, f'Data about the {self.model.__name__} were fetched.', data)
        except Exception as e:
            return status_json(Status.INTERNAL_SERVER_ERROR, f'Failed to get {self.model.__name__}: {e}')

    @jwt_required()
    def put(self, id_):
        args = {k: v for k, v in dict(request.args).items() if v}
        if args.get('day'):
            args['day'] = from_iso_day(args['day'])
        args['id'] = id_
        try:
            data = self.db.update(self.model, args)
            return status_json(Status.CREATED, f'Model {self.model.__name__} was updated successfully.', data)
        except Exception as e:
            return status_json(Status.INTERNAL_SERVER_ERROR, f'Failed to add to {self.model.__name__}: {e}')

    @jwt_required()
    def post(self, name, group_id = None):
        args = {k: v for k, v in dict(request.args).items() if v}
        args['name'] = name
        if args.get('day'):
            args['day'] = from_iso_day(args['day'])
        if group_id:
            args['restaurant_id'] = group_id
        try:
            data = self.db.insert(self.model(**args))
            return status_json(Status.CREATED, f'Model {self.model.__name__} was added successfully.', data)
        except Exception as e:
            return status_json(Status.INTERNAL_SERVER_ERROR, f'Failed to add restaurant: {e}')

    @jwt_required()
    def delete(self, id_):
        try:
            data = self.db.delete(self.model, id_)
            return status_json(Status.OK, f'Restaurant with id {id_} was deleted.', data)
        except Exception as e:
            return status_json(Status.INTERNAL_SERVER_ERROR, f'Failed to delete restaurant: {e}')


def register_api(model, name):
    item = ModelAPI.as_view(f"{name}-item", model)
    app.add_url_rule(f"/{name}/", view_func=item)
    app.add_url_rule(f"/{name}/<int:id_>", view_func=item)
    app.add_url_rule(f"/{name}/<int:group_id>/<int:id_>", view_func=item)
    app.add_url_rule(f"/{name}/<name>", view_func=item)
    app.add_url_rule(f"/{name}/<int:group_id>/<name>", view_func=item)


# routes section
register_api(Restaurant, "restaurants")
register_api(Food, "food")

@app.route('/', methods=["GET"])
def version():  # put application's code here
    return status_json(Status.OK, 'Request was successful.',
                       {"version": __version__, 'app_name': __name__})

@app.route('/token', methods=["GET"])
def token():
    access_token = create_access_token(identity='admin')
    return status_json(Status.OK, 'Here is your token, enjoy!', {'token': access_token})


if __name__ == '__main__':
    app.run(debug=True)

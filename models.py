
from typing import Type

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Date
from sqlalchemy.orm import declarative_base
from flask import jsonify
from http import HTTPStatus as Status

Base = declarative_base()


def status_json(code: int, message: str, data = None) -> Type[jsonify]:
    http_code_ranges = {"informational": Status(code).is_informational,
                        "success": Status(code).is_success,
                        "redirection": Status(code).is_redirection,
                        "client error": Status(code).is_client_error,
                        "server error": Status(code).is_server_error}
    res: dict = {
        "status": next(k for k, v in http_code_ranges.items() if v),
        "message": message,
        "errors": {
            "code": code,
            "detail": "Invalid input data." if code == 400 else "Error."
        },
        "data": data,
    }
    if not data:
        res.pop('data')
    else:
        res.pop('errors')
    return jsonify(res)


class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    active = Column(Boolean, nullable=False)


class Food(Base):
    __tablename__ = 'foods'

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"),)
    name = Column(String(255), nullable=False)
    # day = Column(String, nullable=False)
    price = Column(Float, nullable=True)
    valid_from = Column(Date)

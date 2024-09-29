
from typing import Type, Any

from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import declarative_base, relationship
from flask import jsonify
from http import HTTPStatus as Status

Base = declarative_base()


def status_json(code: int, message: str, data = None) -> tuple[Type[jsonify], int]:
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
    return jsonify(res), code


class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    contact = Column(String(255), nullable=True)
    opening_hours = Column(String(225), nullable=True)
    address = Column(String(225), nullable=True)

    foods = relationship('Food', back_populates="restaurants", cascade="all, delete")


class Food(Base):
    __tablename__ = 'foods'

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    day = Column(Date, nullable=True)
    price = Column(Float, nullable=True)

    restaurants = relationship("Restaurant", back_populates="foods")

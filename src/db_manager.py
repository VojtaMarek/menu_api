import os
from copy import copy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

import config

from models import Restaurant, Food, Base

logger = logging.getLogger(__name__)

# decorator logging database operations
def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f'An error occurred: {e}')
            raise e
    return wrapper


class DatabaseManager:
    def __init__(self, model = None):
        # Set up the engine and metadata
        url = os.environ.get('DB_URL') or config.DB_URL
        self.engine = create_engine(url=url+'?charset=utf8', echo=True, future=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.model = model

    @handle_exception
    def insert(self, record: Restaurant | Food):
        # Insert data into the database using ORM session
        session = self.Session()
        try:
            session.add(record)
            session.commit()
            session.refresh(record)
            return self.serialize(record)
        finally:
            # session.expunge_all()
            session.close()

    @handle_exception
    def get(self, model, id_, group_id):
        # Get data based on its type and ID.
        session = self.Session()
        try:
            if group_id and not id_:
                return [self.serialize(i) for i in session.query(model).filter_by(restaurant_id=group_id).all()]
            elif id_:
                return self.serialize(session.query(model).filter_by(id=id_).first())
            elif not id_:
                return [self.serialize(i) for i in session.query(model).all()]
        finally:
            session.close()

    @handle_exception
    def update(self, model, data):
        # Update based on ID
        session = self.Session()
        try:
            record = session.query(model).filter_by(id=data['id']).first()
            data.pop('id')
            for k, v in data.items():
                setattr(record, k, data.get(k))
            session.commit()
            session.refresh(record)
            return self.serialize(record)
        finally:
            session.close()

    @handle_exception
    def delete(self, model, id_):
        session = self.Session()
        try:
            record = session.query(model).filter_by(id=id_).first()
            data = copy(self.serialize(record))
            session.delete(record)
            session.commit()
            return data
        finally:
            session.close()

    @staticmethod
    def serialize(values) -> dict:
        if not values:
            raise ValueError('No value fetched from DB.')
        return {k: v for k, v in values.__dict__.items() if not k.startswith('_')}
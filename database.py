from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

from config import DB_URL
from models import Restaurant, Food, Base

logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self):
        # Set up the engine and metadata
        self.engine = create_engine(url=DB_URL, echo=True, future=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def insert(self, data: Restaurant | Food):
        # Insert data into the database using ORM session
        session = self.Session()
        try:
            session.add(data)
            session.commit()
            session.refresh(data)
            return self.serialize(data)
        finally:
            # session.expunge_all()
            session.close()

    def get(self, model, id_):
        # Get data based on its type and ID.
        session = self.Session()
        try:
            if int(id_) >= 1:
                data = session.query(model).filter_by(id=id_).first()
                data = self.serialize(data)
            else:
                data = [self.serialize(i) for i in session.query(model).all()]
            return data
        finally:
            session.close()

    def update(self, model, put_dict):
        # Update based on ID
        session = self.Session()
        try:
            data = session.query(model).filter_by(id=put_dict['id']).first()
            put_dict.pop('id')
            for k, v in put_dict.items():
                setattr(data, k, put_dict.get(k))
            session.commit()
            session.refresh(data)
            return self.serialize(data)
        finally:
            session.close()

    @staticmethod
    def serialize(values) -> dict:
        return {k: v for k, v in values.__dict__.items() if not k.startswith('_')}
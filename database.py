from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

from config import DB_URL
from models import Restaurant, Base

logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self):
        # Set up the engine and metadata
        self.engine = create_engine(url=DB_URL, echo=True, future=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def insert(self, data: Restaurant):
        # Insert data into the database using ORM session
        session = self.Session()
        try:
            session.add(data)
            session.commit()
            session.refresh(data)
            data = {k: v for k, v in data.__dict__.items() if not k.startswith('_')}
            return data
        finally:
            # session.expunge_all()
            session.close()

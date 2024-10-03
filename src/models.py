from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


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

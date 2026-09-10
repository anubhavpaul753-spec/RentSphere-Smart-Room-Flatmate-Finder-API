from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    city = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    city = Column(String, nullable=False)
    rent_amount = Column(Integer, nullable=False)
    room_type = Column(String, nullable=False, server_default='single')
    is_available = Column(Boolean, server_default=text('true'), nullable=False)
    locality = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    distance_campus = Column(String, nullable=True)
    distance_mall = Column(String, nullable=True)
    distance_market = Column(String, nullable=True)
    distance_food = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class Bookmark(Base):
    __tablename__ = "bookmarks"

    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    room_id = Column(Integer, ForeignKey(
        "rooms.id", ondelete="CASCADE"), primary_key=True)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    room_id = Column(Integer, ForeignKey(
        "rooms.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User")
    room = relationship("Room")

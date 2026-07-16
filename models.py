from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    age = Column(Integer)
    weight = Column(Float)
    height = Column(Float)

    fitness_level = Column(String(50))
    goal = Column(String(100))

    created_at = Column(DateTime, default=datetime.utcnow)

    workouts = relationship("Workout", back_populates="user")
    nutritions = relationship("Nutrition", back_populates="user")
    measurements = relationship("Measurement", back_populates="user")


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    exercise = Column(String(200))
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(Float)
    duration = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="workouts")


class Nutrition(Base):
    __tablename__ = "nutrition"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    meal = Column(String(100))
    food = Column(Text)

    calories = Column(Integer)
    protein = Column(Float)
    carbs = Column(Float)
    fats = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="nutritions")


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    weight = Column(Float)
    body_fat = Column(Float)
    chest = Column(Float)
    waist = Column(Float)
    arms = Column(Float)
    legs = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="measurements")

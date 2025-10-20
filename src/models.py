from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Numeric, Integer, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorites_characters = Table(
    "favorites characters",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("character_id", ForeignKey("character.id"), primary_key=True)
)

favorites_vehicles = Table(
    "favorites vehicles",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("vehicle_id", ForeignKey("vehicle.id"), primary_key=True)
)

favorites_planets = Table(
    "favorites planets",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("planet_id", ForeignKey("planet.id"), primary_key=True)
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    characters_favorites: Mapped[List["Character"]] = relationship(
        secondary=favorites_characters, back_populates="users")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites_characters": [c.serialize() for c in self.characters_favorites]
            # do not serialize the password, its a security breach
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str] = mapped_column(String(120), nullable=False)
    eye_color: Mapped[str] = mapped_column(String(120), nullable=False)
    mass: Mapped[Numeric] = mapped_column(Numeric(5, 2), nullable=False)
    users: Mapped[List["User"]] = relationship(
        secondary=favorites_characters, back_populates="characters_favorites")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "eye_color": self.eye_color,
            "mass": self.mass,
            "users": [u.serialize()["email"] for u in self.users]
        }


class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    model: Mapped[str] = mapped_column(String(80), nullable=False)
    passengers: Mapped[int] = mapped_column(Integer, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "passengers": self.passengers
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    climate: Mapped[str] = mapped_column(String(20), nullable=False)
    terrain: Mapped[str] = mapped_column(String(35), nullable=False)
    gravity: Mapped[str] = mapped_column(str(50), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "gravity": self.gravity
        }

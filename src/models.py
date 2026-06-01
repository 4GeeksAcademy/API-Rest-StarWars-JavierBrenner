from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    
    favorite =  relationship('Favorite')

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    img: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    birth_year: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    height: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)

    favorite: Mapped[List["Favorite"]] = relationship(back_populates="character")

    def serialize(self):
        return{
           "id": self.id,
           "img": self.img,
           "name": self.name,
           "birth_year": self.birth_year,
           "gender": self.gender,
           "height": self.height,
           "description": self.description
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    img: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    diameter: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    gravity: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)

    favorite: Mapped[List["Favorite"]] = relationship(back_populates="planet")

    def serialize(self):
        return{
            "id": self.id,
            "img": self.img,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "description": self.description
        }

class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    user = relationship('User')

    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))
    character: Mapped["Character"] = relationship(back_populates="favorite")
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    planet: Mapped["Planet"] = relationship(back_populates="favorite")


    def serialize_favorite(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character": self.character.name if self.character else None,
            "planet": self.planet.name if self.planet else None
        }
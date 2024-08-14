from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from flask_login import UserMixin

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Cafe(db.Model):
    __tablename__='cafe'
    id :Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str] = mapped_column(String(250), nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url:Mapped[str] = mapped_column(String(500), nullable=False)
    location:Mapped[str] = mapped_column(String(250), nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean,nullable=False)
    seats: Mapped[String] = mapped_column(String(250), nullable=False)
    coffee_price: Mapped[String] = mapped_column(String(250), nullable=False)


class User(UserMixin,db.Model):
    __tablename__='user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250),nullable=False)
    email: Mapped[str] = mapped_column(String(250),nullable=False)
    password: Mapped[str] = mapped_column(String(1000))


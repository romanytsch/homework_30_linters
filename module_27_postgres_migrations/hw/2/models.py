from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy import text

db = SQLAlchemy()


class Coffee(db.Model):
    __tablename__ = 'coffee'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200))
    description = db.Column(db.String(200))
    reviews = db.Column(ARRAY(db.String))  # PostgreSQL ARRAY


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    has_sale = db.Column(db.Boolean, default=False)
    address = db.Column(JSONB)  # PostgreSQL JSON
    coffee_id = db.Column(db.Integer, db.ForeignKey('coffee.id'))
    coffee = db.relationship('Coffee', backref='users')

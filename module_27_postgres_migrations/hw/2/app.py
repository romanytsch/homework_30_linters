from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@localhost/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модели
from sqlalchemy.dialects.postgresql import ARRAY, JSONB


class Coffee(db.Model):
    __tablename__ = 'coffee'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    reviews = db.Column(ARRAY(db.String))


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(JSONB)
    coffee_id = db.Column(db.Integer, db.ForeignKey('coffee.id'))
    coffee = db.relationship('Coffee', backref='users')


# Данные один раз
def init_db():
    with app.app_context():
        db.create_all()
        if not Coffee.query.first():
            coffee = Coffee(title="Арабика", reviews=["Отличный", "Хороший"])
            db.session.add(coffee)
            db.session.flush()

            User(name="Иван", address={'country': 'Russia'}, coffee_id=coffee.id)
            User(name="Мария", address={'country': 'Belarus'}, coffee_id=coffee.id)
            db.session.commit()


# Роуты
@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.json.get('name')
    user = User(name=name, address={'country': 'Belarus'}, coffee_id=1)
    db.session.add(user)
    db.session.commit()
    return jsonify({'user': {'name': user.name, 'coffee': user.coffee.title}})


@app.route('/search_coffee/<query>')
def search_coffee(query):
    from sqlalchemy import text
    return jsonify([c.title for c in db.session.query(Coffee)
                   .filter(text("title ilike :q")).params(q=f'%{query}%').all()])


@app.route('/unique_reviews')
def unique_reviews():
    from sqlalchemy import func
    return jsonify([{'review': r.review} for r in
                    db.session.query(func.unnest(Coffee.reviews).label('review')).distinct()])


@app.route('/users_by_country/<country>')
def users_by_country(country):
    return jsonify([{'name': u.name} for u in
                    User.query.filter(User.address['country'].astext == country)])


if __name__ == '__main__':
    init_db()
    app.run(debug=True)

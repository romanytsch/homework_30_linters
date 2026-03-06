from app import app
from models import db, Coffee, User
from flask import request, jsonify
import requests
from sqlalchemy import text, func

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')

    # Создаем случайный адрес
    addr_resp = requests.get('https://dummyjson.com/users')
    addr_data = addr_resp.json()['users'][0]['address']
    address = {'country': addr_data['country'], 'city': addr_data['city']}

    user = User(
        name=name,
        has_sale=False,
        address=address,
        coffee_id=1  # Первый кофе
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'user': {
            'id': user.id,
            'name': user.name,
            'coffee': user.coffee.title
        }
    })


@app.route('/search_coffee/<query>')
def search_coffee(query):
    # Полнотекстовый поиск PostgreSQL через SQLAlchemy
    search = db.session.query(Coffee) \
        .filter(text("to_tsvector('russian', title) @@ plainto_tsquery('russian', :query)")) \
        .params(query=query).all()

    return jsonify([{
        'id': c.id,
        'title': c.title,
        'category': c.category
    } for c in search])


@app.route('/unique_reviews')
def unique_reviews():
    reviews = db.session.query(func.unnest(Coffee.reviews).label('review')) \
        .distinct().all()

    return jsonify([{'review': r.review} for r in reviews])


@app.route('/users_by_country/<country>')
def users_by_country(country):
    users = db.session.query(User) \
        .filter(User.address['country'].astext == country).all()

    return jsonify([{
        'id': u.id,
        'name': u.name,
        'coffee': u.coffee.title if u.coffee else None
    } for u in users])
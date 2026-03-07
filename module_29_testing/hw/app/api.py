from flask import Blueprint, jsonify, request
from .database import db
from .models import Client, Parking, ClientParking
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError

api_bp = Blueprint('api', __name__)


@api_bp.route('/clients', methods=['GET'])
def get_clients():
    """Список всех клиентов"""
    clients = Client.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'surname': c.surname,
        'car_number': c.car_number
    } for c in clients])


@api_bp.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    """Информация клиента по ID"""
    client = Client.query.get_or_404(client_id)
    return jsonify({
        'id': client.id,
        'name': client.name,
        'surname': client.surname,
        'credit_card': client.credit_card or None,
        'car_number': client.car_number
    })


@api_bp.route('/clients', methods=['POST'])
def create_client():
    """Создать нового клиента"""
    data = request.get_json()

    if not all(key in data for key in ['name', 'surname', 'car_number']):
        return jsonify({'error': 'Требуются name, surname, car_number'}), 400

    client = Client(
        name=data['name'],
        surname=data['surname'],
        credit_card=data.get('credit_card'),
        car_number=data['car_number']
    )

    try:
        db.session.add(client)
        db.session.commit()
        db.session.refresh(client)
        return jsonify({
            'id': client.id,
            'message': 'Клиент создан успешно'
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Клиент с таким номером авто уже существует'}), 409


@api_bp.route('/parkings', methods=['POST'])
def create_parking():
    """Создать парковочную зону"""
    data = request.get_json()

    if not all(key in data for key in ['address', 'count_places']):
        return jsonify({'error': 'Требуются address, count_places'}), 400

    if data['count_places'] <= 0:
        return jsonify({'error': 'Количество мест должно быть > 0'}), 400

    parking = Parking(
        address=data['address'],
        opened=data.get('opened', True),
        count_places=data['count_places'],
        count_available_places=data['count_places']
    )

    db.session.add(parking)
    db.session.commit()
    db.session.refresh(parking)

    return jsonify({
        'id': parking.id,
        'address': parking.address,
        'total_places': parking.count_places,
        'message': 'Парковка создана'
    }), 201


@api_bp.route('/client_parkings', methods=['POST'])
def client_enter_parking():
    """Заезд на парковку"""
    data = request.get_json()

    if not all(key in data for key in ['client_id', 'parking_id']):
        return jsonify({'error': 'Требуются client_id, parking_id'}), 400

    client_id = data['client_id']
    parking_id = data['parking_id']

    # Проверки
    client = Client.query.get_or_404(client_id)
    parking = Parking.query.get_or_404(parking_id)

    if not parking.opened:
        return jsonify({'error': 'Парковка закрыта'}), 400

    if parking.count_available_places <= 0:
        return jsonify({'error': 'Нет свободных мест'}), 400

    # Уже на парковке?
    existing = ClientParking.query.filter_by(
        client_id=client_id,
        parking_id=parking_id,
        time_out=None
    ).first()

    if existing:
        return jsonify({'error': 'Клиент уже на парковке'}), 400

    # Заезд
    entry = ClientParking(
        client_id=client_id,
        parking_id=parking_id,
        time_in=datetime.now(timezone.utc)
    )
    db.session.add(entry)
    parking.count_available_places -= 1
    db.session.commit()

    return jsonify({
        'message': 'Шлагбаум поднят',
        'places_left': parking.count_available_places,
        'total_places': parking.count_places
    })


@api_bp.route('/client_parkings', methods=['DELETE'])
def client_exit_parking():
    """Выезд с парковки"""
    data = request.get_json()

    if not all(key in data for key in ['client_id', 'parking_id']):
        return jsonify({'error': 'Требуются client_id, parking_id'}), 400

    client_id = data['client_id']
    parking_id = data['parking_id']

    # Найти активную сессию
    entry = ClientParking.query.filter_by(
        client_id=client_id,
        parking_id=parking_id,
        time_out=None
    ).first_or_404()

    client = Client.query.get(client_id)
    parking = Parking.query.get(parking_id)

    # Проверка оплаты
    if not client.credit_card:
        return jsonify({'error': 'Карта не привязана для оплаты'}), 400

    # Расчет оплаты (2 руб/мин)
    now = datetime.now(timezone.utc)
    duration = now - entry.time_in
    minutes = duration.total_seconds() / 60
    cost = round(minutes * 2, 2)

    # Выезд
    entry.time_out = now
    parking.count_available_places += 1
    db.session.commit()

    return jsonify({
        'message': 'Шлагбаум открыт',
        'duration_minutes': round(minutes, 1),
        'cost': f'{cost} ₽',
        'places_left': parking.count_available_places
    })

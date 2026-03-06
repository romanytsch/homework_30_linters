from flask import Blueprint, jsonify, request
from sqlalchemy import select, and_
from datetime import datetime, timezone
from database import async_session
from models import Client, Parking, ClientParking

api_bp = Blueprint('api', __name__, url_prefix='/v1')


@api_bp.post("/clients")
async def create_client():
    data = request.get_json()

    async with async_session() as session:
        client = Client(
            name=data['name'],
            surname=data['surname'],
            credit_card=data.get('credit_card'),
            car_number=data['car_number']
        )
        session.add(client)
        await session.commit()
        await session.refresh(client)

        return jsonify({
            "status": "ok",
            "client_id": client.id,
            "message": "Клиент зарегистрирован"
        }), 201


@api_bp.get("/parking/<int:parking_id>/enter/<car_number>")
async def car_enter(parking_id: int, car_number: str):
    async with async_session() as session:
        result = await session.execute(
            select(Client).where(Client.car_number == car_number)
        )
        client = result.scalar_one_or_none()

        if not client:
            return jsonify({"error": "Клиент не найден"}), 404

        result = await session.execute(
            select(Parking).where(Parking.id == parking_id)
        )
        parking = result.scalar_one()

        if parking.count_available_places <= 0:
            return jsonify({"error": "Нет свободных мест"}), 400

        result = await session.execute(
            select(ClientParking)
            .where(and_(
                ClientParking.client_id == client.id,
                ClientParking.parking_id == parking_id,
                ClientParking.time_out.is_(None)
            ))
        )
        if result.scalar_one_or_none():
            return jsonify({"error": "Машина уже на парковке"}), 400

        entry = ClientParking(
            client_id=client.id,
            parking_id=parking_id,
            time_in=datetime.now(timezone.utc)
        )
        session.add(entry)
        parking.count_available_places -= 1

        await session.commit()

        return jsonify({
            "status": "ok",
            "action": "enter_granted",
            "message": "Шлагбаум поднят",
            "places_left": parking.count_available_places
        })


@api_bp.get("/parking/<int:parking_id>/exit/<car_number>")
async def car_exit(parking_id: int, car_number: str):
    async with async_session() as session:
        result = await session.execute(
            select(ClientParking)
            .where(and_(
                ClientParking.parking_id == parking_id,
                ClientParking.time_out.is_(None),
                ClientParking.client.has(car_number=car_number)
            ))
        )
        entry = result.scalar_one_or_none()

        if not entry:
            return jsonify({"error": "Машина не на парковке"}), 404

        entry.time_out = datetime.now(timezone.utc)
        parking = await session.get(Parking, parking_id)
        parking.count_available_places += 1

        duration = entry.time_out - entry.time_in
        minutes = duration.total_seconds() / 60
        cost = round(minutes * 2, 2)

        await session.commit()

        return jsonify({
            "status": "ok",
            "action": "exit_granted",
            "duration_minutes": round(minutes, 1),
            "cost_rub": cost,
            "places_left": parking.count_available_places
        })


@api_bp.get("/parking/<int:parking_id>/status")
async def parking_status(parking_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(Parking).where(Parking.id == parking_id)
        )
        parking = result.scalar_one()

        occupied_result = await session.execute(
            select(ClientParking)
            .where(and_(
                ClientParking.parking_id == parking_id,
                ClientParking.time_out.is_(None)
            ))
        )
        occupied_count = len(occupied_result.scalars().all())

        return jsonify({
            "parking_id": parking.id,
            "address": parking.address,
            "total_places": parking.count_places,
            "available_places": parking.count_available_places,
            "occupied_now": occupied_count,
            "opened": parking.opened
        })


@api_bp.get("/parking")
async def all_parkings():
    async with async_session() as session:
        result = await session.execute(select(Parking))
        parkings = result.scalars().all()

        return jsonify([{
            "id": p.id,
            "address": p.address,
            "total_places": p.count_places,
            "available_places": p.count_available_places
        } for p in parkings])

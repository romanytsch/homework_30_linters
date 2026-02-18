from flask import Flask, request, jsonify
from services import BookingService
from database import HotelRepository

app = Flask(__name__)
repo = HotelRepository()
service = BookingService(repo)


@app.route('/add-room', methods=['POST'])
def add_room():
    data = request.get_json()
    room_id = service.add_room(
        data['floor'], data['beds'], data['guestNum'], data['price']
    )
    return jsonify({'roomId': room_id}), 200


@app.route('/room', methods=['GET'])
def get_rooms():
    check_in = request.args.get('checkIn', '19000101')
    check_out = request.args.get('checkOut', '21000101')
    guests_num = int(request.args.get('guestsNum', 1))

    rooms_data = service.find_available_rooms(check_in, check_out, guests_num)
    result = [{
        'roomId': r['room_id'],
        'floor': r['floor'],
        'guestNum': r['guest_num'],
        'beds': r['beds'],
        'price': r['price']
    } for r in rooms_data]
    return jsonify({'rooms': result}), 200


@app.route('/booking', methods=['POST'])
def create_booking():
    try:
        data = request.get_json()
        success = service.book_room(
            data['roomId'], data['firstName'], data['lastName'],
            data['bookingDates']['checkIn'], data['bookingDates']['checkOut']
        )
        if not success:
            return '', 409
        return '', 200
    except KeyError:
        return '', 400
    except Exception:
        return '', 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)

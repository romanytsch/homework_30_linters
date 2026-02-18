import sqlite3
from typing import List, Dict, Any
from models import Room, Booking


class HotelRepository:
    def __init__(self, db_path: str = "hotel.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS rooms (
                    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    floor INTEGER NOT NULL,
                    beds INTEGER NOT NULL,
                    guest_num INTEGER NOT NULL,
                    price INTEGER NOT NULL,
                    is_booked BOOLEAN DEFAULT FALSE
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS bookings (
                    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_id INTEGER NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    check_in TEXT NOT NULL,
                    check_out TEXT NOT NULL
                )
            ''')
            conn.commit()

    def create_room(self, floor: int, beds: int, guest_num: int, price: int) -> int:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                'INSERT INTO rooms (floor, beds, guest_num, price) VALUES (?, ?, ?, ?)',
                (floor, beds, guest_num, price)
            )
            return conn.execute('SELECT last_insert_rowid()').fetchone()[0]

    def find_available_rooms(self, guests_num: int) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT room_id, floor, guest_num, beds, price, is_booked
                FROM rooms WHERE guest_num >= ? AND is_booked = FALSE
            ''', (guests_num,))
            return [dict(row) for row in cursor.fetchall()]

    def book_room(self, room_id: int, booking: Booking) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT is_booked FROM rooms WHERE room_id = ?', (room_id,)
            )
            result = cursor.fetchone()
            if not result or result[0]:  # result[0] вместо result['is_booked']
                return False

            conn.execute('UPDATE rooms SET is_booked = TRUE WHERE room_id = ?', (room_id,))
            conn.execute('''
                INSERT INTO bookings (room_id, first_name, last_name, check_in, check_out)
                VALUES (?, ?, ?, ?, ?)
            ''', (booking.room_id, booking.first_name, booking.last_name,
                  booking.check_in, booking.check_out))
            conn.commit()
            return True


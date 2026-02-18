from typing import List
from models import Room, Booking
from database import HotelRepository


class BookingService:
    def __init__(self, repo: HotelRepository):
        self.repo = repo

    def add_room(self, floor: int, beds: int, guest_num: int, price: int) -> int:
        return self.repo.create_room(floor, beds, guest_num, price)

    def find_available_rooms(self, check_in: str, check_out: str, guests_num: int) -> List[dict]:
        return self.repo.find_available_rooms(guests_num)

    def book_room(self, room_id: int, first_name: str, last_name: str,
                  check_in: str, check_out: str) -> bool:
        booking = Booking(room_id, first_name, last_name, check_in, check_out)
        return self.repo.book_room(room_id, booking)
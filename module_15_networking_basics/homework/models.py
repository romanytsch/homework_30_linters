from dataclasses import dataclass

@dataclass
class Room:
    room_id: int
    floor: int
    beds: int
    guest_num: int
    price: int
    is_booked: bool = False

@dataclass
class Booking:
    room_id: int
    first_name: str
    last_name: str
    check_in: str
    check_out: str

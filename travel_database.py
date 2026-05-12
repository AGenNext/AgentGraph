"""
Travel Database - Complete Booking System

Travel database:
- Flights, Hotels, Cars
- Destinations
- Bookings
- Airlines, Hotel chains

Reference:
- Expedia/Booking.com style
- Travel booking systems
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, date, time
from enum import Enum
from base_entity import Entity


# =============================================================================
# TYPES
# =============================================================================

class TripType(Enum):
    One_Way = "One_Way"
    Round_Trip = "Round_Trip"
    Multi_City = "Multi_City"


class CabinClass(Enum):
    Economy = "Economy"
    Premium_Economy = "Premium_Economy"
    Business = "Business"
    First = "First"


class HotelType(Enum):
    Hotel = "Hotel"
    Resort = "Resort"
    Hostel = "Hostel"
    Apartment = "Apartment"
    Villa = "Villa"


class BookingStatus(Enum):
    Confirmed = "Confirmed"
    Pending = "Pending"
    Cancelled = "Cancelled"
    Completed = "Completed"


# =============================================================================
# ENTITIES
# =============================================================================

@dataclass
class Entity(Entity):
class Airport:
    """Airport"""
    code: str  # IATA code
    name: str
    
    city: str
    country: str
    
    timezone: str = ""
    
    def to_dict(self) -> Dict:
        return {"code": self.code, "name": self.name, "city": self.city}


@dataclass
class Entity(Entity):
class Flight:
    """Flight"""
    id: str
    
    airline: str
    
    flight_number: str
    
    origin: str  # airport code
    destination: str
    
    departure: datetime
    arrival: datetime
    
    duration_minutes: int
    
    aircraft: str = ""
    
    price: float = 0.0
    
    cabin_class: CabinClass = CabinClass.Economy
    
    seats_available: int = 0
    
    stops: int = 0
    
    layover_airports: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "airline": self.airline,
            "route": f"{self.origin} -> {self.destination}",
            "price": self.price
        }


@dataclass
class Entity(Entity):
class Airline:
    """Airline"""
    code: str  # IATA code
    name: str
    
    country: str = ""
    
    fleet_size: int = 0
    
    destinations: int = 0
    
    website: str = ""


@dataclass
class Entity(Entity):
class Hotel:
    """Hotel"""
    id: str
    name: str
    
    location: str  # city or address
    
    hotel_type: HotelType = HotelType.Hotel
    
    star_rating: int = 3
    
    price_per_night: float = 0.0
    
    currency: str = "USD"
    
    description: str = ""
    
    amenities: List[str] = field(default_factory=list)
    
    images: List[str] = field(default_factory=list)
    
    review_score: float = 0.0
    review_count: int = 0
    
    rooms: int = 0
    
    check_in: time = field(default_factory=lambda: time(15, 0))
    check_out: time = field(default_factory=lambda: time(11, 0))
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "price": self.price_per_night
        }


@dataclass
class Entity(Entity):
class Room:
    """Hotel room"""
    id: str
    hotel_id: str
    
    room_type: str  # Standard, Deluxe, Suite
    
    beds: str = ""  # 1 King, 2 Queen
    
    max_occupancy: int = 2
    
    price: float = 0.0
    
    amenities: List[str] = field(default_factory=list)
    
    available: bool = True


@dataclass
class Entity(Entity):
class Destination:
    """Travel destination"""
    id: str
    name: str
    
    country: str
    region: str = ""
    
    description: str = ""
    
    best_time: List[str] = field(default_factory=list)  # months
    
    attractions: List[str] = field(default_factory=list)
    
    avg_cost_per_day: float = 0.0
    
    safety_score: float = 0.0
    
    visa_required: bool = False


@dataclass
class Entity(Entity):
class Booking:
    """Travel booking"""
    id: str
    user_id: str
    
    booking_type: str  # flight, hotel, car
    
    status: BookingStatus = BookingStatus.Pending
    
    created_at: datetime = field(default_factory=datetime.now)
    
    total_price: float = 0.0
    
    confirmation_code: str = ""


# =============================================================================
# FLIGHT BOOKING
# =============================================================================

@dataclass
class Entity(Entity):
class FlightBooking(Booking):
    """Flight booking"""
    flight_id: str = ""
    
    passengers: int = 1
    
    cabin_class: CabinClass = CabinClass.Economy
    
    trip_type: TripType = TripType.One_Way
    
    return_flight_id: str = ""


# =============================================================================
# HOTEL BOOKING
# =============================================================================

@dataclass
class Entity(Entity):
class HotelBooking(Booking):
    """Hotel booking"""
    hotel_id: str = ""
    room_id: str = ""
    
    check_in: date = None
    check_out: date = None
    
    guests: int = 1
    
    nights: int = 1


# =============================================================================
# DATABASE
# =============================================================================

class TravelDatabase:
    """Travel database"""
    
    def __init__(self):
        # Core data
        self.airports: Dict[str, Airport] = {}
        self.airlines: Dict[str, Airline] = {}
        self.flights: Dict[str, Flight] = {}
        
        self.hotels: Dict[str, Hotel] = {}
        self.rooms: Dict[str, Room] = {}
        
        self.destinations: Dict[str, Destination] = {}
        
        # Bookings
        self.bookings: Dict[str, Booking] = {}
        
        self.flight_bookings: Dict[str, FlightBooking] = {}
        self.hotel_bookings: Dict[str, HotelBooking] = {}
    
    # Airports
    def add_airport(
        self,
        code: str,
        name: str,
        city: str,
        country: str,
        **kwargs
    ) -> Airport:
        airport = Airport(
            code=code,
            name=name,
            city=city,
            country=country,
            **kwargs
        )
        self.airports[code] = return airport
    
    def get_airport(self, code: str) -> Optional[Airport]:
        return self.airports.get(code)
    
    def search_airports(self, query: str) -> List[Airport]:
        q = query.lower()
        return [
            a for a in self.airports.values()
            if q in a.name.lower() or q in a.city.lower()
        ]
    
    # Airlines
    def add_airline(
        self,
        code: str,
        name: str,
        **kwargs
    ) -> Airline:
        airline = Airline(code=code, name=name, **kwargs)
        self.airlines[code] = return airline
    
    def get_airline(self, code: str) -> Optional[Airline]:
        return self.airlines.get(code)
    
    # Flights
    def add_flight(
        self,
        flight: Flight
    ) -> str:
        self.flights[flight.id] = return flight.id
    
    def search_flights(
        self,
        origin: str,
        destination: str,
        date: date = None,
        cabin_class: CabinClass = None
    ) -> List[Flight]:
        results = [
            f for f in self.flights.values()
            if f.origin == origin and f.destination == destination
        ]
        
        if cabin_class:
            results = [f for f in results if f.cabin_class == cabin_class]
        
        results.sort(key=lambda f: f.price)
        
        return results
    
    def get_flight(self, flight_id: str) -> Optional[Flight]:
        return self.flights.get(flight_id)
    
    # Hotels
    def add_hotel(
        self,
        hotel: Hotel
    ) -> str:
        self.hotels[hotel.id] = return hotel.id
    
    def get_hotel(self, hotel_id: str) -> Optional[Hotel]:
        return self.hotels.get(hotel_id)
    
    def search_hotels(
        self,
        location: str = None,
        min_rating: float = None
    ) -> List[Hotel]:
        results = list(self.hotels.values())
        
        if location:
            l = location.lower()
            results = [
                h for h in results
                if l in h.location.lower()
            ]
        
        if min_rating:
            results = [
                h for h in results
                if h.review_score >= min_rating
            ]
        
        results.sort(key=lambda h: h.price_per_night)
        
        return results
    
    def get_location_hotels(self, location: str) -> List[Hotel]:
        l = location.lower()
        return [
            h for h in self.hotels.values()
            if l in h.location.lower()
        ]
    
    # Room
    def add_room(self, room: Room) -> str:
        self.rooms[room.id] = return room.id
    
    def get_hotel_rooms(self, hotel_id: str) -> List[Room]:
        return [r for r in self.rooms.values() if r.hotel_id == hotel_id]
    
    # Destinations
    def add_destination(
        self,
        dest: Destination
    ) -> str:
        self.destinations[dest.id] = return dest.id
    
    def get_destination(self, dest_id: str) -> Optional[Destination]:
        return self.destinations.get(dest_id)
    
    def search_destinations(
        self,
        country: str = None,
        attractions: str = None
    ) -> List[Destination]:
        results = list(self.destinations.values())
        
        if country:
            results = [
                d for d in results
                if country.lower() in d.country.lower()
            ]
        
        if attractions:
            a = attractions.lower()
            results = [
                d for d in results
                if a in [att.lower() for att in d.attractions]
            ]
        
        return results
    
    # Bookings
    def book_flight(
        self,
        user_id: str,
        flight_id: str,
        passengers: int = 1,
        cabin_class: CabinClass = CabinClass.Economy
    ) -> Optional[FlightBooking]:
        flight = self.flights.get(flight_id)
        if not flight:
            return None
        
        booking = FlightBooking(
            id=f"fb_{flight_id}_{user_id}",
            user_id=user_id,
            flight_id=flight_id,
            passengers=passengers,
            cabin_class=cabin_class,
            total_price=flight.price * passengers,
            status=BookingStatus.Confirmed
        )
        
        self.flight_bookings[booking.id] = booking
        self.bookings[booking.id] = booking
        
        return booking
    
    def book_hotel(
        self,
        user_id: str,
        hotel_id: str,
        check_in: date,
        check_out: date,
        guests: int = 1
    ) -> Optional[HotelBooking]:
        hotel = self.hotels.get(hotel_id)
        if not hotel:
            return None
        
        nights = (check_out - check_in).days
        price = hotel.price_per_night * nights
        
        booking = HotelBooking(
            id=f"hb_{hotel_id}_{user_id}",
            user_id=user_id,
            hotel_id=hotel_id,
            check_in=check_in,
            check_out=check_out,
            guests=guests,
            nights=nights,
            total_price=price,
            status=BookingStatus.Confirmed
        )
        
        self.hotel_bookings[booking.id] = booking
        self.bookings[booking.id] = booking
        
        return booking
    
    def get_user_bookings(self, user_id: str) -> List[Booking]:
        return [b for b in self.bookings.values() if b.user_id == user_id]
    
    # Statistics
    def stats(self) -> Dict:
        return {
            "airports": len(self.airports),
            "flights": len(self.flights),
            "hotels": len(self.hotels),
            "destinations": len(self.destinations),
            "bookings": len(self.bookings)
        }


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("Travel Database")
    print("=" * 50)
    
    db = TravelDatabase()
    
    # Add airports
    airports = [
        ("JFK", "Kennedy International", "New York", "USA"),
        ("LAX", "Los Angeles International", "Los Angeles", "USA"),
        ("LHR", "Heathrow", "London", "UK"),
        ("CDG", "Charles de Gaulle", "Paris", "France"),
    ]
    
    for code, name, city, country in airports:
        db.add_airport(code, name, city, country)
    
    # Add flight
    flight = Flight(
        id="f1",
        airline="AA",
        flight_number="AA100",
        origin="JFK",
        destination="LAX",
        departure=datetime(2024, 6, 15, 10, 0),
        arrival=datetime(2024, 6, 15, 13, 30),
        duration_minutes=330,
        price=299.99,
        seats_available=50
    )
    db.add_flight(flight)
    
    # Search flights
    print("\nSearch JFK -> LAX:")
    flights = db.search_flights("JFK", "LAX")
    for f in flights:
        print(f"  {f.airline} {f.flight_number}: ${f.price}")
    
    # Add hotels
    hotel = Hotel(
        id="h1",
        name="Grand Hotel",
        location="New York",
        star_rating=4,
        price_per_night=199.99,
        review_score=8.5
    )
    db.add_hotel(hotel)
    
    # Search hotels
    print("\nSearch New York hotels:")
    hotels = db.search_hotels("New York")
    for h in hotels:
        print(f"  {h.name}: ${h.price_per_night}/night")
    
    # Book flight
    booking = db.book_flight("user1", "f1", passengers=2)
    print(f"\nFlight booked: {booking.total_price}")
    
    print(f"\nStats:")
    stats = db.stats()
    print(f"  Flights: {stats['flights']}")
    print(f"  Hotels: {stats['hotels']}")


if __name__ == "__main__":
    main()


"""
Travel Database Usage

    db = TravelDatabase()
    
    # Flights
    flight = db.search_flights("JFK", "LAX")
    flights = db.search_flights("JFK", "LAX", cabin_class=CabinClass.Business)
    
    # Hotels
    hotels = db.search_hotels("New York", min_rating=8.0)
    hotels = db.get_location_hotels("Paris")
    
    # Destinations
    destinations = db.search_destinations(country="Italy")
    
    # Bookings
    booking = db.book_flight("user1", "flight_id", passengers=2)
    booking = db.book_hotel("user1", "hotel_id", check_in, check_out)
    bookings = db.get_user_bookings("user1")
"""
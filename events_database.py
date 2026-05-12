"""
Events Database - Conferences & Events

Events database:
- Conferences, Meetups
- Venues, Locations
- Speakers, Sponsors
- Tickets, Registration

Reference:
- Eventbrite: https://www.eventbrite.com/platform/api
- Meetup API: https://www.meetup.com/api/
- Lanyard (speakers): https://lanyard.com/
- Ticketmaster: https://developer.ticketmaster.com/

Data Sources:
- Eventbrite API
- Meetup API
- Lanyard (speaker bios)
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

class EventType(Enum):
    Conference = "Conference"
    Meetup = "Meetup"
    Workshop = "Workshop"
    Concert = "Concert"
    Festival = "Festival"
    Webinar = "Webinar"
    Hackathon = "Hackathon"
    Networking = "Networking"


class TicketType(Enum):
    Free = "Free"
    General = "General"
    VIP = "VIP"
    Early_Bird = "Early_Bird"
    Student = "Student"


# =============================================================================
# ENTITIES
# =============================================================================

@dataclass
class Entity(Entity):
class Event:
    """Event"""
    id: str
    name: str
    
    event_type: EventType = EventType.Conference
    
    description: str = ""
    
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    
    start_time: str = ""
    end_time: str = ""
    
    venue: str = ""
    city: str = ""
    country: str = ""
    
    online: bool = False
    online_url: str = ""
    
    organizer_id: str = ""
    
    capacity: int = 0
    attendees: int = 0
    
    price_min: float = 0.0
    price_max: float = 0.0
    
    currency: str = "USD"
    
    tags: List[str] = field(default_factory=list)
    
    website: str = ""
    
    registration_deadline: Optional[date] = None


@dataclass
class Entity(Entity):
class Organizer:
    """Event organizer"""
    id: str
    name: str
    
    description: str = ""
    
    email: str = ""
    phone: str = ""
    
    website: str = ""
    
    events_count: int = 0


@dataclass
class Entity(Entity):
class Speaker:
    """Speaker"""
    id: str
    name: str
    
    title: str = ""
    company: str = ""
    
    bio: str = ""
    
    image_url: str = ""
    
    twitter: str = ""
    linkedin: str = ""
    
    topics: List[str] = field(default_factory=list)


@dataclass
class Entity(Entity):
class Sponsor:
    """Sponsor"""
    id: str
    name: str
    
    tier: str = ""  # Platinum, Gold, Silver
    
    logo_url: str = ""
    
    website: str = ""
    
    description: str = ""


@dataclass
class Entity(Entity):
class Session:
    """Event session"""
    id: str
    event_id: str
    
    title: str = ""
    description: str = ""
    
    speaker_ids: List[str] = field(default_factory=list)
    
    start_time: str = ""
    end_time: str = ""
    
    room: str = ""
    
    track: str = ""


# =============================================================================
# DATABASE
# =============================================================================

class EventsDatabase:
    """Events database"""
    
    def __init__(self):
        self.events: Dict[str, Event] = {}
        self.organizers: Dict[str, Organizer] = {}
        self.speakers: Dict[str, Speaker] = {}
        self.sponsors: Dict[str, Sponsor] = {}
        self.sessions: Dict[str, Session] = {}
        
        # Indexes
        self.events_by_organizer: Dict[str, List[str]] = {}
        self.events_by_city: Dict[str, List[str]] = {}
        self.sessions_by_event: Dict[str, List[str]] = {}
    
    # Events
    def add_event(self, event: Event) -> str:
        self.events[event.id] = event
        
        # Index
        if event.organizer_id:
            if event.organizer_id not in self.events_by_organizer:
                self.events_by_organizer[event.organizer_id] = []
            self.events_by_organizer[event.organizer_id].append(event.id)
        
        if event.city:
            key = event.city.lower()
            if key not in self.events_by_city:
                self.events_by_city[key] = []
            self.events_by_city[key].append(event.id)
        
        return event.id
    
    def get_event(self, event_id: str) -> Optional[Event]:
        return self.events.get(event_id)
    
    def search_events(
        self,
        query: str = None,
        event_type: EventType = None,
        city: str = None,
        after_date: date = None
    ) -> List[Event]:
        results = list(self.events.values())
        
        if query:
            q = query.lower()
            results = [
                e for e in results
                if q in e.name.lower() or q in e.description.lower()
            ]
        
        if event_type:
            results = [e for e in results if e.event_type == event_type]
        
        if city:
            results = [e for e in results if e.city.lower() == city.lower()]
        
        if after_date:
            results = [
                e for e in results
                if e.start_date and e.start_date >= after_date
            ]
        
        results.sort(key=lambda e: e.start_date or date(1900, 1, 1))
        
        return results
    
    def get_upcoming_events(self, limit: int = 10) -> List[Event]:
        today = date.today()
        return self.search_events(after_date=today)[:limit]
    
    # Speakers
    def add_speaker(self, speaker: Speaker) -> str:
        self.speakers[speaker.id] = speaker
        return speaker.id
    
    def get_speaker(self, speaker_id: str) -> Optional[Speaker]:
        return self.speakers.get(speaker_id)
    
    def search_speakers(
        self,
        topic: str = None
    ) -> List[Speaker]:
        results = list(self.speakers.values())
        
        if topic:
            t = topic.lower()
            results = [
                s for s in results
                if any(t in topic.lower() for topic in s.topics)
            ]
        
        return results
    
    # Sessions
    def add_session(self, session: Session) -> str:
        self.sessions[session.id] = session
        
        # Index
        if session.event_id:
            if session.event_id not in self.sessions_by_event:
                self.sessions_by_event[session.event_id] = []
            self.sessions_by_event[session.event_id].append(session.id)
        
        return session.id
    
    def get_event_sessions(self, event_id: str) -> List[Session]:
        session_ids = self.sessions_by_event.get(event_id, [])
        return sorted(
            [self.sessions[sid] for sid in session_ids if sid in self.sessions],
            key=lambda s: s.start_time
        )
    
    # Stats
    def stats(self) -> Dict:
        return {
            "events": len(self.events),
            "speakers": len(self.speakers),
            "sessions": len(self.sessions),
            "upcoming": len(self.get_upcoming_events(100))
        }


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 50)
    print("Events Database")
    print("=" * 50)
    
    db = EventsDatabase()
    
    # Add event
    event = Event(
        id="e1",
        name="Tech Conference 2024",
        event_type=EventType.Conference,
        start_date=date(2024, 6, 15),
        city="San Francisco",
        country="USA",
        capacity=5000
    )
    db.add_event(event)
    
    print(f"\nEvent: {event.name}")
    print(f"  Type: {event.event_type.value}")
    print(f"  When: {event.start_date}")
    
    # Add speaker
    speaker = Speaker(
        id="s1",
        name="Jane Smith",
        title="CTO",
        company="TechCorp",
        topics=["AI", "Machine Learning"]
    )
    db.add_speaker(speaker)
    
    print(f"\nSpeaker: {speaker.name}")
    
    print(f"\nStats:")
    print(f"  {db.stats()}")


if __name__ == "__main__":
    main()
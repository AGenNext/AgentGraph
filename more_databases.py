"""
More Databases - Weather, News, Travel, Jobs, Social

Added databases:
- Weather
- News/Articles
- Travel/Booking
- Job Listings
- Social Media
- IoT/Devices
- Cryptocurrency

Reference: Various APIs
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, date, time
from enum import Enum


# =============================================================================
# WEATHER DATABASE
# =============================================================================

class WeatherCondition(Enum):
    SUNNY = "Sunny"
    CLOUDY = "Cloudy"
    PARTLY_CLOUDY = "Partly Cloudy"
    RAINY = "Rainy"
    STORMY = "Stormy"
    SNOWY = "Snowy"
    FOGGY = "Foggy"
    WINDY = "Windy"


@dataclass
class Weather:
    """Weather data"""
    id: str
    location: str
    
    temperature: float  # Fahrenheit
    feels_like: float
    
    condition: WeatherCondition
    
    humidity: float  # percentage
    pressure: float  # inches
    visibility: float  # miles
    
    wind_speed: float  # mph
    wind_direction: str  # N, S, E, W
    
    uv_index: int = 0
    air_quality: int = 0  # 0-500 AQI
    
    forecast: List[Dict] = field(default_factory=list)
    
    updated_at: Optional[datetime] = None


@dataclass
class Forecast:
    """Weather forecast"""
    id: str
    location: str
    
    date: date
    high: float
    low: float
    condition: WeatherCondition
    precipitation_chance: float


# =============================================================================
# NEWS DATABASE
# =============================================================================

class NewsCategory(Enum):
    BUSINESS = "Business"
    TECHNOLOGY = "Technology"
    POLITICS = "Politics"
    SCIENCE = "Science"
    HEALTH = "Health"
    SPORTS = "Sports"
    ENTERTAINMENT = "Entertainment"
    WORLD = "World"


@dataclass
class Article:
    """News article"""
    id: str
    title: str
    
    category: NewsCategory
    
    summary: Optional[str] = None
    content: Optional[str] = None
    
    author: Optional[str] = None
    source: Optional[str] = None
    
    url: Optional[str] = None
    
    image_url: Optional[str] = None
    
    published_at: Optional[datetime] = None
    
    tags: List[str] = field(default_factory=list)
    
    def to_schema(self) -> Dict:
        return {
            "@type": "NewsArticle",
            "@id": self.id,
            "headline": self.title,
            "articleSection": self.category.value
        }


@dataclass
class NewsSource:
    """News source"""
    id: str
    name: str
    
    url: Optional[str] = None
    
    logo_url: Optional[str] = None
    
    categories: List[NewsCategory] = field(default_factory=list)
    
    subscription_required: bool = False


# =============================================================================
# TRAVEL DATABASE
# =============================================================================

class TripStatus(Enum):
    PLANNING = "Planning"
    BOOKED = "Booked"
    IN_PROGRESS = "InProgress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


@dataclass
class Flight:
    """Flight"""
    id: str
    airline: str
    
    flight_number: str
    
    origin: str  # airport code
    destination: str
    
    departure_time: datetime
    arrival_time: datetime
    
    duration_minutes: int
    
    aircraft: Optional[str] = None
    
    price: Optional[float] = None
    
    seats_available: int = 0
    
    class_code: str = "Economy"  # First, Business, Economy


@dataclass
class HotelBooking:
    """Hotel booking"""
    id: str
    hotel_id: str
    guest_id: str
    
    check_in: date
    check_out: date
    
    room_type: str
    guests: int = 1
    
    price_total: float = 0
    
    confirmed: bool = False
    
    amenities: List[str] = field(default_factory=list)


@dataclass
class Trip:
    """Trip"""
    id: str
    name: str
    user_id: str
    
    status: TripStatus = TripStatus.PLANNING
    
    flights: List[Flight] = field(default_factory=list)
    hotels: List[HotelBooking] = field(default_factory=list)
    
    destinations: List[str] = field(default_factory=list)
    
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    
    budget: Optional[float] = None
    
    notes: Optional[str] = None


@dataclass
class Destination:
    """Travel destination"""
    id: str
    name: str
    
    country: Optional[str] = None
    region: Optional[str] = None
    
    description: Optional[str] = None
    
    attractions: List[str] = field(default_factory=list)
    
    best_time_to_visit: List[str] = field(default_factory=list)
    
    avg_cost_per_day: float = 0
    
    safety_rating: float = 0  # 1-10
    fun_rating: float = 0  # 1-10


# =============================================================================
# JOB DATABASE
# =============================================================================

class JobType(Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    INTERNSHIP = "Internship"
    TEMPORARY = "Temporary"
    REMOTE = "Remote"


class ExperienceLevel(Enum):
    ENTRY = "Entry"
    MID = "Mid"
    SENIOR = "Senior"
    EXECUTIVE = "Executive"


@dataclass
class Job:
    """Job listing"""
    id: str
    title: str
    
    company: str
    
    location: Optional[str] = None
    remote: bool = False
    
    job_type: JobType = JobType.FULL_TIME
    experience: ExperienceLevel = ExperienceLevel.MID
    
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    
    description: Optional[str] = None
    requirements: List[str] = field(default_factory=list)
    
    benefits: List[str] = field(default_factory=list)
    
    posted_at: Optional[datetime] = None
    
    apply_url: Optional[str] = None
    
    def to_schema(self) -> Dict:
        return {
            "@type": "JobPosting",
            "@id": self.id,
            "title": self.title,
            "hiringOrganization": self.company,
            "datePosted": str(self.posted_at) if self.posted_at else None
        }


@dataclass
class Employer:
    """Employer/Company"""
    id: str
    name: str
    
    industry: Optional[str] = None
    size: Optional[str] = None  # 1-10, 11-50, etc.
    
    headquarters: Optional[str] = None
    
    website: Optional[str] = None
    
    description: Optional[str] = None
    
    benefits: List[str] = field(default_factory=list)
    
    jobs: List[str] = field(default_factory=list)  # job IDs


# =============================================================================
# SOCIAL MEDIA DATABASE
# =============================================================================

class Platform(Enum):
    TWITTER = "Twitter"
    INSTAGRAM = "Instagram"
    FACEBOOK = "Facebook"
    LINKEDIN = "LinkedIn"
    TIKTOK = "TikTok"
    YOUTUBE = "YouTube"
    REDDIT = "Reddit"


@dataclass
class SocialPost:
    """Social media post"""
    id: str
    platform: Platform
    user_id: str
    
    content: str
    
    media_urls: List[str] = field(default_factory=list)
    
    likes: int = 0
    shares: int = 0
    comments: int = 0
    
    posted_at: Optional[datetime] = None
    
    hashtags: List[str] = field(default_factory=list)
    
    mentions: List[str] = field(default_factory=list)
    
    def to_schema(self) -> Dict:
        return {
            "@type": "SocialMediaPosting",
            "@id": self.id,
            "contentUrl": f"{self.platform.value}/{self.id}",
            "interactionStatistic": [
                {"@type": "InteractionCounter", "userLikes": self.likes},
                {"@type": "InteractionCounter", "userShares": self.shares}
            ]
        }


@dataclass
class SocialUser:
    """Social media user"""
    id: str
    username: str
    
    platform: Platform
    
    display_name: Optional[str] = None
    bio: Optional[str] = None
    
    followers: int = 0
    following: int = 0
    
    posts: List[str] = field(default_factory=list)  # post IDs
    
    verified: bool = False
    
    profile_image_url: Optional[str] = None


# =============================================================================
# IOT/DEVICES DATABASE
# =============================================================================

class DeviceType(Enum):
    SENSOR = "Sensor"
    CAMERA = "Camera"
    SPEAKER = "Speaker"
    LIGHT = "Light"
    THERMOSTAT = "Thermostat"
    LOCK = "Lock"
    CAMPAIN = "Appliance"
    WEARABLE = "Wearable"
    VEHICLE = "Vehicle"


class DeviceStatus(Enum):
    ONLINE = "Online"
    OFFLINE = "Offline"
    ERROR = "Error"
    UPDATING = "Updating"


@dataclass
class IoTDevice:
    """IoT device"""
    id: str
    name: str
    device_type: DeviceType
    
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    
    firmware_version: Optional[str] = None
    
    status: DeviceStatus = DeviceStatus.ONLINE
    
    location: Optional[str] = None
    
    last_seen: Optional[datetime] = None
    
    properties: Dict[str, Any] = field(default_factory=dict)
    
    # - temperature, humidity, motion, etc.
    
    def to_schema(self) -> Dict:
        return {
            "@type": "Product",
            "@id": self.id,
            "name": self.name,
            "manufacturer": self.manufacturer,
            "model": self.model
        }


@dataclass
class DeviceEvent:
    """IoT event"""
    id: str
    device_id: str
    
    event_type: str  # motion, temperature, door_open
    
    value: Any
    
    timestamp: datetime
    
    location: Optional[str] = None


# =============================================================================
# CRYPTOCURRENCY DATABASE
# =============================================================================

@dataclass
class Crypto:
    """Cryptocurrency"""
    id: str
    symbol: str  # BTC, ETH
    
    name: str
    
    price: float
    
    change_24h: float  # percentage
    change_7d: float
    
    market_cap: float
    
    volume_24h: float
    
    circulating_supply: float
    
    max_supply: Optional[float] = None
    
    rank: int = 0
    
    def to_schema(self) -> Dict:
        return {
            "@type": "Product",
            "@id": self.id,
            "name": self.name,
            "offers": {
                "@type": "Offer",
                "price": self.price
            }
        }


@dataclass
class CryptoWallet:
    """Crypto wallet"""
    id: str
    user_id: str
    
    address: str
    cryptocurrency: str  # BTC, ETH
    
    balance: float
    
    transactions: List[Dict] = field(default_factory=list)


# =============================================================================
# MAIN - SHOW ALL DATABASES
# =============================================================================

def main():
    """Show all database types"""
    
    print("=" * 60)
    print("All Databases Created")
    print("=" * 60)
    
    # List all databases
    databases = [
        ("Agent Platform", "agent_platform.py"),
        ("Knowledge Graph", "knowledge_graph.py"),
        ("Movie Database", "movie_database.py"),
        ("Sports Database", "sports_database.py"),
        ("Healthcare", "additional_databases.py"),
        ("Weather", "more_databases.py"),
        ("News", "more_databases.py"),
        ("Travel", "more_databases.py"),
        ("Jobs", "more_databases.py"),
        ("Social Media", "more_databases.py"),
        ("IoT/Devices", "more_databases.py"),
        ("Cryptocurrency", "more_databases.py"),
    ]
    
    print(f"\nTotal: {len(databases)} databases")
    
    for name, _ in databases:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
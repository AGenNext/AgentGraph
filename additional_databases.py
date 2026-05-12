"""
Healthcare Database - Complete Schema.org Implementation

Healthcare system with:
- Doctors, Nurses, Specialists
- Hospitals, Clinics
- Patients, Appointments
- Insurance, Billing
- Medical Records, Prescriptions

Reference:
- Schema.org: https://schema.org/MedicalOrganization
- HL7 FHIR: https://www.hl7.org/fhir/
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, date, time
from enum import Enum
from base_entity import Entity


# =============================================================================
# ENUMERATIONS
# =============================================================================

class MedicalSpecialty(Enum):
    """Medical specialties"""
    GENERAL = "General Practice"
    INTERNAL = "Internal Medicine"
    CARDIOLOGY = "Cardiology"
    DERMATOLOGY = "Dermatology"
    EMERGENCY = "Emergency Medicine"
    NEUROLOGY = "Neurology"
    ONCOLOGY = "Oncology"
    ORTHOPEDICS = "Orthopedics"
    PEDIATRICS = "Pediatrics"
    PSYCHIATRY = "Psychiatry"
    RADIOLOGY = "Radiology"
    SURGERY = "Surgery"
    UROLOGY = "Urology"


class InsuranceType(Enum):
    """Insurance types"""
    HMO = "HMO"
    PPO = "PPO"
    EPO = "EPO"
    POS = "POS"
    MEDICARE = "Medicare"
    MEDICAID = "Medicaid"
    PRIVATE = "Private"


class AppointmentStatus(Enum):
    """Appointment status"""
    SCHEDULED = "Scheduled"
    CONFIRMED = "Confirmed"
    CHECKED_IN = "Checked In"
    IN_PROGRESS = "InProgress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    NO_SHOW = "No Show"


class Gender(Enum):
    """Gender"""
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


# =============================================================================
# CLASSES
# =============================================================================

@dataclass
class Patient:
    """Patient"""
    id: str
    name: str
    
    # Demographics
    birth_date: Optional[date] = None
    gender: Optional[Gender] = None
    
    # Contact
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    
    # Medical
    blood_type: Optional[str] = None
    allergies: List[str] = field(default_factory=list)
    conditions: List[str] = field(default_factory=list)
    
    # Insurance
    insurance_id: Optional[str] = None
    insurance_provider: Optional[str] = None
    
    # Record
    primary_physician_id: Optional[str] = None
    
    def to_schema(self) -> Dict:
        return {
            "@type": "Patient",
            "@id": self.id,
            "name": self.name,
            "birthDate": str(self.birth_date) if self.birth_date else None
        }


@dataclass
class Physician:
    """Doctor/Physician"""
    id: str
    name: str
    
    # Medical
    specialty: Optional[MedicalSpecialty] = None
    license_number: Optional[str] = None
    
    # Education
    medical_school: Optional[str] = None
    residency: Optional[str] = None
    fellowship: Optional[str] = None
    
    # Board certification
    board_certified: List[str] = field(default_factory=list)
    
    # Languages
    languages: List[str] = field(default_factory=list)
    
    # Practice
    hospital_affiliations: List[str] = field(default_factory=list)
    accepting_new_patients: bool = True
    
    # Rating
    rating: Optional[float] = None
    review_count: int = 0
    
    # Contact
    phone: Optional[str] = None
    fax: Optional[str] = None
    
    def to_schema(self) -> Dict:
        return {
            "@type": "Physician",
            "@id": self.id,
            "name": self.name,
            "jobTitle": self.specialty.value if self.specialty else None
        }


@dataclass
class Hospital:
    """Hospital/Medical Facility"""
    id: str
    name: str
    
    # Location
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    
    # Geo
    lat: Optional[float] = None
    lon: Optional[float] = None
    
    # Type
    hospital_type: str = "General"  # General, Teaching, Specialty
    emergency: bool = True
    trauma_center: Optional[str] = None  # Level 1-5
    
    # Stats
    beds: int = 0
    icu_beds: int = 0
    
    # Services
    services: List[str] = field(default_factory=list)
    specialties: List[MedicalSpecialty] = field(default_factory=list)
    
    # Insurance accepted
    insurance_accepted: List[str] = field(default_factory=list)
    
    # Contact
    phone: Optional[str] = None
    website: Optional[str] = None
    
    def to_schema(self) -> Dict:
        return {
            "@type": "Hospital",
            "@id": self.id,
            "name": self.name,
            "address": self.address,
            "telephone": self.phone
        }


@dataclass
class Appointment:
    """Medical Appointment"""
    id: str
    patient_id: str
    physician_id: str
    facility_id: str
    
    # Time
    scheduled_time: Optional[datetime] = None
    check_in_time: Optional[datetime] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    # Status
    status: AppointmentStatus = AppointmentStatus.SCHEDULED
    
    # Type
    appointment_type: str = "Office Visit"  # Follow-up, Annual, New Patient
    
    # Reason
    reason: Optional[str] = None
    chief_complaint: Optional[str] = None
    
    # Notes
    notes: Optional[str] = None
    
    # Insurance
    copay: Optional[float] = None
    covered: bool = True
    
    def to_schema(self) -> Dict:
        return {
            "@type": "Appointment",
            "@id": self.id,
            "startDate": self.scheduled_time.isoformat() if self.scheduled_time else None,
            "status": self.status.value
        }


@dataclass
class MedicalRecord:
    """Medical Record"""
    id: str
    patient_id: str
    
    # Encounter
    visit_date: Optional[datetime] = None
    facility_id: Optional[str] = None
    provider_id: Optional[str] = None
    
    # Vitals
    vitals: Dict[str, Any] = field(default_factory=dict)
    # - blood_pressure_systolic, blood_pressure_diastolic
    # - heart_rate, temperature, weight, height
    
    # Assessment
    chief_complaint: Optional[str] = None
    diagnosis: List[str] = field(default_factory=list)
    icd_codes: List[str] = field(default_factory=list)
    
    # Treatment
    plan: Optional[str] = None
    prescriptions: List[str] = field(default_factory=list)
    
    # CPT codes
    cpt_codes: List[str] = field(default_factory=list)


@dataclass
class Prescription:
    """Prescription"""
    id: str
    patient_id: str
    physician_id: str
    
    # Medication
    medication: str
    dosage: str
    frequency: str
    quantity: Optional[int] = None
    refills: int = 0
    
    # Instructions
    instructions: Optional[str] = None
    
    # Pharmacy
    pharmacy: Optional[str] = None
    
    # Status
    filled: bool = False
    fill_date: Optional[date] = None
    
    # Insurance
    covered: bool = True
    copay: Optional[float] = None


# =============================================================================
# HEALTHCARE DATABASE
# =============================================================================

class HealthcareDatabase:
    """Healthcare database"""
    
    def __init__(self):
        self.patients: Dict[str, Patient] = {}
        self.physicians: Dict[str, Physician] = {}
        self.hospitals: Dict[str, Hospital] = {}
        self.appointments: Dict[str, Appointment] = {}
        self.records: Dict[str, MedicalRecord] = {}
        self.prescriptions: Dict[str, Prescription] = {}
    
    def add_patient(self, patient: Patient) -> str:
        self.patients[patient.id] = patient
        return patient.id
    
    def add_physician(self, physician: Physician) -> str:
        self.physicians[physician.id] = physician
        return physician.id
    
    def add_hospital(self, hospital: Hospital) -> str:
        self.hospitals[hospital.id] = hospital
        return hospital.id
    
    def add_appointment(self, appointment: Appointment) -> str:
        self.appointments[appointment.id] = appointment
        return appointment.id
    
    def get_patient_appointments(self, patient_id: str) -> List[Appointment]:
        return [a for a in self.appointments.values() 
                if a.patient_id == patient_id]
    
    def get_physician_schedule(self, physician_id: str) -> List[Appointment]:
        return [a for a in self.appointments.values() 
                if a.physician_id == physician_id]
    
    def to_jsonld(self) -> Dict:
        graph = []
        for p in self.patients.values():
            graph.append(p.to_schema())
        for d in self.physicians.values():
            graph.append(d.to_schema())
        for h in self.hospitals.values():
            graph.append(h.to_schema())
        return {"@context": "https://schema.org", "@graph": graph}


# =============================================================================
# RESTAURANT DATABASE
# =============================================================================

@dataclass
class Restaurant:
    """Restaurant"""
    id: str
    name: str
    
    # Location
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    
    # Type
    cuisine: List[str] = field(default_factory=list)
    price_range: str = "$$"  # $, $$, $$$, $$$$
    
    # Rating
    rating: Optional[float] = None
    review_count: int = 0
    
    # Hours
    hours: Dict[str, str] = field(default_factory=dict)
    
    # Features
    outdoor_seating: bool = False
    delivery: bool = False
    takeout: bool = False
    reservations: bool = False
    
    # Contact
    phone: Optional[str] = None
    website: Optional[str] = None
    
    def to_schema(self) -> Dict:
        return {
            "@type": "Restaurant",
            "@id": self.id,
            "name": self.name,
            "address": self.address,
            "servesCuisine": self.cuisine
        }


@dataclass
class MenuItem:
    """Menu Item"""
    id: str
    restaurant_id: str
    
    name: str
    description: Optional[str] = None
    
    price: Optional[float] = None
    
    category: str = "Main"  # Appetizer, Main, Dessert, Drink
    
    dietary: List[str] = field(default_factory=list)  # Vegetarian, Vegan, Gluten-Free
    
    allergens: List[str] = field(default_factory=list)


@dataclass
class Menu:
    """Restaurant Menu"""
    id: str
    restaurant_id: str
    
    items: List[MenuItem] = field(default_factory=list)


# =============================================================================
# MUSIC DATABASE
# =============================================================================

@dataclass
class Artist:
    """Music Artist"""
    id: str
    name: str
    
    # Type
    artist_type: str = "Solo"  # Solo, Band, Duo
    
    # Members (if band)
    members: List[str] = field(default_factory=list)
    
    # Origin
    origin: Optional[str] = None
    formed_year: Optional[int] = None
    
    # Genres
    genres: List[str] = field(default_factory=list)
    
    # Stats
    followers: int = 0
    monthly_listeners: int = 0
    
    # Image
    image_url: Optional[str] = None
    
    # Social
    spotify: Optional[str] = None
    instagram: Optional[str] = None
    twitter: Optional[str] = None


@dataclass
class Album:
    """Music Album"""
    id: str
    title: str
    artist_id: str
    
    release_date: Optional[date] = None
    
    genre: List[str] = field(default_factory=list)
    
    tracks: int = 0
    duration_minutes: int = 0
    
    type: str = "Studio"  # Studio, Live, Compilation, EP
    
    label: Optional[str] = None
    
    rating: Optional[float] = None


@dataclass
class Song:
    """Song/Track"""
    id: str
    title: str
    artist_id: str
    album_id: Optional[str] = None
    
    track_number: Optional[int] = None
    
    duration_seconds: int = 0
    
    explicit: bool = False
    
    composer: Optional[str] = None
    producer: Optional[str] = None
    
    plays: int = 0


# =============================================================================
# REAL ESTATE DATABASE
# =============================================================================

@dataclass
class Property:
    """Real Estate Property"""
    id: str
    title: str
    
    # Type
    property_type: str = "House"  # House, Condo, Townhouse, Land, Commercial
    
    # Location
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    
    # Geo
    lat: Optional[float] = None
    lon: Optional[float] = None
    
    # Details
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    sqft: Optional[int] = None
    lot_size: Optional[float] = None
    
    # Year built
    year_built: Optional[int] = None
    
    # Price
    price: Optional[int] = None
    price_per_sqft: Optional[float] = None
    
    # Status
    status: str = "For Sale"  # For Sale, Pending, Sold
    
    # Listing
    listing_date: Optional[date] = None
    mls_number: Optional[str] = None
    
    # Features
    features: List[str] = field(default_factory=list)
    
    # Images
    photos: List[str] = field(default_factory=list)
    
    # Agent
    listing_agent_id: Optional[str] = None
    
    def to_schema(self) -> Dict:
        return {
            "@type": "RealEstateListing",
            "@id": self.id,
            "name": self.title,
            "address": self.address,
            "price": self.price
        }


@dataclass
class Agent:
    """Real Estate Agent"""
    id: str
    name: str
    
    license: Optional[str] = None
    brokerage: Optional[str] = None
    
    phone: Optional[str] = None
    email: Optional[str] = None
    
    properties: List[str] = field(default_factory=list)


# =============================================================================
# E-COMMERCE DATABASE
# =============================================================================

@dataclass
class Product:
    """E-commerce Product"""
    id: str
    name: str
    
    description: Optional[str] = None
    
    category: Optional[str] = None
    
    brand: Optional[str] = None
    
    sku: Optional[str] = None
    
    price: Optional[float] = None
    original_price: Optional[float] = None
    
    availability: str = "In Stock"  # In Stock, Pre-order, Out of Stock
    
    condition: str = "New"  # New, Used, Refurbished
    
    weight_oz: Optional[float] = None
    
    dimensions: Optional[Dict] = None
    
    images: List[str] = field(default_factory=list)
    
    reviews: int = 0
    rating: Optional[float] = None


@dataclass
class Order:
    """Order"""
    id: str
    customer_id: str
    
    items: List[Dict] = field(default_factory=list)
    
    subtotal: float = 0
    tax: float = 0
    shipping: float = 0
    total: float = 0
    
    status: str = "Processing"
    
    shipping_address: Optional[str] = None
    
    tracking_number: Optional[str] = None
    
    created_at: Optional[datetime] = None
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None


# =============================================================================
# EDUCATION DATABASE
# =============================================================================

@dataclass
class School:
    """School/University"""
    id: str
    name: str
    
    # Type
    school_type: str = "University"  # University, High School, Elementary
    
    # Location
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    
    # Stats
    enrollment: int = 0
    tuition: Optional[float] = None
    
    # Academics
    acceptance_rate: Optional[float] = None
    graduation_rate: Optional[float] = None
    
    # Ranking
    national_ranking: Optional[int] = None
    
    # Programs
    programs: List[str] = field(default_factory=list)
    
    # Sports
    conference: Optional[str] = None
    
    def to_schema(self) -> Dict:
        return {
            "@type": "EducationalOrganization",
            "@id": self.id,
            "name": self.name,
            "address": self.address
        }


@dataclass
class Student:
    """Student"""
    id: str
    name: str
    
    birth_date: Optional[date] = None
    
    grade: Optional[int] = None
    
    school_id: Optional[str] = None
    
    gpa: Optional[float] = None
    
    major: Optional[str] = None
    
    enrollment_date: Optional[date] = None
    
    graduation_date: Optional[date] = None
    
    status: str = "Active"


@dataclass
class Course:
    """Course/Class"""
    id: str
    code: str  # CS101
    name: str
    
    school_id: Optional[str] = None
    
    credits: int = 3
    
    instructor_id: Optional[str] = None
    
    schedule: Optional[str] = None  # "MWF 10am-11am"
    
    capacity: int = 0
    enrolled: int = 0
    
    prerequisites: List[str] = field(default_factory=list)


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example - Healthcare DB"""
    
    db = HealthcareDatabase()
    
    # Add hospital
    hospital = Hospital(
        id="h1",
        name="General Hospital",
        address="123 Main St",
        city="Boston",
        beds=500,
        emergency=True
    )
    db.add_hospital(hospital)
    
    # Add doctor
    doctor = Physician(
        id="d1",
        name="Dr. Smith",
        specialty=MedicalSpecialty.CARDIOLOGY,
        hospital_affiliations=["h1"]
    )
    db.add_physician(doctor)
    
    # Add patient
    patient = Patient(
        id="p1",
        name="John Doe",
        birth_date=date(1980, 5, 15),
        insurance_provider="Blue Cross"
    )
    db.add_patient(patient)
    
    # Add appointment
    appt = Appointment(
        id="a1",
        patient_id="p1",
        physician_id="d1",
        facility_id="h1",
        scheduled_time=datetime(2024, 11, 15, 10, 0)
    )
    db.add_appointment(appt)
    
    # Export
    print(db.to_jsonld())


if __name__ == "__main__":
    main()
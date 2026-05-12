"""
Healthcare Database - Medical Records

Healthcare database:
- Patients, Providers
- Medical records
- Diagnoses, Medications
- Appointments, Claims

Reference:
- EHR/EMR systems
- Healthcare APIs
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum
from base_entity import Entity


# =============================================================================
# TYPES
# =============================================================================

class Gender(Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"


class BloodType(Enum):
    A_Positive = "A+"
    A_Negative = "A-"
    B_Positive = "B+"
    B_Negative = "B-"
    AB_Positive = "AB+"
    AB_Negative = "AB-"
    O_Positive = "O+"
    O_Negative = "O-"


class AppointmentStatus(Enum):
    Scheduled = "Scheduled"
    Confirmed = "Confirmed"
    Checked_In = "Checked_In"
    In_Progress = "In_Progress"
    Completed = "Completed"
    Cancelled = "Cancelled"
    No_Show = "No_Show"


class ClaimStatus(Enum):
    Submitted = "Submitted"
    Pending = "Pending"
    Approved = "Approved"
    Denied = "Denied"
    Paid = "Paid"


# =============================================================================
# ENTITIES
# =============================================================================

@dataclass
class Entity(Entity):
class Patient:
    """Patient"""
    id: str
    first_name: str
    last_name: str
    
    date_of_birth: date
    gender: Gender = Gender.Male
    
    ssn: str = ""  # Last 4
    
    email: str = ""
    phone: str = ""
    
    address: Dict[str, str] = field(default_factory=dict)
    
    emergency_contact: Dict[str, str] = field(default_factory=dict)
    
    blood_type: BloodType = None
    
    insurance_id: str = ""
    
    primary_provider_id: str = ""
    
    allergies: List[str] = field(default_factory=list)
    
    conditions: List[str] = field(default_factory=list)
    
    medications: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": f"{self.first_name} {self.last_name}",
            "dob": str(self.date_of_birth)
        }
    
    def age(self) -> int:
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )


@dataclass
class Entity(Entity):
class Provider:
    """Healthcare provider"""
    id: str
    name: str  # Dr. Name
    
    specialty: str = ""
    
    npi: str = ""  # National Provider Identifier
    
    license: str = ""
    
    dea: str = ""  # Drug Enforcement Admin
    
    phone: str = ""
    email: str = ""
    
    address: Dict[str, str] = field(default_factory=dict)
    
    accepting_new: bool = True
    
    languages: List[str] = field(default_factory=list)
    
    education: List[str] = field(default_factory=list)


@dataclass
class Entity(Entity):
class MedicalRecord:
    """Medical record"""
    id: str
    patient_id: str
    provider_id: str
    
    visit_date: datetime = field(default_factory=datetime.now)
    
    chief_complaint: str = ""
    
    diagnosis: List[Dict] = field(default_factory=list)  # {code, description}
    
    vitals: Dict[str, Any] = field(default_factory=dict)  # BP, HR, temp
    
    notes: str = ""
    
    prescriptions: List[Dict] = field(default_factory=list)
    
    lab_results: List[Dict] = field(default_factory=list)
    
    follow_up: str = ""


@dataclass
class Entity(Entity):
class Appointment:
    """Appointment"""
    id: str
    patient_id: str
    provider_id: str
    
    appointment_date: datetime
    
    duration_minutes: int = 30
    
    appointment_type: str = ""  # Checkup, Follow-up, etc.
    
    status: AppointmentStatus = AppointmentStatus.Scheduled
    
    reason: str = ""
    
    notes: str = ""
    
    checked_in_at: Optional[datetime] = None
    
    completed_at: Optional[datetime] = None
    
    room: str = ""


@dataclass
class Entity(Entity):
class Prescription:
    """Prescription"""
    id: str
    patient_id: str
    provider_id: str
    
    medication: str
    
    dosage: str
    
    frequency: str
    
    quantity: int = 0
    
    refills: int = 0
    
    instructions: str = ""
    
    start_date: date = None
    end_date: Optional[date] = None
    
    status: str = "Active"  # Active, Expired, Cancelled


@dataclass
class Entity(Entity):
class Claim:
    """Insurance claim"""
    id: str
    patient_id: str
    provider_id: str
    
    appointment_id: str = ""
    
    service_date: date = None
    
    diagnosis_codes: List[str] = field(default_factory=list)
    
    procedure_codes: List[str] = field(default_factory=list)
    
    charged_amount: float = 0.0
    
    allowed_amount: float = 0.0
    
    paid_amount: float = 0.0
    
    patient_responsibility: float = 0.0
    
    status: ClaimStatus = ClaimStatus.Submitted
    
    submitted_at: datetime = field(default_factory=datetime.now)
    
    paid_at: Optional[datetime] = None


@dataclass
class Entity(Entity):
class Facility:
    """Healthcare facility"""
    id: str
    name: str
    
    facility_type: str = ""  # Hospital, Clinic, etc.
    
    address: Dict[str, str] = field(default_factory=dict)
    
    phone: str = ""
    
    hours: Dict[str, str] = field(default_factory=dict)
    
    services: List[str] = field(default_factory=list)
    
    accepting_new_patients: bool = True


# =============================================================================
# DATABASE
# =============================================================================

class HealthcareDatabase:
    """Healthcare database"""
    
    def __init__(self):
        self.patients: Dict[str, Patient] = {}
        self.providers: Dict[str, Provider] = {}
        self.facilities: Dict[str, Facility] = {}
        
        self.records: Dict[str, MedicalRecord] = {}
        self.appointments: Dict[str, Appointment] = {}
        self.prescriptions: Dict[str, Prescription] = {}
        self.claims: Dict[str, Claim] = {}
        
        self.records_by_patient: Dict[str, List[str]] = {}
        self.appointments_by_provider: Dict[str, List[str]] = {}
    
    # Patients
    def add_patient(self, patient: Patient) -> str:
        self.patients[patient.id] = patient
        return patient.id
    
    def get_patient(self, patient_id: str) -> Optional[Patient]:
        return self.patients.get(patient_id)
    
    def search_patients(
        self,
        query: str = None,
        by_name: bool = True
    ) -> List[Patient]:
        results = list(self.patients.values())
        
        if query:
            q = query.lower()
            if by_name:
                results = [
                    p for p in results
                    if q in f"{p.first_name} {p.last_name}".lower()
                ]
        
        return results
    
    def get_patient_summary(self, patient_id: str) -> Optional[Dict]:
        patient = self.patients.get(patient_id)
        if not patient:
            return None
        
        record_ids = self.records_by_patient.get(patient_id, [])
        
        return {
            "patient": patient.to_dict(),
            "record_count": len(record_ids),
            "allergies": patient.allergies,
            "conditions": patient.conditions,
            "age": patient.age()
        }
    
    # Providers
    def add_provider(self, provider: Provider) -> str:
        self.providers[provider.id] = provider
        return provider.id
    
    def get_provider(self, provider_id: str) -> Optional[Provider]:
        return self.providers.get(provider_id)
    
    def search_providers(
        self,
        specialty: str = None
    ) -> List[Provider]:
        results = list(self.providers.values())
        
        if specialty:
            s = specialty.lower()
            results = [
                p for p in results
                if s in p.specialty.lower()
            ]
        
        return results
    
    # Medical Records
    def add_record(self, record: MedicalRecord) -> str:
        self.records[record.id] = record
        
        # Index
        if record.patient_id not in self.records_by_patient:
            self.records_by_patient[record.patient_id] = []
        self.records_by_patient[record.patient_id].append(record.id)
        
        return record.id
    
    def get_record(self, record_id: str) -> Optional[MedicalRecord]:
        return self.records.get(record_id)
    
    def get_patient_records(
        self,
        patient_id: str,
        limit: int = None
    ) -> List[MedicalRecord]:
        record_ids = self.records_by_patient.get(patient_id, [])
        
        records = sorted(
            [self.records[rid] for rid in record_ids if rid in self.records],
            key=lambda r: r.visit_date,
            reverse=True
        )
        
        if limit:
            records = records[:limit]
        
        return records
    
    # Appointments
    def schedule_appointment(
        self,
        appointment: Appointment
    ) -> str:
        self.appointments[appointment.id] = appointment
        
        # Index
        if appointment.provider_id not in self.appointments_by_provider:
            self.appointments_by_provider[appointment.provider_id] = []
        self.appointments_by_provider[appointment.provider_id].append(appointment.id)
        
        return appointment.id
    
    def get_appointment(self, appt_id: str) -> Optional[Appointment]:
        return self.appointments.get(appt_id)
    
    def get_provider_appointments(
        self,
        provider_id: str,
        date: date = None
    ) -> List[Appointment]:
        appt_ids = self.appointments_by_provider.get(provider_id, [])
        
        appointments = [
            self.appointments[aid]
            for aid in appt_ids
            if aid in self.appointments
        ]
        
        if date:
            appointments = [
                a for a in appointments
                if a.appointment_date.date() == date
            ]
        
        return sorted(appointments, key=lambda a: a.appointment_date)
    
    def update_appointment_status(
        self,
        appt_id: str,
        status: AppointmentStatus
    ) -> bool:
        appt = self.appointments.get(appt_id)
        if not appt:
            return False
        
        appt.status = status
        
        if status == AppointmentStatus.Checked_In:
            appt.checked_in_at = datetime.now()
        elif status == AppointmentStatus.Completed:
            appt.completed_at = datetime.now()
        
        return True
    
    # Prescriptions
    def add_prescription(self, prescription: Prescription) -> str:
        self.prescriptions[prescription.id] = prescription
        return prescription.id
    
    def get_patient_prescriptions(
        self,
        patient_id: str,
        active_only: bool = True
    ) -> List[Prescription]:
        results = [
            p for p in self.prescriptions.values()
            if p.patient_id == patient_id
        ]
        
        if active_only:
            results = [p for p in results if p.status == "Active"]
        
        return results
    
    # Claims
    def submit_claim(self, claim: Claim) -> str:
        self.claims[claim.id] = claim
        return claim.id
    
    def get_claim(self, claim_id: str) -> Optional[Claim]:
        return self.claims.get(claim_id)
    
    def get_patient_claims(
        self,
        patient_id: str
    ) -> List[Claim]:
        return [
            c for c in self.claims.values()
            if c.patient_id == patient_id
        ]
    
    # Statistics
    def stats(self) -> Dict:
        return {
            "total_patients": len(self.patients),
            "total_providers": len(self.providers),
            "total_records": len(self.records),
            "total_appointments": len(self.appointments),
            "total_claims": len(self.claims)
        }


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("Healthcare Database")
    print("=" * 50)
    
    db = HealthcareDatabase()
    
    # Add patient
    patient = Patient(
        id="p1",
        first_name="John",
        last_name="Doe",
        date_of_birth=date(1980, 5, 15),
        gender=Gender.Male,
        allergies=["Penicillin"],
        conditions=["Hypertension"]
    )
    db.add_patient(patient)
    
    print(f"\nPatient: {patient.first_name} {patient.last_name}")
    print(f"  Age: {patient.age()}")
    
    # Add provider
    provider = Provider(
        id="dr1",
        name="Dr. Jane Smith",
        specialty="Internal Medicine",
        npi="1234567890"
    )
    db.add_provider(provider)
    
    print(f"\nProvider: {provider.name}")
    print(f"  Specialty: {provider.specialty}")
    
    # Add record
    record = MedicalRecord(
        id="r1",
        patient_id="p1",
        provider_id="dr1",
        chief_complaint="Annual checkup",
        vitals={"bp": "120/80", "hr": 72}
    )
    db.add_record(record)
    
    print(f"\nRecord: {record.chief_complaint}")
    
    # Schedule appointment
    appointment = Appointment(
        id="a1",
        patient_id="p1",
        provider_id="dr1",
        appointment_date=datetime(2024, 7, 1, 10, 0),
        appointment_type="Checkup"
    )
    db.schedule_appointment(appointment)
    
    print(f"\nAppointment: {appointment.appointment_type}")
    
    # Get patient records
    records = db.get_patient_records("p1")
    print(f"\nPatient records: {len(records)}")
    
    # Statistics
    print(f"\nStats:")
    stats = db.stats()
    print(f"  Patients: {stats['total_patients']}")
    print(f"  Providers: {stats['total_providers']}")


if __name__ == "__main__":
    main()


"""
Healthcare Database Usage

    db = HealthcareDatabase()
    
    # Patients
    patient = db.add_patient(Patient(...))
    patient = db.get_patient(patient_id)
    patients = db.search_patients("name")
    summary = db.get_patient_summary(patient_id)
    
    # Providers
    provider = db.add_provider(Provider(...))
    providers = db.search_providers("specialty")
    
    # Medical Records
    record = db.add_record(MedicalRecord(...))
    records = db.get_patient_records(patient_id)
    
    # Appointments
    appointment = db.schedule_appointment(Appointment(...))
    appointments = db.get_provider_appointments(provider_id)
    db.update_appointment_status(appt_id, AppointmentStatus.Completed)
    
    # Prescriptions
    prescriptions = db.get_patient_prescriptions(patient_id)
    
    # Claims
    claims = db.get_patient_claims(patient_id)
    
    # Stats
    stats = db.stats()
"""
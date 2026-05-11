"""
Person & Organization Database

People and organizations:
- Person profiles
- Organizations
- Relationships
- Roles

Reference:
- LinkedIn style
- Schema.org Person/Organization
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum


# =============================================================================
# TYPES
# =============================================================================

class Gender(Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"
    Not_Specified = "Not_Specified"


class OrganizationType(Enum):
    Corporation = "Corporation"
    LLC = "LLC"
    Partnership = "Partnership"
    Sole_Proprietorship = "Sole_Proprietorship"
    Nonprofit = "Nonprofit"
    Government = "Government"
    Educational = "Educational"


class RoleType(Enum):
    Employee = "Employee"
    Contractor = "Contractor"
    Founder = "Founder"
    Board_Member = "Board_Member"
    Investor = "Investor"
    Advisor = "Advisor"


# =============================================================================
# PERSON
# =============================================================================

@dataclass
class Person:
    """Person"""
    id: str
    first_name: str
    last_name: str
    
    middle_name: str = ""
    maiden_name: str = ""
    
    birth_date: Optional[date] = None
    gender: Gender = Gender.Not_Specified
    
    email: str = ""
    phone: str = ""
    
    address: Dict[str, str] = field(default_factory=dict)
    
    headline: str = ""  # Professional headline
    
    summary: str = ""
    
    avatar_url: str = ""
    
    location: str = ""
    location_country: str = ""
    
    timezone: str = ""
    
    languages: List[str] = field(default_factory=list)
    
    # Professional
    current_title: str = ""
    current_company: str = ""
    
    skills: List[str] = field(default_factory=list)
    
    certifications: List[str] = field(default_factory=list)
    
    # Education
    education: List[Dict] = field(default_factory=list)  # {school, degree, year}
    
    # Work history
    work_history: List[Dict] = field(default_factory=list)  # {company, title, years}
    
    # Social
    linkedin: str = ""
    twitter: str = ""
    github: str = ""
    website: str = ""
    
    # Connections
    connections_count: int = 0
    
    # Visibility
    profile_visibility: str = "Public"  # Public, Private, Network
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.full_name(),
            "title": self.current_title,
            "company": self.current_company
        }
    
    def full_name(self) -> str:
        name = f"{self.first_name} {self.last_name}"
        if self.middle_name:
            name = f"{self.first_name} {self.middle_name} {self.last_name}"
        return name
    
    def age(self) -> Optional[int]:
        if not self.birth_date:
            return None
        today = date.today()
        return today.year - self.birth_date.year


# =============================================================================
# ORGANIZATION
# =============================================================================

@dataclass
class Organization:
    """Organization"""
    id: str
    name: str
    
    legal_name: str = ""
    
    type: OrganizationType = OrganizationType.Corporation
    
    industry: str = ""
    
    founded_date: Optional[date] = None
    
    address: Dict[str, str] = field(default_factory=dict)
    
    headquarters: str = ""
    
    website: str = ""
    
    phone: str = ""
    email: str = ""
    
    description: str = ""
    
    mission: str = ""
    vision: str = ""
    
    logo_url: str = ""
    
    employee_count: int = 0
    
    revenue: float = 0.0
    
    stock_symbol: str = ""
    
    # Social
    linkedin: str = ""
    twitter: str = ""
    
    # Connections
    subsidiaries: List[str] = field(default_factory=list)
    
    investors: List[str] = field(default_factory=list)
    
    parent_company: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value,
            "industry": self.industry
        }
    
    def age(self) -> Optional[int]:
        if not self.founded_date:
            return None
        today = date.today()
        return today.year - self.founded_date.year


# =============================================================================
# RELATIONSHIPS
# =============================================================================

@dataclass
class PersonRole:
    """Person role at organization"""
    id: str
    person_id: str
    organization_id: str
    
    role_type: RoleType
    
    title: str = ""
    
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    
    current: bool = True
    
    description: str = ""
    
    location: str = ""
    
    department: str = ""
    
    salary: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "person_id": self.person_id,
            "organization_id": self.organization_id,
            "role_type": self.role_type.value,
            "title": self.title
        }


@dataclass
class Ownership:
    """Ownership relationship"""
    id: str
    person_id: str
    organization_id: str
    
    percentage: float = 0.0
    
    shares: int = 0
    
    value: float = 0.0
    
    start_date: Optional[date] = None


@dataclass
class Partnership:
    """Organization partnership"""
    id: str
    from_org_id: str
    to_org_id: str
    
    partnership_type: str = ""  # Vendor, Customer, Partner, etc.
    
    description: str = ""
    
    start_date: Optional[date] = None


# =============================================================================
# DATABASE
# =============================================================================

class PersonOrgDatabase:
    """Person & Organization database"""
    
    def __init__(self):
        # People
        self.people: Dict[str, Person] = {}
        self.roles: Dict[str, PersonRole] = {}
        
        # Organizations
        self.organizations: Dict[str, Organization] = {}
        self.ownerships: Dict[str, Ownership] = {}
        self.partnerships: Dict[str, Partnership] = {}
        
        # Indexes
        self.people_by_company: Dict[str, List[str]] = {}
        self.roles_by_person: Dict[str, List[str]] = {}
        self.roles_by_org: Dict[str, List[str]] = {}
    
    # Persons
    def add_person(self, person: Person) -> str:
        self.people[person.id] = person
        return person.id
    
    def get_person(self, person_id: str) -> Optional[Person]:
        return self.people.get(person_id)
    
    def search_people(
        self,
        query: str = None,
        skills: str = None,
        company: str = None,
        location: str = None
    ) -> List[Person]:
        results = list(self.people.values())
        
        if query:
            q = query.lower()
            results = [
                p for p in results
                if q in p.full_name().lower() or q in p.headline.lower()
            ]
        
        if skills:
            s = skills.lower()
            results = [
                p for p in results
                if any(s in skill.lower() for skill in p.skills)
            ]
        
        if company:
            results = [
                p for p in results
                if p.current_company == company
            ]
        
        if location:
            l = location.lower()
            results = [
                p for p in results
                if l in p.location.lower()
            ]
        
        return results
    
    def get_person_by_email(self, email: str) -> Optional[Person]:
        for person in self.people.values():
            if person.email == email:
                return person
        return None
    
    # Organizations
    def add_organization(self, org: Organization) -> str:
        self.organizations[org.id] = org
        return org.id
    
    def get_organization(self, org_id: str) -> Optional[Organization]:
        return self.organizations.get(org_id)
    
    def search_organizations(
        self,
        query: str = None,
        type: OrganizationType = None,
        industry: str = None,
        location: str = None
    ) -> List[Organization]:
        results = list(self.organizations.values())
        
        if query:
            q = query.lower()
            results = [
                o for o in results
                if q in o.name.lower() or q in o.description.lower()
            ]
        
        if type:
            results = [o for o in results if o.type == type]
        
        if industry:
            i = industry.lower()
            results = [
                o for o in results
                if i in o.industry.lower()
            ]
        
        if location:
            l = location.lower()
            results = [
                o for o in results
                if l in o.headquarters.lower()
            ]
        
        return results
    
    def get_organization_by_domain(self, domain: str) -> Optional[Organization]:
        for org in self.organizations.values():
            if org.website and domain in org.website:
                return org
        return None
    
    # Roles
    def add_role(self, role: PersonRole) -> str:
        self.roles[role.id] = role
        
        # Index by person
        if role.person_id not in self.roles_by_person:
            self.roles_by_person[role.person_id] = []
        self.roles_by_person[role.person_id].append(role.id)
        
        # Index by org
        if role.organization_id not in self.roles_by_org:
            self.roles_by_org[role.organization_id] = []
        self.roles_by_org[role.organization_id].append(role.id)
        
        # Index by company
        if role.current and role.organization_id:
            if role.organization_id not in self.people_by_company:
                self.people_by_company[role.organization_id] = []
            if role.person_id not in self.people_by_company[role.organization_id]:
                self.people_by_company[role.organization_id].append(role.person_id)
        
        return role.id
    
    def get_person_roles(self, person_id: str) -> List[PersonRole]:
        role_ids = self.roles_by_person.get(person_id, [])
        return [self.roles[rid] for rid in role_ids if rid in self.roles]
    
    def get_current_role(self, person_id: str) -> Optional[PersonRole]:
        roles = self.get_person_roles(person_id)
        for role in roles:
            if role.current:
                return role
        return None
    
    def get_organization_employees(
        self,
        org_id: str,
        current_only: bool = True
    ) -> List[Person]:
        person_ids = self.people_by_company.get(org_id, [])
        
        people = []
        
        for pid in person_ids:
            person = self.people.get(pid)
            if person:
                if current_only:
                    role = self.get_current_role(pid)
                    if role and role.organization_id == org_id:
                        people.append(person)
                else:
                    people.append(person)
        
        return people
    
    def get_organization_role_count(self, org_id: str, role_type: RoleType = None) -> int:
        role_ids = self.roles_by_org.get(org_id, [])
        
        count = 0
        for rid in role_ids:
            role = self.roles.get(rid)
            if role:
                if role_type:
                    if role.role_type == role_type and role.current:
                        count += 1
                elif role.current:
                    count += 1
        
        return count
    
    # Ownership
    def add_ownership(self, ownership: Ownership) -> str:
        self.ownerships[ownership.id] = ownership
        return ownership.id
    
    def get_organization_owners(self, org_id: str) -> List[Person]:
        owners = [
            o for o in self.ownerships.values()
            if o.organization_id == org_id
        ]
        
        return [
            self.people.get(o.person_id)
            for o in owners
            if o.person_id in self.people
        ]
    
    # Statistics
    def stats(self) -> Dict:
        return {
            "total_people": len(self.people),
            "total_organizations": len(self.organizations),
            "total_roles": len(self.roles),
            "total_ownerships": len(self.ownerships)
        }


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("Person & Organization Database")
    print("=" * 50)
    
    db = PersonOrgDatabase()
    
    # Add organizations
    orgs = [
        Organization(
            id="o1",
            name="Acme Corp",
            type=OrganizationType.Corporation,
            industry="Technology",
            founded_date=date(2010, 1, 1),
            employee_count=100,
            headquarters="San Francisco"
        ),
        Organization(
            id="o2",
            name="GlobalTech Inc",
            type=OrganizationType.Corporation,
            industry="Technology",
            employee_count=500,
            headquarters="New York"
        ),
    ]
    
    for org in orgs:
        db.add_organization(org)
    
    print(f"\nOrganizations: {len(orgs)}")
    
    # Add people
    people = [
        Person(
            id="p1",
            first_name="John",
            last_name="Smith",
            email="john@acme.com",
            headline="Software Engineer",
            current_title="Senior Engineer",
            current_company="o1",
            skills=["Python", "Go", "AWS"]
        ),
        Person(
            id="p2",
            first_name="Jane",
            last_name="Doe",
            email="jane@acme.com",
            headline="Product Manager",
            current_title="Product Lead",
            current_company="o1",
            skills=["Product", "Agile"]
        ),
    ]
    
    for person in people:
        db.add_person(person)
    
    print(f"\nPeople: {len(people)}")
    
    # Add roles
    role1 = PersonRole(
        id="r1",
        person_id="p1",
        organization_id="o1",
        role_type=RoleType.Employee,
        title="Senior Engineer"
    )
    db.add_role(role1)
    
    # Search
    print("\nSearch 'Python':")
    results = db.search_people(skills="Python")
    for p in results:
        print(f"  {p.full_name()}")
    
    print("\nSearch organizations:")
    results = db.search_organizations(industry="Technology")
    for o in results:
        print(f"  {o.name}")
    
    # Get employees
    employees = db.get_organization_employees("o1")
    print(f"\nAcme employees: {len(employees)}")
    
    print(f"\nStats:")
    stats = db.stats()
    print(f"  People: {stats['total_people']}")
    print(f"  Organizations: {stats['total_organizations']}")


if __name__ == "__main__":
    main()


"""
Person & Organization Database Usage

    db = PersonOrgDatabase()
    
    # Persons
    person = db.add_person(Person(...))
    people = db.search_people(skills="Python", company="Google")
    person = db.get_person(person_id)
    
    # Organizations
    org = db.add_organization(Organization(...))
    orgs = db.search_organizations(industry="Technology")
    org = db.get_organization(org_id)
    
    # Roles
    role = db.add_role(PersonRole(...))
    roles = db.get_person_roles(person_id)
    employees = db.get_organization_employees(org_id)
    
    # Ownership
    ownership = db.add_ownership(Ownership(...))
    owners = db.get_organization_owners(org_id)
    
    # Stats
    stats = db.stats()
"""
"""
Employment Graph - Work Network

Employment graph for:
- Companies and organizations
- Employees and contractors
- Jobs and positions
- Employment history

Reference:
- LinkedIn-style networks
- HR systems
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum


# =============================================================================
# TYPES
# =============================================================================

class EmploymentType(Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"


class JobLevel(Enum):
    ENTRY = "entry"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    MANAGER = "manager"
    DIRECTOR = "director"
    EXECUTIVE = "executive"


class Industry(Enum):
    TECHNOLOGY = "Technology"
    FINANCE = "Finance"
    HEALTHCARE = "Healthcare"
    EDUCATION = "Education"
    RETAIL = "Retail"
    MANUFACTURING = "Manufacturing"
    MEDIA = "Media"
    CONSULTING = "Consulting"


# =============================================================================
# NODES
# =============================================================================

@dataclass
class Company:
    """Company node"""
    id: str
    name: str
    
    industry: Optional[Industry] = None
    
    size: str = ""  # 1-10, 11-50, 51-200, 201-500, 501-1000, 1000+
    
    founded: Optional[int] = None
    
    headquarters: str = ""
    
    website: str = ""
    
    description: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "industry": self.industry.value if self.industry else None,
            "size": self.size,
            "founded": self.founded
        }


@dataclass
class Person:
    """Person node (employee)"""
    id: str
    name: str
    
    email: str = ""
    
    title: str = ""
    
    skills: List[str] = field(default_factory=list)
    
    experience_years: int = 0
    
    education: List[str] = field(default_factory=list)
    
    linkedin: str = ""
    
    github: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "skills": self.skills
        }


@dataclass
class Job:
    """Job posting"""
    id: str
    company_id: str
    
    title: str
    
    description: str = ""
    
    employment_type: EmploymentType = EmploymentType.FULL_TIME
    
    level: JobLevel = JobLevel.ENTRY
    
    requirements: List[str] = field(default_factory=list)
    
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    
    location: str = ""
    
    remote: bool = False
    
    posted_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "company_id": self.company_id,
            "title": self.title,
            "employment_type": self.employment_type.value,
            "level": self.level.value
        }


# =============================================================================
# EMPLOYMENT GRAPH
# =============================================================================

class EmploymentGraph:
    """Employment network graph"""
    
    def __init__(self):
        # Nodes
        self.companies: Dict[str, Company] = {}
        self.people: Dict[str, Person] = {}
        self.jobs: Dict[str, Job] = {}
        
        # Employment relationships
        # employee_history[person_id] = [employment_records]
        self.employment: Dict[str, List[Dict]] = {}
        
        # Company employees
        self.company_employees: Dict[str, Set[str]] = {}
        
        # Skills index
        self.skills_index: Dict[str, Set[str]] = {}
        
        # Industry index
        self.industry_index: Dict[str, Set[str]] = {}
    
    # Companies
    def add_company(
        self,
        id: str,
        name: str,
        industry: Industry = None,
        size: str = "",
        **kwargs
    ) -> Company:
        """Add company"""
        company = Company(
            id=id,
            name=name,
            industry=industry,
            size=size,
            **kwargs
        )
        self.companies[id] = company
        
        if industry:
            if industry.value not in self.industry_index:
                self.industry_index[industry.value] = set()
            self.industry_index[industry.value].add(id)
        
        return company
    
    def get_company(self, company_id: str) -> Optional[Company]:
        """Get company"""
        return self.companies.get(company_id)
    
    def get_companies_by_industry(self, industry: str) -> List[Company]:
        """Get companies by industry"""
        company_ids = self.industry_index.get(industry, set())
        return [self.companies[cid] for cid in company_ids if cid in self.companies]
    
    # People
    def add_person(
        self,
        id: str,
        name: str,
        title: str = "",
        skills: List[str] = None,
        **kwargs
    ) -> Person:
        """Add person"""
        person = Person(
            id=id,
            name=name,
            title=title,
            skills=skills or [],
            **kwargs
        )
        self.people[id] = person
        
        # Index skills
        for skill in person.skills:
            if skill not in self.skills_index:
                self.skills_index[skill] = set()
            self.skills_index[skill].add(id)
        
        return person
    
    def get_person(self, person_id: str) -> Optional[Person]:
        """Get person"""
        return self.people.get(person_id)
    
    def get_people_by_skill(self, skill: str) -> List[Person]:
        """Get people with skill"""
        person_ids = self.skills_index.get(skill, set())
        return [self.people[pid] for pid in person_ids if pid in self.people]
    
    # Employment
    def hire(
        self,
        person_id: str,
        company_id: str,
        title: str = "",
        start_date: date = None,
        end_date: date = None,
        salary: int = None
    ) -> bool:
        """Hire person at company"""
        if person_id not in self.people or company_id not in self.companies:
            return False
        
        # Add employment record
        if person_id not in self.employment:
            self.employment[person_id] = []
        
        self.employment[person_id].append({
            "company_id": company_id,
            "title": title,
            "start_date": start_date or date.today(),
            "end_date": end_date,
            "salary": salary
        })
        
        # Add to company employees
        if company_id not in self.company_employees:
            self.company_employees[company_id] = set()
        self.company_employees[company_id].add(person_id)
        
        return True
    
    def get_employment_history(self, person_id: str) -> List[Dict]:
        """Get employment history"""
        return self.employment.get(person_id, [])
    
    def get_current_company(self, person_id: str) -> Optional[Company]:
        """Get current company"""
        history = self.employment.get(person_id, [])
        
        for record in reversed(history):
            if record.get("end_date") is None:
                return self.companies.get(record["company_id"])
        
        return None
    
    def get_company_employees(self, company_id: str) -> List[Person]:
        """Get current employees"""
        employee_ids = self.company_employees.get(company_id, set())
        
        # Filter to current employees
        current = []
        
        for eid in employee_ids:
            current_company = self.get_current_company(eid)
            if current_company and current_company.id == company_id:
                current.append(self.people[eid])
        
        return current
    
    def get_company_size(self, company_id: str) -> int:
        """Get company size"""
        return len(self.get_company_employees(company_id))
    
    # Jobs
    def post_job(
        self,
        id: str,
        company_id: str,
        title: str,
        **kwargs
    ) -> Job:
        """Post job"""
        job = Job(
            id=id,
            company_id=company_id,
            title=title,
            **kwargs
        )
        self.jobs[id] = job
        return job
    
    def get_company_jobs(self, company_id: str) -> List[Job]:
        """Get company jobs"""
        return [j for j in self.jobs.values() if j.company_id == company_id]
    
    def search_jobs(
        self,
        skills: List[str] = None,
        level: JobLevel = None,
        employment_type: EmploymentType = None,
        location: str = None,
        remote: bool = None
    ) -> List[Job]:
        """Search jobs"""
        results = []
        
        for job in self.jobs.values():
            # Check skills
            if skills:
                if not any(req in skills for req in job.requirements):
                    continue
            
            # Check level
            if level and job.level != level:
                continue
            
            # Check employment type
            if employment_type and job.employment_type != employment_type:
                continue
            
            # Check location
            if location and location.lower() not in job.location.lower():
                continue
            
            # Check remote
            if remote is not None and job.remote != remote:
                continue
            
            results.append(job)
        
        return results
    
    # Network analysis
    def find_coworkers(self, person1: str, person2: str) -> bool:
        """Check if worked together"""
        history1 = self.employment.get(person1, [])
        history2 = self.employment.get(person2, [])
        
        companies1 = {r["company_id"] for r in history1}
        companies2 = {r["company_id"] for r in history2}
        
        return bool(companies1 & companies2)
    
    def suggest_colleagues(self, person_id: str, limit: int = 5) -> List[Person]:
        """Suggest potential colleagues"""
        current = self.get_current_company(person_id)
        if not current:
            return []
        
        # Find people with overlapping skills
        person = self.people.get(person_id)
        if not person:
            return []
        
        suggestions = []
        
        for skill in person.skills:
            for pid in self.skills_index.get(skill, set()):
                if pid != person_id:
                    # Check if already worked together
                    if not self.find_coworkers(person_id, pid):
                        suggestions.append(self.people[pid])
        
        return suggestions[:limit]
    
    def get_company_graph(self, company_id: str) -> Dict:
        """Get company as graph"""
        company = self.companies.get(company_id)
        if not company:
            return {}
        
        employees = self.get_company_employees(company_id)
        
        return {
            "company": company.to_dict(),
            "employees": [e.to_dict() for e in employees],
            "employee_count": len(employees),
            "jobs": [j.to_dict() for j in self.get_company_jobs(company_id)]
        }
    
    # Statistics
    def total_companies(self) -> int:
        return len(self.companies)
    
    def total_people(self) -> int:
        return len(self.people)
    
    def total_jobs(self) -> int:
        return len(self.jobs)


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("Employment Graph")
    print("=" * 50)
    
    graph = EmploymentGraph()
    
    # Add companies
    companies = [
        ("c1", "Google", Industry.TECHNOLOGY, "10000+"),
        ("c2", "Meta", Industry.TECHNOLOGY, "10000+"),
        ("c3", "Apple", Industry.TECHNOLOGY, "10000+"),
        ("c4", "Amazon", Industry.TECHNOLOGY, "10000+"),
    ]
    
    for cid, name, industry, size in companies:
        graph.add_company(cid, name, industry, size)
    
    # Add people
    people = [
        ("p1", "Alice", "Software Engineer", ["Python", "Go", "Cloud"]),
        ("p2", "Bob", "Product Manager", ["Product", "Agile"]),
        ("p3", "Charlie", "Data Scientist", ["Python", "ML", "SQL"]),
        ("p4", "Diana", "DevOps Engineer", ["AWS", "Kubernetes", "Docker"]),
    ]
    
    for pid, name, title, skills in people:
        graph.add_person(pid, name, title, skills)
    
    # Hire employees
    graph.hire("p1", "c1", "Software Engineer")
    graph.hire("p2", "c1", "Product Manager")
    graph.hire("p3", "c1", "Data Scientist")
    graph.hire("p4", "c1", "DevOps Engineer")
    
    # Post jobs
    graph.post_job("j1", "c2", "Senior Engineer", employment_type=EmploymentType.FULL_TIME, remote=True)
    graph.post_job("j2", "c3", "ML Engineer", requirements=["Python", "ML"])
    
    # Statistics
    print(f"\nStatistics:")
    print(f"  Companies: {graph.total_companies()}")
    print(f"  People: {graph.total_people()}")
    print(f"  Jobs: {graph.total_jobs()}")
    
    # Get company
    google = graph.get_company("c1")
    print(f"\n{google.name} ({google.industry.value}):")
    employees = graph.get_company_employees("c1")
    for e in employees:
        print(f"  - {e.name}: {e.title}")
    
    # Search jobs
    print(f"\nRemote jobs:")
    jobs = graph.search_jobs(remote=True)
    for j in jobs:
        print(f"  - {j.title} at {j.company_id}")
    
    # Skills
    print(f"\nPeople with Python:")
    python_people = graph.get_people_by_skill("Python")
    for p in python_people:
        print(f"  - {p.name}")


if __name__ == "__main__":
    main()


"""
Employment Graph Usage

    graph = EmploymentGraph()
    
    # Add companies
    graph.add_company("c1", "Google", Industry.TECHNOLOGY)
    
    # Add people
    graph.add_person("p1", "Alice", skills=["Python"])
    
    # Hire
    graph.hire("p1", "c1", "Engineer")
    
    # Employment history
    history = graph.get_employment_history("p1")
    company = graph.get_current_company("p1")
    
    # Jobs
    graph.post_job("j1", "c1", "Engineer")
    jobs = graph.search_jobs(skills=["Python"])
    
    # Network
    graph.find_coworkers("p1", "p2")
    suggestions = graph.suggest_colleagues("p1")
"""
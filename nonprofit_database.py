"""
nonprofit Database - Charities & Causes

nonprofit database:
- Charities, Nonprofits
- Donors, Volunteers
- Grants, Donations

Reference:
- IRS Tax Exempt Organization Search
- Guidestar: https://www.guidestar.org/

Schema.org: Nonprofit,NGO, Charity

Data Sources:
- IRS EO Database
- Guidestar
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


class NonprofitType(Enum):
    Public_Charity = "Public Charity"
    Private_Foundation = "Private Foundation"
    Religious = "Religious"
    Educational = "Educational"


@dataclass
class Nonprofit:
    id: str
    name: str
    
    ein: str = ""  # Employer Identification Number
    
    nonprofit_type: NonprofitType = NonprofitType.Public_Charity
    
    mission: str = ""
    
    revenue: float = 0.0
    
    expenses: float = 0.0
    
    website: str = ""


@dataclass
class Grant:
    id: str
    
    funder: str = ""  # Foundation name
    
    amount: float = 0.0
    
    deadline: str = ""


class NonprofitDatabase:
    def __init__(self):
        self.nonprofits: Dict[str, Nonprofit] = {}
        self.grants: Dict[str, Grant] = {}
    
    def add_nonprofit(self, n: Nonprofit) -> str:
        self.nonprofits[n.id] = n
        return n.id
    
    def search_nonprofits(self, nonprofit_type: NonprofitType) -> List[Nonprofit]:
        return [n for n in self.nonprofits.values() if n.nonprofit_type == nonprofit_type]
    
    def stats(self) -> Dict:
        return {"nonprofits": len(self.nonprofits), "grants": len(self.grants)}


def main():
    db = NonprofitDatabase()
    
    n = Nonprofit(id="n1", name="Red Cross", ein="53-0196609")
    db.add_nonprofit(n)
    
    print(f"Nonprofit: {n.name}, EIN: {n.ein}")
    print(f"Stats: {db.stats()}")


if __name__ == "__main__":
    main()
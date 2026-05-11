"""
Legal Database - Law & Attorneys

Legal database:
- Attorneys, Law Firms
- Case Law, Statutes
- Courts, Judges

Reference:
- Justia: https://law.justia.com/
- Caselaw Access Project: https://case.law/

Schema.org: Attorney, LawFirm, Courthouse, Court

Data Sources:
- Justia (case law)
- CourtListener API
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


class PracticeArea(Enum):
    Criminal = "Criminal"
    Civil = "Civil"
    Corporate = "Corporate"
    Family = "Family"
    IP = "Intellectual Property"


@dataclass
class Attorney:
    id: str
    name: str
    
    bar_number: str = ""
    state: str = ""
    practice_areas: List[PracticeArea] = field(default_factory=list)


@dataclass
class LawFirm:
    id: str
    name: str
    
    attorneys: int = 0
    locations: int = 0


@dataclass
class Court:
    id: str
    name: str
    
    jurisdiction: str = ""
    level: str = ""  # Federal, State


class LegalDatabase:
    def __init__(self):
        self.attorneys: Dict[str, Attorney] = {}
        self.firms: Dict[str, LawFirm] = {}
        self.courts: Dict[str, Court] = {}
    
    def add_attorney(self, a: Attorney) -> str:
        self.attorneys[a.id] = a
        return a.id
    
    def search_attorneys(self, state: str) -> List[Attorney]:
        return [a for a in self.attorneys.values() if a.state == state]
    
    def stats(self) -> Dict:
        return {"attorneys": len(self.attorneys), "firms": len(self.firms)}


def main():
    db = LegalDatabase()
    
    a = Attorney(id="a1", name="Jane Doe", bar_number="CA123", state="CA")
    db.add_attorney(a)
    
    print(f"Attorney: {a.name}, {a.state}")
    print(f"Stats: {db.stats()}")


if __name__ == "__main__":
    main()
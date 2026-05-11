"""
Insurance Database - Policies & Claims

Insurance database:
- Policies, Coverage
- Claims, Adjusters
- Carriers, Agents

Reference:
- NAIC: https://www.naic.org/
- ACORD: https://www.acord.org/

Data Sources:
- NAIC (National Association of Insurance Commissioners)
- State insurance databases
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum


class InsuranceType(Enum):
    Auto = "Auto"
    Home = "Home"
    Life = "Life"
    Health = "Health"
    Business = "Business"


@dataclass
class Policy:
    id: str
    type: InsuranceType
    
    carrier: str = ""
    premium: float = 0.0
    deductible: float = 0.0
    
    coverage_limit: float = 0.0
    start_date: Optional[date] = None


@dataclass
class Claim:
    id: str
    policy_id: str
    
    status: str = "Filed"
    amount: float = 0.0


class InsuranceDatabase:
    def __init__(self):
        self.policies: Dict[str, Policy] = {}
        self.claims: Dict[str, Claim] = {}
    
    def add_policy(self, p: Policy) -> str:
        self.policies[p.id] = p
        return p.id
    
    def file_claim(self, c: Claim) -> str:
        self.claims[c.id] = c
        return c.id
    
    def stats(self) -> Dict:
        return {"policies": len(self.policies), "claims": len(self.claims)}


def main():
    db = InsuranceDatabase()
    
    p = Policy(id="pol1", type=InsuranceType.Auto, carrier="GEICO", premium=1200)
    db.add_policy(p)
    
    print(f"Policy: {p.carrier}, ${p.premium}/yr")
    print(f"Stats: {db.stats()}")


if __name__ == "__main__":
    main()
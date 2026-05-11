"""
Software Categories Database - G2 & Gartner

Software categories from G2 and Gartner:
- Software Categories
- Product Reviews
- Vendor Information
- Magic Quadrant

Reference:
- G2: https://www.g2.com/
- Gartner: https://www.gartner.com/

Schema.org: SoftwareApplication, Product, Review

Data Sources:
- G2 Crowd (software reviews)
- Gartner Magic Quadrant
- Capterra
- GetApp
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


class SoftwareCategory(Enum):
    CRM = "CRM"
    ERP = "ERP"
    Marketing_Automation = "Marketing Automation"
    Helpdesk = "Helpdesk"
    Accounting = "Accounting"
    Project_Management = "Project Management"
    HR = "HR"
    Analytics = "Analytics"
    Security = "Security"
    DevOps = "DevOps"
    AI_ML = "AI/ML"


class Quadrant(Enum):
    Leaders = "Leaders"
    Challengers = "Challengers"
    Niche_Players = "Niche Players"
    Visionaries = "Visionaries"


@dataclass
class SoftwareProduct:
    id: str
    name: str
    
    category: SoftwareCategory = SoftwareCategory.CRM
    
    vendor: str = ""
    founded: int = 0
    
    website: str = ""
    
    description: str = ""
    
    pricing: str = ""  # Starting at
    
    rating: float = 0.0
    reviews: int = 0
    
    g2_url: str = ""


@dataclass
class SoftwareReview:
    id: str
    product_id: str
    
    rating: int = 5
    
    pros: str = ""
    cons: str = ""
    
    verified: bool = True
    
    author: str = ""
    company: str = ""


class SoftwareCategoryDatabase:
    def __init__(self):
        self.products: Dict[str, SoftwareProduct] = {}
        self.reviews: Dict[str, SoftwareReview] = {}
    
    def add_product(self, p: SoftwareProduct) -> str:
        self.products[p.id] = p
        return p.id
    
    def search_products(self, category: SoftwareCategory) -> List[SoftwareProduct]:
        return [p for p in self.products.values() if p.category == category]
    
    def get_top_products(self, category: SoftwareCategory = None, limit: int = 10) -> List[SoftwareProduct]:
        products = self.products.values()
        if category:
            products = [p for p in products if p.category == category]
        return sorted(products, key=lambda p: p.rating, reverse=True)[:limit]
    
    def stats(self) -> Dict:
        return {"products": len(self.products), "reviews": len(self.reviews)}


def main():
    db = SoftwareCategoryDatabase()
    
    p = SoftwareProduct(
        id="s1",
        name="Salesforce",
        category=SoftwareCategory.CRM,
        vendor="Salesforce",
        rating=4.5
    )
    db.add_product(p)
    
    print(f"Product: {p.name}")
    print(f"Category: {p.category.value}")
    print(f"Gartner Quadrant: {Quadrant.Leaders.value}")
    print(f"Stats: {db.stats()}")


if __name__ == "__main__":
    main()

"""
Software Categories Database covers:
- G2 software categories
- Gartner Magic Quadrant
- Product reviews and ratings
- Vendor information
"""
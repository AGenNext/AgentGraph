"""
Real Estate Database - Property Listings

Real estate database:
- Properties, Listings
- Agents, Agencies
- Listings, Sales, Rentals
- Locations, Features

Reference:
- Zillow: https://www.zillow.com/howto/api/APIOverview.htm
- Realtor.com: https://www.realtor.com/
- Redfin: https://www.redfin.com/

Schema.org: RealEstateListing, Apartment, LodgingBusiness

Data Sources:
- Realtor.com API
- Zillow API
- Multiple Listing Service (MLS)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum


# =============================================================================
# TYPES
# =============================================================================

class PropertyType(Enum):
    House = "House"
    Apartment = "Apartment"
    Condo = "Condo"
    Townhouse = "Townhouse"
    Land = "Land"
    Commercial = "Commercial"
    Industrial = "Industrial"


class ListingType(Enum):
    For_Sale = "For Sale"
    For_rent = "For Rent"
    Pending = "Pending"
    Sold = "Sold"


# =============================================================================
# ENTITIES
# =============================================================================

@dataclass
class Property:
    id: str
    address: str
    
    property_type: PropertyType = PropertyType.House
    
    price: float = 0.0
    
    bedrooms: int = 0
    bathrooms: float = 0.0
    sqft: int = 0
    
    lot_size: float = 0.0
    
    year_built: Optional[int] = None
    
    description: str = ""
    
    images: List[str] = field(default_factory=list)
    
    features: List[str] = field(default_factory=list)
    
    status: ListingType = ListingType.For_Sale
    
    days_on_market: int = 0


@dataclass
class Agent:
    id: str
    name: str
    
    email: str = ""
    phone: str = ""
    
    license: str = ""
    
    agency: str = ""
    
    image_url: str = ""
    
    sales: int = 0


@dataclass
class Agency:
    id: str
    name: str
    
    address: str = ""
    phone: str = ""
    
    website: str = ""
    
    agents: int = 0


# =============================================================================
# DATABASE
# =============================================================================

class RealEstateDatabase:
    def __init__(self):
        self.properties: Dict[str, Property] = {}
        self.agents: Dict[str, Agent] = {}
        self.agencies: Dict[str, Agency] = {}
    
    def add_property(self, p: Property) -> str:
        self.properties[p.id] = p
        return p.id
    
    def search_properties(
        self,
        min_price: float = None,
        max_price: float = None,
        bedrooms: int = None
    ) -> List[Property]:
        results = list(self.properties.values())
        
        if min_price:
            results = [p for p in results if p.price >= min_price]
        if max_price:
            results = [p for p in results if p.price <= max_price]
        if bedrooms:
            results = [p for p in results if p.bedrooms >= bedrooms]
        
        return results
    
    def add_agent(self, a: Agent) -> str:
        self.agents[a.id] = a
        return a.id
    
    def stats(self) -> Dict:
        return {"properties": len(self.properties), "agents": len(self.agents)}


def main():
    db = RealEstateDatabase()
    
    p = Property(id="p1", address="123 Main St", price=500000, bedrooms=3)
    db.add_property(p)
    
    print(f"Property: {p.address}, ${p.price}")
    print(f"Stats: {db.stats()}")


if __name__ == "__main__":
    main()
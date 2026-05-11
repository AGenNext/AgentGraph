"""
Schema.org Utility Functions and Helpers

Practical utilities for working with Schema.org types:
- Serialization (JSON-LD, dict)
- Validation
- CRUD operations
- Query helpers
- Type conversion
"""

from __future__ import annotations

import json
import hashlib
from datetime import datetime, timedelta
from typing import (
    Optional,
    List,
    Union,
    Any,
    Dict,
    Type,
    TypeVar,
    Callable,
    get_type_hints,
)

from schema_org_things_actions import (
    Thing,
    Action,
    Person,
    Organization,
    Product,
    Offer,
    Place,
    PostalAddress,
    GeoCoordinates,
    Event,
    CreativeWork,
    Rating,
    AggregateRating,
    ImageObject,
    VideoObject,
    AudioObject,
    MediaObject,
    Service,
    MonetaryAmount,
    QuantitativeValue,
    PriceSpecification,
    OpeningHoursSpecification,
    ContactPoint,
    Brand,
    BlogPosting,
    Article,
    Review,
    JobPosting,
    Reservation,
    FlightReservation,
    Order,
    OrderItem,
    Invoice,
    ProgramMembership,
    FAQPage,
    Question,
    Answer,
)

from schema_org_things_actions import (
    SCHEMA_ORG_CONTEXT,
    OfferItemCondition,
    ItemAvailability,
    EventStatusType,
    EventAttendanceMode,
    DayOfWeek,
    ActionStatusType,
)

T = TypeVar("T", bound=Thing)


# =============================================================================
# SERIALIZATION - Convert between formats
# =============================================================================

def to_json(thing: Thing, indent: int = 2, **kwargs) -> str:
    """Convert Schema.org thing to JSON string."""
    return json.dumps(thing.to_jsonld(), indent=indent, **kwargs)


def to_dict(thing: Thing) -> Dict[str, Any]:
    """Convert Schema.org thing to Python dict."""
    return thing.to_jsonld()


def from_dict(data: Dict[str, Any]) -> Thing:
    """Create Schema.org thing from dict/JSON-LD."""
    type_name = data.get("@type", "Thing")
    
    # Map types to classes
    type_map: Dict[str, Type[Thing]] = {
        "Thing": Thing,
        "Action": Action,
        "Person": Person,
        "Organization": Organization,
        "Product": Product,
        "Offer": Offer,
        "Place": Place,
        "PostalAddress": PostalAddress,
        "GeoCoordinates": GeoCoordinates,
        "Event": Event,
        "CreativeWork": CreativeWork,
        "Article": Article,
        "BlogPosting": BlogPosting,
        "Review": Review,
        "Rating": Rating,
        "AggregateRating": AggregateRating,
        "ImageObject": ImageObject,
        "VideoObject": VideoObject,
        "AudioObject": AudioObject,
        "MediaObject": MediaObject,
        "Service": Service,
        "JobPosting": JobPosting,
        "Reservation": Reservation,
        "FlightReservation": FlightReservation,
        "Order": Order,
        "Invoice": Invoice,
        "ProgramMembership": ProgramMembership,
        "FAQPage": FAQPage,
        "Question": Question,
        "Answer": Answer,
    }
    
    cls = type_map.get(type_name, Thing)
    
    # Extract known fields
    kwargs = {k: v for k, v in data.items() 
             if k not in ("@context", "@type", "@id") and v is not None}
    
    # Handle nested objects
    for field in ["image", "address", "geo", "location", "organizer"]:
        if field in data and isinstance(data[field], dict):
            kwargs[field] = from_dict(data[field])
    
    return cls(**kwargs)


def from_json(json_str: str) -> Thing:
    """Create Schema.org thing from JSON string."""
    return from_dict(json.loads(json_str))


# =============================================================================
# VALIDATION - Validate Schema.org entities
# =============================================================================

def validate(thing: Thing) -> ValidationResult:
    """Validate a Schema.org thing."""
    errors: List[str] = []
    warnings: List[str] = []
    
    # Required fields check
    if not thing.id and not thing.name:
        errors.append("Either 'id' or 'name' is required")
    
    # Type-specific validation
    if isinstance(thing, Product):
        if not thing.name and not thing.sku:
            errors.append("Product requires 'name' or 'sku'")
        if not thing.offers:
            warnings.append("Product has no 'offers'")
    
    if isinstance(thing, Person):
        if not thing.name:
            warnings.append("Person has no 'name'")
    
    if isinstance(thing, Organization):
        if not thing.name:
            warnings.append("Organization has no 'name'")
    
    if isinstance(thing, Offer):
        if thing.price is None:
            errors.append("Offer requires 'price'")
        if not thing.price_currency:
            warnings.append("Offer has no 'price_currency'")
    
    if isinstance(thing, Event):
        if not thing.start_date:
            errors.append("Event requires 'start_date'")
    
    if isinstance(thing, PostalAddress):
        if not any([thing.street_address, thing.address_locality, 
                    thing.postal_code, thing.address_country]):
            errors.append("PostalAddress requires address fields")
    
    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    )


class ValidationResult:
    """Result of validation."""
    def __init__(
        self, 
        valid: bool, 
        errors: List[str] = [], 
        warnings: List[str] = []
    ):
        self.valid = valid
        self.errors = errors
        self.warnings = warnings
    
    def __repr__(self):
        if self.valid:
            return f"ValidationResult(valid=True, warnings={len(self.warnings)})"
        return f"ValidationResult(valid=False, errors={self.errors})"


# =============================================================================
# ID GENERATION - Create Schema.org IDs
# =============================================================================

def generate_id(
    base_url: str, 
    entity_type: str, 
    identifier: str = None
) -> str:
    """Generate a Schema.org @id URL."""
    if identifier:
        return f"{base_url}/{entity_type}/{identifier}"
    return f"{base_url}/{entity_type}/{datetime.now().timestamp()}"


def hash_id(thing: Thing) -> str:
    """Generate deterministic ID from thing properties."""
    data = f"{thing.type}{thing.name or ''}{thing.description or ''}"
    return hashlib.md5(data.encode()).hexdigest()[:16]


# =============================================================================
# QUERY HELPERS - Filter and search
# =============================================================================

def filter_by_type(things: List[Thing], type_name: str) -> List[Thing]:
    """Filter things by @type."""
    return [t for t in things if t.type == type_name]


def filter_by_property(
    things: List[Thing], 
    property_name: str, 
    value: Any
) -> List[Thing]:
    """Filter things by property value."""
    return [
        t for t in things 
        if getattr(t, property_name, None) == value
    ]


def search(things: List[Thing], query: str) -> List[Thing]:
    """Full-text search across things."""
    query_lower = query.lower()
    results = []
    
    for thing in things:
        # Search in name and description
        if thing.name and query_lower in thing.name.lower():
            results.append(thing)
        elif thing.description and query_lower in thing.description.lower():
            results.append(thing)
        # Search in alternate names
        elif thing.alternate_name:
            for alt in thing.alternate_name:
                if query_lower in alt.lower():
                    results.append(thing)
                    break
    
    return results


def find_related(thing: Thing, things: List[Thing]) -> List[Thing]:
    """Find related entities."""
    related: List[Thing] = []
    
    # If it's a Product, find related products
    if isinstance(thing, Product):
        for other in things:
            if other.type == "Product" and other != thing:
                # Check category match
                if getattr(thing, "category") and getattr(other, "category"):
                    if set(thing.category) & set(other.category):
                        related.append(other)
    
    # If it's a Place, find events at this place
    if isinstance(thing, Place):
        for other in things:
            if isinstance(other, Event):
                if getattr(other, "location") == thing:
                    related.append(other)
    
    return related


# =============================================================================
# CRUD OPERATIONS - Database-like operations
# =============================================================================

class Repository:
    """Simple in-memory repository for Schema.org entities."""
    
    def __init__(self):
        self._things: Dict[str, Thing] = {}
        self._by_type: Dict[str, List[str]] = {}
    
    def add(self, thing: Thing) -> Thing:
        """Add an entity."""
        # Generate ID if not provided
        if not thing.id:
            thing.id = generate_id("https://example.com", thing.type)
        
        self._things[thing.id] = thing
        
        # Index by type
        if thing.type not in self._by_type:
            self._by_type[thing.type] = []
        if thing.id not in self._by_type[thing.type]:
            self._by_type[thing.type].append(thing.id)
        
        return thing
    
    def get(self, id: str) -> Optional[Thing]:
        """Get entity by ID."""
        return self._things.get(id)
    
    def update(self, thing: Thing) -> Thing:
        """Update an entity."""
        if thing.id not in self._things:
            raise KeyError(f"Entity not found: {thing.id}")
        self._things[thing.id] = thing
        return thing
    
    def delete(self, id: str) -> bool:
        """Delete an entity."""
        if id not in self._things:
            return False
        
        thing = self._things[id]
        if thing.type in self._by_type:
            self._by_type[thing.type].remove(id)
        
        del self._things[id]
        return True
    
    def list(self, type_name: str = None) -> List[Thing]:
        """List all entities, optionally filtered by type."""
        if type_name:
            ids = self._by_type.get(type_name, [])
            return [self._things[i] for i in ids]
        return list(self._things.values())
    
    def find(self, **filters) -> List[Thing]:
        """Find entities by property filters."""
        results = []
        for thing in self._things.values():
            match = True
            for prop, value in filters.items():
                if getattr(thing, prop, None) != value:
                    match = False
                    break
            if match:
                results.append(thing)
        return results


# =============================================================================
# TYPE CONVERSION - Convert between Schema.org types
# =============================================================================

def to_product(service: Service) -> Product:
    """Convert Service to Product."""
    return Product(
        name=service.name,
        description=service.description,
        offers=service.offers,
    )


def to_image_object(url: str, **kwargs) -> ImageObject:
    """Create ImageObject from URL."""
    return ImageObject(
        url=url,
        content_url=url,
        **kwargs
    )


def to_review(rating: Rating, **kwargs) -> Review:
    """Convert Rating to Review."""
    return Review(
        name=kwargs.get("name", f"Review of {rating.id}"),
        review_rating=rating,
        **kwargs
    )


def to_offer(product: Product) -> Optional[Offer]:
    """Extract primary Offer from Product."""
    if product.offers:
        return product.offers[0]
    return None


def to_place(address: PostalAddress) -> Place:
    """Convert PostalAddress to Place."""
    return Place(
        name=address.name,
        address=address,
        geo=GeoCoordinates(
            latitude=getattr(address, "latitude", None),
            longitude=getattr(address, "longitude", None),
        ) if hasattr(address, "latitude") else None
    )


# =============================================================================
# AGGREGATION - Group and count
# =============================================================================

def count_by_type(things: List[Thing]) -> Dict[str, int]:
    """Count entities by type."""
    counts: Dict[str, int] = {}
    for thing in things:
        counts[thing.type] = counts.get(thing.type, 0) + 1
    return counts


def group_by_type(things: List[Thing]) -> Dict[str, List[Thing]]:
    """Group entities by type."""
    groups: Dict[str, List[Thing]] = {}
    for thing in things:
        if thing.type not in groups:
            groups[thing.type] = []
        groups[thing.type].append(thing)
    return groups


def group_by_property(
    things: List[Thing], 
    property_name: str
) -> Dict[Any, List[Thing]]:
    """Group by property value."""
    groups: Dict[Any, List[Thing]] = {}
    for thing in things:
        value = getattr(thing, property_name, None)
        if value is not None:
            if value not in groups:
                groups[value] = []
            groups[value].append(thing)
    return groups


def top_rated(things: List[Thing], limit: int = 10) -> List[Thing]:
    """Get top rated entities."""
    rated = [t for t in things if isinstance(t, Product) and t.aggregate_rating]
    rated.sort(
        key=lambda x: x.aggregate_rating.rating_value 
        if x.aggregate_rating else 0, 
        reverse=True
    )
    return rated[:limit]


def average_rating(things: List[Thing]) -> float:
    """Calculate average rating across entities."""
    ratings = [
        t.aggregate_rating.rating_value 
        for t in things 
        if isinstance(t, Product) and t.aggregate_rating
    ]
    return sum(ratings) / len(ratings) if ratings else 0.0


# =============================================================================
# TEMPORAL HELPERS - Time-based operations
# =============================================================================

def upcoming_events(things: List[Thing]) -> List[Event]:
    """Get upcoming events."""
    now = datetime.now()
    events = [e for e in things if isinstance(e, Event)]
    return [
        e for e in events 
        if e.start_date and e.start_date > now
    ]


def past_events(things: List[Thing]) -> List[Event]:
    """Get past events."""
    now = datetime.now()
    events = [e for e in things if isinstance(e, Event)]
    return [
        e for e in events 
        if e.start_date and e.start_date <= now
    ]


def events_in_range(
    things: List[Thing], 
    start: datetime, 
    end: datetime
) -> List[Event]:
    """Get events in date range."""
    events = [e for e in things if isinstance(e, Event)]
    return [
        e for e in events 
        if e.start_date and start <= e.start_date <= end
    ]


def is_open_now(place: Place) -> bool:
    """Check if place is currently open."""
    now = datetime.now()
    if not place.opening_hours_specification:
        return False
    
    current_day = now.strftime("%A")
    current_time = now.strftime("%H:%M")
    
    for hours in place.opening_hours_specification:
        if str(hours.day_of_week) == current_day:
            if hours.opens and hours.closes:
                if hours.opens <= current_time <= hours.closes:
                    return True
    return False


# =============================================================================
# PRICE HELPERS - Price operations
# =============================================================================

def lowest_price(product: Product) -> Optional[float]:
    """Get lowest price from product offers."""
    if not product.offers:
        return None
    prices = [o.price for o in product.offers if o.price is not None]
    return min(prices) if prices else None


def highest_price(product: Product) -> Optional[float]:
    """Get highest price from product offers."""
    if not product.offers:
        return None
    prices = [o.price for o in product.offers if o.price is not None]
    return max(prices) if prices else None


def price_range(product: Product) -> Optional[tuple]:
    """Get price range from product offers."""
    lowest = lowest_price(product)
    highest = highest_price(product)
    if lowest and highest:
        return (lowest, highest)
    return None


def in_budget(
    products: List[Product], 
    min_price: float = 0, 
    max_price: float = float("inf")
) -> List[Product]:
    """Filter products by budget."""
    return [
        p for p in products 
        if lowest_price(p) and min_price <= lowest_price(p) <= max_price
    ]


# =============================================================================
# EXPORT HELPERS - Export to various formats
# =============================================================================

def to_jsonld_collection(things: List[Thing]) -> Dict[str, Any]:
    """Export collection as JSON-LD graph."""
    return {
        "@context": SCHEMA_ORG_CONTEXT,
        "@graph": [t.to_jsonld() for t in things]
    }


def to_html_display(things: List[Thing]) -> str:
    """Generate HTML for displaying entities."""
    html = ['<div class="schema-org-entities">']
    
    for thing in things:
        html.append(f'<div class="entity entity-{thing.type.lower()}">')
        html.append(f'  <h3>{thing.name or thing.id}</h3>')
        html.append(f'  <span class="type">{thing.type}</span>')
        
        if thing.description:
            html.append(f'  <p>{thing.description}</p>')
        
        if isinstance(thing, Product) and thing.offers:
            for offer in thing.offers:
                if offer.price:
                    html.append(f'  <span class="price">${offer.price}</span>')
        
        if isinstance(thing, AggregateRating):
            if thing.rating_value:
                html.append(f'  <span class="rating">{thing.rating_value}★</span>')
        
        html.append('</div>')
    
    html.append('</div>')
    return '\n'.join(html)


def to_rdf(thing: Thing) -> str:
    """Export as Turtle RDF."""
    lines = [
        f"@prefix schema: <https://schema.org/> .",
        "",
        f"<{thing.id}> a schema:{thing.type} ;",
    ]
    
    if thing.name:
        lines.append(f'    schema:name "{thing.name}" ;')
    
    if thing.description:
        lines.append(f'    schema:description """{thing.description}""" ;')
    
    if thing.url:
        lines.append(f'    schema:url <{thing.url}> .')
    
    return '\n'.join(lines)


def to_microdata(thing: Thing) -> str:
    """Export as HTML Microdata."""
    attrs = [
        f'itemscope',
        f'itemtype="https://schema.org/{thing.type}"',
    ]
    
    html = [f'<div {" ".join(attrs)}>']
    
    if thing.name:
        html.append(f'  <div itemprop="name">{thing.name}</div>')
    
    if thing.description:
        html.append(f'  <div itemprop="description">{thing.description}</div>')
    
    if thing.url:
        html.append(f'  <link itemprop="url" href="{thing.url}"/>')
    
    html.append('</div>')
    return '\n'.join(html)


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

def main():
    """Example usage of Schema.org utilities."""
    
    # Create a repository
    repo = Repository()
    
    # Create organizations
    acme = Organization(
        id="https://example.com/orgs/acme",
        name="Acme Corp",
        description="A leading widget manufacturer",
        url="https://acme.com",
    )
    repo.add(acme)
    
    # Create products
    widget = Product(
        id="https://example.com/products/widget",
        name="Super Widget",
        description="The best widget ever",
        sku="SW-001",
        brand=acme.name,
        offers=[
            Offer(
                price=99.99,
                price_currency="USD",
                availability=ItemAvailability.IN_STOCK,
            )
        ],
        aggregate_rating=AggregateRating(
            rating_value=4.5,
            rating_count=128,
        ),
    )
    repo.add(widget)
    
    # Create person
    john = Person(
        id="https://example.com/people/john",
        name="John Doe",
        email="john@acme.com",
        job_title="Engineer",
        works_for=[acme],
    )
    repo.add(john)
    
    # Validation
    print("=== Validation ===")
    print(f"Widget valid: {validate(widget)}")
    print(f"Person valid: {validate(john)}")
    
    # Query
    print("\n=== Query ===")
    products = repo.list("Product")
    print(f"Products: {len(products)}")
    
    # Search
    results = repo.list()
    found = search(results, "widget")
    print(f"Search 'widget': {len(found)} results")
    
    # Export
    print("\n=== Export ===")
    print("JSON-LD:")
    print(to_json(widget))
    
    print("\nMicrodata:")
    print(to_microdata(widget))
    
    # Aggregations
    print("\n=== Aggregations ===")
    all_things = repo.list()
    by_type = count_by_type(all_things)
    print(f"By type: {by_type}")
    
    print(f"\nAverage rating: {average_rating([widget])}")
    
    print(f"\nLowest price: ${lowest_price(widget)}")


if __name__ == "__main__":
    main()


"""
Schema.org Utility Functions

Usage:
    from schema_org_utils import (
        to_json, from_dict, validate,
        Repository, search, filter_by_type,
    )
    
    # Validate
    result = validate(product)
    if not result.valid:
        print(f"Errors: {result.errors}")
    
    # Repository CRUD
    repo = Repository()
    repo.add(product)
    found = repo.find(name="Widget")
    
    # Export
    print(to_json(product))
    
    # Filter
    products = filter_by_type(things, "Product")

References:
    - https://schema.org/docs/schemas.html
    - https://json-ld.org/
"""
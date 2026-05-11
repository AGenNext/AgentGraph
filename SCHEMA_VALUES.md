# Schema.org Property Values (Expected Types)

Reference: https://schema.org/docs/full.html

## Property Value Types

### Text Values
- name: "Avatar" → str
- description: "A sci-fi movie" → str
- headline: "Breaking News" → str
- color: "black" → str
- keywords: "action, adventure" → str

### URL Values
- url: "https://example.com" → str
- image: "https://example.com/image.jpg" → str

### Number Values
- price: 19.99 → float
- rating: 4.5 → float
- elevation: 1000 → QuantitativeValue

### Boolean Values
- isic: True → bool

### Date/Time Values
- datePublished: "2024-01-15" → date
- startDate: "2024-01-15T10:00:00" → datetime
- validFrom: "2024-01-01" → datetime

### Enumeration Values (Constrained)

| Property | Values |
|----------|--------|
| **eventStatus** | EventScheduled, EventCancelled, EventPostponed |
| **availability** | InStock, OutOfStock, PreOrder, Discontinued |
| **itemCondition** | NewCondition, UsedCondition, Refurbished |
| **dayOfWeek** | Monday, Tuesday... Sunday |
| **genderType** | Male, Female |

### Structured Values (Nested Objects)

| Property | Type | Example |
|----------|------|---------|
| address | PostalAddress | {street, city, postalCode} |
| geo | GeoCoordinates | {latitude, longitude} |
| contactPoint | ContactPoint | {telephone, email} |
| price | MonetaryAmount | {currency, price} |

### Reference Types (Links)

| Property | Expected Type | Our Implementation |
|----------|-------------|----------------|
| author | Person/Organization | author_id: str |
| location | Place | location_id: str |
| performer | Person/Organization | performer_id: str |
| employee | Person | employee_id: str |

## Data Types

| DataType | Python | Example |
|----------|--------|---------|
| Boolean | bool | True/False |
| Date | date | 2024-01-15 |
| DateTime | datetime | 2024-01-15T10:00:00 |
| Float | float | 3.14 |
| Integer | int | 42 |
| Text | str | "Hello" |
| Time | time | 10:00:00 |
| URL | str | "https://..." |
| Duration | str | "PT1H30M" (ISO 8601) |

## Our Implementation

All value types implemented as Python dataclass fields:

```python
from datetime import date, datetime, time

@dataclass
class Product:
    # Text
    name: str = ""
    
    # Number
    price: float = 0.0
    
    # Boolean
    active: bool = True
    
    # Date
    date_published: Optional[date] = None
    
    # DateTime
    created_at: Optional[datetime] = None
    
    # Enumeration
    availability: ItemAvailability = ItemAvailability.InStock
    
    # Nested (as dict or link)
    address: dict = field(default_factory=dict)
    geo: dict = field(default_factory=dict)
    
    # Reference (as ID)
    brand_id: str = ""
```

Reference: https://schema.org/docs/full.html
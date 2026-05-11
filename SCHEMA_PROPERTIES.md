# Schema.org Properties (Attributes)

Reference: https://schema.org/docs/full.html

## Properties by Type

### THING (Root Properties)
- name (Text)
- description (Text)
- url (URL)
- image (URL or ImageObject)

### ACTION
- name (Text)
- startTime (DateTime)
- endTime (DateTime)
- object (Thing)
- result (Thing)
- target (URL)
- error (Thing)

### CREATIVE WORK
- name (Text)
- author (Person or Organization)
- datePublished (Date)
- dateCreated (Date)
- dateModified (Date)
- contentRating (Text)
- inLanguage (Text)
- encoding (MediaObject)
- headline (Text)
- text (Text)
- about (Thing)
- genre (Text)
- keywords (Text)

### EVENT
- name (Text)
- startDate (DateTime)
- endDate (DateTime)
- eventStatus (EventStatusType)
- eventAttendanceMode (EventAttendanceMode)
- location (Place or PostalAddress)
- performer (Person or Organization)
- organizer (Person or Organization)

### ORGANIZATION
- name (Text)
- url (URL)
- logo (ImageObject)
- foundingDate (Date)
- dissolutionDate (Date)
- address (PostalAddress)
- founder (Person)
- member (Person or Organization)
- employee (Person)

### PERSON
- name (Text)
- jobTitle (Text)
- birthDate (Date)
- deathDate (Date)
- address (PostalAddress)
- email (Text)
- telephone (Text)
- url (URL)

### PLACE
- name (Text)
- address (PostalAddress)
- geo (GeoCoordinates)
- openingHoursSpecification (OpeningHoursSpecification)
- telephone (Text)
- url (URL)

### PRODUCT
- name (Text)
- brand (Brand or Text)
- manufacturer (Organization)
- model (ProductModel or Text)
- sku (Text)
- color (Text)
- weight (QuantitativeValue)
- width, height, depth (QuantitativeValue)

### OFFER (Intangible)
- price (Number or Text)
- priceCurrency (Text)
- availability (ItemAvailability)
- validFrom (DateTime)
- validThrough (DateTime)
- itemCondition (OfferItemCondition)

### MEDICAL ENTITY
- code (MedicalCode)
- guideline (MedicalGuideline)
- relevantSpecialty (MedicalSpecialty)
- study (MedicalStudy)

## Our Implementation

All properties map to dataclass fields:

```python
@dataclass
class Movie:
    name: str = ""                    # name
    description: str = ""              # description
    url: str = ""                  # url
    image: str = ""                # image
    date_published: datetime = None    # datePublished
    date_created: datetime = None     # dateCreated
    author_id: str = ""              # author (link)
    genre: str = ""                # genre
    content_rating: str = ""          # contentRating
```

Reference: https://schema.org/docs/full.html
# Schema.org Best Practices

## Implementation Best Practices

### 1. Type Hierarchy

✅ **DO**
- Use most specific type possible
- Inherit from core types
- Map to existing Schema.org types

```python
# ✅ Good: Specific type
@dataclass
class Restaurant(LocalBusiness):  # More specific
    servesCuisine: str = ""
    menu: List[MenuItem] = []

# ❌ Bad: Too generic
@dataclass
class Restaurant(Thing):  # Too generic
    name: str = ""
```

### 2. Property Naming

✅ **DO**
- Use Schema.org property names exactly
- Use camelCase for JSON-LD
- Map Python snake_case to camelCase

```python
# ✅ Good: Schema.org names
@dataclass
class Book:
    name: str = ""           # schema.org/name
    author: str = ""          # schema.org/author
    datePublished: date = None  # schema.org/datePublished

# ❌ Bad: Custom names
@dataclass
class Book:
    title: str = ""          # Wrong!
    writer: str = ""         # Wrong!
```

### 3. Required Properties

| Type | Required Properties |
|------|---------------------|
| Thing | name |
| CreativeWork | name |
| Organization | name |
| Person | name |
| Product | name |
| Event | name, startDate |

### 4. Expected Types

✅ **DO**
- Use expected type when property accepts multiple types

```python
# ✅ Good: Use specific type
location: "Place"  # Works with Place, CivicStructure, etc.

# ❌ Bad: Force specific
location: "CivicStructure"  # Too specific if Place expected
```

### 5. Enumerations

✅ **DO**
- Use Schema.org enumerations when available

```python
# ✅ Good: Schema.org enum
class DayOfWeek(Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    # ...
```

### 6. Nested Items

✅ **DO**
- Use embedded items for complex relationships

```python
# ✅ Good: Embedded
@dataclass
class Movie:
    name: str = ""
    director: str = ""  # ID reference
    
    @property
    def director_person(self) -> Person:
        return db.get(self.director)
```

### 7. URLs vs Text

| Property | Use URL When | Use Text When |
|----------|--------------|--------------|
| url | External links | - |
| email | - | Email address |
| telephone | - | Phone number |
| sameAs | Social URLs | - |

### 8. Data Types

| Schema.org | Python | Example |
|-----------|--------|---------|
| Boolean | bool | True/False |
| Date | date | 2024-01-15 |
| DateTime | datetime | 2024-01-15T10:00:00 |
| Float | float | 3.14 |
| Integer | int | 42 |
| Text | str | "Hello" |
| URL | str | "https://..." |

### 9. Validation

✅ **DO**
- Validate all properties before creation
- Use schema validators

```python
def validate_movie(movie: Movie) -> bool:
    errors = []
    
    if not movie.name:
        errors.append("name is required")
    
    if movie.datePublished and movie.datePublished > date.today():
        errors.append("datePublished cannot be in future")
    
    return len(errors) == 0
```

### 10. SEO Best Practices

| Property | SEO Value |
|----------|----------|
| name | Page title |
| description | Meta description |
| image | OG Image |
| url | Canonical URL |
| headline | H1 |

### 11. JSON-LD Structure

```json
{
  "@context": "https://schema.org",
  "@type": "Movie",
  "name": "Avatar",
  "director": {
    "@type": "Person",
    "name": "James Cameron"
  }
}
```

### 12. Common Mistakes

| Mistake | Solution |
|--------|-----------|
| Missing @context | Always include @context: "https://schema.org" |
| Wrong @type | Use exact type name from schema.org |
| Missing required | Always include name |
| Using custom props | Use standard Schema.org properties |
| Old vocab versions | Use latest (v30.0) |

### 13. Testing

```python
def test_movie_schema():
    movie = Movie(
        name="Avatar",
        director_id="jc1"
    )
    
    # Validate required
    assert movie.name is not None
    
    # Check type
    assert is_valid_schema_type(movie, "Movie")
    
    # Check properties
    assert has_property(movie, "name")
```

### 14. Documentation

- Always reference: https://schema.org/docs/full.html
- Document mappings in DATABASE_SOURCES.md
- Include Schema.org type in docstrings

Reference: https://schema.org/docs/ | https://developers.google.com/search/docs/guides/intro-structured-data
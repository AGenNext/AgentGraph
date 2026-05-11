"""
Schema.org Database ORM

Object-Relational Mapping for Schema.org entities:
- Model class for CRUD operations
- Relationships between entities
- Query building
- Migration support
"""

from __future__ import annotations

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
    Generic,
    Literal,
)
from dataclasses import dataclass, field
import json
import sqlite3
from pathlib import Path

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
    MediaObject,
    Service,
    JobPosting,
    Reservation,
    FlightReservation,
    Order,
    Invoice,
    BlogPosting,
    Article,
    Review,
    FAQPage,
    Question,
    Answer,
    OpeningHoursSpecification,
    ContactPoint,
    Brand,
    SCHEMA_ORG_CONTEXT,
)
from schema_org_things_actions import (
    OfferItemCondition,
    ItemAvailability,
    EventStatusType,
    EventAttendanceMode,
    ActionStatusType,
)

T = TypeVar("T", bound=Thing)


# =============================================================================
# BASE MODEL - Abstract Model
# =============================================================================

class Model(Generic[T]):
    """Base model for Schema.org entities."""
    
    table_name: str
    fields: Dict[str, str] = {}  # field_name -> sqlite_type
    
    def __init__(self, db: Database):
        self.db = db
    
    def _to_row(self, entity: T) -> Dict[str, Any]:
        """Convert entity to database row."""
        raise NotImplementedError
    
    def _from_row(self, row: Dict[str, Any]) -> T:
        """Convert database row to entity."""
        raise NotImplementedError
    
    def save(self, entity: T) -> T:
        """Save entity to database."""
        data = self._to_row(entity)
        
        # Check if exists
        if entity.id and self.db.fetch_one(self.table_name, {"id": entity.id}):
            self.db.update(self.table_name, data, {"id": entity.id})
        else:
            self.db.insert(self.table_name, data)
        
        return entity
    
    def get(self, id: str) -> Optional[T]:
        """Get entity by ID."""
        row = self.db.fetch_one(self.table_name, {"id": id})
        if row:
            return self._from_row(row)
        return None
    
    def delete(self, id: str) -> bool:
        """Delete entity by ID."""
        return self.db.delete(self.table_name, {"id": id})
    
    def all(self) -> List[T]:
        """Get all entities."""
        rows = self.db.fetch_all(self.table_name)
        return [self._from_row(r) for r in rows]
    
    def filter(self, **filters) -> List[T]:
        """Filter entities."""
        rows = self.db.fetch_all(self.table_name, filters)
        return [self._from_row(r) for r in rows]


# =============================================================================
# DATABASE - SQLite database wrapper
# =============================================================================

class Database:
    """SQLite database for Schema.org entities."""
    
    def __init__(self, db_path: str = "schema_org.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
    
    def _create_tables(self):
        """Create database tables."""
        cursor = self.conn.cursor()
        
        # Thing base table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS things (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                name TEXT,
                description TEXT,
                url TEXT,
                image TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        
        # Person table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS persons (
                id TEXT PRIMARY KEY,
                family_name TEXT,
                given_name TEXT,
                email TEXT,
                job_title TEXT,
                telephone TEXT,
                birth_date TEXT,
                FOREIGN KEY (id) REFERENCES things (id)
            )
        """)
        
        # Organization table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS organizations (
                id TEXT PRIMARY KEY,
                legal_name TEXT,
                email TEXT,
                telephone TEXT,
                fax_number TEXT,
                founding_date TEXT,
                FOREIGN KEY (id) REFERENCES things (id)
            )
        """)
        
        # Product table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT,
                sku TEXT,
                gtin TEXT,
                mpn TEXT,
                brand TEXT,
                manufacturer TEXT,
                product_id TEXT,
                FOREIGN KEY (id) REFERENCES things (id)
            )
        """)
        
        # Offer table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS offers (
                id TEXT PRIMARY KEY,
                price REAL,
                price_currency TEXT,
                availability TEXT,
                item_condition TEXT,
                valid_from TEXT,
                valid_through TEXT,
                product_id TEXT,
                seller_id TEXT
            )
        """)
        
        # Place table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS places (
                id TEXT PRIMARY KEY,
                latitude REAL,
                longitude REAL,
                elevation REAL,
                is_accessible_for_free INTEGER,
                FOREIGN KEY (id) REFERENCES things (id)
            )
        """)
        
        # PostalAddress table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS postal_addresses (
                id TEXT PRIMARY KEY,
                street_address TEXT,
                address_locality TEXT,
                address_region TEXT,
                address_country TEXT,
                postal_code TEXT
            )
        """)
        
        # Event table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                start_date TEXT,
                end_date TEXT,
                event_status TEXT,
                event_attendance_mode TEXT,
                location_id TEXT,
                organizer_id TEXT,
                FOREIGN KEY (id) REFERENCES things (id)
            )
        """)
        
        # Rating table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ratings (
                id TEXT PRIMARY KEY,
                rating_value REAL,
                best_rating REAL,
                worst_rating REAL,
                rating_count INTEGER,
                review_count INTEGER,
                type TEXT
            )
        """)
        
        # Offer relationship table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_offers (
                product_id TEXT,
                offer_id TEXT,
                PRIMARY KEY (product_id, offer_id)
            )
        """)
        
        # Organization relationships
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS org_members (
                org_id TEXT,
                person_id TEXT,
                PRIMARY KEY (org_id, person_id)
            )
        """)
        
        # Product relationships
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_related (
                product_id TEXT,
                related_id TEXT,
                relationship_type TEXT,
                PRIMARY KEY (product_id, related_id)
            )
        """)
        
        self.conn.commit()
    
    def insert(self, table: str, data: Dict[str, Any]):
        """Insert a row."""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        sql = f"INSERT OR REPLACE INTO {table} ({columns}) VALUES ({placeholders})"
        
        cursor = self.conn.cursor()
        cursor.execute(sql, list(data.values()))
        self.conn.commit()
    
    def update(self, table: str, data: Dict[str, Any], where: Dict[str, Any]):
        """Update rows."""
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        where_clause = " AND ".join([f"{k} = ?" for k in where.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        
        cursor = self.conn.cursor()
        cursor.execute(sql, list(data.values()) + list(where.values()))
        self.conn.commit()
    
    def delete(self, table: str, where: Dict[str, Any]) -> bool:
        """Delete rows."""
        where_clause = " AND ".join([f"{k} = ?" for k in where.keys()])
        sql = f"DELETE FROM {table} WHERE {where_clause}"
        
        cursor = self.conn.cursor()
        cursor.execute(sql, list(where.values()))
        return cursor.rowcount > 0
    
    def fetch_one(
        self, 
        table: str, 
        where: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Fetch one row."""
        where_clause = " AND ".join([f"{k} = ?" for k in where.keys()])
        sql = f"SELECT * FROM {table} WHERE {where_clause} LIMIT 1"
        
        cursor = self.conn.cursor()
        cursor.execute(sql, list(where.values()))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    
    def fetch_all(
        self, 
        table: str, 
        where: Dict[str, Any] = {},
        limit: int = None
    ) -> List[Dict[str, Any]]:
        """Fetch all rows."""
        if where:
            where_clause = " AND ".join([f"{k} = ?" for k in where.keys()])
            sql = f"SELECT * FROM {table} WHERE {where_clause}"
        else:
            sql = f"SELECT * FROM {table}"
        
        if limit:
            sql += f" LIMIT {limit}"
        
        cursor = self.conn.cursor()
        cursor.execute(sql, list(where.values()) if where else [])
        return [dict(row) for row in cursor.fetchall()]
    
    def execute(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute raw SQL."""
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def close(self):
        """Close database."""
        self.conn.close()


# =============================================================================
# MODEL IMPLEMENTATIONS
# =============================================================================

class ThingModel(Model[Thing]):
    """Model for Thing entities."""
    
    table_name = "things"
    
    def _to_row(self, entity: Thing) -> Dict[str, Any]:
        return {
            "id": entity.id,
            "type": entity.type,
            "name": entity.name,
            "description": entity.description,
            "url": entity.url,
            "image": entity.image.url if isinstance(entity.image, ImageObject) else entity.image,
            "created_at": entity.created_at.isoformat() if entity.created_at else None,
            "updated_at": entity.updated_at.isoformat() if entity.updated_at else None,
        }
    
    def _from_row(self, row: Dict[str, Any]) -> Thing:
        return Thing(
            id=row["id"],
            type=row["type"],
            name=row["name"],
            description=row["description"],
            url=row["url"],
            image=row["image"],
        )


class PersonModel(ThingModel):
    """Model for Person entities."""
    
    table_name = "persons"
    
    def _to_row(self, entity: Person) -> Dict[str, Any]:
        base = super()._to_row(entity)
        base.update({
            "family_name": entity.family_name,
            "given_name": entity.given_name,
            "email": entity.email,
            "job_title": entity.job_title,
            "telephone": entity.telephone,
            "birth_date": entity.birth_date.isoformat() if entity.birth_date else None,
        })
        return base
    
    def _from_row(self, row: Dict[str, Any]) -> Person:
        return Person(
            id=row["id"],
            name=f"{row.get('given_name', '')} {row.get('family_name', '')}".strip(),
            family_name=row.get("family_name"),
            given_name=row.get("given_name"),
            email=row.get("email"),
            job_title=row.get("job_title"),
            telephone=row.get("telephone"),
        )


class OrganizationModel(ThingModel):
    """Model for Organization entities."""
    
    table_name = "organizations"
    
    def _to_row(self, entity: Organization) -> Dict[str, Any]:
        base = super()._to_row(entity)
        base.update({
            "legal_name": entity.legal_name,
            "email": entity.email,
            "telephone": entity.telephone,
            "fax_number": entity.fax_number,
            "founding_date": entity.founding_date.isoformat() if entity.founding_date else None,
        })
        return base
    
    def _from_row(self, row: Dict[str, Any]) -> Organization:
        return Organization(
            id=row["id"],
            name=row["name"] or row.get("legal_name"),
            legal_name=row.get("legal_name"),
            email=row.get("email"),
            telephone=row.get("telephone"),
        )


class ProductModel(ThingModel):
    """Model for Product entities."""
    
    table_name = "products"
    
    def _to_row(self, entity: Product) -> Dict[str, Any]:
        base = super()._to_row(entity)
        base.update({
            "sku": entity.sku,
            "gtin": entity.gtin,
            "mpn": entity.mpn,
            "brand": entity.brand.name if isinstance(entity.brand, Brand) else entity.brand,
            "product_id": entity.product_id,
        })
        return base
    
    def _from_row(self, row: Dict[str, Any]) -> Product:
        return Product(
            id=row["id"],
            name=row["name"],
            sku=row.get("sku"),
            gtin=row.get("gtin"),
            mpn=row.get("mpn"),
            product_id=row.get("product_id"),
        )
    
    def get_with_offers(self, id: str) -> Optional[Product]:
        """Get product with offers."""
        product = self.get(id)
        if not product:
            return None
        
        # Fetch offers
        offer_model = OfferModel(self.db)
        product.offers = offer_model.filter(product_id=id)
        
        return product


class OfferModel(Model[Offer]):
    """Model for Offer entities."""
    
    table_name = "offers"
    
    def _to_row(self, entity: Offer) -> Dict[str, Any]:
        # Generate ID if not exists
        offer_id = entity.id or f"{entity.item_offered.id}/offer" if entity.item_offered else None
        
        return {
            "id": offer_id,
            "price": entity.price,
            "price_currency": entity.price_currency,
            "availability": entity.availability.value if entity.availability else None,
            "item_condition": entity.item_condition.value if entity.item_condition else None,
            "valid_from": entity.valid_from.isoformat() if entity.valid_from else None,
            "valid_through": entity.valid_through.isoformat() if entity.valid_through else None,
            "product_id": entity.item_offered.id if entity.item_offered else None,
            "seller_id": entity.seller.id if entity.seller else None,
        }
    
    def _from_row(self, row: Dict[str, Any]) -> Offer:
        return Offer(
            id=row["id"],
            price=row.get("price"),
            price_currency=row.get("price_currency"),
            availability=ItemAvailability(row["availability"]) if row.get("availability") else None,
            item_condition=OfferItemCondition(row["item_condition"]) if row.get("item_condition") else None,
            valid_from=datetime.fromisoformat(row["valid_from"]) if row.get("valid_from") else None,
            valid_through=datetime.fromisoformat(row["valid_through"]) if row.get("valid_through") else None,
        )
    
    def filter(self, product_id: str) -> List[Offer]:
        """Filter by product."""
        return self.filter(product_id=product_id)


class PlaceModel(ThingModel):
    """Model for Place entities."""
    
    table_name = "places"
    
    def _to_row(self, entity: Place) -> Dict[str, Any]:
        base = super()._to_row(entity)
        base.update({
            "latitude": entity.latitude,
            "longitude": entity.longitude,
            "elevation": entity.elevation,
            "is_accessible_for_free": 1 if entity.is_accessible_for_free else 0,
        })
        return base
    
    def _from_row(self, row: Dict[str, Any]) -> Place:
        return Place(
            id=row["id"],
            name=row["name"],
            latitude=row.get("latitude"),
            longitude=row.get("longitude"),
            elevation=row.get("elevation"),
        )


class EventModel(ThingModel):
    """Model for Event entities."""
    
    table_name = "events"
    
    def _to_row(self, entity: Event) -> Dict[str, Any]:
        base = super()._to_row(entity)
        base.update({
            "start_date": entity.start_date.isoformat() if entity.start_date else None,
            "end_date": entity.end_date.isoformat() if entity.end_date else None,
            "event_status": entity.event_status.value if entity.event_status else None,
            "event_attendance_mode": entity.event_attendance_mode.value if entity.event_attendance_mode else None,
            "location_id": entity.location.id if isinstance(entity.location, Place) else None,
            "organizer_id": entity.organizer.id if isinstance(entity.organizer, (Organization, Person)) else None,
        })
        return base
    
    def _from_row(self, row: Dict[str, Any]) -> Event:
        return Event(
            id=row["id"],
            name=row["name"],
            start_date=datetime.fromisoformat(row["start_date"]) if row.get("start_date") else None,
            end_date=datetime.fromisoformat(row["end_date"]) if row.get("end_date") else None,
            event_status=EventStatusType(row["event_status"]) if row.get("event_status") else None,
            event_attendance_mode=EventAttendanceMode(row["event_attendance_mode"]) if row.get("event_attendance_mode") else None,
        )
    
    def upcoming(self) -> List[Event]:
        """Get upcoming events."""
        now = datetime.now().isoformat()
        rows = self.db.fetch_all(
            self.table_name,
            {"start_date >": now}
        )
        return [self._from_row(r) for r in rows]


class RatingModel(Model[Rating]):
    """Model for Rating entities."""
    
    table_name = "ratings"
    
    def _to_row(self, entity: Rating) -> Dict[str, Any]:
        is_aggregate = isinstance(entity, AggregateRating)
        return {
            "id": entity.id,
            "rating_value": entity.rating_value,
            "best_rating": entity.best_rating,
            "worst_rating": entity.worst_rating,
            "rating_count": getattr(entity, "rating_count", None),
            "review_count": getattr(entity, "review_count", None),
            "type": "AggregateRating" if is_aggregate else "Rating",
        }
    
    def _from_row(self, row: Dict[str, Any]) -> Rating:
        if row.get("type") == "AggregateRating":
            return AggregateRating(
                id=row["id"],
                rating_value=row.get("rating_value"),
                best_rating=row.get("best_rating"),
                worst_rating=row.get("worst_rating"),
                rating_count=row.get("rating_count"),
                review_count=row.get("review_count"),
            )
        return Rating(
            id=row["id"],
            rating_value=row.get("rating_value"),
            best_rating=row.get("best_rating"),
            worst_rating=row.get("worst_rating"),
        )


# =============================================================================
# SESSION - Database session
# =============================================================================

class Session:
    """Database session for Schema.org entities."""
    
    def __init__(self, db_path: str = "schema_org.db"):
        self.db = Database(db_path)
        self.things = ThingModel(self.db)
        self.persons = PersonModel(self.db)
        self.organizations = OrganizationModel(self.db)
        self.products = ProductModel(self.db)
        self.offers = OfferModel(self.db)
        self.places = PlaceModel(self.db)
        self.events = EventModel(self.db)
        self.ratings = RatingModel(self.db)
    
    def save(self, entity: Thing) -> Thing:
        """Save any Schema.org entity."""
        if isinstance(entity, Person):
            return self.persons.save(entity)
        elif isinstance(entity, Organization):
            return self.organizations.save(entity)
        elif isinstance(entity, Product):
            return self.products.save(entity)
        elif isinstance(entity, Offer):
            return self.offers.save(entity)
        elif isinstance(entity, Place):
            return self.places.save(entity)
        elif isinstance(entity, Event):
            return self.events.save(entity)
        elif isinstance(entity, Rating):
            return self.ratings.save(entity)
        return self.things.save(entity)
    
    def get(self, id: str) -> Optional[Thing]:
        """Get entity by ID."""
        # Try to find entity type
        row = self.db.fetch_one("things", {"id": id})
        if not row:
            return None
        
        # Return appropriate model
        model_map = {
            "Person": self.persons,
            "Organization": self.organizations,
            "Product": self.products,
            "Offer": self.offers,
            "Place": self.places,
            "Event": self.events,
        }
        
        model = model_map.get(row["type"])
        if model:
            return model.get(id)
        return self.things.get(id)
    
    def delete(self, id: str) -> bool:
        """Delete entity by ID."""
        return self.things.delete(id)
    
    def query(self, sql: str, **params) -> List[Dict[str, Any]]:
        """Execute raw SQL query."""
        return self.db.execute(sql, tuple(params.values()))
    
    def close(self):
        """Close session."""
        self.db.close()


# =============================================================================
# MIGRATIONS - Database migrations
# =============================================================================

class Migration:
    """Database migration manager."""
    
    def __init__(self, db: Database):
        self.db = db
        self._create_version_table()
    
    def _create_version_table(self):
        """Create version tracking table."""
        self.db.conn.execute("""
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY,
                applied_at TEXT,
                description TEXT
            )
        """)
        self.db.conn.commit()
    
    def current_version(self) -> int:
        """Get current schema version."""
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT MAX(version) as v FROM schema_version")
        row = cursor.fetchone()
        return row[0] if row[0] else 0
    
    def apply(self, version: int, sql: str, description: str):
        """Apply a migration."""
        cursor = self.db.conn.cursor()
        cursor.execute(sql)
        
        # Record version
        cursor.execute(
            "INSERT INTO schema_version VALUES (?, ?, ?)",
            (version, datetime.now().isoformat(), description)
        )
        self.db.conn.commit()
    
    def migrate(self):
        """Apply all pending migrations."""
        current = self.current_version()
        
        migrations = [
            (1, "CREATE INDEX IF NOT EXISTS idx_things_type ON things(type)", "Add type index"),
            (2, "CREATE INDEX IF NOT EXISTS idx_products_sku ON products(sku)", "Add SKU index"),
            (3, "CREATE INDEX IF NOT EXISTS idx_events_start ON events(start_date)", "Add event date index"),
        ]
        
        for version, sql, description in migrations:
            if version > current:
                self.apply(version, sql, description)
                print(f"Applied migration {version}: {description}")


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

def main():
    """Example usage of ORM."""
    
    # Create session
    session = Session("schema_org.db")
    
    # Create organization
    acme = Organization(
        id="https://example.com/orgs/acme",
        name="Acme Corp",
        legal_name="Acme Corporation",
        email="contact@acme.com",
    )
    session.save(acme)
    
    # Create product
    widget = Product(
        id="https://example.com/products/widget",
        name="Super Widget",
        sku="SW-001",
        manufacturer=acme,
    )
    session.save(widget)
    
    # Create offer
    offer = Offer(
        id="https://example.com/offers/widget",
        price=99.99,
        price_currency="USD",
        item_offered=widget,
        seller=acme,
        availability=ItemAvailability.IN_STOCK,
    )
    session.save(offer)
    
    # Create person
    john = Person(
        id="https://example.com/people/john",
        name="John Doe",
        given_name="John",
        family_name="Doe",
        email="john@acme.com",
        job_title="Engineer",
    )
    session.save(john)
    
    # Query
    print("=== Queries ===")
    
    products = session.products.all()
    print(f"Products: {len(products)}")
    
    widget_found = session.products.get("https://example.com/products/widget")
    print(f"Found widget: {widget_found.name}")
    
    # Search
    row = session.db.fetch_one("products", {"sku": "SW-001"})
    print(f"By SKU: {row}")
    
    # Upcoming events
    print("\n=== Events ===")
    # session.events.upcoming()
    
    # Run migrations
    print("\n=== Migrations ===")
    migration = Migration(session.db)
    migration.migrate()
    print(f"Current version: {migration.current_version()}")
    
    # Close
    session.close()
    print("\nDone!")


if __name__ == "__main__":
    main()


"""
Schema.org Database ORM

Usage:
    # Create session
    session = Session("schema_org.db")
    
    # Save entities
    session.save(organization)
    session.save(product)
    session.save(person)
    
    # Query
    product = session.products.get(id)
    products = session.products.all()
    
    # Filter
    cheap_products = session.products.filter(price__lt=50)
    
    # Delete
    session.delete(id)
    
    # Raw SQL
    results = session.query("SELECT * FROM products WHERE sku = ?", sku="SW-001")

Models:
    - ThingModel: Base model
    - PersonModel: Person entities
    - OrganizationModel: Organization entities
    - ProductModel: Product entities
    - OfferModel: Offer entities
    - PlaceModel: Place entities
    - EventModel: Event entities
    - RatingModel: Rating entities
"""
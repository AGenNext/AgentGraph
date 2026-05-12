"""
Schema.org Time Search

Time-based search and filtering for Schema.org entities.
Includes metadata for search optimization and analytics.

Reference: https://schema.org/docs/full.html
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime, date, timedelta
from enum import Enum
import re
import json


# Search Metadata
@dataclass
class SearchMetadata:
    """Metadata for search queries"""
    
    # Query info
    query_id: str = ""
    query_name: str = ""
    table: str = ""
    
    # Time info
    created_at: datetime = field(default_factory=datetime.now)
    executed_at: Optional[datetime] = None
    duration_ms: float = 0.0
    
    # Results info
    results_count: int = 0
    results_page: int = 1
    results_per_page: int = 100
    
    # Filters
    time_property: str = ""
    operator: str = ""
    value: Any = None
    
    # Performance
    cached: bool = False
    cache_ttl: int = 0
    index_used: Optional[str] = None
    
    # Context
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "query_id": self.query_id,
            "query_name": self.query_name,
            "table": self.table,
            "created_at": self.created_at.isoformat(),
            "executed_at": self.executed_at.isoformat() if self.executed_at else None,
            "duration_ms": self.duration_ms,
            "results_count": self.results_count,
            "results_page": self.results_page,
            "results_per_page": self.results_per_page,
            "time_property": self.time_property,
            "operator": self.operator,
            "cached": self.cached,
            "cache_ttl": self.cache_ttl,
            "index_used": self.index_used,
        }


# Search Metadata Storage
SEARCH_METADATA: List[SearchMetadata] = []


# Time Search Operators
class TimeOperator(Enum):
    EQUALS = "="
    NOT_EQUALS = "!="
    BEFORE = "<"
    AFTER = ">"
    ON_OR_BEFORE = "<="
    ON_OR_AFTER = ">="
    BETWEEN = "BETWEEN"
    DURING = "DURING"
    WITHIN = "WITHIN"


# Schema.org Date/Time Properties
TIME_PROPERTIES = {
    # Thing
    "Thing": ["dateCreated", "dateModified", "datePublished", "dateIssued"],
    
    # Person
    "Person": ["birthDate", "deathDate"],
    
    # Organization  
    "Organization": ["foundingDate", "dissolutionDate"],
    
    # Event
    "Event": ["startDate", "endDate", "eventDate", "doorTime", "doorsStartDate"],
    
    # Action
    "Action": ["startTime", "endTime", "executionTime"],
    
    # CreativeWork
    "CreativeWork": ["dateCreated", "dateModified", "datePublished", "dateCreated"],
    
    # Product
    "Product": ["dateValidFrom", "dateValidUntil", "purchaseDate"],
    
    # JobPosting
    "JobPosting": ["datePosted", "validThrough", "expiresDate"],
    
    # Order
    "Order": ["orderDate", "deliveryDate", "orderStatus"],
    
    # Offer
    "Offer": ["validFrom", "validThrough", "priceValidUntil"],
    
    # QuantitativeValue
    "QuantitativeValue": ["maxValue", "minValue"],
}


# Search Templates
TIME_SEARCH_TEMPLATES = {
    # All events in a date range
    "EVENTS_IN_RANGE": """
        SELECT * FROM events 
        WHERE startDate >= $start_date 
        AND startDate <= $end_date
        ORDER BY startDate ASC;
    """,
    
    # Upcoming events
    "UPCOMING_EVENTS": """
        SELECT * FROM events 
        WHERE startDate > $now
        ORDER BY startDate ASC
        LIMIT $limit;
    """,
    
    # Past events
    "PAST_EVENTS": """
        SELECT * FROM events 
        WHERE endDate < $now
        ORDER BY endDate DESC
        LIMIT $limit;
    """,
    
    # Products on sale (date valid)
    "PRODUCTS_ON_SALE": """
        SELECT * FROM products 
        WHERE dateValidFrom <= $now
        AND dateValidUntil >= $now;
    """,
    
    # Recent items
    "RECENTLY_CREATED": """
        SELECT * FROM $table 
        ORDER BY dateCreated DESC
        LIMIT $limit;
    """,
    
    # Recently modified
    "RECENTLY_MODIFIED": """
        SELECT * FROM $table 
        ORDER BY dateModified DESC
        LIMIT $limit;
    """,
    
    # Expiring soon
    "EXPIRING_SOON": """
        SELECT * FROM $table 
        WHERE expiresDate BETWEEN $now AND $future
        ORDER BY expiresDate ASC;
    """,
    
    # Person born in year
    "PERSON_BORN_IN_YEAR": """
        SELECT * FROM persons 
        WHERE birthDate >= $year_start 
        AND birthDate < $year_end;
    """,
    
    # Founded in date range
    "ORG_FOUNDED_IN_RANGE": """
        SELECT * FROM organizations 
        WHERE foundingDate >= $start_date 
        AND foundingDate <= $end_date;
    """,
    
    # Created between dates
    "CREATED_BETWEEN": """
        SELECT * FROM $table 
        WHERE dateCreated >= $start 
        AND dateCreated <= $end;
    """,
    
    # Live queries for time
    "LIVE_UPCOMING": """
        LIVE SELECT * FROM events 
        WHERE startDate > $now
        ORDER BY startDate ASC;
    """,
}


# Time Range Presets
TIME_RANGES = {
    "today": {
        "start": lambda: datetime.now().replace(hour=0, minute=0, second=0),
        "end": lambda: datetime.now().replace(hour=23, minute=59, second=59),
    },
    "this_week": {
        "start": lambda: datetime.now() - timedelta(days=datetime.now().weekday()),
        "end": lambda: datetime.now() + timedelta(days=7),
    },
    "this_month": {
        "start": lambda: datetime.now().replace(day=1),
        "end": lambda: datetime.now().replace(day=31),
    },
    "this_quarter": {
        "start": lambda: datetime.now().replace(month=((datetime.now().month-1)//3)*3+1, day=1),
        "end": lambda: datetime.now().replace(month=((datetime.now().month-1)//3)*3+4, day=1),
    },
    "this_year": {
        "start": lambda: datetime.now().replace(month=1, day=1),
        "end": lambda: datetime.now().replace(month=12, day=31),
    },
    "last_7_days": {
        "start": lambda: datetime.now() - timedelta(days=7),
        "end": lambda: datetime.now(),
    },
    "last_30_days": {
        "start": lambda: datetime.now() - timedelta(days=30),
        "end": lambda: datetime.now(),
    },
    "last_90_days": {
        "start": lambda: datetime.now() - timedelta(days=90),
        "end": lambda: datetime.now(),
    },
    "next_7_days": {
        "start": lambda: datetime.now(),
        "end": lambda: datetime.now() + timedelta(days=7),
    },
    "next_30_days": {
        "start": lambda: datetime.now(),
        "end": lambda: datetime.now() + timedelta(days=30),
    },
    "next_90_days": {
        "start": lambda: datetime.now(),
        "end": lambda: datetime.now() + timedelta(days=90),
    },
}


# Time Search Functions
def parse_date(date_str: str) -> Optional[datetime]:
    """Parse various date formats"""
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%m/%d/%Y",
        "%d/%m/%Y",
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    # Try natural language
    natural = {
        "today": datetime.now(),
        "yesterday": datetime.now() - timedelta(days=1),
        "tomorrow": datetime.now() + timedelta(days=1),
        "now": datetime.now(),
    }
    
    if date_str.lower() in natural:
        return natural[date_str.lower()]
    
    return None


def build_time_filter(
    property: str,
    operator: TimeOperator,
    value: Any
) -> str:
    """Build SurrealDB time filter"""
    
    if isinstance(value, str):
        parsed = parse_date(value)
        if parsed:
            value = parsed.isoformat()
        else:
            value = f'"{value}"'
    elif isinstance(value, datetime):
        value = value.isoformat()
    elif isinstance(value, date):
        value = datetime.combine(value, datetime.min.time()).isoformat()
    
    op_map = {
        TimeOperator.EQUALS: "=",
        TimeOperator.NOT_EQUALS: "!=",
        TimeOperator.BEFORE: "<",
        TimeOperator.AFTER: ">",
        TimeOperator.ON_OR_BEFORE: "<=",
        TimeOperator.ON_OR_AFTER: ">=",
    }
    
    return f"{property} {op_map[operator]} {value}"


def time_search(
    table: str,
    property: str,
    operator: TimeOperator,
    value: Any,
    limit: int = 100
) -> str:
    """Generate time-based search query"""
    
    filter_clause = build_time_filter(property, operator, value)
    
    return f"""
        SELECT * FROM {table} 
        WHERE {filter_clause}
        ORDER BY {property} DESC
        LIMIT {limit};
    """.strip()


def build_range_filter(
    start_property: str,
    end_property: str,
    start_date: Any,
    end_date: Any
) -> str:
    """Build date range filter"""
    
    start = parse_date(start_date) if isinstance(start_date, str) else start_date
    end = parse_date(end_date) if isinstance(end_date, str) else end_date
    
    if start and end:
        start_str = start.isoformat()
        end_str = end.isoformat()
        
        return f"""
            {start_property} <= {end_str} 
            AND {end_property} >= {start_str}
        """
    
    return ""


@dataclass
class TimeSearch:
    """Time-based search for Schema.org"""
    
    def search(
        self,
        table: str,
        time_property: str,
        operator: TimeOperator,
        value: Any,
        limit: int = 100
    ) -> str:
        """Execute time search"""
        return time_search(table, time_property, operator, value, limit)
    
    def upcoming(self, table: str, limit: int = 10) -> str:
        """Get upcoming items"""
        now = datetime.now().isoformat()
        return f"""
            SELECT * FROM {table}
            WHERE startDate > {now}
            ORDER BY startDate ASC
            LIMIT {limit};
        """.strip()
    
    def expired(self, table: str, limit: int = 10) -> str:
        """Get expired items"""
        now = datetime.now().isoformat()
        return f"""
            SELECT * FROM {table}
            WHERE endDate < {now}
            ORDER BY endDate DESC
            LIMIT {limit};
        """.strip()
    
    def in_range(
        self,
        table: str,
        start_property: str,
        start_date: str,
        end_date: str,
        limit: int = 100
    ) -> str:
        """Items in date range"""
        start = parse_date(start_date)
        end = parse_date(end_date)
        
        if start and end:
            return f"""
                SELECT * FROM {table}
                WHERE {start_property} >= {start.isoformat()}
                AND {start_property} <= {end.isoformat()}
                ORDER BY {start_property} ASC
                LIMIT {limit};
            """.strip()
        
        return ""


def main():
    ts = TimeSearch()
    
    print("=== Schema.org Time Search ===")
    
    # Time properties
    print("\n--- Time Properties ---")
    for schema_type, props in TIME_PROPERTIES.items():
        print(f"{schema_type}: {props}")
    
    # Time ranges
    print("\n--- Time Ranges ---")
    for name in list(TIME_RANGES.keys())[:5]:
        print(f"  - {name}")
    
    # Example searches
    print("\n--- Example Searches ---")
    print(ts.search("events", "startDate", TimeOperator.AFTER, "2024-01-01"))
    print("\n" + ts.upcoming("events", 5))
    print("\n" + ts.in_range("events", "startDate", "2024-01-01", "2024-12-31"))


if __name__ == "__main__":
    main()

"""
Time Search Complete:
- Time operators: =, !=, <, >, <=, >=, BETWEEN
- Time properties mapped to Schema.org types
- Preset time ranges: today, this_week, etc.
- SurrealDB query generation

Reference: 
- https://schema.org/docs/full.html
- https://surrealdb.com/docs/surrealql/queries
"""
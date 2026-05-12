"""
Relational Database Schema

Relational database structure with:
- Tables, Columns, Keys
- Foreign Keys, Joins
- Indexes, Constraints
- MySQL/PostgreSQL compatible

Reference:
- SQL Standard
- MySQL: https://dev.mysql.com/doc/
- PostgreSQL: https://www.postgresql.org/docs/
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from base_entity import Entity


# =============================================================================
# SQL TYPES
# =============================================================================

class DataType(Enum):
    """SQL data types"""
    # Strings
    VARCHAR = "VARCHAR"
    CHAR = "CHAR"
    TEXT = "TEXT"
    MEDIUMTEXT = "MEDIUMTEXT"
    LONGTEXT = "LONGTEXT"
    
    # Integers
    TINYINT = "TINYINT"
    SMALLINT = "SMALLINT"
    INT = "INT"
    BIGINT = "BIGINT"
    
    # Decimals
    DECIMAL = "DECIMAL"
    FLOAT = "FLOAT"
    DOUBLE = "DOUBLE"
    
    # Date/Time
    DATE = "DATE"
    DATETIME = "DATETIME"
    TIME = "TIME"
    TIMESTAMP = "TIMESTAMP"
    
    # Boolean
    BOOLEAN = "BOOLEAN"
    BOOL = "BOOL"
    
    # Binary
    BLOB = "BLOB"
    BINARY = "BINARY"
    
    # JSON
    JSON = "JSON"
    JSONB = "JSONB"
    
    # UUID
    UUID = "UUID"


class KeyType(Enum):
    """Key types"""
    PRIMARY = "PRIMARY KEY"
    FOREIGN = "FOREIGN KEY"
    UNIQUE = "UNIQUE"
    INDEX = "INDEX"
    FULLTEXT = "FULLTEXT"


class JoinType(Enum):
    """JOIN types"""
    INNER = "INNER JOIN"
    LEFT = "LEFT JOIN"
    RIGHT = "RIGHT JOIN"
    FULL = "FULL OUTER JOIN"
    CROSS = "CROSS JOIN"


class ConstraintType(Enum):
    """Constraints"""
    NOT_NULL = "NOT NULL"
    UNIQUE = "UNIQUE"
    CHECK = "CHECK"
    DEFAULT = "DEFAULT"
    AUTO_INCREMENT = "AUTO_INCREMENT"
    PRIMARY = "PRIMARY KEY"


# =============================================================================
# RELATIONAL STRUCTURE
# =============================================================================

@dataclass
class Column:
    """Database column"""
    name: str
    data_type: DataType
    
    # Constraints
    not_null: bool = False
    unique: bool = False
    primary_key: bool = False
    
    # Length/Precision
    length: Optional[int] = None
    precision: Optional[int] = None
    scale: Optional[int] = None
    
    # Default
    default: Any = None
    
    # Specific
    auto_increment: bool = False
    comment: Optional[str] = None
    
    def sql_definition(self) -> str:
        """Get SQL column definition"""
        definition = f"{self.name} {self.data_type.value}"
        
        if self.length:
            definition += f"({self.length})"
        
        if self.primary_key:
            definition += " PRIMARY KEY"
        elif self.not_null:
            definition += " NOT NULL"
        
        if self.auto_increment:
            definition += " AUTO_INCREMENT"
        
        if self.default is not None:
            definition += f" DEFAULT {self.default}"
        
        if self.comment:
            definition += f" COMMENT '{self.comment}'"
        
        return definition


@dataclass
class Table:
    """Database table"""
    name: str
    
    columns: List[Column] = field(default_factory=list)
    
    primary_key: List[str] = field(default_factory=list)
    
    indexes: List[Dict] = field(default_factory=list)  # {name, columns, type}
    
    foreign_keys: List[Dict] = field(default_factory=list)  # {column, references, on_delete}
    
    comment: Optional[str] = None
    
    engine: str = "InnoDB"  # MySQL
    charset: str = "utf8mb4"
    
    def add_column(self, column: Column):
        self.columns.append(column)
        
        if column.primary_key:
            self.primary_key.append(column.name)
    
    def add_index(self, name: str, columns: List[str], unique: bool = False):
        self.indexes.append({
            "name": name,
            "columns": columns,
            "unique": unique
        })
    
    def add_foreign_key(
        self,
        column: str,
        references: str,  # table.column
        on_delete: str = "CASCADE",
        on_update: str = "CASCADE"
    ):
        self.foreign_keys.append({
            "column": column,
            "references": references,
            "on_delete": on_delete,
            "on_update": on_update
        })
    
    def sql_create(self) -> str:
        """Generate CREATE TABLE SQL"""
        lines = [f"CREATE TABLE {self.name} ("]
        
        # Columns
        for col in self.columns:
            lines.append(f"  {col.sql_definition()},")
        
        # Primary key
        if self.primary_key:
            lines.append(f"  PRIMARY KEY ({', '.join(self.primary_key)}),")
        
        # Foreign keys
        for fk in self.foreign_keys:
            lines.append(
                f"  FOREIGN KEY ({fk['column']}) REFERENCES {fk['references']} "
                f"ON DELETE {fk['on_delete']} ON UPDATE {fk['on_update']},"
            )
        
        #Indexes
        for idx in self.indexes:
            unique = "UNIQUE " if idx["unique"] else ""
            lines.append(
                f"  {unique}INDEX {idx['name']} ({', '.join(idx['columns'])}),"
            )
        
        # Remove last comma
        lines[-1] = lines[-1].rstrip(',')
        
        lines.append(")")
        
        # Table options
        lines.append(f"ENGINE={self.engine}")
        lines.append(f"DEFAULT CHARSET={self.charset}")
        
        if self.comment:
            lines.append(f"COMMENT='{self.comment}'")
        
        return " ".join(lines) + ";"


# =============================================================================
# RELATIONSHIPS
# =============================================================================

@dataclass
class Relationship:
    """Table relationship"""
    name: str
    
    from_table: str
    from_column: str
    
    to_table: str
    to_column: str
    
    join_type: JoinType = JoinType.INNER
    
    on_condition: Optional[str] = None
    
    def sql_join(self) -> str:
        """Generate JOIN SQL"""
        return f"{self.join_type.value} {self.to_table} ON {self.from_table}.{self.from_column} = {self.to_table}.{self.to_column}"


@dataclass
class View:
    """Database view"""
    name: str
    
    query: str
    
    columns: List[str] = field(default_factory=list)
    
    def sql_create(self) -> str:
        return f"CREATE VIEW {self.name} AS {self.query};"


@dataclass
class StoredProcedure:
    """Stored procedure"""
    name: str
    
    parameters: List[Dict] = field(default_factory=list)  # {name, type, mode}
    
    body: str
    
    def sql_create(self) -> str:
        params = ", ".join([f"{p['name']} {p['type']}" for p in self.parameters])
        return f"CREATE PROCEDURE {self.name}({params}) BEGIN {self.body} END;"


@dataclass
class Trigger:
    """Database trigger"""
    name: str
    
    table: str
    
    timing: str  # BEFORE, AFTER
    event: str  # INSERT, UPDATE, DELETE
    
    body: str
    
    def sql_create(self) -> str:
        return f"CREATE TRIGGER {self.name} {timing} {event} ON {table} FOR EACH ROW BEGIN {self.body} END;"


# =============================================================================
# SCHEMA MAPPING
# =============================================================================

def movie_schema() -> List[Table]:
    """Create movie database schema"""
    tables = []
    
    # actors table
    actors = Table(name="actors")
    actors.add_column(Column("id", DataType.INT, primary_key=True, auto_increment=True))
    actors.add_column(Column("name", DataType.VARCHAR, length=255))
    actors.add_column(Column("birth_date", DataType.DATE))
    actors.add_column(Column("bio", DataType.TEXT))
    actors.add_column(Column("created_at", DataType.DATETIME, default="CURRENT_TIMESTAMP"))
    tables.append(actors)
    
    # movies table
    movies = Table(name="movies")
    movies.add_column(Column("id", DataType.INT, primary_key=True, auto_increment=True))
    movies.add_column(Column("title", DataType.VARCHAR, length=255))
    movies.add_column(Column("release_date", DataType.DATE))
    movies.add_column(Column("runtime", DataType.INT))
    movies.add_column(Column("description", DataType.TEXT))
    movies.add_column(Column("rating", DataType.DECIMAL, precision=3, scale=2))
    movies.add_column(Column("created_at", DataType.DATETIME, default="CURRENT_TIMESTAMP"))
    tables.append(movies)
    
    # movie_actors (junction)
    movie_actors = Table(name="movie_actors")
    movie_actors.add_column(Column("movie_id", DataType.INT))
    movie_actors.add_column(Column("actor_id", DataType.INT))
    movie_actors.add_column(Column("role", DataType.VARCHAR, length=255))
    movie_actors.add_foreign_key("actor_id", "actors.id")
    movie_actors.add_foreign_key("movie_id", "movies.id")
    tables.append(movie_actors)
    
    # reviews table
    reviews = Table(name="reviews")
    reviews.add_column(Column("id", DataType.INT, primary_key=True, auto_increment=True))
    reviews.add_column(Column("movie_id", DataType.INT))
    reviews.add_column(Column("user_id", DataType.INT))
    reviews.add_column(Column("rating", DataType.DECIMAL, precision=3, scale=2))
    reviews.add_column(Column("comment", DataType.TEXT))
    reviews.add_column(Column("created_at", DataType.DATETIME, default="CURRENT_TIMESTAMP"))
    reviews.add_foreign_key("movie_id", "movies.id")
    tables.append(reviews)
    
    return tables


def healthcare_schema() -> List[Table]:
    """Create healthcare schema"""
    tables = []
    
    # patients
    patients = Table(name="patients")
    patients.add_column(Column("id", DataType.INT, primary_key=True, auto_increment=True))
    patients.add_column(Column("name", DataType.VARCHAR, length=255))
    patients.add_column(Column("email", DataType.VARCHAR, length=255))
    patients.add_column(Column("phone", DataType.VARCHAR, length=20))
    patients.add_column(Column("dob", DataType.DATE))
    patients.add_column(Column("address", DataType.TEXT))
    tables.append(patients)
    
    # physicians
    physicians = Table(name="physicians")
    physicians.add_column(Column("id", DataType.INT, primary_key=True, auto_increment=True))
    physicians.add_column(Column("name", DataType.VARCHAR, length=255))
    physicians.add_column(Column("specialty", DataType.VARCHAR, length=100))
    physicians.add_column(Column("license", DataType.VARCHAR, length=50))
    physicians.add_column(Column("hospital_id", DataType.INT))
    tables.append(physicians)
    
    # appointments
    appointments = Table(name="appointments")
    appointments.add_column(Column("id", DataType.INT, primary_key=True, auto_increment=True))
    appointments.add_column(Column("patient_id", DataType.INT))
    appointments.add_column(Column("physician_id", DataType.INT))
    appointments.add_column(Column("scheduled_time", DataType.DATETIME))
    appointments.add_column(Column("status", DataType.VARCHAR, length=20))
    appointments.add_foreign_key("patient_id", "patients.id")
    appointments.add_foreign_key("physician_id", "physicians.id")
    tables.append(appointments)
    
    return tables


def ecommerce_schema() -> List[Table]:
    """Create e-commerce schema"""
    tables = []
    
    # users
    users = Table(name="users")
    users.add_column(Column("id", DataType.INT, primary_key=True, auto_increment=True))
    users.add_column(Column("email", DataType.VARCHAR, length=255, unique=True))
    users.add_column(Column("password_hash", DataType.VARCHAR, length=255))
    users.add_column(Column("name", DataType.VARCHAR, length=255))
    users.add_column(Column("created_at", DataType.DATETIME, default="CURRENT_TIMESTAMP"))
    tables.append(users)
    
    # products
    products = Table(name="products")
    products.add_column(Column("id", DataType.INT, primary_key=True, auto_increment=True))
    products.add_column(Column("name", DataType.VARCHAR, length=255))
    products.add_column(Column("description", DataType.TEXT))
    products.add_column(Column("price", DataType.DECIMAL, precision=10, scale=2))
    products.add_column(Column("category", DataType.VARCHAR, length=100))
    products.add_column(Column("stock", DataType.INT))
    tables.append(products)
    
    # orders
    orders = Table(name="orders")
    orders.add_column(Column("id", DataType.INT, primary_key=True, auto_increment=True))
    orders.add_column(Column("user_id", DataType.INT))
    orders.add_column(Column("total", DataType.DECIMAL, precision=10, scale=2))
    orders.add_column(Column("status", DataType.VARCHAR, length=20))
    orders.add_column(Column("created_at", DataType.DATETIME, default="CURRENT_TIMESTAMP"))
    orders.add_foreign_key("user_id", "users.id")
    tables.append(orders)
    
    # order_items
    order_items = Table(name="order_items")
    order_items.add_column(Column("id", DataType.INT, primary_key=True, auto_increment=True))
    order_items.add_column(Column("order_id", DataType.INT))
    order_items.add_column(Column("product_id", DataType.INT))
    order_items.add_column(Column("quantity", DataType.INT))
    order_items.add_column(Column("price", DataType.DECIMAL, precision=10, scale=2))
    order_items.add_foreign_key("order_id", "orders.id")
    order_items.add_foreign_key("product_id", "products.id")
    tables.append(order_items)
    
    return tables


# =============================================================================
# DATABASE
# =============================================================================

class RelationalDatabase:
    """Complete relational database"""
    
    def __init__(self, name: str):
        self.name = name
        self.tables: Dict[str, Table] = {}
        self.views: Dict[str, View] = {}
        self.procedures: Dict[str, StoredProcedure] = {}
        self.triggers: Dict[str, Trigger] = {}
    
    def add_table(self, table: Table):
        self.tables[table.name] = table
    
    def get_table(self, name: str) -> Optional[Table]:
        return self.tables.get(name)
    
    def create_schema(self, schema_func) -> List[str]:
        """Create schema from function"""
        tables = schema_func()
        for table in tables:
            self.add_table(table)
        return [t.sql_create() for t in tables]
    
    def sql_dump(self) -> List[str]:
        """Generate complete SQL dump"""
        sql = []
        
        for table in self.tables.values():
            sql.append(table.sql_create())
            sql.append("")  # blank line
        
        return sql


# =============================================================================
# USAGE
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("Relational Database Schema")
    print("=" * 50)
    
    # Create database
    db = RelationalDatabase("movie_db")
    
    # Create tables
    db.create_schema(movie_schema)
    
    # Print SQL
    for sql in db.sql_dump():
        print(sql)
        print()


if __name__ == "__main__":
    main()


"""
Relational Database Usage

    # Create database
    db = RelationalDatabase("mydb")
    
    # Create schema
    db.create_schema(movie_schema)
    db.create_schema(healthcare_schema)
    db.create_schema(ecommerce_schema)
    
    # Get SQL
    for sql in db.sql_dump():
        print(sql)
    
    # Individual tables
    movies = db.get_table("movies")
    print(movies.sql_create())

Tables created:
- actors, movies, movie_actors, reviews (movie)
- patients, physicians, appointments (healthcare) 
- users, products, orders, order_items (ecommerce)
"""
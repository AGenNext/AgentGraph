"""
Retail Product Database - E-commerce

Retail database:
- Products, Categories
- Inventory, Pricing
- Orders, Customers
- Suppliers

Reference:
- Amazon/Walmart style
- POS systems
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum
from base_entity import Entity


# =============================================================================
# TYPES
# =============================================================================

class ProductCategory(Enum):
    Electronics = "Electronics"
    Clothing = "Clothing"
    Home_Garden = "Home & Garden"
    Sports_Outdoors = "Sports & Outdoors"
    Grocery = "Grocery"
    Beauty_Health = "Beauty & Health"
    Toys_Games = "Toys & Games"
    Books_Media = "Books & Media"
    Automotive = "Automotive"
    Office_Supplies = "Office Supplies"


class ProductCondition(Enum):
    New = "New"
    Open_Box = "Open Box"
    Certified_Refurbished = "Certified Refurbished"
    Used_Good = "Used - Good"
    Used_Acceptable = "Used - Acceptable"


class OrderStatus(Enum):
    Pending = "Pending"
    Processing = "Processing"
    Shipped = "Shipped"
    Delivered = "Delivered"
    Cancelled = "Cancelled"
    Returned = "Returned"


# =============================================================================
# ENTITIES
# =============================================================================

@dataclass
class Entity(Entity):
class Product:
    """Product"""
    id: str
    name: str
    
    category: ProductCategory = ProductCategory.Electronics
    
    sku: str = ""
    upc: str = ""
    
    description: str = ""
    
    brand: str = ""
    
    price: float = 0.0
    compare_at_price: float = 0.0  # Original price for comparison
    
    cost: float = 0.0  # Cost to seller
    
    condition: ProductCondition = ProductCondition.New
    
    weight_oz: float = 0.0
    
    dimensions: Dict[str, float] = field(default_factory=dict)  # L, W, H
    
    images: List[str] = field(default_factory=list)
    
    inventory: int = 0
    
    reserved: int = 0
    
    reorder_level: int = 0
    
    vendor: str = ""
    
    vendor_sku: str = ""
    
    tags: List[str] = field(default_factory=list)
    
    active: bool = True
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "inventory": self.inventory
        }
    
    def avg_cost(self) -> float:
        return self.price - self.cost
    
    def margin_percent(self) -> float:
        if self.price == 0:
            return 0
        return ((self.price - self.cost) / self.price) * 100
    
    def in_stock(self) -> bool:
        return self.inventory > 0


@dataclass
class Entity(Entity):
class Category:
    """Product category"""
    id: str
    name: str
    
    parent_id: str = ""
    
    description: str = ""
    
    image: str = ""
    
    product_count: int = 0
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "products": self.product_count
        }


@dataclass
class Entity(Entity):
class Customer:
    """Customer"""
    id: str
    name: str
    
    email: str = ""
    phone: str = ""
    
    billing_address: Dict[str, str] = field(default_factory=dict)
    shipping_address: Dict[str, str] = field(default_factory=dict)
    
    account_created: datetime = field(default_factory=datetime.now)
    
    total_orders: int = 0
    total_spent: float = 0.0
    
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "total_orders": self.total_orders
        }


@dataclass
class Entity(Entity):
class Order:
    """Order"""
    id: str
    customer_id: str
    
    items: List[Dict] = field(default_factory=list)  # {product_id, qty, price}
    
    subtotal: float = 0.0
    tax: float = 0.0
    shipping: float = 0.0
    discount: float = 0.0
    
    total: float = 0.0
    
    status: OrderStatus = OrderStatus.Pending
    
    shipping_address: Dict[str, str] = field(default_factory=dict)
    billing_address: Dict[str, str] = field(default_factory=dict)
    
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    
    tracking_number: str = ""
    
    notes: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "total": self.total,
            "status": self.status.value
        }


@dataclass
class Entity(Entity):
class Supplier:
    """Supplier/Vendor"""
    id: str
    name: str
    
    contact_name: str = ""
    email: str = ""
    phone: str = ""
    
    address: Dict[str, str] = field(default_factory=dict)
    
    lead_time_days: int = 0
    
    minimum_order: float = 0.0
    
    terms: str = ""  # Net 30, etc.
    
    product_count: int = 0


# =============================================================================
# DATABASE
# =============================================================================

class RetailDatabase:
    """Retail database"""
    
    def __init__(self):
        # Products
        self.products: Dict[str, Product] = {}
        self.categories: Dict[str, Category] = {}
        self.suppliers: Dict[str, Supplier] = {}
        
        # Customers & Orders
        self.customers: Dict[str, Customer] = {}
        self.orders: Dict[str, Order] = {}
        
        # Relationships
        self.products_by_category: Dict[str, List[str]] = {}
        self.products_by_brand: Dict[str, List[str]] = {}
        self.orders_by_customer: Dict[str, List[str]] = {}
    
    # Products
    def add_product(
        self,
        product: Product
    ) -> str:
        self.products[product.id] = product
        
        # Index by category
        cat = product.category.value
        if cat not in self.products_by_category:
            self.products_by_category[cat] = []
        self.products_by_category[cat].append(product.id)
        
        # Index by brand
        if product.brand:
            if product.brand not in self.products_by_brand:
                self.products_by_brand[product.brand] = []
            self.products_by_brand[product.brand].append(product.id)
        
        return product.id
    
    def get_product(self, product_id: str) -> Optional[Product]:
        return self.products.get(product_id)
    
    def search_products(
        self,
        query: str = None,
        category: ProductCategory = None,
        brand: str = None,
        in_stock: bool = None,
        min_price: float = None,
        max_price: float = None
    ) -> List[Product]:
        results = list(self.products.values())
        
        # Filter active
        results = [p for p in results if p.active]
        
        if query:
            q = query.lower()
            results = [
                p for p in results
                if q in p.name.lower() or q in p.description.lower()
            ]
        
        if category:
            results = [p for p in results if p.category == category]
        
        if brand:
            results = [p for p in results if p.brand == brand]
        
        if in_stock:
            results = [p for p in results if p.in_stock()]
        
        if min_price is not None:
            results = [p for p in results if p.price >= min_price]
        
        if max_price is not None:
            results = [p for p in results if p.price <= max_price]
        
        return results
    
    def get_products_by_category(
        self,
        category: ProductCategory
    ) -> List[Product]:
        product_ids = self.products_by_category.get(category.value, [])
        return [self.products[pid] for pid in product_ids if pid in self.products]
    
    def get_trending_products(self, limit: int = 10) -> List[Product]:
        return sorted(
            self.products.values(),
            key=lambda p: p.inventory,
            reverse=True
        )[:limit]
    
    def get_low_inventory(self) -> List[Product]:
        return [
            p for p in self.products.values()
            if p.inventory <= p.reorder_level
        ]
    
    # Categories
    def add_category(self, category: Category) -> str:
        self.categories[category.id] = category
        return category.id
    
    def get_category(self, category_id: str) -> Optional[Category]:
        return self.categories.get(category_id)
    
    # Customers
    def add_customer(self, customer: Customer) -> str:
        self.customers[customer.id] = customer
        return customer.id
    
    def get_customer(self, customer_id: str) -> Optional[Customer]:
        return self.customers.get(customer_id)
    
    def search_customers(self, query: str) -> List[Customer]:
        q = query.lower()
        return [
            c for c in self.customers.values()
            if q in c.name.lower() or q in c.email.lower()
        ]
    
    def get_top_customers(self, limit: int = 10) -> List[Customer]:
        return sorted(
            self.customers.values(),
            key=lambda c: c.total_spent,
            reverse=True
        )[:limit]
    
    # Orders
    def create_order(
        self,
        customer_id: str,
        items: List[Dict],
        shipping_address: Dict[str, str] = None
    ) -> Optional[Order]:
        customer = self.customers.get(customer_id)
        if not customer:
            return None
        
        # Calculate totals
        subtotal = sum(item["price"] * item["qty"] for item in items)
        tax = subtotal * 0.08  # 8% tax
        shipping = 9.99 if subtotal < 50 else 0
        total = subtotal + tax + shipping
        
        order = Order(
            id=f"order_{customer_id}_{datetime.now().timestamp()}",
            customer_id=customer_id,
            items=items,
            subtotal=subtotal,
            tax=tax,
            shipping=shipping,
            total=total,
            shipping_address=shipping_address or customer.shipping_address
        )
        
        self.orders[order.id] = order
        
        # Update customer stats
        customer.total_orders += 1
        customer.total_spent += total
        
        # Update inventory
        for item in items:
            product = self.products.get(item["product_id"])
            if product:
                product.inventory -= item["qty"]
        
        return order
    
    def get_order(self, order_id: str) -> Optional[Order]:
        return self.orders.get(order_id)
    
    def get_customer_orders(self, customer_id: str) -> List[Order]:
        return [
            o for o in self.orders.values()
            if o.customer_id == customer_id
        ]
    
    def update_order_status(
        self,
        order_id: str,
        status: OrderStatus
    ) -> bool:
        order = self.orders.get(order_id)
        if not order:
            return False
        
        order.status = status
        order.updated_at = datetime.now()
        
        if status == OrderStatus.Shipped:
            order.shipped_at = datetime.now()
        elif status == OrderStatus.Delivered:
            order.delivered_at = datetime.now()
        
        return True
    
    # Suppliers
    def add_supplier(self, supplier: Supplier) -> str:
        self.suppliers[supplier.id] = supplier
        return supplier.id
    
    def get_supplier(self, supplier_id: str) -> Optional[Supplier]:
        return self.suppliers.get(supplier_id)
    
    # Statistics
    def stats(self) -> Dict:
        total_inventory = sum(p.inventory for p in self.products.values())
        total_value = sum(p.inventory * p.cost for p in self.products.values())
        
        return {
            "total_products": len(self.products),
            "total_categories": len(self.categories),
            "total_customers": len(self.customers),
            "total_orders": len(self.orders),
            "total_inventory": total_inventory,
            "inventory_value": total_value,
            "low_inventory_count": len(self.get_low_inventory())
        }


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("Retail Database")
    print("=" * 50)
    
    db = RetailDatabase()
    
    # Add products
    products = [
        Product(
            id="p1", name="Wireless Headphones",
            category=ProductCategory.Electronics,
            brand="AudioTech",
            price=79.99, cost=40.00,
            inventory=100
        ),
        Product(
            id="p2", name="Running Shoes",
            category=ProductCategory.Clothing,
            brand="SpeedRun",
            price=129.99, cost=60.00,
            inventory=50
        ),
        Product(
            id="p3", name="Coffee Maker",
            category=ProductCategory.Home_Garden,
            brand="BrewMaster",
            price=89.99, cost=45.00,
            inventory=25
        ),
    ]
    
    for product in products:
        db.add_product(product)
    
    # Search
    print("\nSearch 'Wireless':")
    results = db.search_products("Wireless")
    for p in results:
        print(f"  {p.name}: ${p.price}")
    
    # Search electronics
    print("\nElectronics:")
    electronics = db.get_products_by_category(ProductCategory.Electronics)
    for p in electronics:
        print(f"  {p.name} ({p.brand})")
    
    # Add customer
    customer = Customer(
        id="c1",
        name="John Smith",
        email="john@example.com"
    )
    db.add_customer(customer)
    
    # Create order
    order = db.create_order(
        "c1",
        [{"product_id": "p1", "qty": 2, "price": 79.99}],
        {"street": "123 Main St"}
    )
    
    print(f"\nOrder created: ${order.total}")
    
    print(f"\nStats:")
    stats = db.stats()
    print(f"  Products: {stats['total_products']}")
    print(f"  Orders: {stats['total_orders']}")
    print(f"  Inventory value: ${stats['inventory_value']:.2f}")


if __name__ == "__main__":
    main()


"""
Retail Database Usage

    db = RetailDatabase()
    
    # Products
    product = db.add_product(Product(...))
    products = db.search_products("query", category=..., price_range=...)
    products = db.get_products_by_category(Category)
    low = db.get_low_inventory()
    
    # Orders
    order = db.create_order(customer_id, items)
    order = db.update_order_status(order_id, OrderStatus.Shipped)
    orders = db.get_customer_orders(customer_id)
    
    # Customers
    customer = db.add_customer(Customer(...))
    customers = db.get_top_customers()
    
    # Stats
    stats = db.stats()
"""
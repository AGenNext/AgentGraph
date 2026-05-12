"""
Food & Restaurant Database

Restaurant database:
- Restaurants, Menus
- Ingredients, Recipes
- Orders, Reviews
- Delivery

Reference:
- Yelp/DoorDash style
- Restaurant systems
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

class Cuisine(Enum):
    Italian = "Italian"
    Mexican = "Mexican"
    Chinese = "Chinese"
    Japanese = "Japanese"
    Indian = "Indian"
    Thai = "Thai"
    American = "American"
    French = "French"
    Mediterranean = "Mediterranean"
    Vietnamese = "Vietnamese"
    Korean = "Korean"
    Greek = "Greek"


class MealType(Enum):
    Breakfast = "Breakfast"
    Lunch = "Lunch"
    Dinner = "Dinner"
    Snacks = "Snacks"


class Dietary(Enum):
    Vegetarian = "Vegetarian"
    Vegan = "Vegan"
    Gluten_Free = "Gluten_Free"
    Dairy_Free = "Dairy_Free"
    Nut_Free = "Nut_Free"
    Keto = "Keto"
    Halal = "Halal"
    Kosher = "Kosher"


class OrderStatus(Enum):
    Received = "Received"
    Preparing = "Preparing"
    Ready = "Ready"
    On_The_Way = "On_The_Way"
    Delivered = "Delivered"
    Cancelled = "Cancelled"


# =============================================================================
# ENTITIES
# =============================================================================

@dataclass
class Entity(Entity):
class Restaurant:
    """Restaurant"""
    id: str
    name: str
    
    cuisine: Cuisine = Cuisine.American
    
    address: Dict[str, str] = field(default_factory=dict)
    
    phone: str = ""
    website: str = ""
    
    hours: Dict[str, str] = field(default_factory=dict)  # day -> hours
    
    price_range: str = "$$"  # $, $$, $$$, $$$$
    
    rating: float = 0.0
    review_count: int = 0
    
    delivery: bool = True
    pickup: bool = True
    reservations: bool = False
    
    dietary_options: List[Dietary] = field(default_factory=list)
    
    images: List[str] = field(default_factory=list)
    
    owner: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "cuisine": self.cuisine.value,
            "rating": self.rating
        }


@dataclass
class Entity(Entity):
class MenuItem:
    """Menu item"""
    id: str
    restaurant_id: str
    name: str
    
    description: str = ""
    
    price: float = 0.0
    
    category: str = ""  # Appetizer, Main, Dessert
    
    calories: int = 0
    
    dietary: List[Dietary] = field(default_factory=list)
    
    allergens: List[str] = field(default_factory=list)
    
    ingredients: List[str] = field(default_factory=list)
    
    available: bool = True
    
    image: str = ""
    
    prep_time_minutes: int = 15
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }


@dataclass
class Entity(Entity):
class Ingredient:
    """Ingredient"""
    id: str
    name: str
    
    category: str = ""  # Produce, Dairy, Meat
    
    unit: str = ""  # lb, oz, each
    
    cost_per_unit: float = 0.0
    
    supplier: str = ""
    
    in_stock: bool = True
    
    quantity: float = 0.0


@dataclass
class Entity(Entity):
class Recipe:
    """Recipe"""
    id: str
    menu_item_id: str
    
    steps: List[str] = field(default_factory=list)
    
    prep_time: int = 0  # minutes
    cook_time: int = 0
    
    servings: int = 1
    
    ingredients: List[Dict] = field(default_factory=list)  # {ingredient_id, quantity}


@dataclass
class Entity(Entity):
class Order:
    """Order"""
    id: str
    customer_id: str
    restaurant_id: str
    
    items: List[Dict] = field(default_factory=list)  # {menu_item_id, qty, price}
    
    subtotal: float = 0.0
    tax: float = 0.0
    delivery_fee: float = 0.0
    tip: float = 0.0
    total: float = 0.0
    
    status: OrderStatus = OrderStatus.Received
    
    delivery_address: Dict[str, str] = field(default_factory=dict)
    
    created_at: datetime = field(default_factory=datetime.now)
    
    estimated_delivery: datetime = None
    
    delivered_at: Optional[datetime] = None
    
    driver: str = ""
    
    notes: str = ""


@dataclass
class Entity(Entity):
class Review:
    """Review"""
    id: str
    restaurant_id: str
    customer_id: str
    
    rating: int = 5  # 1-5
    
    title: str = ""
    content: str = ""
    
    food_rating: int = 5
    service_rating: int = 5
    value_rating: int = 5
    
    created_at: datetime = field(default_factory=datetime.now)
    
    helpful: int = 0


@dataclass
class Entity(Entity):
class Driver:
    """Delivery driver"""
    id: str
    name: str
    
    phone: str = ""
    
    vehicle: str = ""  # Car, Bike, Scooter
    
    available: bool = True
    
    current_location: Dict[str, float] = field(default_factory=dict)  # lat, lng
    
    rating: float = 0.0
    
    total_deliveries: int = 0


# =============================================================================
# RESTAURANT DATABASE
# =============================================================================

class FoodDatabase:
    """Food & restaurant database"""
    
    def __init__(self):
        self.restaurants: Dict[str, Restaurant] = {}
        self.menu_items: Dict[str, MenuItem] = {}
        self.ingredients: Dict[str, Ingredient] = {}
        self.recipes: Dict[str, Recipe] = {}
        
        self.orders: Dict[str, Order] = {}
        self.reviews: Dict[str, Review] = {}
        self.drivers: Dict[str, Driver] = {}
        
        # Indexes
        self.menu_by_restaurant: Dict[str, List[str]] = {}
        self.orders_by_restaurant: Dict[str, List[str]] = {}
    
    # Restaurants
    def add_restaurant(self, restaurant: Restaurant) -> str:
        self.restaurants[restaurant.id] = restaurant
        return restaurant.id
    
    def get_restaurant(self, restaurant_id: str) -> Optional[Restaurant]:
        return self.restaurants.get(restaurant_id)
    
    def search_restaurants(
        self,
        query: str = None,
        cuisine: Cuisine = None,
        delivery: bool = None,
        min_rating: float = None,
        price_range: str = None
    ) -> List[Restaurant]:
        results = list(self.restaurants.values())
        
        if query:
            q = query.lower()
            results = [
                r for r in results
                if q in r.name.lower()
            ]
        
        if cuisine:
            results = [r for r in results if r.cuisine == cuisine]
        
        if delivery is not None:
            results = [r for r in results if r.delivery == delivery]
        
        if min_rating:
            results = [r for r in results if r.rating >= min_rating]
        
        if price_range:
            results = [r for r in results if r.price_range == price_range]
        
        return results
    
    def get_restaurants_by_cuisine(
        self,
        cuisine: Cuisine
    ) -> List[Restaurant]:
        return [
            r for r in self.restaurants.values()
            if r.cuisine == cuisine
        ]
    
    def get_trending(self, limit: int = 10) -> List[Restaurant]:
        return sorted(
            self.restaurants.values(),
            key=lambda r: r.review_count,
            reverse=True
        )[:limit]
    
    # Menu Items
    def add_menu_item(self, menu_item: MenuItem) -> str:
        self.menu_items[menu_item.id] = menu_item
        
        # Index
        if menu_item.restaurant_id not in self.menu_by_restaurant:
            self.menu_by_restaurant[menu_item.restaurant_id] = []
        self.menu_by_restaurant[menu_item.restaurant_id].append(menu_item.id)
        
        return menu_item.id
    
    def get_menu_item(self, item_id: str) -> Optional[MenuItem]:
        return self.menu_items.get(item_id)
    
    def get_restaurant_menu(
        self,
        restaurant_id: str,
        category: str = None
    ) -> List[MenuItem]:
        item_ids = self.menu_by_restaurant.get(restaurant_id, [])
        
        items = [
            self.menu_items[iid]
            for iid in item_ids
            if iid in self.menu_items
        ]
        
        if category:
            items = [i for i in items if i.category == category]
        
        return items
    
    def get_menu_item_count(self, restaurant_id: str) -> int:
        return len(self.menu_by_restaurant.get(restaurant_id, []))
    
    # Orders
    def create_order(
        self,
        customer_id: str,
        restaurant_id: str,
        items: List[Dict],
        delivery_address: Dict[str, str],
        tip: float = 0.0
    ) -> Optional[Order]:
        # Calculate totals
        subtotal = sum(item["price"] * item["qty"] for item in items)
        tax = subtotal * 0.0875  # 8.75% tax
        delivery_fee = 3.99
        total = subtotal + tax + delivery_fee + tip
        
        # Estimate delivery time
        now = datetime.now()
        estimated = datetime(
            now.year, now.month, now.day,
            now.hour + 30 // 60 + 1, (now.minute + 30) % 60
        )
        
        order = Order(
            id=f"order_{customer_id}_{now.timestamp()}",
            customer_id=customer_id,
            restaurant_id=restaurant_id,
            items=items,
            subtotal=subtotal,
            tax=tax,
            delivery_fee=delivery_fee,
            tip=tip,
            total=total,
            delivery_address=delivery_address,
            estimated_delivery=estimated
        )
        
        self.orders[order.id] = order
        
        # Index
        if restaurant_id not in self.orders_by_restaurant:
            self.orders_by_restaurant[restaurant_id] = []
        self.orders_by_restaurant[restaurant_id].append(order.id)
        
        return order
    
    def get_order(self, order_id: str) -> Optional[Order]:
        return self.orders.get(order_id)
    
    def update_order_status(
        self,
        order_id: str,
        status: OrderStatus
    ) -> bool:
        order = self.orders.get(order_id)
        if not order:
            return False
        
        order.status = status
        
        if status == OrderStatus.Delivered:
            order.delivered_at = datetime.now()
        
        return True
    
    def get_customer_orders(self, customer_id: str) -> List[Order]:
        return [
            o for o in self.orders.values()
            if o.customer_id == customer_id
        ]
    
    # Reviews
    def add_review(self, review: Review) -> str:
        self.reviews[review.id] = review
        
        # Update restaurant rating
        restaurant = self.restaurants.get(review.restaurant_id)
        if restaurant:
            restaurant.review_count += 1
        
        return review.id
    
    def get_restaurant_reviews(
        self,
        restaurant_id: str,
        limit: int = None
    ) -> List[Review]:
        reviews = [
            r for r in self.reviews.values()
            if r.restaurant_id == restaurant_id
        ]
        
        reviews.sort(key=lambda r: r.created_at, reverse=True)
        
        if limit:
            reviews = reviews[:limit]
        
        return reviews
    
    # Drivers
    def add_driver(self, driver: Driver) -> str:
        self.drivers[driver.id] = driver
        return driver.id
    
    def get_available_drivers(self) -> List[Driver]:
        return [
            d for d in self.drivers.values()
            if d.available
        ]
    
    # Statistics
    def stats(self) -> Dict:
        return {
            "total_restaurants": len(self.restaurants),
            "total_menu_items": len(self.menu_items),
            "total_orders": len(self.orders),
            "total_drivers": len(self.drivers),
            "active_orders": len([
                o for o in self.orders.values()
                if o.status not in [OrderStatus.Delivered, OrderStatus.Cancelled]
            ])
        }


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("Food & Restaurant Database")
    print("=" * 50)
    
    db = FoodDatabase()
    
    # Add restaurant
    restaurant = Restaurant(
        id="r1",
        name="Pasta Palace",
        cuisine=Cuisine.Italian,
        address={"street": "123 Main St", "city": "NYC"},
        price_range="$$",
        rating=4.5,
        delivery=True
    )
    db.add_restaurant(restaurant)
    
    print(f"\nRestaurant: {restaurant.name}")
    print(f"  Cuisine: {restaurant.cuisine.value}")
    print(f"  Rating: {restaurant.rating}")
    
    # Add menu items
    items = [
        MenuItem(id="m1", restaurant_id="r1", name="Margherita Pizza", price=16.99, category="Mains"),
        MenuItem(id="m2", restaurant_id="r1", name="Caesar Salad", price=10.99, category="Starters"),
        MenuItem(id="m3", restaurant_id="r1", name="Tiramisu", price=8.99, category="Dessert"),
    ]
    
    for item in items:
        db.add_menu_item(item)
    
    print(f"\nMenu items: {db.get_menu_item_count('r1')}")
    
    # Search
    print("\nSearch Italian:")
    results = db.search_restaurants(cuisine=Cuisine.Italian)
    for r in results:
        print(f"  {r.name}: {r.cuisine.value}")
    
    # Create order
    order = db.create_order(
        "customer1",
        "r1",
        [{"menu_item_id": "m1", "qty": 1, "price": 16.99}],
        {"street": "123 Main St"},
        tip=3.00
    )
    
    print(f"\nOrder: ${order.total:.2f}")
    print(f"  Status: {order.status.value}")
    
    print(f"\nStats:")
    stats = db.stats()
    print(f"  Restaurants: {stats['total_restaurants']}")
    print(f"  Orders: {stats['total_orders']}")


if __name__ == "__main__":
    main()


"""
Food Database Usage

    db = FoodDatabase()
    
    # Restaurants
    restaurant = db.add_restaurant(Restaurant(...))
    restaurants = db.search_restaurants(cuisine=Cuisine.Italian)
    restaurants = db.get_trending()
    
    # Menu
    item = db.add_menu_item(MenuItem(...))
    menu = db.get_restaurant_menu(restaurant_id)
    
    # Orders
    order = db.create_order(customer_id, restaurant_id, items, address)
    db.update_order_status(order_id, OrderStatus.Preparing)
    orders = db.get_customer_orders(customer_id)
    
    # Reviews
    db.add_review(Review(...))
    reviews = db.get_restaurant_reviews(restaurant_id)
    
    # Stats
    stats = db.stats()
"""
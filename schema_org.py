"""
Schema.org Python Dataclasses

Comprehensive Python dataclasses for Schema.org types.
Follows the official Schema.org vocabulary specification.

Source: https://schema.org/docs/schemas.html
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date, time, timedelta
from decimal import Decimal
from enum import Enum
from typing import (
    Optional,
    List,
    Union,
    Any,
    Dict,
    Set,
)
from typing_extensions import TypeAlias

# =============================================================================
# ENUMERATIONS
# =============================================================================

class OfferItemCondition(Enum):
    """A predefined value for a product being new, used, refurbished, etc."""
    NEW = "NewCondition"
    REFURBISHED = "RefurbishedCondition"
    USED = "UsedCondition"
    DAMAGED = "DamagedCondition"
    DISCONTINUED = "DiscontinuedCondition"


class ItemAvailability(Enum):
    """A product's availability."""
    IN_STOCK = "InStock"
    IN_STORE_ONLY = "InStoreOnly"
    ONLINE_ONLY = "OnlineOnly"
    OUT_OF_STOCK = "OutOfStock"
    PRE_ORDER = "PreOrder"
    BACK_ORDER = "BackOrder"
    DISCONTINUED = "Discontinued"
    LIMITED_AVAILABILITY = "LimitedAvailability"
    SOLD_OUT = "SoldOut"


class EventStatusType(Enum):
    """An event's status."""
    EVENT_SCHEDULED = "EventScheduled"
    EVENT_CANCELLED = "EventCancelled"
    EVENT_MOVED_ONLINE = "EventMovedOnline"
    EVENT_POSTPONED = "EventPostponed"
    EVENT_RESCHEDULED = "EventRescheduled"


class EventAttendanceMode(Enum):
    """The attendance mode of an event."""
    OFFLINE = "OfflineEventAttendanceMode"
    ONLINE = "OnlineEventAttendanceMode"
    MIXED = "MixedEventAttendanceMode"


class DayOfWeek(Enum):
    """The day of the week."""
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class RestrictedDiet(Enum):
    """Nutritional restriction."""
    DIABETIC = "DiabeticDiet"
    GLUTEN_FREE = "GlutenFreeDiet"
    HALAL = "HalalDiet"
    HINDU = "HinduDiet"
    KOSHER = "KosherDiet"
    LOW_CALORIE = "LowCalorieDiet"
    LOW_FAT = "LowFatDiet"
    LOW_LACTOSE = "LowLactoseDiet"
    LOW_SALT = "LowSaltDiet"
    VEGAN = "VeganDiet"
    VEGETARIAN = "VegetarianDiet"


class PaymentMethod(Enum):
    """A payment method."""
    CREDIT_CARD = "CreditCard"
    DEBIT_CARD = "DebitCard"
    CASH = "Cash"
    CHECK = "Check"


class DeliveryMethod(Enum):
    """A delivery method."""
    DHL = "DHL"
    FEDEX = "FedEx"
    UPS = "UPS"


# =============================================================================
# CORE TYPES
# =============================================================================

@dataclass
class Thing:
    """The most generic type of item."""
    # Thing properties
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    alternate_name: Optional[List[str]] = field(default_factory=list)
    disambiguating_description: Optional[str] = None
    url: Optional[str] = None
    image: Optional[Union[str, "ImageObject"]] = None
    
    # Internal metadata
    created_at: Optional[datetime] = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = field(default_factory=datetime.now)
    tenant_id: Optional[str] = None


# =============================================================================
# QUANTITATIVE & VALUE TYPES
# =============================================================================

@dataclass
class QuantitativeValue:
    """A point value or range."""
    value: Optional[Union[float, int]] = None
    min_value: Optional[Union[float, int]] = None
    max_value: Optional[Union[float, int]] = None
    unit_code: Optional[str] = None
    unit_text: Optional[str] = None
    value_reference: Optional[QuantitativeValue] = None


@dataclass
class MonetaryAmount:
    """A monetary amount."""
    currency: Optional[str] = None
    value: Optional[Union[float, int, Decimal]] = None
    value_added_tax_included: Optional[bool] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None


@dataclass
class PriceSpecification:
    """A specification of a price."""
    price: Optional[Union[float, int, Decimal]] = None
    price_currency: Optional[str] = None
    valid_from: Optional[datetime] = None
    valid_through: Optional[datetime] = None
    value_added_tax_included: Optional[bool] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None


@dataclass
class PropertyValue:
    """A property-value pair."""
    property_id: Optional[str] = None
    value: Optional[Union[str, float, int, bool]] = None
    value_reference: Optional["PropertyValue"] = None


@dataclass
class DefinedTerm:
    """A defined term."""
    term_code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None


@dataclass
class CategoryCode(DefinedTerm):
    """A category code."""
    code_value: Optional[str] = None


@dataclass
class StructuredValue:
    """A structured value."""
    name_value_pairs: Optional[List[PropertyValue]] = field(default_factory=list)


# =============================================================================
# POSTAL ADDRESS & GEOCOCATION
# =============================================================================

@dataclass
class PostalAddress(Thing):
    """A mailing address."""
    street_address: Optional[str] = None
    address_locality: Optional[str] = None
    address_region: Optional[str] = None
    address_country: Optional[str] = None
    postal_code: Optional[str] = None
    post_office_box_number: Optional[str] = None
    street_number: Optional[str] = None
    premise: Optional[str] = None


@dataclass
class GeoCoordinates(Thing):
    """Geographic coordinates."""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    elevation: Optional[float] = None
    address: Optional[PostalAddress] = None
    address_country: Optional[str] = None
    postal_code: Optional[str] = None


@dataclass
class GeoShape(Thing):
    """A geographic shape."""
    address: Optional[PostalAddress] = None
    address_country: Optional[str] = None
    box: Optional[str] = None
    circle: Optional[str] = None
    elevation: Optional[float] = None
    line: Optional[str] = None
    polygon: Optional[str] = None
    postal_code: Optional[str] = None


@dataclass
class OpeningHoursSpecification(Thing):
    """Opening hours specification."""
    day_of_week: Optional[Union[DayOfWeek, str]] = None
    opens: Optional[str] = None
    closes: Optional[str] = None
    valid_from: Optional[datetime] = None
    valid_through: Optional[datetime] = None


# =============================================================================
# RATING TYPES
# =============================================================================

@dataclass
class Rating(Thing):
    """A rating."""
    author: Optional[Union["Organization", "Person"]] = None
    best_rating: Optional[Union[float, int]] = None
    rating_value: Optional[Union[float, int]] = None
    worst_rating: Optional[Union[float, int]] = None


@dataclass
class AggregateRating(Rating):
    """An aggregate rating."""
    rating_count: Optional[int] = None
    review_count: Optional[int] = None
    rating_explanation: Optional[str] = None


# =============================================================================
# PLACE TYPES
# =============================================================================

@dataclass
class Place(Thing):
    """A place."""
    additional_property: Optional[List[PropertyValue]] = field(default_factory=list)
    address: Optional[PostalAddress] = None
    geo: Optional[GeoCoordinates] = None
    has_map: Optional[str] = None
    is_accessible_for_free: Optional[bool] = False
    opening_hours_specification: Optional[List[OpeningHoursSpecification]] = field(default_factory=list)
    photos: Optional[List["ImageObject"]] = field(default_factory=list)
    reviews: Optional[List[Rating]] = field(default_factory=list)
    telephone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    contained_in_place: Optional["Place"] = None
    contains_place: Optional[List["Place"]] = field(default_factory=list)


@dataclass
class CivicStructure(Place):
    """A public structure."""
    pass


@dataclass
class Accommodation(Place):
    """An accommodation."""
    number_of_rooms: Optional[Union[int, QuantitativeValue]] = None
    permitted_usage: Optional[str] = None
    smoking_allowed: Optional[bool] = False
    bed: Optional["BedDetails"] = None
    occupancy: Optional[QuantitativeValue] = None


@dataclass
class BedDetails:
    """Details about a bed."""
    number_of_beds: Optional[int] = None
    type_of_bed: Optional[str] = None


@dataclass
class Hotel(Accommodation):
    """A hotel."""
    star_rating: Optional[AggregateRating] = None


@dataclass
class VacationRental(Accommodation):
    """A vacation rental."""
    amenity_feature: Optional[List["LocationFeatureSpecification"]] = field(default_factory=list)


@dataclass
class House(Accommodation):
    """A house."""
    number_of_rooms: Optional[int] = None
    occupancy: Optional[QuantitativeValue] = None


@dataclass
class Apartment(House):
    """An apartment."""
    occupancy: Optional[QuantitativeValue] = None


@dataclass
class Room(House):
    """A room within a building."""
    description: Optional[str] = None


@dataclass
class SingleFamilyResidence(House):
    """A single family residence."""
    number_of_rooms: Optional[int] = None


@dataclass
class TouristAttraction(Place):
    """A tourist attraction."""
    tourist_type: Optional[str] = None


@dataclass
class TouristDestination(Place):
    """A tourist destination."""
    does_not_include: Optional[List[str]] = field(default_factory=list)
    includes: Optional[List[str]] = field(default_factory=list)


@dataclass
class AdministrativeArea(Place):
    """An administrative area."""
    name: Optional[str] = None


@dataclass
class Country(AdministrativeArea):
    """A country."""
    pass


@dataclass
class State(AdministrativeArea):
    """A state."""
    pass


@dataclass
class City(AdministrativeArea):
    """A city."""
    pass


@dataclass  
class LocationFeatureSpecification(Thing):
    """A location feature."""
    name: Optional[str] = None
    value: Optional[Union[str, float, int, bool]] = None


# =============================================================================
# ORGANIZATION TYPES
# =============================================================================

@dataclass
class Organization(Thing):
    """An organization."""
    legal_name: Optional[str] = None
    logo: Optional[Union[str, "ImageObject"]] = None
    founding_date: Optional[datetime] = None
    founding_location: Optional[Place] = None
    dissolution_date: Optional[datetime] = None
    number_of_employees: Optional[QuantitativeValue] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    fax_number: Optional[str] = None
    url: Optional[str] = None
    
    # Relationships
    member: Optional[List[Union["Person", "Organization"]]] = field(default_factory=list)
    member_of: Optional[List[Union["Organization", "ProgramMembership"]]] = field(default_factory=list)
    number_of_members: Optional[int] = None
    employee: Optional[List["Person"]] = field(default_factory=list)
    department: Optional[List["Organization"]] = field(default_factory=list)
    parent_organization: Optional["Organization"] = None
    sub_organization: Optional[List["Organization"]] = field(default_factory=list)
    area_served: Optional[Union[Place, str, AdministrativeArea]] = None
    available_service: Optional[List[str]] = field(default_factory=list)
    brand: Optional[Union["Brand", "Organization"]] = None
    contact_point: Optional[List["ContactPoint"]] = field(default_factory=list)
    founder: Optional["Person"] = None
    knows_about: Optional[List[Union[str, Thing]]] = field(default_factory=list)
    knows_language: Optional[Union[str, "Language"]] = None
    makes_offer: Optional[List["Offer"]] = field(default_factory=list)
    keyword: Optional[List[str]] = field(default_factory=list)


@dataclass
class Corporation(Organization):
    """A corporation."""
    ticker_symbol: Optional[str] = None


@dataclass
class GovernmentOrganization(Organization):
    """A government organization."""
    pass


@dataclass
class NonProfitOrganization(Organization):
    """A non-profit organization."""
    registration_number: Optional[str] = None


@dataclass
class Airline(Organization):
    """An airline."""
    iata_code: Optional[str] = None
    icao_code: Optional[str] = None


@dataclass
class SportsTeam(Organization):
    """A sports team."""
    athlete: Optional[List["Person"]] = field(default_factory=list)


@dataclass
class LocalBusiness(Organization):
    """A local business."""
    area_served: Optional[Place] = None
    location: Optional[Union[Place, PostalAddress]] = None
    opening_hours_specification: Optional[List[OpeningHoursSpecification]] = field(default_factory=list)
    price_range: Optional[str] = None
    has_map: Optional[str] = None


@dataclass
class Restaurant(LocalBusiness):
    """A restaurant."""
    serves_cuisine: Optional[List[str]] = field(default_factory=list)
    menu: Optional[Union[str, "MenuItem"]] = None
    has_menu_section: Optional["MenuSection"] = None


@dataclass
class HotelRoom(Accommodation):
    """A hotel room."""
    description: Optional[str] = None


@dataclass
class LodgingBusiness(LocalBusiness):
    """A lodging business."""
    amenity: Optional[List[str]] = field(default_factory=list)
    available_languages: Optional[List[str]] = field(default_factory=list)
    number_of_rooms: Optional[Union[int, QuantitativeValue]] = None
    pets_allowed: Optional[bool] = False
    star_rating: Optional[AggregateRating] = None


# =============================================================================
# PERSON TYPES
# =============================================================================

@dataclass
class Person(Thing):
    """A person."""
    additional_name: Optional[List[str]] = field(default_factory=list)
    address: Optional[Union[PostalAddress, str]] = None
    affiliation: Optional[List[Organization]] = field(default_factory=list)
    alternate_name: Optional[List[str]] = field(default_factory=list)
    award: Optional[List[str]] = field(default_factory=list)
    best_rating: Optional[Union[float, int]] = None
    birth_date: Optional[datetime] = None
    birth_place: Optional[Place] = None
    brand: Optional[Union[Brand, Organization]] = None
    call_sign: Optional[str] = None
    children: Optional[List["Person"]] = field(default_factory=list)
    colleague: Optional[List["Person"]] = field(default_factory=list)
    contact_point: Optional["ContactPoint"] = None
    death_date: Optional[datetime] = None
    death_place: Optional[Place] = None
    email: Optional[str] = None
    family_name: Optional[str] = None
    fax_number: Optional[str] = None
    follows: Optional[List["Person"]] = field(default_factory=list)
    gender: Optional[str] = None
    given_name: Optional[str] = None
    identifier: Optional[str] = None
    job_title: Optional[str] = None
    knows: Optional[List["Person"]] = field(default_factory=list)
    knows_about: Optional[List[Union[str, Thing]]] = field(default_factory=list)
    knows_language: Optional[Union[str, "Language"]] = None
    member_of: Optional[List[Union[Organization, "ProgramMembership"]]] = field(default_factory=list)
    nationality: Optional[Union[str, "Country"]] = None
    owns: Optional[List[Union["Product", "ProductCollection"]]] = field(default_factory=list)
    performer_in: Optional["Event"] = None
    profession: Optional[str] = None
    related_to: Optional[List["Person"]] = field(default_factory=list)
    relative: Optional[List["Person"]] = field(default_factory=list)
    same_as: Optional[List[str]] = field(default_factory=list)
    alumni: Optional[List["Person"]] = field(default_factory=list)
    seeks: Optional[List[Union["Product", "Demand"]]] = field(default_factory=list)
    sibling: Optional[List["Person"]] = field(default_factory=list)
    sponsor: Optional[Union[Organization, str]] = None
    spouse: Optional["Person"] = None
    subpremise: Optional[str] = None
    tax_id: Optional[str] = None
    telephone: Optional[str] = None
    url: Optional[str] = None
    weight: Optional[QuantitativeValue] = None
    works_for: Optional[List[Organization]] = field(default_factory=list)


# =============================================================================
# CONTACT POINT
# =============================================================================

@dataclass
class ContactPoint(Thing):
    """A contact point."""
    telephone: Optional[str] = None
    fax_number: Optional[str] = None
    email: Optional[str] = None
    contact_type: Optional[str] = None
    available_language: Optional[List[str]] = field(default_factory=list)
    contact_option: Optional[List["ContactPointOption"]] = field(default_factory=list)
    product_supported: Optional[Union["Product", str]] = None
    available_hours: Optional[List[OpeningHoursSpecification]] = field(default_factory=list)


@dataclass
class ContactPointOption(Thing):
    """A contact point option."""
    available_on: Optional[datetime] = None
    option_type: Optional[str] = None


# =============================================================================
# BRAND
# =============================================================================

@dataclass
class Brand(Thing):
    """A brand."""
    logo: Optional[Union[str, "ImageObject"]] = None
    aggregate_rating: Optional[AggregateRating] = None


# =============================================================================
# PRODUCT TYPES
# =============================================================================

@dataclass
class Product(Thing):
    """A product."""
    additional_property: Optional[List[PropertyValue]] = field(default_factory=list)
    aggregate_rating: Optional[AggregateRating] = None
    is_accessory_or_spare_part_for: Optional["Product"] = None
    is_related_to: Optional[List["Product"]] = field(default_factory=list)
    is_similar_to: Optional[List["Product"]] = field(default_factory=list)
    is_bundle: Optional[bool] = False
    item_condition: Optional[OfferItemCondition] = None
    manufacturer: Optional[Organization] = None
    model: Optional[Union["ProductModel", str]] = None
    product_id: Optional[str] = None
    production_date: Optional[datetime] = None
    purchase_date: Optional[datetime] = None
    release_date: Optional[datetime] = None
    review: Optional[List[Rating]] = field(default_factory=list)
    sku: Optional[str] = None
    gtin: Optional[str] = None
    gtin12: Optional[str] = None
    gtin13: Optional[str] = None
    gtin14: Optional[str] = None
    mpn: Optional[str] = None
    color: Optional[str] = None
    weight: Optional[QuantitativeValue] = None
    height: Optional[QuantitativeValue] = None
    width: Optional[QuantitativeValue] = None
    depth: Optional[QuantitativeValue] = None
    offers: Optional[List["Offer"]] = field(default_factory=list)
    category: Optional[List[str]] = field(default_factory=list)
    brand: Optional[Union[Brand, Organization, str]] = None
    country_of_origin: Optional[str] = None


@dataclass
class ProductModel(Product):
    """A product model."""
    is_variant_of: Optional["ProductModel"] = None
    predecessor_of: Optional["ProductModel"] = None
    successor_of: Optional["ProductModel"] = None
    related_model: Optional[List["ProductModel"]] = field(default_factory=list)


@dataclass
class SomeProducts(Product):
    """A product collection."""
    number_of_items: Optional[int] = None


@dataclass
class IndividualProduct(Product):
    """An individual product."""
    serial_number: Optional[str] = None


@dataclass
class ProductCollection(SomeProducts):
    """A product collection."""
    pass


# =============================================================================
# OFFER TYPES
# =============================================================================

@dataclass
class Offer(Thing):
    """An offer to sell."""
    accepted_payment_method: Optional[PaymentMethod] = None
    additional_property: Optional[List[PropertyValue]] = field(default_factory=list)
    add_on: Optional["Offer"] = None
    aggregate_rating: Optional[AggregateRating] = None
    availability: Optional[ItemAvailability] = None
    availability_starts: Optional[datetime] = None
    availability_ends: Optional[datetime] = None
    business_function: Optional[str] = None
    delivery_method: Optional[DeliveryMethod] = None
    inventory_level: Optional[QuantitativeValue] = None
    item_condition: Optional[OfferItemCondition] = None
    item_offered: Optional[Union[Product, "Service"]] = None
    earliest_delivery: Optional[datetime] = None
    price: Optional[Union[float, int, Decimal, str]] = None
    price_currency: Optional[str] = None
    price_specification: Optional[PriceSpecification] = None
    valid_from: Optional[datetime] = None
    valid_through: Optional[datetime] = None
    high_price: Optional[Union[float, str]] = None
    low_price: Optional[Union[float, str]] = None
    price_type: Optional[str] = None
    unit_price: Optional[QuantitativeValue] = None
    url: Optional[str] = None
    seller: Optional[Union[Organization, Person]] = None


@dataclass
class AggregateOffer(Offer):
    """An aggregate offer."""
    low_price: Optional[Union[float, Decimal]] = None
    high_price: Optional[Union[float, Decimal]] = None
    offer_count: Optional[int] = None


# =============================================================================
# DEMAND TYPES
# =============================================================================

@dataclass
class Demand(Thing):
    """A demand."""
    accepted_payment_method: Optional[PaymentMethod] = None
    advance_booking_time: Optional[timedelta] = None
    availability: Optional[ItemAvailability] = None
    availability_ends: Optional[datetime] = None
    available_from: Optional[datetime] = None
    available_through: Optional[datetime] = None
    business_function: Optional[str] = None
    delivery_method: Optional[DeliveryMethod] = None
    eligible_quantity: Optional[QuantitativeValue] = None
    eligible_transaction_volume: Optional[PriceSpecification] = None
    inventory_level: Optional[QuantitativeValue] = None
    item_offered: Optional[Union[Product, "Service"]] = None
    member_of: Optional[List[Union[Organization, "ProgramMembership"]]] = field(default_factory=list)
    minimum_price: Optional[MonetaryAmount] = None
    valid_from: Optional[datetime] = None
    valid_through: Optional[datetime] = None
    volume: Optional[QuantitativeValue] = None


# =============================================================================
# SERVICE TYPES
# =============================================================================

@dataclass
class Service(Thing):
    """A service."""
    provider: Optional[Union[Organization, Person]] = None
    provider_mobility: Optional[str] = None
    area_served: Optional[Union[Place, str, AdministrativeArea]] = None
    available_channel: Optional["ServiceChannel"] = None
    category: Optional[Union[CategoryCode, str]] = None
    has_credential: Optional[Union[str, DefinedTerm]] = None
    is_similar_to: Optional[List[Product]] = field(default_factory=list)
    logo: Optional[Union["ImageObject", str]] = None
    official_rating: Optional[Rating] = None
    produces: Optional[List[Union[Product, Thing]]] = field(default_factory=list)
    provider_type: Optional[str] = None
    review: Optional[List[Rating]] = field(default_factory=list)
    same_as: Optional[List[str]] = field(default_factory=list)
    service_output: Optional[Thing] = None
    service_type: Optional[str] = None
    url: Optional[str] = None
    offers: Optional[List[Offer]] = field(default_factory=list)


@dataclass
class ServiceChannel(Thing):
    """A service channel."""
    availability_ends: Optional[datetime] = None
    available_from: Optional[datetime] = None
    provider: Optional[Union[Organization, Person]] = None
    serves: Optional[List[Product]] = field(default_factory=list)
    time_required: Optional[timedelta] = None
    url: Optional[str] = None


@dataclass
class ProfessionalService(Service):
    """A professional service."""
    pass


@dataclass
class FinancialProduct(Service):
    """A financial product."""
    annual_percentage_rate: Optional[Union[float, QuantitativeValue]] = None
    fees_and_commissions_specification: Optional[str] = None
    interest_rate: Optional[Union[float, QuantitativeValue]] = None


@dataclass
class BankAccount(FinancialProduct):
    """A bank account."""
    account_allowed: Optional[str] = None
    account_minimum_balance: Optional[Union[int, QuantitativeValue]] = None
    account_requirements: Optional[str] = None
    overdraft_fees_and_commissions: Optional[str] = None


@dataclass
class LoanOrCredit(FinancialProduct):
    """A loan or credit."""
    amount: Optional[Union[int, MonetaryAmount, PriceSpecification]] = None
    credit_score_requirement: Optional[int] = None
    required_credit_score: Optional[int] = None
    loan_term: Optional[QuantitativeValue] = None
    loan_type: Optional[str] = None
    amount_due: Optional[MonetaryAmount] = None
    number_of_loan_payments: Optional[int] = None


@dataclass
class PaymentCard(FinancialProduct):
    """A payment card."""
    card_issuer: Optional[Organization] = None
    card_number: Optional[str] = None
    cash_back: Optional[Union[int, MonetaryAmount]] = None
    merchant_category: Optional[str] = None
    annual_fee: Optional[MonetaryAmount] = None
    cash_advance_fee: Optional[MonetaryAmount] = None
    cash_advance_interest_rate: Optional[QuantitativeValue] = None
    minimum_payment: Optional[MonetaryAmount] = None


# =============================================================================
# EVENT TYPES
# =============================================================================

@dataclass
class Event(Thing):
    """An event."""
    event_status: Optional[EventStatusType] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    duration: Optional[timedelta] = None
    event_attendance_mode: Optional[EventAttendanceMode] = None
    location: Optional[Union[Place, str]] = None
    organizer: Optional[Union[Organization, Person]] = None
    performer: Optional[List[Union[Organization, Person]]] = field(default_factory=list)
    sponsor: Optional[Union[Organization, Person]] = None
    offers: Optional[List[Offer]] = field(default_factory=list)
    previous_event: Optional["Event"] = None
    next_event: Optional["Event"] = None
    maximum_attendee_capacity: Optional[int] = None
    typical_age_range: Optional[str] = None
    in_language: Optional[str] = None
    previous_start_date: Optional[datetime] = None
    attendee: Optional[List[Union[Organization, Person]]] = field(default_factory=list)
    maximum_physical_attendee_capacity: Optional[int] = None
    maximum_attendees: Optional[int] = None


@dataclass
class PublicationEvent(Event):
    """A publication event."""
    published_on: Optional["BroadcastEvent"] = None


@dataclass
class BroadcastEvent(Event):
    """A broadcast event."""
    is_broadcast_of: Optional["BroadcastService"] = None
    video_format: Optional[str] = None


@dataclass
class BroadcastService(Thing):
    """A broadcast service."""
    name: Optional[str] = None
    provider: Optional[Union[Organization, Person]] = None
    broadcast_feed: Optional[str] = None


@dataclass
class Course(Event):
    """A course."""
    course_code: Optional[str] = None
    course_minimum_attendance: Optional[QuantitativeValue] = None
    course_prereqs: Optional[Union["Course", str]] = None
    has_course_instance: Optional[List["CourseInstance"]] = field(default_factory=list)
    number_of_credits: Optional[int] = None
    professional_category: Optional[str] = None
    requires_completion: Optional[str] = None


@dataclass
class CourseInstance(Event):
    """A course instance."""
    course_mode: Optional[str] = None
    course_workload: Optional[str] = None
    instructor: Optional["Person"] = None


@dataclass
class ScheduledEvent(Event):
    """A scheduled event."""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


# =============================================================================
# CREATIVE WORK TYPES
# =============================================================================

@dataclass
class CreativeWork(Thing):
    """A creative work."""
    headline: Optional[str] = None
    alternative_headline: Optional[str] = None
    date_published: Optional[datetime] = None
    date_created: Optional[datetime] = None
    date_modified: Optional[datetime] = None
    copyright_year: Optional[int] = None
    copyright_holder: Optional[Union[Organization, Person]] = None
    license: Optional[str] = None
    version: Optional[Union[str, int]] = None
    time_required: Optional[timedelta] = None
    encoding: Optional[List["MediaObject"]] = field(default_factory=list)
    file_format: Optional[List[str]] = field(default_factory=list)
    content_rating: Optional[str] = None
    aggregate_rating: Optional[AggregateRating] = None
    review: Optional[List[Rating]] = field(default_factory=list)
    
    # Creator fields
    author: Optional[List[Union[Person, Organization]]] = field(default_factory=list)
    contributor: Optional[List[Union[Person, Organization]]] = field(default_factory=list)
    creator: Optional[Union[Person, Organization]] =None
    editor: Optional[List[Person]] = field(default_factory=list)
    publisher: Optional[Organization] = None
    provider: Optional[Union[Organization, Person]] = None
    
    # Content
    about: Optional[Thing] = None
    associated_media: Optional[List["MediaObject"]] = field(default_factory=list)
    citation: Optional[List[str]] = field(default_factory=list)
    comment: Optional[List["Comment"]] = field(default_factory=list)
    comment_count: Optional[int] = None
    content_reference_time: Optional[datetime] = None
    conditions_of_access: Optional[str] = None
    current_location: Optional[Place] = None
    discussion_url: Optional[str] = None
    
    # Work relations
    has_part: Optional[List["CreativeWork"]] = field(default_factory=list)
    is_based_on: Optional[List["CreativeWork"]] = field(default_factory=list)
    is_part_of: Optional["CreativeWork"] = None
    mentions: Optional[List[Thing]] = field(default_factory=list)


@dataclass
class Article(CreativeWork):
    """An article."""
    article_section: Optional[str] = None
    article_body: Optional[str] = None
    page_end: Optional[int] = None
    page_start: Optional[int] = None
    pagination: Optional[str] = None
    word_count: Optional[int] = None
    published_by: Optional[Union[Organization, Person]] = None
    approved: Optional[bool] = False


@dataclass
class BlogPosting(Article):
    """A blog posting."""
    audio: Optional[Union["MusicGroup", "AudioObject"]] = None
    video: Optional["VideoObject"] = None


@dataclass
class NewsArticle(Article):
    """A news article."""
    dateline: Optional[str] = None
    print_column: Optional[str] = None
    print_edition: Optional[str] = None
    print_page: Optional[str] = None
    print_section: Optional[str] = None


@dataclass
class Report(NewsArticle):
    """A report."""
    page: Optional[str] = None


@dataclass
class SocialMediaPosting(Article):
    """A social media post."""
    speech_to_date: Optional[datetime] = None
    video: Optional["VideoObject"] = None


@dataclass
class BlogPost(CreativeWork):
    """A blog post."""
    audio: Optional[Union["MusicGroup", "AudioObject"]] = field(default_factory=list)


@dataclass
class Comment(CreativeWork):
    """A comment."""
    downvote: Optional[int] = None
    upvote: Optional[int] = None
    parent_item: Optional["Comment"] = None


@dataclass
class Review(CreativeWork):
    """A review."""
    review_rating: Optional[Rating] = None
    review_body: Optional[str] = None
    item_reviewed: Optional[Thing] = None
    reviewer: Optional[Union[Person, Organization]] = None
    review_published_by: Optional[Union[Organization, Person]] = None


# =============================================================================
# MEDIA TYPES
# =============================================================================

@dataclass
class MediaObject(CreativeWork):
    """A media object."""
    content_url: Optional[str] = None
    embed_url: Optional[str] = None
    upload_date: Optional[datetime] = None
    content_size: Optional[str] = None
    content_duration: Optional[timedelta] = None
    encoding_format: Optional[str] = None
    bitrate: Optional[str] = None
    encoding: Optional[List["MediaObject"]] = field(default_factory=list)


@dataclass
class ImageObject(MediaObject):
    """An image."""
    caption: Optional[str] = None
    exif_data: Optional[str] = None
    representative_of_page: Optional[bool] = False
    thumbnail: Optional["ImageObject"] = None


@dataclass
class Photograph(ImageObject):
    """A photograph."""
    pass


@dataclass
class AudioObject(MediaObject):
    """An audio object."""
    transcript: Optional[str] = None
    embed_url: Optional[str] = None
    caption: Optional[List["MediaObject"]] = field(default_factory=list)


@dataclass
class VideoObject(MediaObject):
    """A video object."""
    caption: Optional[str] = None
    video_frame_size: Optional[str] = None
    video_quality: Optional[str] = None
    actor: Optional[List[Person]] = field(default_factory=list)
    director: Optional[Person] = None
    music_by: Optional[Union[Person, Organization]] = None
    thumbnail: Optional[ImageObject] = None


@dataclass
class VideoGame(SoftwareApplication):
    """A video game."""
    cheat_code: Optional[str] = None
    game_server: Optional["GameServer"] = None
    genre: Optional[Union[str, "CreativeWork"]] = None
    game_tip: Optional["CreativeWork"] = None


# =============================================================================
# SOFTWARE & APP TYPES
# =============================================================================

@dataclass
class SoftwareApplication(CreativeWork):
    """A software application."""
    application_category: Optional[str] = None
    application_sub_category: Optional[str] = None
    application_suite: Optional[str] = None
    supporting_data: Optional["DataFeed"] = None
    available_on: Optional[Product] = None
    offers: Optional[List[Offer]] = field(default_factory=list)
    file_size: Optional[str] = None


@dataclass
class SoftwareSourceCode(CreativeWork):
    """Software source code."""
    runtime: Optional[str] = None
    target_product: Optional[Product] = None
    programming_language: Optional[Union["ProgrammingLanguage", str]] = None
    code_repository: Optional[str] = None
    code_sample_type: Optional[str] = None
    date_created: Optional[datetime] = None
    fix_days: Optional[int] = None


@dataclass
class ProgrammingLanguage(Thing):
    """A programming language."""
    alias: Optional[List[str]] = field(default_factory=list)
    predecessor: Optional["ProgrammingLanguage"] = None
    successor: Optional["ProgrammingLanguage"] = None


@dataclass
class WebApplication(SoftwareApplication):
    """A web application."""
    browser_requirements: Optional[str] = None


@dataclass
class GameServer(Thing):
    """A game server."""
    server_status: Optional[Union[str, "GameServerStatus"]] = None
    users_online: Optional[int] = None


class GameServerStatus(Enum):
    """Game server status."""
    ONLINE = "Online"
    OFFLINE = "Offline"
    MAINTENANCE = "Maintenance"


# =============================================================================
# MOVIE & ENTERTAINMENT
# =============================================================================

@dataclass
class Movie(CreativeWork):
    """A movie."""
    duration: Optional[timedelta] = None
    director: Optional[Person] = None
    actor: Optional[List[Person]] = field(default_factory=list)
    trailer: Optional[VideoObject] = None
    music_by: Optional[Union[Person, Organization]] = None


@dataclass
class TVSeries(CreativeWork):
    """A TV series."""
    actor: Optional[List[Person]] = field(default_factory=list)
    director: Optional[List[Person]] = field(default_factory=list)
    episode: Optional[List["Episode"]] = field(default_factory=list)
    season: Optional[List["VideoObject"]] = field(default_factory=list)
    number_of_seasons: Optional[int] = None
    number_of_episodes: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


@dataclass
class Episode(CreativeWork):
    """An episode."""
    episode_number: Optional[int] = None
    part_of_season: Optional["Season"] = None
    part_of_tv_series: Optional[TVSeries] = None


@dataclass
class Season(CreativeWork):
    """A season."""
    season_number: Optional[int] = None
    part_of_tv_series: Optional[TVSeries] = None


@dataclass
class Clip(VideoObject):
    """A clip."""
    part_of_episode: Optional[Episode] = None
    part_of_season: Optional[Season] = None


@dataclass
class MovieSeries(CreativeWork):
    """A movie series."""
    contains: Optional[List[Movie]] = field(default_factory=list)


# =============================================================================
# MUSIC TYPES
# =============================================================================

@dataclass
class MusicGroup(CreativeWork):
    """A music group."""
    member: Optional[List[Union[Organization, Person]] = field(default_factory=list)
    genre: Optional[List[str]] = field(default_factory=list)


@dataclass
class MusicAlbum(CreativeWork):
    """A music album."""
    album_production_type: Optional[str] = None
    album_release_type: Optional[str] = None
    by_artist: Optional[MusicGroup] = None
    num_tracks: Optional[int] = None
    track: Optional[List["MusicRecording"]] = field(default_factory=list)


@dataclass
class MusicRecording(CreativeWork):
    """A music recording."""
    album: Optional[MusicAlbum] = None
    by_artist: Optional[Union[MusicGroup, Person]] = None
    duration: Optional[timedelta] = None
    isrc_code: Optional[str] = None


@dataclass
class MusicComposition(CreativeWork):
    """A music composition."""
    music_arrangement: Optional["MusicComposition"] = None
    composer: Optional[Union[Organization, Person]] = None
    first_performance: Optional[Event] = None
    included_in_composition: Optional["MusicComposition"] = None
    iswc_code: Optional[str] = None
    recorded_as: Optional[MusicRecording] = None
    composition_as_written: Optional["MusicComposition"] = None


@dataclass
class Playlist(CreativeWork):
    """A playlist."""
    track: Optional[List[MusicRecording]] = field(default_factory=list)


# =============================================================================
# RECIPE TYPES
# =============================================================================

@dataclass
class HowToStep(Thing):
    """A step in a how-to."""
    name: Optional[str] = None
    text: Optional[str] = None
    url: Optional[str] = None
    image: Optional[Union[str, ImageObject]] = None


@dataclass
class HowTo(HowToStep):
    """A how-to."""
    steps: Optional[List["HowToStep"]] = field(default_factory=list)


@dataclass
class Recipe(HowTo):
    """A recipe."""
    cook_time: Optional[timedelta] = None
    prep_time: Optional[timedelta] = None
    recipe_yield: Optional[Union[int, List[str]]] = None
    ingredients: Optional[List[str]] = field(default_factory=list)
    nutrition: Optional["NutritionInformation"] = None
    recipe_category: Optional[str] = None
    recipe_cuisine: Optional[str] = None
    suitable_for_diet: Optional[RestrictedDiet] = None


@dataclass
class NutritionInformation(Thing):
    """Nutrition information."""
    serving_size: Optional[str] = None
    calories: Optional["Energy"] = None
    carbohydrate_content: Optional["Mass"] = None
    cholesterol_content: Optional["Mass"] = None
    fat_content: Optional["Mass"] = None
    fiber_content: Optional["Mass"] = None
    protein_content: Optional["Mass"] = None
    sodium_content: Optional["Mass"] = None
    sugar_content: Optional["Mass"] = None
    trans_fat_content: Optional["Mass"] = None


@dataclass
class Energy(Thing):
    """Energy quantity."""
    value: Optional[float] = None
    unit_code: Optional[str] = None


@dataclass
class Mass(Thing):
    """Mass quantity."""
    value: Optional[float] = None
    unit_code: Optional[str] = None


# =============================================================================
# MENU TYPES
# =============================================================================

@dataclass
class MenuItem(Thing):
    """A menu item."""
    nutrition: Optional[NutritionInformation] = None
    offers: Optional[List[Offer]] = field(default_factory=list)
    suitable_for_diet: Optional[RestrictedDiet] = None


@dataclass
class MenuSection(Thing):
    """A menu section."""
    menu_item: Optional[List[MenuItem]] = field(default_factory=list)
    menu_section: Optional[List["MenuSection"]] = field(default_factory=list)


@dataclass
class Menu(Thing):
    """A menu."""
    has_menu_section: Optional[List[MenuSection]] = field(default_factory=list)


# =============================================================================
# RESERVATION TYPES
# =============================================================================

class ReservationStatusType(Enum):
    """Reservation status."""
    RESERVATION_CANCELLED = "ReservationCancelled"
    RESERVATION_CONFIRMED = "ReservationConfirmed"
    RESERVATION_HOLD = "ReservationHold"
    RESERVATION_PENDING = "ReservationPending"


@dataclass
class Reservation(Thing):
    """A reservation."""
    booking_agent: Optional[Union[Organization, Person]] = None
    booking_time: Optional[datetime] = None
    broker: Optional[Union[Organization, Person]] = None
    confirmation_number: Optional[str] = None
    cancellation_policy: Optional[str] = None
    cancellation_deadline: Optional[datetime] = None
    currency: Optional[str] = None
    reservation_for: Optional[Thing] = None
    reservation_id: Optional[str] = None
    reservation_status: Optional[ReservationStatusType] = None
    total_price: Optional[Union[float, PriceSpecification, str]] = None
    under_name: Optional[Union[Organization, Person]] = None


@dataclass
class FlightReservation(Reservation):
    """A flight reservation."""
    boarding_group: Optional[str] = None
    passenger_priority_status: Optional[str] = None
    passenger_legs: Optional[List["Flight"]] = field(default_factory=list)
    security_wait: Optional[int] = None
    terminal: Optional[str] = None
    gate: Optional[str] = None


@dataclass
class LodgingReservation(Reservation):
    """A lodging reservation."""
    checkin_time: Optional[datetime] = None
    checkout_time: Optional[datetime] = None
    lodging_unit: Optional[str] = None
    num_guests: Optional[int] = None


@dataclass
class TaxiReservation(Reservation):
    """A taxi reservation."""
    pickup_time: Optional[datetime] = None
    pickup_location: Optional[Place] = None
    dropoff_location: Optional[Place] = None


@dataclass
class BusReservation(Reservation):
    """A bus reservation."""
    bus_name: Optional[str] = None
    bus_number: Optional[str] = None


@dataclass
class BoatReservation(Reservation):
    """A boat reservation."""
    name: Optional[str] = None


# =============================================================================
# ORDER TYPES
# =============================================================================

class OrderStatusType(Enum):
    """Order status."""
    ORDER_CANCELLED = "OrderCancelled"
    ORDER_DELIVERED = "OrderDelivered"
    ORDER_IN_TRANSIT = "OrderInTransit"
    ORDER_PAYMENT_DUE = "OrderPaymentDue"
    ORDER_PICKUP_AVAILABLE = "OrderPickupAvailable"
    ORDER_PROBLEM = "OrderProblem"
    ORDER_PROCESSING = "OrderProcessing"
    ORDER_RETURNED = "OrderReturned"


class OrderItemStatus(Enum):
    """Order item status."""
    ORDER_ITEM_CANCELLED = "OrderItemCancelled"
    ORDER_ITEM_DELIVERED = "OrderItemDelivered"
    ORDER_ITEM_IN_TRANSIT = "OrderItemInTransit"
    ORDER_ITEM_LOST = "OrderItemLost"
    ORDER_ITEM_PAID = "OrderItemPaid"
    ORDER_ITEM_PICKUP_AVAILABLE = "OrderItemPickupAvailable"
    ORDER_ITEM_PROBLEM = "OrderItemProblem"
    ORDER_ITEM_RETURNED = "OrderItemReturned"
    ORDER_ITEM_SHIPPED = "OrderItemShipped"


@dataclass
class Order(Thing):
    """An order."""
    accepted_offer: Optional[Offer] = None
    billing_address: Optional[PostalAddress] = None
    broker: Optional[Union[Organization, Person]] = None
    confirmation_number: Optional[str] = None
    customer: Optional[Union[Organization, Person]] = None
    discount: Optional[Union[float, str]] = None
    discount_code: Optional[str] = None
    is_gift: Optional[bool] = False
    order_date: Optional[datetime] = None
    order_item: Optional[List["OrderItem"]] = field(default_factory=list)
    order_number: Optional[str] = None
    order_status: Optional[OrderStatusType] = None
    part_of_invoice: Optional["Invoice"] = None
    payment_due_date: Optional[datetime] = None
    seller: Optional[Union[Organization, Person]] = None
    total_payment_due: Optional[Union[float, MonetaryAmount]] = None


@dataclass
class OrderItem(Thing):
    """An order item."""
    order_delivery: Optional["ParcelDelivery"] = None
    order_item_number: Optional[str] = None
    order_item_status: Optional[OrderItemStatus] = None
    order_quantity: Optional[int] = None
    ordered_item: Optional[Union[Product, Service]] = None
    price: Optional[MonetaryAmount] = None


@dataclass
class ParcelDelivery(Thing):
    """A parcel delivery."""
    delivery_address: Optional[PostalAddress] = None
    delivery_date: Optional[datetime] = None
    delivery_time: Optional[timedelta] = None
    carrier: Optional[Organization] = None
    has_tracking_number: Optional[str] = None
    destination: Optional[PostalAddress] = None
    origin_address: Optional[PostalAddress] = None
    item_shipped: Optional[List[Product]] = field(default_factory=list)
    tracking_url: Optional[str] = None


@dataclass
class Invoice(Thing):
    """An invoice."""
    account_number: Optional[str] = None
    billing_period: Optional[str] = None
    broker: Optional[Union[Organization, Person]] = None
    category: Optional[Union[CategoryCode, str]] = None
    confirmation_number: Optional[str] = None
    customer: Optional[Union[Organization, Person]] = None
    discount: Optional[Union[float, str]] = None
    discount_percent: Optional[float] = None
    due_date: Optional[datetime] = None
    minimum_payment_due: Optional[MonetaryAmount] = None
    number_of_periods: Optional[int] = None
    payment_due: Optional[datetime] = None
    payment_terms: Optional[str] = None
    payment_method: Optional[PaymentMethod] = None
    payment_method_id: Optional[str] = None
    payment_status: Optional[str] = None
    provides_service: Optional[Organization] = None
    purchase_order_reference: Optional[str] = None
    reference_grant: Optional[Grant] = None
    scheduled_payment_date: Optional[datetime] = None
    total_payment_due: Optional[MonetaryAmount] = None
    transaction_id: Optional[str] = None


# =============================================================================
# GRANT & TENDER
# =============================================================================

@dataclass
class Grant(Thing):
    """A grant."""
    funded_amount: Optional[Union[float, MonetaryAmount]] = None
    sponsor: Optional[Union[Organization, Person]] = None
    url: Optional[str] = None


@dataclass
class Tender(Thing):
    """A tender."""
    bid_submission_deadline: Optional[datetime] = None
    bid_window: Optional[str] = None
    qualification_bidders: Optional[List[Organization]] = field(default_factory=list)
    requirements: Optional[str] = None
    tender_for: Optional[Thing] = None
    winner: Optional[Organization] = None


# =============================================================================
# PROGRAM MEMBERSHIP
# =============================================================================

@dataclass
class ProgramMembership(Thing):
    """A program membership."""
    member_number: Optional[str] = None
    program_name: Optional[str] = None
    member: Optional[Organization] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    tenant: Optional[str] = None


# =============================================================================
# JOB POSTING
# =============================================================================

@dataclass
class JobPosting(Thing):
    """A job posting."""
    date_posted: Optional[datetime] = None
    textual: Optional[str] = None
    base_salary: Optional[Union[float, MonetaryAmount, PriceSpecification]] = None
    direct_application: Optional[bool] = False
    employment_type: Optional[str] = None
    hiring_organization: Optional[Organization] = None
    industry: Optional[str] = None
    job_location: Optional[Place] = None
    job_location_type: Optional[str] = None
    next_posting: Optional[datetime] = None
    occupational_category: Optional[str] = None
    qualifications: Optional[str] = None
    related_to: Optional[JobPosting] = None
    responsibilities: Optional[str] = None
    relevant_occupation: Optional[str] = None
    security_clearance_requirement: Optional[str] = None
    sensory_detail_requirement: Optional[str] = None
    skills: Optional[Union[str, DefinedTerm]] = None
    special_commitments: Optional[str] = None
    work_hours: Optional[str] = None


# =============================================================================
# DATA FEED
# =============================================================================

@dataclass
class DataFeed(Thing):
    """A data feed."""
    data_feed_element: Optional[List["DataFeedItem"]] = field(default_factory=list)


@dataclass
class DataFeedItem(Thing):
    """A data feed item."""
    item: Optional[Union[str, Thing]] = None
    date_modified: Optional[datetime] = None
    target: Optional[Thing] = None


# =============================================================================
# LANGUAGE
# =============================================================================

@dataclass
class Language(Thing):
    """A language."""
    alternate_name: Optional[List[str]] = field(default_factory=list)
    name: Optional[str] = None


# =============================================================================
# FLIGHT & TRANSPORT
# =============================================================================

@dataclass
class Flight(Thing):
    """A flight."""
    flight_number: Optional[str] = None
    airline: Optional[Organization] = None
    departure_airport: Optional[Union[Place, Airport]] = None
    departure_time: Optional[datetime] = None
    arrival_airport: Optional[Union[Place, Airport]] = None
    arrival_time: Optional[datetime] = None
    arrival_terminal: Optional[str] = None
    departure_terminal: Optional[str] = None
    aircraft: Optional[Union[str, "Vehicle"]] = None


@dataclass
class Airport(Place):
    """An airport."""
    iata_code: Optional[str] = None
    icao_code: Optional[str] = None


@dataclass
class TrainTrip(Thing):
    """A train trip."""
    name: Optional[str] = None
    departure_station: Optional[Place] = None
    arrival_station: Optional[Place] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    train_name: Optional[str] = None
    train_number: Optional[str] = None


@dataclass
class BusTrip(Thing):
    """A bus trip."""
    name: Optional[str] = None
    arrival_bus_station: Optional[BusStation] = None
    arrival_time: Optional[datetime] = None
    departure_bus_station: Optional[BusStation] = None
    departure_time: Optional[datetime] = None
    bus_name: Optional[str] = None
    bus_number: Optional[str] = None


@dataclass
class BusStation(Place):
    """A bus station."""
    pass


@dataclass
class Taxi(Service):
    """A taxi service."""
    vehicle: Optional[" TAXIVehicle "] = None


@dataclass
class TAXIVehicle(Vehicle):
    """A taxi vehicle."""
    vehicle_registration_number: Optional[str] = None


@dataclass
class Vehicle(Thing):
    """A vehicle."""
    vehicle_identification_number: Optional[str] = None
    vehicle_configuration: Optional[str] = None
    vehicle_engine: Optional["EngineSpecification"] = None
    vehicle_interior_type: Optional[str] = None
    vehicle_interior_color: Optional[str] = None
    vehicle_number_of_forward_gears: Optional[int] = None
    vehicle_number_of_wheels: Optional[int] = None
    steering_position: Optional[str] = None


@dataclass
class EngineSpecification(Thing):
    """An engine specification."""
    engine_displacement: Optional[QuantitativeValue] = None
    engine_power: Optional[QuantitativeValue] = None
    engine_name: Optional[str] = None
    engine_type: Optional[str] = None
    torque: Optional[QuantitativeValue] = None


# =============================================================================
# FAQ & Q&A
# =============================================================================

@dataclass
class FAQPage(CreativeWork):
    """An FAQ page."""
    main_entity: Optional[List[Question]] = field(default_factory=list)


@dataclass
class Question(CreativeWork):
    """A question."""
    answer_count: Optional[int] = None
    downvote_count: Optional[int] = None
    upvote_count: Optional[int] = None
    suggested_answer: Optional[List["Answer"]] = field(default_factory=list)
    answer: Optional[List["Answer"]] = field(default_factory=list)


@dataclass
class Answer(CreativeWork):
    """An answer."""
    answer_option: Optional[List["Answer"]] = field(default_factory=list)
    downvote_count: Optional[int] = None
    upvote_count: Optional[int] = None
    suggested_answer: Optional[List["Answer"]] = field(default_factory=list)


# =============================================================================
# WEB CONTENT
# =============================================================================

@dataclass
class WebPage(CreativeWork):
    """A web page."""
    breadcrumb: Optional["BreadcrumbList"] = None
    is_part_of: Optional["WebSite"] = None
    primary_image_of_page: Optional[ImageObject] = None
    related_link: Optional[List[str]] = field(default_factory=list)
    speakable: Optional[str] = None


@dataclass
class WebSite(Thing):
    """A web site."""
    name: Optional[str] = None
    url: Optional[str] = None
    alternate_name: Optional[str] = None
    
    # Relations
    is_part_of: Optional["WebSite"] = None
    url: Optional[str] = None


@dataclass
class BreadcrumbList(Thing):
    """A breadcrumb list."""
    item_list_element: Optional[List["ListItem"]] = field(default_factory=list)


@dataclass
class ListItem(Thing):
    """A list item."""
    item: Optional[Union[Thing, str]] = None
    next_item: Optional["ListItem"] = None
    position: Optional[int] = None
    previous_item: Optional["ListItem"] = None


@dataclass
class SiteNavigationElement(WebPage):
    """A site navigation element."""
    name: Optional[str] = None


# =============================================================================
# ABOUT THIS FILE
# =============================================================================

"""
Schema.org Python Dataclasses

Usage:
    from schema_org import Person, Organization, Product, Offer
    
    # Create entities
    person = Person(
        id="https://example.com/people/john",
        name="John Doe",
        email="john@example.com"
    )
    
    org = Organization(
        name="Acme Corp",
        email="contact@acme.com"
    )
    
    product = Product(
        name="Super Widget",
        sku="SW-001",
        offers=[Offer(price=99.99)]
    )

Type Safety:
    All classes use Python dataclasses with type hints.
    Use with mypy for static type checking.
    Use with pydantic for validation.

References:
    - Schema.org: https://schema.org/docs/schemas.html
    - Python typing: https://docs.python.org/3/library/typing.html
"""
"""
Schema.org Things and Actions - Complete Schema.org Python Implementation

This module provides proper Schema.org types using:
- Thing (base entity)  
- Action (for operations)
- CreativeWork, Event, Organization, Person, Product, Place, etc.

All types use Schema.org's @context and @type for JSON-LD compatibility.
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
    Callable,
)
from typing_extensions import TypeAlias

# =============================================================================
# SCHEMA.ORG CONSTANTS
# =============================================================================

SCHEMA_ORG_CONTEXT = "https://schema.org"
SCHEMA_ORG_VERSION = "https://schema.org/version/3.9/"

# =============================================================================
# ENUMERATIONS - Schema.org defined enumerations
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


class ActionStatusType(Enum):
    """The status of an action."""
    ACTIVE = "ActionStatus"
    COMPLETED = "CompletedActionStatus"
    FAILED = "FailedActionStatus"
    POTENTIAL = "PotentialActionStatus"


class ActionType(Enum):
    """The type of action."""
    ACTION = "Action"
    ACHIEVE_ACTIONS = "AchieveAction"
    CONSUME_ACTIONS = "ConsumeAction"
    CONTROL_ACTIONS = "ControlAction"
    CREATE_ACTIONS = "CreateAction"
    DELETE_ACTIONS = "DeleteAction"
    FIND_ACTIONS = "FindAction"
    MOVE_ACTIONS = "MoveAction"
    ORGANIZE_ACTIONS = "OrganizeAction"
    PLAY_ACTIONS = "PlayAction"
    SEARCH_ACTIONS = "SearchAction"
    TRADE_ACTIONS = "TradeAction"
    TRANSFER_ACTIONS = "TransferAction"
    UPDATE_ACTIONS = "UpdateAction"


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
# THING - Base Schema.org type
# =============================================================================

@dataclass
class Thing:
    """
    The most generic type of item.
    
    Schema.org Thing: https://schema.org/Thing
    """
    # Schema.org metadata
    context: str = field(default=SCHEMA_ORG_CONTEXT, repr=False)
    type: str = field(default="Thing", repr=True)
    
    # Core Thing properties
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    alternate_name: Optional[List[str]] = field(default_factory=list)
    disambiguating_description: Optional[str] = None
    url: Optional[str] = None
    image: Optional[Union[str, ImageObject]] = None
    
    # SameAs links
    same_as: Optional[List[str]] = field(default_factory=list)
    
    # Internal metadata
    created_at: Optional[datetime] = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = field(default_factory=datetime.now)
    tenant_id: Optional[str] = None
    
    def to_jsonld(self) -> Dict[str, Any]:
        """Convert to JSON-LD format."""
        result = {"@context": self.context}
        
        # Add type
        if self.type != "Thing":
            result["@type"] = self.type
            
        # Add core properties
        if self.id:
            result["@id"] = self.id
        if self.name:
            result["name"] = self.name
        if self.description:
            result["description"] = self.description
        if self.alternate_name:
            result["alternateName"] = self.alternate_name
        if self.disambiguating_description:
            result["disambiguatingDescription"] = self.disambiguating_description
        if self.url:
            result["url"] = self.url
        if self.image:
            if isinstance(self.image, ImageObject):
                result["image"] = self.image.to_jsonld()
            else:
                result["image"] = self.image
        if self.same_as:
            result["sameAs"] = self.same_as
            
        return result
    
    @classmethod
    def from_jsonld(cls, data: Dict[str, Any]) -> Thing:
        """Create from JSON-LD data."""
        return cls(
            id=data.get("@id"),
            name=data.get("name"),
            description=data.get("description"),
            alternate_name=data.get("alternateName", []),
            disambiguating_description=data.get("disambiguatingDescription"),
            url=data.get("url"),
            image=data.get("image"),
            same_as=data.get("sameAs", []),
        )


# =============================================================================
# ACTION - Schema.org Action types
# =============================================================================

@dataclass
class Action(Thing):
    """
    An action performed by an agent.
    
    Schema.org Action: https://schema.org/Action
    """
    type: str = "Action"
    
    # Action properties
    action_status: Optional[ActionStatusType] = None
    target: Optional[EntryPoint] = None
    object: Optional[Thing] = None
    result: Optional[Thing] = None
    
    # Agent who performed/will perform
    agent: Optional[Union[Person, Organization]] = None
    participant: Optional[List[Union[Person, Organization]]] = field(default_factory=list)
    instrument: Optional[Thing] = None
    
    # Timing
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[timedelta] = None
    
    # Error handling
    error: Optional[Thing] = None
    
    # Potential action
    potential_action: Optional[Action] = None
    
    # Object of the action
    action_platform: Optional[Union[str, URL]] = None
    
    # Location of action
    location: Optional[Union[Place, PostalAddress, str]] = None


@dataclass
class AchieveAction(Action):
    """The act of accomplishing something."""
    type: str = "AchieveAction"


@dataclass
class ConsumeAction(Action):
    """The act of consuming something."""
    type: str = "ConsumeAction"
    amount: Optional[Union[QuantitativeValue, MonetaryAmount]] = None
    object: Optional[Thing] = None  # What was consumed


@dataclass
class UseAction(ConsumeAction):
    """The act of using something."""
    type: str = "UseAction"
    reuse: Optional[bool] = False


@dataclass
class ConsumeFoodAction(ConsumeAction):
    """The act of consuming food."""
    type: str = "ConsumeFoodAction"


@dataclass
class DrinkAlcoholAction(ConsumeAction):
    """The act of consuming alcohol."""
    type: str = "DrinkAlcoholAction"


@dataclass
class TakeAction(ConsumeAction):
    """The act of taking something from a place."""
    type: str = "TakeAction"


@dataclass
class ControlAction(Action):
    """Controlling a device or application."""
    type: str = "ControlAction"
    control_device: Optional[Thing] = None


@dataclass
class DeactivateAction(Action):
    """The act of deactivating a device or application."""
    type: str = "DeactivateAction"


@dataclass
class ActivateAction(Action):
    """The act of activating a device or application."""
    type: str = "ActivateAction"


@dataclass
class ResumeAction(Action):
    """Resuming a process or task."""
    type: str = "ResumeAction"


@dataclass
class SuspendAction(Action):
    """Suspending a process or task."""
    type: str = "SuspendAction"


@dataclass
class CreateAction(Action):
    """The act of creating something."""
    type: str = "CreateAction"


@dataclass
class FilmAction(CreateAction):
    """The act of filming."""
    type: str = "FilmAction"


@dataclass
class PaintAction(CreateAction):
    """The act of painting."""
    type: str = "PaintAction"


@dataclass
class PhotographAction(CreateAction):
    """The act of taking a photograph."""
    type: str = "PhotographAction"


@dataclass
class WriteAction(CreateAction):
    """The act of writing."""
    type: str = "WriteAction"


@dataclass
class DeleteAction(Action):
    """The act of deleting something."""
    type: str = "DeleteAction"


@dataclass
class UnSubscribeAction(DeleteAction):
    """The act of unsubscribing."""
    type: str = "UnSubscribeAction"


@dataclass
class DislikeAction(Action):
    """Express a dislike."""
    type: str = "DislikeAction"


@dataclass
class IgnoreAction(Action):
    """Ignore something."""
    type: str = "IgnoreAction"


@dataclass
class FindAction(Action):
    """The act of finding an item."""
    type: str = "FindAction"
    found: Optional[Thing] = None


@dataclass
class DiscoverAction(FindAction):
    """The act of discovering."""
    type: str = "DiscoverAction"


@dataclass
class CheckAction(FindAction):
    """The act of checking."""
    type: str = "CheckAction"


@dataclass
class CompareAction(FindAction):
    """The act of comparing."""
    type: str = "CompareAction"


@dataclass
class FilterAction(Action):
    """Select criteria to filter."""
    type: str = "FilterAction"
    items_per_page: Optional[int] = None
    number_of_pages: Optional[int] = None


@dataclass
class SortAction(Action):
    """Sort a list of items."""
    type: str = "SortAction"
    sort_order: Optional[str] = None
    sort_type: Optional[str] = None


@dataclass
class MoveAction(Action):
    """The act of moving."""
    type: str = "MoveAction"
    from_location: Optional[Place] = None
    to_location: Optional[Place] = None
    distance: Optional[QuantitativeValue] = None


@dataclass
class ArriveAction(MoveAction):
    """Arriving at a place."""
    type: str = "ArriveAction"


@dataclass
class DepartAction(MoveAction):
    """Departing from a place."""
    type: str = "DepartAction"


@dataclass
class TravelAction(MoveAction):
    """Traveling to a place."""
    type: str = "TravelAction"


@dataclass
class BoardAction(MoveAction):
    """Boarding a vehicle."""
    type: str = "BoardAction"


@dataclass
class LeaveAction(MoveAction):
    """Leaving a vehicle."""
    type: str = "LeaveAction"


@dataclass
class RideShareAction(MoveAction):
    """Ride sharing."""
    type: str = "RideShareAction"


@dataclass
class OrganizeAction(Action):
    """The act of organizing."""
    type: str = "OrganizeAction"


@dataclass
class AllocateAction(OrganizeAction):
    """Allocating resources."""
    type: str = "AllocateAction"
    purpose: Optional[Thing] = None


@dataclass
class AcceptAction(OrganizeAction):
    """Accepting something."""
    type: str = "AcceptAction"


@dataclass
class AssignAction(OrganizeAction):
    """Assigning something."""
    type: str = "AssignAction"


@dataclass
class AuthorizeAction(OrganizeAction):
    """Authorizing something."""
    type: str = "AuthorizeAction"
    obligation: Optional[Thing] = None


@dataclass
class RejectAction(OrganizeAction):
    """Rejecting something."""
    type: str = "RejectAction"


@dataclass
class JoinAction(OrganizeAction):
    """Joining a group."""
    type: str = "JoinAction"


@dataclass
class LeaveAction(OrganizeAction):
    """Leaving a group."""
    type: str = "LeaveAction"


@dataclass
class SubscribeAction(OrganizeAction):
    """Subscribing to something."""
    type: str = "SubscribeAction"


@dataclass
class RegisterAction(OrganizeAction):
    """Registering something."""
    type: str = "RegisterAction"


@dataclass
class UnregisterAction(OrganizeAction):
    """Unregistering something."""
    type: str = "UnregisterAction"


@dataclass
class PlayAction(Action):
    """Playing an entertainment."""
    type: str = "PlayAction"


@dataclass
class ExerciseAction(PlayAction):
    """Exercising."""
    type: str = "ExerciseAction"
    course: Optional[Place] = None
    distance: Optional[QuantitativeValue] = None


@dataclass
class PerformAction(PlayAction):
    """Performing an entertainment."""
    type: str = "PerformAction"


@dataclass
class RecipeAction(CreateAction):
    """Cooking action."""
    type: str = "RecipeAction"


@dataclass
class SearchAction(Action):
    """Searching for something."""
    type: str = "SearchAction"
    query: Optional[str] = None


@dataclass
class FindAction(SearchAction):
    """Finding something."""
    type: str = "FindAction"


@dataclass
class TrackAction(SearchAction):
    """Tracking an item."""
    type: str = "TrackAction"


@dataclass
class TradeAction(Action):
    """Trading something."""
    type: str = "TradeAction"
    buyer: Optional[Person] = None
    seller: Optional[Person] = None


@dataclass
class BuyAction(TradeAction):
    """Buying something."""
    type: str = "BuyAction"
    seller: Optional[Union[Organization, Person]] = None
    buyer: Optional[Union[Organization, Person]] = None
    price: Optional[Union[float, MonetaryAmount, str]] = None
    price_currency: Optional[str] = None


@dataclass
class PayAction(TradeAction):
    """Paying for something."""
    type: str = "PayAction"
    purpose: Optional[Thing] = None
    recipient: Optional[Union[Organization, Person]] = None


@dataclass
class OrderAction(TradeAction):
    """Ordering something."""
    type: str = "OrderAction"


@dataclass
class DonateAction(TradeAction):
    """Donating something."""
    type: str = "DonateAction"


@dataclass
class TipAction(DonateAction):
    """Tipping someone."""
    type: str = "TipAction"


@dataclass
class TransferAction(Action):
    """Transferring something."""
    type: str = "TransferAction"
    from_location: Optional[Place] = None
    to_location: Optional[Place] = None


@dataclass
class CopyAction(TransferAction):
    """Copying something."""
    type: str = "TransferAction"


@dataclass
class DownloadAction(TransferAction):
    """Downloading something."""
    type: str = "DownloadAction"


@dataclass
class SendAction(TransferAction):
    """Sending something."""
    type: str = "SendAction"
    recipient: Optional[Union[Organization, Person]] = None


@dataclass
class ShareAction(SendAction):
    """Sharing something."""
    type: str = "ShareAction"


@dataclass
class ReceiveAction(TransferAction):
    """Receiving something."""
    type: str = "ReceiveAction"


@dataclass
class ReturnAction(TransferAction):
    """Returning something."""
    type: str = "ReturnAction"


@dataclass
class UpdateAction(Action):
    """Updating something."""
    type: str = "UpdateAction"


@dataclass
class AddAction(UpdateAction):
    """Adding something."""
    type: str = "AddAction"
    target_collection: Optional[Thing] = None


@dataclass
class InsertAction(AddAction):
    """Inserting something."""
    type: str = "InsertAction"


@dataclass
class AppendAction(InsertAction):
    """Appending something."""
    type: str = "AppendAction"


@dataclass
class PrependAction(InsertAction):
    """Prepending something."""
    type: str = "PrependAction"


@dataclass
class InsertAction(AddAction):
    """Inserting data."""
    type: str = "InsertAction"
    position: Optional[int] = None


@dataclass
class RemoveAction(UpdateAction):
    """Removing something."""
    type: str = "RemoveAction"
    removee: Optional[Thing] = None
    from_location: Optional[Place] = None


@dataclass
class DeleteAction(RemoveAction):
    """Deleting something."""
    type: str = "DeleteAction"


@dataclass
class RemoveAction(RemoveAction):
    """Removing from a collection."""
    type: str = "RemoveAction"


@dataclass
class ReplaceAction(UpdateAction):
    """Replacing something."""
    type: str = "ReplaceAction"
    replacee: Optional[Thing] = None
    replacer: Optional[Thing] = None


@dataclass
class SetAction(UpdateAction):
    """Setting a value."""
    type: str = "SetAction"
    object_to_set: Optional[Thing] = None


# =============================================================================
# QUANTITATIVE & VALUE TYPES
# =============================================================================

@dataclass
class QuantitativeValue(Thing):
    """A point value or range."""
    type: str = "QuantitativeValue"
    value: Optional[Union[float, int]] = None
    min_value: Optional[Union[float, int]] = None
    max_value: Optional[Union[float, int]] = None
    unit_code: Optional[str] = None
    unit_text: Optional[str] = None
    value_reference: Optional[QuantitativeValue] = None


@dataclass
class MonetaryAmount(Thing):
    """A monetary amount."""
    type: str = "MonetaryAmount"
    currency: Optional[str] = None
    value: Optional[Union[float, int, Decimal]] = None
    value_added_tax_included: Optional[bool] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None


@dataclass
class PriceSpecification(Thing):
    """A price specification."""
    type: str = "PriceSpecification"
    price: Optional[Union[float, int, Decimal]] = None
    price_currency: Optional[str] = None
    valid_from: Optional[datetime] = None
    valid_through: Optional[datetime] = None
    value_added_tax_included: Optional[bool] = None


@dataclass
class UnitPriceSpecification(PriceSpecification):
    """A unit price specification."""
    type: str = "UnitPriceSpecification"
    price_per_unit: Optional[float] = None
    unit_code: Optional[str] = None


@dataclass
class PropertyValue(Thing):
    """A property-value pair."""
    type: str = "PropertyValue"
    property_id: Optional[str] = None
    value: Optional[Union[str, float, int, bool]] = None
    value_reference: Optional[PropertyValue] = None


@dataclass
class DefinedTerm(Thing):
    """A defined term."""
    type: str = "DefinedTerm"
    term_code: Optional[str] = None


@dataclass
class CategoryCode(DefinedTerm):
    """A category code."""
    type: str = "CategoryCode"
    code_value: Optional[str] = None


@dataclass
class StructuredValue(Thing):
    """A structured value."""
    type: str = "StructuredValue"
    name: Optional[str] = None


@dataclass
class MeasurementType(Thing):
    """A measurement type."""
    type: str = "MeasurementType"
    measurement: Optional[QuantitativeValue] = None
    measurement_method: Optional[str] = None
    measurement_system: Optional[str] = None


@dataclass
class Distance(MeasurementType):
    """A distance measurement."""
    type: str = "Distance"


@dataclass
class Mass(MeasurementType):
    """A mass measurement."""
    type: str = "Mass"


@dataclass
class Energy(MeasurementType):
    """An energy measurement."""
    type: str = "Energy"


@dataclass
class Length(MeasurementType):
    """A length measurement."""
    type: str = "Length"


# =============================================================================
# POSTAL ADDRESS & GEOCOORDINATES
# =============================================================================

@dataclass
class PostalAddress(Thing):
    """A mailing address."""
    type: str = "PostalAddress"
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
    type: str = "GeoCoordinates"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    elevation: Optional[float] = None
    address: Optional[PostalAddress] = None


@dataclass
class GeoShape(Thing):
    """A geographic shape."""
    type: str = "GeoShape"
    address: Optional[PostalAddress] = None
    address_country: Optional[str] = None
    box: Optional[str] = None
    circle: Optional[str] = None
    line: Optional[str] = None
    polygon: Optional[str] = None
    postal_code: Optional[str] = None


@dataclass
class OpeningHoursSpecification(Thing):
    """Opening hours."""
    type: str = "OpeningHoursSpecification"
    day_of_week: Optional[DayOfWeek] = None
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
    type: str = "Rating"
    author: Optional[Union[Organization, Person]] = None
    best_rating: Optional[Union[float, int]] = None
    rating_value: Optional[Union[float, int]] = None
    worst_rating: Optional[Union[float, int]] = None


@dataclass
class AggregateRating(Rating):
    """An aggregate rating."""
    type: str = "AggregateRating"
    rating_count: Optional[int] = None
    review_count: Optional[int] = None
    rating_explanation: Optional[str] = None


# =============================================================================
# ENTRY POINT - For actions
# =============================================================================

@dataclass
class EntryPoint(Thing):
    """An entry point for actions."""
    type: str = "EntryPoint"
    url_template: Optional[str] = None
    action_platform: Optional[Union[str, ActionPlatform]] = None
    content_type: Optional[str] = None
    encoding_type: Optional[str] = None
    http_method: Optional[str] = None
    application: Optional[SoftwareApplication] = None


class ActionPlatform(Enum):
    """Platform for actions."""
    DESKTOP_WEB = "DesktopWebPlatform"
    MOBILE_WEB = "MobileWebPlatform"
    ANDROID = "AndroidPlatform"
    IOS = "iOSPlatform"


# =============================================================================
# PLACE TYPES
# =============================================================================

@dataclass
class Place(Thing):
    """A place."""
    type: str = "Place"
    additional_property: Optional[List[PropertyValue]] = field(default_factory=list)
    address: Optional[PostalAddress] = None
    geo: Optional[GeoCoordinates] = None
    has_map: Optional[str] = None
    is_accessible_for_free: Optional[bool] = False
    opening_hours_specification: Optional[List[OpeningHoursSpecification]] = field(default_factory=list)
    photos: Optional[List[ImageObject]] = field(default_factory=list)
    reviews: Optional[List[Rating]] = field(default_factory=list)
    telephone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    contained_in_place: Optional[Place] = None
    contains_place: Optional[List[Place]] = field(default_factory=list)


@dataclass
class CivicStructure(Place):
    """A civic structure."""
    type: str = "CivicStructure"


@dataclass
class Accommodation(Place):
    """An accommodation."""
    type: str = "Accommodation"
    number_of_rooms: Optional[Union[int, QuantitativeValue]] = None
    permitted_usage: Optional[str] = None
    smoking_allowed: Optional[bool] = False
    bed: Optional[BedDetails] = None
    occupancy: Optional[QuantitativeValue] = None


@dataclass
class BedDetails(Thing):
    """Bed details."""
    type: str = "BedDetails"
    number_of_beds: Optional[int] = None
    type_of_bed: Optional[str] = None


@dataclass
class Hotel(Accommodation):
    """A hotel."""
    type: str = "Hotel"
    star_rating: Optional[AggregateRating] = None


@dataclass
class VacationRental(Accommodation):
    """A vacation rental."""
    type: str = "VacationRental"


@dataclass
class House(Accommodation):
    """A house."""
    type: str = "House"
    number_of_rooms: Optional[int] = None


@dataclass
class Apartment(House):
    """An apartment."""
    type: str = "Apartment"


@dataclass
class SingleFamilyResidence(House):
    """A single family residence."""
    type: str = "SingleFamilyResidence"


@dataclass
class TouristAttraction(Place):
    """A tourist attraction."""
    type: str = "TouristAttraction"
    tourist_type: Optional[str] = None


@dataclass
class TouristDestination(Place):
    """A tourist destination."""
    type: str = "TouristDestination"


@dataclass
class AdministrativeArea(Place):
    """An administrative area."""
    type: str = "AdministrativeArea"
    name: Optional[str] = None


@dataclass
class Country(AdministrativeArea):
    """A country."""
    type: str = "Country"


@dataclass
class State(AdministrativeArea):
    """A state."""
    type: str = "State"


@dataclass
class City(AdministrativeArea):
    """A city."""
    type: str = "City"


@dataclass
class Region(AdministrativeArea):
    """A region."""
    type: str = "Region"


@dataclass
class LocalBusiness(Place):
    """A local business."""
    type: str = "LocalBusiness"
    price_range: Optional[str] = None


@dataclass
class Restaurant(LocalBusiness):
    """A restaurant."""
    type: str = "Restaurant"
    serves_cuisine: Optional[List[str]] = field(default_factory=list)


@dataclass
class LodgingBusiness(LocalBusiness):
    """A lodging business."""
    type: str = "LodgingBusiness"
    star_rating: Optional[AggregateRating] = None
    pets_allowed: Optional[bool] = False


@dataclass
class Airport(Place):
    """An airport."""
    type: str = "Airport"
    iata_code: Optional[str] = None


@dataclass
class BusStation(Place):
    """A bus station."""
    type: str = "BusStation"


@dataclass
class TrainStation(Place):
    """A train station."""
    type: str = "TrainStation"


@dataclass
class Aquarium(Place):
    """An aquarium."""
    type: str = "Aquarium"


@dataclass
class Beach(Place):
    """A beach."""
    type: str = "Beach"


@dataclass
class Bridge(Place):
    """A bridge."""
    type: str = "Bridge"


@dataclass
class Cemetery(Place):
    """A cemetery."""
    type: str = "Cemetery"


@dataclass
class Church(Place):
    """A church."""
    type: str = "Church"


@dataclass
class Crematorium(Place):
    """A crematorium."""
    type: str = "Crematorium"


@dataclass
class EventVenue(Place):
    """An event venue."""
    type: str = "EventVenue"


@dataclass
class GeneralContractor(Place):
    """A general contractor."""
    type: str = "GeneralContractor"


@dataclass
class GovernmentBuilding(Place):
    """A government building."""
    type: str = "GovernmentBuilding"


@dataclass
class Hospital(Place):
    """A hospital."""
    type: str = "Hospital"
    ambulance_service: Optional[bool] = False


@dataclass
class MovieTheater(Place):
    """A movie theater."""
    type: str = "MovieTheater"
    screen_count: Optional[int] = None


@dataclass
class Museum(Place):
    """A museum."""
    type: str = "Museum"


@dataclass
class MusicVenue(Place):
    """A music venue."""
    type: str = "MusicVenue"


@dataclass
class Park(Place):
    """A park."""
    type: str = "Park"


@dataclass
class ParkingFacility(Place):
    """A parking facility."""
    type: str = "ParkingFacility"


@dataclass
class Playground(Place):
    """A playground."""
    type: str = "Playground"


@dataclass
class RVPark(Place):
    """An RV park."""
    type: str = "RVPark"


@dataclass
class Shrine(Place):
    """A shrine."""
    type: str = "Shrine"


@dataclass
class Stadium(Place):
    """A stadium."""
    type: str = "Stadium"


@dataclass
class Synagogue(Place):
    """A synagogue."""
    type: str = "Synagogue"


@dataclass
class TattooParlor(Place):
    """A tattoo parlor."""
    type: str = "TattooParlor"


@dataclass
class TelevisionStation(Place):
    """A television station."""
    type: str = "TelevisionStation"


@dataclass
class TouristAttraction(Place):
    """A tourist attraction."""
    type: str = "TouristAttraction"


# =============================================================================
# ORGANIZATION TYPES
# =============================================================================

@dataclass
class Organization(Thing):
    """An organization."""
    type: str = "Organization"
    legal_name: Optional[str] = None
    logo: Optional[Union[str, ImageObject]] = None
    founding_date: Optional[datetime] = None
    founding_location: Optional[Place] = None
    dissolution_date: Optional[datetime] = None
    number_of_employees: Optional[QuantitativeValue] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    fax_number: Optional[str] = None
    url: Optional[str] = None
    
    # Relationships
    member: Optional[List[Union[Person, Organization]]] = field(default_factory=list)
    member_of: Optional[List[Union[Organization, ProgramMembership]]] = field(default_factory=list)
    number_of_members: Optional[int] = None
    employee: Optional[List[Person]] = field(default_factory=list)
    department: Optional[List[Organization]] = field(default_factory=list)
    parent_organization: Optional[Organization] = None
    sub_organization: Optional[List[Organization]] = field(default_factory=list)
    area_served: Optional[Union[Place, str]] = field(default_factory=list)
    available_service: Optional[List[str]] = field(default_factory=list)
    brand: Optional[Union[Brand, Organization]] = None
    contact_point: Optional[List[ContactPoint]] = field(default_factory=list)
    founder: Optional[Person] = None


@dataclass
class Corporation(Organization):
    """A corporation."""
    type: str = "Corporation"
    ticker_symbol: Optional[str] = None


@dataclass
class GovernmentOrganization(Organization):
    """A government organization."""
    type: str = "GovernmentOrganization"


@dataclass
class NonProfitOrganization(Organization):
    """A non-profit organization."""
    type: str = "NonProfitOrganization"
    registration_number: Optional[str] = None


@dataclass
class Airline(Organization):
    """An airline."""
    type: str = "Airline"
    iata_code: Optional[str] = None


@dataclass
class SportsTeam(Organization):
    """A sports team."""
    type: str = "SportsTeam"
    athlete: Optional[List[Person]] = field(default_factory=list)


@dataclass
class LocalBusiness(Organization):
    """A local business."""
    type: str = "LocalBusiness"
    area_served: Optional[Place] = None
    location: Optional[Union[Place, PostalAddress]] = None
    opening_hours_specification: Optional[List[OpeningHoursSpecification]] = field(default_factory=list)
    price_range: Optional[str] = None


@dataclass
class Restaurant(LocalBusiness):
    """A restaurant."""
    type: str = "Restaurant"
    serves_cuisine: Optional[List[str]] = field(default_factory=list)


@dataclass
class Hotel(LocalBusiness):
    """A hotel."""
    type: str = "Hotel"


@dataclass
class LodgingBusiness(LocalBusiness):
    """A lodging business."""
    type: str = "LodgingBusiness"
    amenity: Optional[List[str]] = field(default_factory=list)


@dataclass
class Brand(Thing):
    """A brand."""
    type: str = "Brand"
    logo: Optional[Union[str, ImageObject]] = None
    aggregate_rating: Optional[AggregateRating] = None


@dataclass
class ContactPoint(Thing):
    """A contact point."""
    type: str = "ContactPoint"
    telephone: Optional[str] = None
    fax_number: Optional[str] = None
    email: Optional[str] = None
    contact_type: Optional[str] = None
    available_language: Optional[List[str]] = field(default_factory=list)
    product_supported: Optional[Union[Product, str]] = None


# =============================================================================
# PERSON TYPES
# =============================================================================

@dataclass
class Person(Thing):
    """A person."""
    type: str = "Person"
    additional_name: Optional[List[str]] = field(default_factory=list)
    address: Optional[Union[PostalAddress, str]] = None
    affiliation: Optional[List[Organization]] = field(default_factory=list)
    award: Optional[List[str]] = field(default_factory=list)
    birth_date: Optional[datetime] = None
    birth_place: Optional[Place] = None
    brand: Optional[Union[Brand, Organization]] = None
    children: Optional[List[Person]] = field(default_factory=list)
    colleague: Optional[List[Person]] = field(default_factory=list)
    death_date: Optional[datetime] = None
    death_place: Optional[Place] = None
    email: Optional[str] = None
    family_name: Optional[str] = None
    fax_number: Optional[str] = None
    follows: Optional[List[Person]] = field(default_factory=list)
    gender: Optional[str] = None
    given_name: Optional[str] = None
    job_title: Optional[str] = None
    knows: Optional[List[Person]] = field(default_factory=list)
    knows_about: Optional[List[Union[str, Thing]]] = field(default_factory=list)
    knows_language: Optional[List[str]] = field(default_factory=list)
    member_of: Optional[List[Union[Organization, ProgramMembership]]] = field(default_factory=list)
    nationality: Optional[str] = None
    owns: Optional[List[Product]] = field(default_factory=list)
    performer_in: Optional[Event] = None
    related_to: Optional[List[Person]] = field(default_factory=list)
    relative: Optional[List[Person]] = field(default_factory=list)
    sibling: Optional[List[Person]] = field(default_factory=list)
    sponsor: Optional[Union[Organization, str]] = None
    spouse: Optional[Person] = None
    tax_id: Optional[str] = None
    telephone: Optional[str] = None
    url: Optional[str] = None
    weight: Optional[QuantitativeValue] = None
    works_for: Optional[List[Organization]] = field(default_factory=list)
    alumni: Optional[List[Person]] = field(default_factory=list)


# =============================================================================
# PRODUCT TYPES
# =============================================================================

@dataclass
class Product(Thing):
    """A product."""
    type: str = "Product"
    additional_property: Optional[List[PropertyValue]] = field(default_factory=list)
    aggregate_rating: Optional[AggregateRating] = None
    is_accessory_or_spare_part_for: Optional[Product] = None
    is_related_to: Optional[List[Product]] = field(default_factory=list)
    is_similar_to: Optional[List[Product]] = field(default_factory=list)
    is_bundle: Optional[bool] = False
    item_condition: Optional[OfferItemCondition] = None
    manufacturer: Optional[Organization] = None
    model: Optional[Union[ProductModel, str]] = None
    product_id: Optional[str] = None
    production_date: Optional[datetime] = None
    purchase_date: Optional[datetime] = None
    release_date: Optional[datetime] = None
    review: Optional[List[Rating]] = field(default_factory=list)
    sku: Optional[str] = None
    gtin: Optional[str] = None
    color: Optional[str] = None
    weight: Optional[QuantitativeValue] = None
    height: Optional[QuantitativeValue] = None
    width: Optional[QuantitativeValue] = None
    depth: Optional[QuantitativeValue] = None
    offers: Optional[List[Offer]] = field(default_factory=list)
    category: Optional[List[str]] = field(default_factory=list)
    brand: Optional[Union[Brand, Organization, str]] = None


@dataclass
class ProductModel(Product):
    """A product model."""
    type: str = "ProductModel"
    is_variant_of: Optional[ProductModel] = None
    predecessor_of: Optional[ProductModel] = None
    successor_of: Optional[ProductModel] = None


@dataclass
class SomeProducts(Product):
    """A product collection."""
    type: str = "SomeProducts"
    number_of_items: Optional[int] = None


@dataclass
class Offer(Thing):
    """An offer."""
    type: str = "Offer"
    accepted_payment_method: Optional[PaymentMethod] = None
    additional_property: Optional[List[PropertyValue]] = field(default_factory=list)
    add_on: Optional[Offer] = None
    aggregate_rating: Optional[AggregateRating] = None
    availability: Optional[ItemAvailability] = None
    availability_starts: Optional[datetime] = None
    availability_ends: Optional[datetime] = None
    business_function: Optional[str] = None
    delivery_method: Optional[DeliveryMethod] = None
    inventory_level: Optional[QuantitativeValue] = None
    item_condition: Optional[OfferItemCondition] = None
    item_offered: Optional[Union[Product, Service]] = None
    price: Optional[Union[float, int, Decimal, str]] = None
    price_currency: Optional[str] = None
    price_specification: Optional[PriceSpecification] = None
    valid_from: Optional[datetime] = None
    valid_through: Optional[datetime] = None
    high_price: Optional[Union[float, str]] = None
    low_price: Optional[Union[float, str]] = None
    url: Optional[str] = None
    seller: Optional[Union[Organization, Person]] = None


@dataclass
class AggregateOffer(Offer):
    """An aggregate offer."""
    type: str = "AggregateOffer"
    low_price: Optional[Union[float, Decimal]] = None
    high_price: Optional[Union[float, Decimal]] = None
    offer_count: Optional[int] = None


@dataclass
class Demand(Thing):
    """A demand."""
    type: str = "Demand"
    accepted_payment_method: Optional[PaymentMethod] = None
    availability: Optional[ItemAvailability] = None
    item_offered: Optional[Union[Product, Service]] = None
    valid_from: Optional[datetime] = None
    valid_through: Optional[datetime] = None


# =============================================================================
# SERVICE TYPES
# =============================================================================

@dataclass
class Service(Thing):
    """A service."""
    type: str = "Service"
    provider: Optional[Union[Organization, Person]] = None
    provider_mobility: Optional[str] = None
    area_served: Optional[Union[Place, str]] = field(default_factory=list)
    available_channel: Optional[ServiceChannel] = None
    category: Optional[Union[CategoryCode, str]] = None
    has_credential: Optional[Union[str, DefinedTerm]] = None
    logo: Optional[Union[ImageObject, str]] = None
    official_rating: Optional[Rating] = None
    produces: Optional[List[Union[Product, Thing]]] = field(default_factory=list)
    service_type: Optional[str] = None
    review: Optional[List[Rating]] = field(default_factory=list)
    offers: Optional[List[Offer]] = field(default_factory=list)


@dataclass
class ServiceChannel(Thing):
    """A service channel."""
    type: str = "ServiceChannel"
    availability_ends: Optional[datetime] = None
    available_from: Optional[datetime] = None
    provider: Optional[Union[Organization, Person]] = None
    serves: Optional[List[Product]] = field(default_factory=list)
    url: Optional[str] = None


@dataclass
class FinancialProduct(Service):
    """A financial product."""
    type: str = "FinancialProduct"
    annual_percentage_rate: Optional[Union[float, QuantitativeValue]] = None
    interest_rate: Optional[Union[float, QuantitativeValue]] = None


@dataclass
class BankAccount(FinancialProduct):
    """A bank account."""
    type: str = "BankAccount"
    account_minimum_balance: Optional[Union[int, QuantitativeValue]] = None


@dataclass
class LoanOrCredit(FinancialProduct):
    """A loan or credit."""
    type: str = "LoanOrCredit"
    amount: Optional[Union[int, MonetaryAmount, PriceSpecification]] = None
    required_credit_score: Optional[int] = None
    loan_term: Optional[QuantitativeValue] = None


@dataclass
class PaymentCard(FinancialProduct):
    """A payment card."""
    type: str = "PaymentCard"
    card_issuer: Optional[Organization] = None
    annual_fee: Optional[MonetaryAmount] = None


# =============================================================================
# EVENT TYPES
# =============================================================================

@dataclass
class Event(Thing):
    """An event."""
    type: str = "Event"
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
    previous_event: Optional[Event] = None
    next_event: Optional[Event] = None
    maximum_attendee_capacity: Optional[int] = None
    typical_age_range: Optional[str] = None
    in_language: Optional[str] = None
    attendee: Optional[List[Union[Organization, Person]]] = field(default_factory=list)


@dataclass
class PublicationEvent(Event):
    """A publication event."""
    type: str = "PublicationEvent"
    published_on: Optional[BroadcastEvent] = None


@dataclass
class BroadcastEvent(Event):
    """A broadcast event."""
    type: str = "BroadcastEvent"
    is_broadcast_of: Optional[BroadcastService] = None


@dataclass
class BroadcastService(Thing):
    """A broadcast service."""
    type: str = "BroadcastService"
    name: Optional[str] = None
    provider: Optional[Union[Organization, Person]] = None


@dataclass
class Course(Event):
    """A course."""
    type: str = "Course"
    course_code: Optional[str] = None
    has_course_instance: Optional[List[CourseInstance]] = field(default_factory=list)
    number_of_credits: Optional[int] = None


@dataclass
class CourseInstance(Event):
    """A course instance."""
    type: str = "CourseInstance"
    course_mode: Optional[str] = None
    course_workload: Optional[str] = None
    instructor: Optional[Person] = None


@dataclass
class ExhibitionEvent(Event):
    """An exhibition event."""
    type: str = "ExhibitionEvent"


@dataclass
class Festival(Event):
    """A festival."""
    type: str = "Festival"


@dataclass
class MusicEvent(Event):
    """A music event."""
    type: str = "MusicEvent"


@dataclass
class PerformingArtsEvent(Event):
    """A performing arts event."""
    type: str = "PerformingArtsEvent"


@dataclass
class SportsEvent(Event):
    """A sports event."""
    type: str = "SportsEvent"


@dataclass
class ComedyEvent(Event):
    """A comedy event."""
    type: str = "ComedyEvent"


@dataclass
class CourseInstance(Event):
    """A course instance."""
    type: str = "CourseInstance"


# =============================================================================
# CREATIVE WORK TYPES
# =============================================================================

@dataclass
class CreativeWork(Thing):
    """A creative work."""
    type: str = "CreativeWork"
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
    encoding: Optional[List[MediaObject]] = field(default_factory=list)
    file_format: Optional[List[str]] = field(default_factory=list)
    content_rating: Optional[str] = None
    aggregate_rating: Optional[AggregateRating] = None
    review: Optional[List[Rating]] = field(default_factory=list)
    
    # Creator
    author: Optional[List[Union[Person, Organization]]] = field(default_factory=list)
    contributor: Optional[List[Union[Person, Organization]]] = field(default_factory=list)
    creator: Optional[Union[Person, Organization]] = None
    editor: Optional[List[Person]] = field(default_factory=list)
    publisher: Optional[Organization] = None
    provider: Optional[Union[Organization, Person]] = None
    
    # Content
    about: Optional[Thing] = None
    associated_media: Optional[List[MediaObject]] = field(default_factory=list)
    citation: Optional[List[str]] = field(default_factory=list)
    comment: Optional[List[Comment]] = field(default_factory=list)
    comment_count: Optional[int] = None
    
    # Relations
    has_part: Optional[List[CreativeWork]] = field(default_factory=list)
    is_part_of: Optional[CreativeWork] = None
    mentions: Optional[List[Thing]] = field(default_factory=list)


@dataclass
class Article(CreativeWork):
    """An article."""
    type: str = "Article"
    article_section: Optional[str] = None
    article_body: Optional[str] = None
    page_end: Optional[int] = None
    page_start: Optional[int] = None
    word_count: Optional[int] = None


@dataclass
class BlogPosting(Article):
    """A blog posting."""
    type: str = "BlogPosting"
    audio: Optional[Union[MusicGroup, AudioObject]] = None
    video: Optional[VideoObject] = None


@dataclass
class NewsArticle(Article):
    """A news article."""
    type: str = "NewsArticle"
    dateline: Optional[str] = None
    print_column: Optional[str] = None
    print_page: Optional[str] = None


@dataclass
class Report(NewsArticle):
    """A report."""
    type: str = "Report"
    page: Optional[str] = None


@dataclass
class SocialMediaPosting(Article):
    """A social media post."""
    type: str = "SocialMediaPosting"
    speech_to_date: Optional[datetime] = None


@dataclass
class BlogPost(CreativeWork):
    """A blog post."""
    type: str = "BlogPost"


@dataclass
class Comment(CreativeWork):
    """A comment."""
    type: str = "Comment"
    downvote: Optional[int] = None
    upvote: Optional[int] = None
    parent_item: Optional[Comment] = None


@dataclass
class Review(CreativeWork):
    """A review."""
    type: str = "Review"
    review_rating: Optional[Rating] = None
    review_body: Optional[str] = None
    item_reviewed: Optional[Thing] = None
    reviewer: Optional[Union[Person, Organization]] = None


@dataclass
class Clip(VideoObject):
    """A clip."""
    type: str = "Clip"
    part_of_episode: Optional[Episode] = None
    part_of_season: Optional[Season] = None


@dataclass
class TVEpisode(VideoObject):
    """A TV episode."""
    type: str = "TVEpisode"
    episode_number: Optional[int] = None
    part_of_tv_series: Optional[TVSeries] = None


@dataclass
class Movie(VideoObject):
    """A movie."""
    type: str = "Movie"
    duration: Optional[timedelta] = None
    director: Optional[Person] = None
    actor: Optional[List[Person]] = field(default_factory=list)
    music_by: Optional[Union[Person, Organization]] = None


@dataclass
class TVSeries(CreativeWork):
    """A TV series."""
    type: str = "TVSeries"
    actor: Optional[List[Person]] = field(default_factory=list)
    director: Optional[List[Person]] = field(default_factory=list)
    episode: Optional[List[Episode]] = field(default_factory=list)
    season: Optional[List[Season]] = field(default_factory=list)
    number_of_seasons: Optional[int] = None
    number_of_episodes: Optional[int] = None


@dataclass
class Episode(CreativeWork):
    """An episode."""
    type: str = "Episode"
    episode_number: Optional[int] = None
    part_of_season: Optional[Season] = None
    part_of_tv_series: Optional[TVSeries] = None


@dataclass
class Season(CreativeWork):
    """A season."""
    type: str = "Season"
    season_number: Optional[int] = None
    part_of_tv_series: Optional[TVSeries] = None


@dataclass
class MovieSeries(CreativeWork):
    """A movie series."""
    type: str = "MovieSeries"
    contains: Optional[List[Movie]] = field(default_factory=list)


@dataclass
class Book(CreativeWork):
    """A book."""
    type: str = "Book"
    book_edition: Optional[str] = None
    number_of_pages: Optional[int] = None


@dataclass
class ComicIssue(CreativeWork):
    """A comic issue."""
    type: str = "ComicIssue"
    penciler: Optional[Person] = None
    colorist: Optional[Person] = None
    inker: Optional[Person] = None
    letterer: Optional[Person] = None


@dataclass
class ComicSeries(CreativeWork):
    """A comic series."""
    type: str = "ComicSeries"


@dataclass
class CoverArt(CreativeWork):
    """Cover art."""
    type: str = "CoverArt"


@dataclass
class Manuscript(CreativeWork):
    """A manuscript."""
    type: str = "Manuscript"


# =============================================================================
# MEDIA TYPES
# =============================================================================

@dataclass
class MediaObject(CreativeWork):
    """A media object."""
    type: str = "MediaObject"
    content_url: Optional[str] = None
    embed_url: Optional[str] = None
    upload_date: Optional[datetime] = None
    content_size: Optional[str] = None
    content_duration: Optional[timedelta] = None
    encoding_format: Optional[str] = None
    bitrate: Optional[str] = None


@dataclass
class ImageObject(MediaObject):
    """An image."""
    type: str = "ImageObject"
    caption: Optional[str] = None
    exif_data: Optional[str] = None
    representative_of_page: Optional[bool] = False
    thumbnail: Optional[ImageObject] = None


@dataclass
class Photograph(ImageObject):
    """A photograph."""
    type: str = "Photograph"


@dataclass
class AudioObject(MediaObject):
    """An audio object."""
    type: str = "AudioObject"
    transcript: Optional[str] = None


@dataclass
class VideoObject(MediaObject):
    """A video object."""
    type: str = "VideoObject"
    caption: Optional[str] = None
    video_frame_size: Optional[str] = None
    video_quality: Optional[str] = None
    actor: Optional[List[Person]] = field(default_factory=list)
    director: Optional[Person] = None
    music_by: Optional[Union[Person, Organization]] = None
    thumbnail: Optional[ImageObject] = None


@dataclass
class Audiobook(AudioObject):
    """An audiobook."""
    type: str = "Audiobook"
    duration: Optional[timedelta] = None


@dataclass
class DataDownload(MediaObject):
    """A data download."""
    type: str = "DataDownload"


# =============================================================================
# SOFTWARE TYPES
# =============================================================================

@dataclass
class SoftwareApplication(CreativeWork):
    """A software application."""
    type: str = "SoftwareApplication"
    application_category: Optional[str] = None
    application_sub_category: Optional[str] = None
    application_suite: Optional[str] = None
    available_on: Optional[Product] = None
    file_size: Optional[str] = None


@dataclass
class SoftwareSourceCode(CreativeWork):
    """Software source code."""
    type: str = "SoftwareSourceCode"
    runtime: Optional[str] = None
    programming_language: Optional[Union[ProgrammingLanguage, str]] = None
    code_repository: Optional[str] = None
    date_created: Optional[datetime] = None


@dataclass
class ProgrammingLanguage(Thing):
    """A programming language."""
    type: str = "ProgrammingLanguage"
    alias: Optional[List[str]] = field(default_factory=list)


@dataclass
class WebApplication(SoftwareApplication):
    """A web application."""
    type: str = "WebApplication"
    browser_requirements: Optional[str] = None


@dataclass
class VideoGame(SoftwareApplication):
    """A video game."""
    type: str = "VideoGame"
    cheat_code: Optional[str] = None
    game_server: Optional[Thing] = None
    genre: Optional[Union[str, CreativeWork]] = None


# =============================================================================
# MUSIC TYPES
# =============================================================================

@dataclass
class MusicGroup(CreativeWork):
    """A music group."""
    type: str = "MusicGroup"
    member: Optional[List[Union[Person, Organization]]] = field(default_factory=list)
    genre: Optional[List[str]] = field(default_factory=list)


@dataclass
class MusicAlbum(CreativeWork):
    """A music album."""
    type: str = "MusicAlbum"
    album_production_type: Optional[str] = None
    album_release_type: Optional[str] = None
    by_artist: Optional[MusicGroup] = None
    num_tracks: Optional[int] = None


@dataclass
class MusicRecording(CreativeWork):
    """A music recording."""
    type: str = "MusicRecording"
    album: Optional[MusicAlbum] = None
    by_artist: Optional[Union[MusicGroup, Person]] = None
    duration: Optional[timedelta] = None
    isrc_code: Optional[str] = None


@dataclass
class MusicComposition(CreativeWork):
    """A music composition."""
    type: str = "MusicComposition"
    composer: Optional[Union[Organization, Person]] = None
    first_performance: Optional[Event] = None
    iswc_code: Optional[str] = None


@dataclass
class Playlist(CreativeWork):
    """A playlist."""
    type: str = "Playlist"
    track: Optional[List[MusicRecording]] = field(default_factory=list)


@dataclass
class MusicPlaylist(Playlist):
    """A music playlist."""
    type: str = "MusicPlaylist"


# =============================================================================
# RECIPE TYPES
# =============================================================================

@dataclass
class HowTo(HowToStep):
    """A how-to."""
    type: str = "HowTo"
    step: Optional[List[HowToStep]] = field(default_factory=list)
    total_time: Optional[timedelta] = None


@dataclass
class HowToStep(Thing):
    """A step in a how-to."""
    type: str = "HowToStep"
    name: Optional[str] = None
    text: Optional[str] = None
    url: Optional[str] = None
    image: Optional[Union[str, ImageObject]] = None


@dataclass
class Recipe(HowTo):
    """A recipe."""
    type: str = "Recipe"
    cook_time: Optional[timedelta] = None
    prep_time: Optional[timedelta] = None
    recipe_yield: Optional[Union[int, List[str]]] = None
    ingredients: Optional[List[str]] = field(default_factory=list)
    nutrition: Optional[NutritionInformation] = None
    recipe_category: Optional[str] = None
    recipe_cuisine: Optional[str] = None
    suitable_for_diet: Optional[RestrictedDiet] = None


@dataclass
class NutritionInformation(Thing):
    """Nutrition information."""
    type: str = "NutritionInformation"
    serving_size: Optional[str] = None
    calories: Optional[QuantitativeValue] = None
    carbohydrate_content: Optional[QuantitativeValue] = None
    cholesterol_content: Optional[QuantitativeValue] = None
    fat_content: Optional[QuantitativeValue] = None
    fiber_content: Optional[QuantitativeValue] = None
    protein_content: Optional[QuantitativeValue] = None
    sodium_content: Optional[QuantitativeValue] = None
    sugar_content: Optional[QuantitativeValue] = None


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
    type: str = "Reservation"
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
    under_name: Optional[Union[Person, Organization]] = None


@dataclass
class FlightReservation(Reservation):
    """A flight reservation."""
    type: str = "FlightReservation"
    boarding_group: Optional[str] = None
    passenger_priority_status: Optional[str] = None
    security_wait: Optional[int] = None
    departure_airport: Optional[Place] = None
    arrival_airport: Optional[Place] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None


@dataclass
class LodgingReservation(Reservation):
    """A lodging reservation."""
    type: str = "LodgingReservation"
    checkin_time: Optional[datetime] = None
    checkout_time: Optional[datetime] = None
    lodging_unit: Optional[str] = None
    num_guests: Optional[int] = None


@dataclass
class TaxiReservation(Reservation):
    """A taxi reservation."""
    type: str = "TaxiReservation"
    pickup_time: Optional[datetime] = None
    pickup_location: Optional[Place] = None


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


@dataclass
class Order(Thing):
    """An order."""
    type: str = "Order"
    accepted_offer: Optional[Offer] = None
    billing_address: Optional[PostalAddress] = None
    broker: Optional[Union[Organization, Person]] = None
    confirmation_number: Optional[str] = None
    customer: Optional[Union[Organization, Person]] = None
    discount: Optional[Union[float, str]] = None
    is_gift: Optional[bool] = False
    order_date: Optional[datetime] = None
    order_item: Optional[List[OrderItem]] = field(default_factory=list)
    order_number: Optional[str] = None
    order_status: Optional[OrderStatusType] = None
    seller: Optional[Union[Organization, Person]] = None
    total_payment_due: Optional[Union[float, MonetaryAmount]] = None


@dataclass
class OrderItem(Thing):
    """An order item."""
    type: str = "OrderItem"
    order_delivery: Optional[ParcelDelivery] = None
    order_item_number: Optional[str] = None
    ordered_item: Optional[Union[Product, Service]] = None
    quantity: Optional[int] = None


@dataclass
class ParcelDelivery(Thing):
    """A parcel delivery."""
    type: str = "ParcelDelivery"
    delivery_address: Optional[PostalAddress] = None
    delivery_date: Optional[datetime] = None
    carrier: Optional[Organization] = None
    has_tracking_number: Optional[str] = None
    origin_address: Optional[PostalAddress] = None
    tracking_url: Optional[str] = None


@dataclass
class Invoice(Thing):
    """An invoice."""
    type: str = "Invoice"
    account_number: Optional[str] = None
    billing_period: Optional[str] = None
    broker: Optional[Union[Organization, Person]] = None
    customer: Optional[Union[Organization, Person]] = None
    discount: Optional[Union[float, str]] = None
    due_date: Optional[datetime] = None
    minimum_payment_due: Optional[MonetaryAmount] = None
    payment_due: Optional[datetime] = None
    payment_method: Optional[PaymentMethod] = None
    payment_status: Optional[str] = None
    total_payment_due: Optional[MonetaryAmount] = None
    transaction_id: Optional[str] = None


# =============================================================================
# PROGRAM MEMBERSHIP
# =============================================================================

@dataclass
class ProgramMembership(Thing):
    """A program membership."""
    type: str = "ProgramMembership"
    member_number: Optional[str] = None
    program_name: Optional[str] = None
    member: Optional[Organization] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


# =============================================================================
# JOB POSTING
# =============================================================================

@dataclass
class JobPosting(Thing):
    """A job posting."""
    type: str = "JobPosting"
    date_posted: Optional[datetime] = None
    base_salary: Optional[Union[float, MonetaryAmount, PriceSpecification]] = None
    direct_application: Optional[bool] = False
    employment_type: Optional[str] = None
    hiring_organization: Optional[Organization] = None
    industry: Optional[str] = None
    job_location: Optional[Place] = None
    occupational_category: Optional[str] = None
    qualifications: Optional[str] = None
    responsibilities: Optional[str] = None
    security_clearance_requirement: Optional[str] = None
    work_hours: Optional[str] = None


# =============================================================================
# FLIGHT & TRANSPORT
# =============================================================================

@dataclass
class Flight(Thing):
    """A flight."""
    type: str = "Flight"
    flight_number: Optional[str] = None
    airline: Optional[Organization] = None
    departure_airport: Optional[Place] = None
    departure_time: Optional[datetime] = None
    arrival_airport: Optional[Place] = None
    arrival_time: Optional[datetime] = None
    arrival_terminal: Optional[str] = None
    departure_terminal: Optional[str] = None


@dataclass
class TrainTrip(Thing):
    """A train trip."""
    type: str = "TrainTrip"
    arrival_station: Optional[Place] = None
    arrival_time: Optional[datetime] = None
    departure_station: Optional[Place] = None
    departure_time: Optional[datetime] = None
    train_name: Optional[str] = None


@dataclass
class BusTrip(Thing):
    """A bus trip."""
    type: str = "BusTrip"
    arrival_bus_station: Optional[Place] = None
    arrival_time: Optional[datetime] = None
    departure_bus_station: Optional[Place] = None
    departure_time: Optional[datetime] = None
    bus_name: Optional[str] = None
    bus_number: Optional[str] = None


@dataclass
class Vehicle(Thing):
    """A vehicle."""
    type: str = "Vehicle"
    vehicle_identification_number: Optional[str] = None
    vehicle_config: Optional[str] = None
    vehicle_interior_type: Optional[str] = None
    vehicle_number_of_wheels: Optional[int] = None


@dataclass
class Car(Vehicle):
    """A car."""
    type: str = "Car"


@dataclass
class Bus(Vehicle):
    """A bus."""
    type: str = "Bus"


@dataclass
class Motorcycle(Vehicle):
    """A motorcycle."""
    type: str = "Motorcycle"


@dataclass
class Bicycle(Vehicle):
    """A bicycle."""
    type: str = "Bicycle"


# =============================================================================
# WEB CONTENT
# =============================================================================

@dataclass
class WebPage(CreativeWork):
    """A web page."""
    type: str = "WebPage"
    is_part_of: Optional[WebSite] = None
    primary_image_of_page: Optional[ImageObject] = None
    related_link: Optional[List[str]] = field(default_factory=list)


@dataclass
class WebSite(Thing):
    """A web site."""
    type: str = "WebSite"
    url: Optional[str] = None


@dataclass
class FAQPage(WebPage):
    """An FAQ page."""
    type: str = "FAQPage"


@dataclass
class AboutPage(WebPage):
    """An about page."""
    type: str = "AboutPage"


@dataclass
class CheckoutPage(WebPage):
    """A checkout page."""
    type: str = "CheckoutPage"


@dataclass
class CollectionPage(WebPage):
    """A collection page."""
    type: str = "CollectionPage"


@dataclass
class ContactPage(WebPage):
    """A contact page."""
    type: str = "ContactPage"


@dataclass
class ContentPage(WebPage):
    """A content page."""
    type: str = "ContentPage"


@dataclass
class FAQPage(WebPage):
    """An FAQ page."""
    type: str = "FAQPage"


@dataclass
class ProfilePage(WebPage):
    """A profile page."""
    type: str = "ProfilePage"


@dataclass
class QAPage(WebPage):
    """A Q&A page."""
    type: str = "QAPage"


@dataclass
class RecipePage(WebPage):
    """A recipe page."""
    type: str = "RecipePage"


@dataclass
class SearchResultsPage(WebPage):
    """A search results page."""
    type: str = "SearchResultsPage"


# =============================================================================
# QUESTION & ANSWER
# =============================================================================

@dataclass
class Question(CreativeWork):
    """A question."""
    type: str = "Question"
    answer_count: Optional[int] = None
    upvote_count: Optional[int] = None
    downvote_count: Optional[int] = None
    suggested_answer: Optional[List[Answer]] = field(default_factory=list)


@dataclass
class Answer(CreativeWork):
    """An answer."""
    type: str = "Answer"
    upvote_count: Optional[int] = None
    downvote_count: Optional[int] = None


# =============================================================================
# ABOUT THIS FILE
# =============================================================================

"""
Schema.org Things and Actions - Complete Implementation

This module provides proper Schema.org types using:
- Thing as base class with @context and @type
- Action with all action types (Create, Delete, Update, etc.)
- All major Schema.org types

Usage:
    from schema_org import Person, Organization, Product, BuyAction
    
    # Create a person
    person = Person(
        id="https://example.com/people/john",
        name="John Doe",
        email="john@example.com"
    )
    
    # Create an action (buy)
    buy = BuyAction(
        id="https://example.com/actions/buy-001",
        agent=person,
        object=product,
        price=99.99,
        price_currency="USD"
    )
    
    # Export as JSON-LD
    print(buy.to_jsonld())

References:
    - Schema.org: https://schema.org/docs/schemas.html
    - Action: https://schema.org/Action
    - Thing: https://schema.org/Thing
"""
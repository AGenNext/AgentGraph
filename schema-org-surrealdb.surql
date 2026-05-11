/**
 * SurrealDB Schema for Schema.org
 * 
 * SurrealDB is a cloud-native multi-model database supporting:
 * - Document (JSON)
 * - Graph (edges/vertices)
 * - Time-series
 * - Key-value
 * - Full-text search
 * 
 * This schema uses SurrealDB's native features:
 * - DEFINE for schema
 * - SCHEMAFULL for type safety
 * -Embedded graph edges
 * - TIME SERIES tables
 * - ANALYZERS for FTS
 * 
 * Source: https://surrealdb.com/docs/surrealdb/reference-guide
 */

// =============================================================================
// DATABASE CONFIGURATION
// =============================================================================

// Define namespace and database
DEFINE NAMESPACE schema_org;
DEFINE DATABASE schema_store;

// =============================================================================
// TYPE DEFINITIONS - Schema.org enums
// =============================================================================

DEFINE TYPE enum OfferItemCondition SCHEMAFULL (
  "NewCondition", 
  "RefurbishedCondition", 
  "UsedCondition", 
  "DamagedCondition", 
  "DiscontinuedCondition"
);

DEFINE TYPE enum ItemAvailability SCHEMAFULL (
  "InStock", 
  "InStoreOnly", 
  "OnlineOnly", 
  "OutOfStock", 
  "PreOrder", 
  "BackOrder", 
  "Discontinued", 
  "LimitedAvailability", 
  "SoldOut"
);

DEFINE TYPE enum EventStatusType SCHEMAFULL (
  "EventScheduled", 
  "EventCancelled", 
  "EventMovedOnline", 
  "EventPostponed", 
  "EventRescheduled"
);

DEFINE TYPE enum EventAttendanceMode SCHEMAFULL (
  "OfflineEventAttendanceMode", 
  "OnlineEventAttendanceMode", 
  "MixedEventAttendanceMode"
);

DEFINE TYPE enum DayOfWeek SCHEMAFULL (
  "Monday", 
  "Tuesday", 
  "Wednesday", 
  "Thursday", 
  "Friday", 
  "Saturday", 
  "Sunday"
);

// =============================================================================
// FULL-TEXT SEARCH ANALYZERS
// =============================================================================

// Default text analyzer with stemming
DEFINE ANALYZER schema_default TOKENIZERS blank, class FILTERS ascii, lower, porterstem(1) SCHEMALESS;

// Exact match for codes (SKU, GTIN, ISBN)
DEFINE ANALYZER schema_exact TOKENIZERS identity SCHEMALESS;

// Autocomplete analyzer
DEFINE ANALYZER schema_autocomplete TOKENIZERS blank FILTERS ascii, lower, ngram(1, 2) SCHEMALESS;

// Email analyzer
DEFINE ANALYZER schema_email TOKENIZERS blank FILTERS ascii, lower SCHEMALESS;

// =============================================================================
// SCHEMA DOCxENTS - Core entity storage (document model)
// =============================================================================

/**
 * Thing - Base schema for all Schema.org entities
 * SurrealDB automatically handles inheritance
 */
DEFINE TABLE thing SCHEMAFULL;

DEFINE FIELD thing._tenant ON TABLE thing TYPE option<string>;
DEFINE FIELD thing._created_at ON TABLE thing TYPE datetime DEFAULT time::now();
DEFINE FIELD thing._updated_at ON TABLE thing TYPE datetime DEFAULT time::now();
DEFINE FIELD thing._created_by ON TABLE thing TYPE option<string>;
DEFINE FIELD thing._updated_by ON TABLE thing TYPE option<string>;

DEFINE FIELD thing.id ON TABLE thing TYPE string;
DEFINE FIELD thing.name ON TABLE thing TYPE string;
DEFINE FIELD thing.description ON TABLE thing TYPE option<string>;
DEFINE FIELD thing.alternateName ON TABLE thing TYPE option<array<string>>;
DEFINE FIELD thing.disambiguatingDescription ON TABLE thing TYPE option<string>;
DEFINE FIELD thing.url ON TABLE thing TYPE option<string>;
DEFINE FIELD thing.image ON TABLE thing TYPE option<object>;

DEFINE INDEX thing._tenant ON TABLE thing FIELDS _tenant;
DEFINE INDEX thing.id ON TABLE thing FIELDS id UNIQUE;

// =============================================================================

/**
 * Person - Schema.org Person type
 * Extends Thing with person-specific fields
 */
DEFINE TABLE person SCHEMAFULL EXTENDS thing;

DEFINE FIELD person.additionalName ON TABLE person TYPE option<array<string>>;
DEFINE FIELD person.familyName ON TABLE person TYPE option<string>;
DEFINE FIELD person.givenName ON TABLE person TYPE option<string>;
DEFINE FIELD person.honorificPrefix ON TABLE person TYPE option<string>;
DEFINE FIELD person.honorificSuffix ON TABLE person TYPE option<string>;
DEFINE FIELD person.jobTitle ON TABLE person TYPE option<string>;
DEFINE FIELD person.birthDate ON TABLE person TYPE option<datetime>;
DEFINE FIELD person.deathDate ON TABLE person TYPE option<datetime>;
DEFINE FIELD person.gender ON TABLE person TYPE option<string>;
DEFINE FIELD person.nationality ON TABLE person TYPE option<string>;
DEFINE FIELD person.email ON TABLE person TYPE option<string>;
DEFINE FIELD person.telephone ON TABLE person TYPE option<string>;
DEFINE FIELD person.faxNumber ON TABLE person TYPE option<string>;
DEFINE FIELD person.taxID ON TABLE person TYPE option<string>;
DEFINE FIELD person.knowsLanguage ON TABLE person TYPE option<array<object>>;

DEFINE FIELD person.address ON TABLE person TYPE option<record(postal_address)>;
DEFINE FIELD person.spouse ON TABLE person TYPE option<record(person)>;
DEFINE FIELD person.parent ON TABLE person TYPE option<array<record(person)>>;
DEFINE FIELD person.child ON TABLE person TYPE option<array<record(person)>>;
DEFINE FIELD person.sibling ON TABLE person TYPE option<array<record(person)>>;
DEFINE FIELD person.colleague ON TABLE person TYPE option<array<record(person)>>;
DEFINE FIELD person.alumniOf ON TABLE person TYPE option<array<record(organization)>>;
DEFINE FIELD person.memberOf ON TABLE person TYPE option<array<record(organization)>>;
DEFINE FIELD person.worksFor ON TABLE person TYPE option<array<record(organization)>>;

// Indexes for common lookups
DEFINE INDEX person.email ON TABLE person FIELDS email UNIQUE;
DEFINE INDEX person.jobTitle ON TABLE person FIELDS jobTitle;
DEFINE INDEX person.birthDate ON TABLE person FIELDS birthDate;

// FTS on searchable fields
DEFINE ANALYZER person_fts FOR search ON TABLE person 
  FIELDS ANALYZER schema_default(name, description, jobTitle)
  METADATA AS {
    "description": "Person full-text search"
  };

// =============================================================================

/**
 * Organization - Schema.org Organization type
 */
DEFINE TABLE organization SCHEMAFULL EXTENDS thing;

DEFINE FIELD organization.legalName ON TABLE organization TYPE option<string>;
DEFINE FIELD organization.dba ON TABLE organization TYPE option<string>;
DEFINE FIELD organization.foundingDate ON TABLE organization TYPE option<datetime>;
DEFINE FIELD organization.dissolutionDate ON TABLE organization TYPE option<datetime>;
DEFINE FIELD organization.numberOfEmployees ON TABLE organization TYPE option<object>;
DEFINE FIELD organization.email ON TABLE organization TYPE option<string>;
DEFINE FIELD organization.telephone ON TABLE organization TYPE option<string>;
DEFINE FIELD organization.faxNumber ON TABLE organization TYPE option<string>;
DEFINE FIELD organization.url ON TABLE organization TYPE option<string>;
DEFINE FIELD organization.employeeCountRange ON TABLE organization TYPE option<string>;

DEFINE FIELD organization.address ON TABLE organization TYPE option<record(postal_address)>;
DEFINE FIELD organization.location ON TABLE organization TYPE option<record(place)>;
DEFINE FIELD organization.foundingLocation ON TABLE organization TYPE option<record(place)>;
DEFINE FIELD organization.member ON TABLE organization TYPE option<array<record(person)>>;
DEFINE FIELD organization.employee ON TABLE organization TYPE option<array<record(person)>>;
DEFINE FIELD organization.department ON TABLE organization TYPE option<array<record(organization)>>;
DEFINE FIELD organization.parentOrganization ON TABLE organization TYPE option<record(organization)>;
DEFINE FIELD organization.subOrganization ON TABLE organization TYPE option<array<record(organization)>>;
DEFINE FIELD organization.areaServed ON TABLE organization TYPE option<array<record(place)>>;
DEFINE FIELD organization.availableService ON TABLE organization TYPE option<array<string>>;
DEFINE FIELD organization.contactPoint ON TABLE organization TYPE option<array<record(contact_point)>>;

DEFINE INDEX organization.legalName ON TABLE organization FIELDS legalName;

// =============================================================================

/**
 * Place - Schema.org Place type
 */
DEFINE TABLE place SCHEMAFULL EXTENDS thing;

DEFINE FIELD place.additionalProperty ON TABLE place TYPE option<array<object>>;
DEFINE FIELD place.address ON TABLE place TYPE option<record(postal_address)>;
DEFINE FIELD place.geo ON TABLE place TYPE option<record(geo_coordinates)>;
DEFINE FIELD place.hasMap ON TABLE place TYPE option<string>;
DEFINE FIELD place.isAccessibleForFree ON TABLE place TYPE option<bool>;
DEFINE FIELD place.openingHoursSpecification ON TABLE place TYPE option<array<record(opening_hours_specification)>>;
DEFINE FIELD place.photos ON TABLE place TYPE option<array<record(image_object)>>;
DEFINE FIELD place.review ON TABLE place TYPE option<array<record(review)>>;
DEFINE FIELD place.telephone ON TABLE place TYPE option<string>;
DEFINE FIELD place.latitude ON TABLE place TYPE option<float>;
DEFINE FIELD place.longitude ON TABLE place TYPE option<float>;
DEFINE FIELD place.elevation ON TABLE place TYPE option<float>;
DEFINE FIELD place.floorLevel ON TABLE place TYPE option<string>;

DEFINE FIELD place.containedInPlace ON TABLE place TYPE option<record(place)>;
DEFINE FIELD place.containsPlace ON TABLE place TYPE option<array<record(place)>>;

// =============================================================================

/**
 * PostalAddress - Schema.org PostalAddress type
 */
DEFINE TABLE postal_address SCHEMAFULL EXTENDS thing;

DEFINE FIELD postal_address.streetAddress ON TABLE postal_address TYPE option<string>;
DEFINE FIELD postal_address.addressLocality ON TABLE postal_address TYPE option<string>;
DEFINE FIELD postal_address.addressRegion ON TABLE postal_address TYPE option<string>;
DEFINE FIELD postal_address.addressCountry ON TABLE postal_address TYPE option<string>;
DEFINE FIELD postal_address.postalCode ON TABLE postal_address TYPE option<string>;
DEFINE FIELD postal_address.postOfficeBoxNumber ON TABLE postal_address TYPE option<string>;
DEFINE FIELD postal_address.streetNumber ON TABLE postal_address TYPE option<string>;
DEFINE FIELD postal_address.premise ON TABLE postal_address TYPE option<string>;

DEFINE INDEX postal_address.lookup ON TABLE postal_address 
  FIELDS addressCountry, addressRegion, addressLocality, postalCode;

// =============================================================================

/**
 * GeoCoordinates - Schema.org GeoCoordinates type
 */
DEFINE TABLE geo_coordinates SCHEMAFULL EXTENDS thing;

DEFINE FIELD geo_coordinates.latitude ON TABLE geo_coordinates TYPE option<float>;
DEFINE FIELD geo_coordinates.longitude ON TABLE geo_coordinates TYPE option<float>;
DEFINE FIELD geo_coordinates.elevation ON TABLE geo_coordinates TYPE option<float>;
DEFINE FIELD geo_coordinates.address ON TABLE geo_coordinates TYPE option<record(postal_address)>;
DEFINE FIELD geo_coordinates.addressCountry ON TABLE geo_coordinates TYPE option<string>;
DEFINE FIELD geo_coordinates.postalCode ON TABLE geo_coordinates TYPE option<string>;

// =============================================================================

/**
 * ContactPoint - Schema.org ContactPoint type
 */
DEFINE TABLE contact_point SCHEMAFULL EXTENDS thing;

DEFINE FIELD contact_point.telephone ON TABLE contact_point TYPE option<string>;
DEFINE FIELD contact_point.faxNumber ON TABLE contact_point TYPE option<string>;
DEFINE FIELD contact_point.email ON TABLE contact_point TYPE option<string>;
DEFINE FIELD contact_point.contactType ON TABLE contact_point TYPE option<string>;
DEFINE FIELD contact_point.availableLanguage ON TABLE contact_point TYPE option<array<string>>;
DEFINE FIELD contact_point.contactOption ON TABLE contact_point TYPE option<array<object>>;

// =============================================================================

/**
 * Product - Schema.org Product type
 */
DEFINE TABLE product SCHEMAFULL EXTENDS thing;

DEFINE FIELD product.sku ON TABLE product TYPE option<string>;
DEFINE FIELD product.gtin ON TABLE product TYPE option<string>;
DEFINE FIELD product.gtin12 ON TABLE product TYPE option<string>;
DEFINE FIELD product.gtin13 ON TABLE product TYPE option<string>;
DEFINE FIELD product.gtin14 ON TABLE product TYPE option<string>;
DEFINE FIELD product.mpn ON TABLE product TYPE option<string>;
DEFINE FIELD product.brand ON TABLE product TYPE option<record(brand)>;
DEFINE FIELD product.color ON TABLE product TYPE option<string>;
DEFINE FIELD product.material ON TABLE product TYPE option<string>;
DEFINE FIELD product.productID ON TABLE product TYPE option<string>;
DEFINE FIELD product.itemCondition ON TABLE product TYPE option<OfferItemCondition>;
DEFINE FIELD product.itemNote ON TABLE product TYPE option<string>;
DEFINE FIELD product.colorSwatch ON TABLE product TYPE option<string>;

DEFINE FIELD product.weight ON TABLE product TYPE option<record(quantitative_value)>;
DEFINE FIELD product.height ON TABLE product TYPE option<record(quantitative_value)>;
DEFINE FIELD product.width ON TABLE product TYPE option<record(quantitative_value)>;
DEFINE FIELD product.depth ON TABLE product TYPE option<record(quantitative_value)>;

DEFINE FIELD product.manufacturer ON TABLE product TYPE option<record(organization)>;
DEFINE FIELD product.model ON TABLE product TYPE option<record(product_model)>;
DEFINE FIELD product.aggregateRating ON TABLE product TYPE option<record(aggregate_rating)>;
DEFINE FIELD product.review ON TABLE product TYPE option<array<record(review)>>;
DEFINE FIELD product.offers ON TABLE product TYPE option<array<record(offer)>>;
DEFINE FIELD product.category ON TABLE product TYPE option<array<string>>;
DEFINE FIELD product.isRelatedTo ON TABLE product TYPE option<array<record(product)>>;
DEFINE FIELD product.isSimilarTo ON TABLE product TYPE option<array<record(product)>>;
DEFINE FIELD product.countryOfOrigin ON TABLE product TYPE option<string>;

DEFINE INDEX product.sku ON TABLE product FIELDS sku UNIQUE;
DEFINE INDEX product.gtin ON TABLE product FIELDS gtin;

// =============================================================================

/**
 * Offer - Schema.org Offer type
 */
DEFINE TABLE offer SCHEMAFULL EXTENDS thing;

DEFINE FIELD offer.price ON TABLE offer TYPE option<float>;
DEFINE FIELD offer.priceCurrency ON TABLE offer TYPE option<string>;
DEFINE FIELD offer.minPrice ON TABLE offer TYPE option<float>;
DEFINE FIELD offer.maxPrice ON TABLE offer TYPE option<float>;
DEFINE FIELD offer.priceType ON TABLE offer TYPE option<string>;
DEFINE FIELD offer.validFrom ON TABLE offer TYPE option<datetime>;
DEFINE FIELD offer.validThrough ON TABLE offer TYPE option<datetime>;
DEFINE FIELD offer.availability ON TABLE offer TYPE option<ItemAvailability>;
DEFINE FIELD offer.availabilityStarts ON TABLE offer TYPE option<datetime>;
DEFINE FIELD offer.availabilityEnds ON TABLE offer TYPE option<datetime>;
DEFINE FIELD offer.inventoryLevel ON TABLE offer TYPE option<record(quantitative_value)>;

DEFINE FIELD offer.itemOffered ON TABLE offer TYPE option<record(product)>;
DEFINE FIELD offer.seller ON TABLE offer TYPE option<record(organization)>;
DEFINE FIELD offer.addOn ON TABLE offer TYPE option<record(offer)>;

// =============================================================================

/**
 * Brand - Schema.org Brand type
 */
DEFINE TABLE brand SCHEMAFULL EXTENDS thing;

DEFINE FIELD brand.logo ON TABLE brand TYPE option<string>;
DEFINE FIELD brand.aggregateRating ON TABLE brand TYPE option<record(aggregate_rating)>;

// =============================================================================

/**
 * ProductModel - Schema.org ProductModel type
 */
DEFINE TABLE product_model SCHEMAFULL EXTENDS thing;

DEFINE FIELD product_model.isVariantOf ON TABLE product_model TYPE option<record(product_model)>;
DEFINE FIELD product_model.predecessorOf ON TABLE product_model TYPE option<record(product_model)>;
DEFINE FIELD product_model.successorOf ON TABLE product_model TYPE option<record(product_model)>;
DEFINE FIELD product_model.relatedModel ON TABLE product_model TYPE option<array<record(product_model)>>;

// =============================================================================

/**
 * AggregateRating - Schema.org AggregateRating type
 */
DEFINE TABLE aggregate_rating SCHEMAFULL EXTENDS thing;

DEFINE FIELD aggregate_rating.ratingValue ON TABLE aggregate_rating TYPE option<float>;
DEFINE FIELD aggregate_rating.bestRating ON TABLE aggregate_rating TYPE option<float>;
DEFINE FIELD aggregate_rating.worstRating ON TABLE aggregate_rating TYPE option<float>;
DEFINE FIELD aggregate_rating.ratingCount ON TABLE aggregate_rating TYPE option<int>;
DEFINE FIELD aggregate_rating.reviewCount ON TABLE aggregate_rating TYPE option<int>;
DEFINE FIELD aggregate_rating.ratingExplanation ON TABLE aggregate_rating TYPE option<string>;

// =============================================================================

/**
 * Review - Schema.org Review type
 */
DEFINE TABLE review SCHEMAFULL EXTENDS thing;

DEFINE FIELD review.reviewRating ON TABLE review TYPE option<record(rating)>;
DEFINE FIELD review.reviewBody ON TABLE review TYPE option<string>;
DEFINE FIELD review.reviewAspect ON TABLE review TYPE option<string>;

DEFINE FIELD review.itemReviewed ON TABLE review TYPE option<record(thing)>;
DEFINE FIELD review.reviewer ON TABLE review TYPE option<record(person)>;
DEFINE FIELD review.reviewPublishedBy ON TABLE review TYPE option<record(organization)>;

// =============================================================================

/**
 * Rating - Schema.org Rating type
 */
DEFINE TABLE rating SCHEMAFULL EXTENDS thing;

DEFINE FIELD rating.worstRating ON TABLE rating TYPE option<float>;
DEFINE FIELD rating.bestRating ON TABLE rating TYPE option<float>;
DEFINE FIELD rating.ratingValue ON TABLE rating TYPE option<float>;

// =============================================================================

/**
 * Event - Schema.org Event type
 */
DEFINE TABLE event SCHEMAFULL EXTENDS thing;

DEFINE FIELD event.startDate ON TABLE event TYPE option<datetime>;
DEFINE FIELD event.endDate ON TABLE event TYPE option<datetime>;
DEFINE FIELD event.duration ON TABLE event TYPE option<duration>;
DEFINE FIELD event.eventStatus ON TABLE event TYPE option<EventStatusType>;
DEFINE FIELD event.eventAttendanceMode ON TABLE event TYPE option<EventAttendanceMode>;
DEFINE FIELD event.previousEvent ON TABLE event TYPE option<record(event)>;
DEFINE FIELD event.nextEvent ON TABLE event TYPE option<record(event)>;
DEFINE FIELD event.maximumAttendeeCapacity ON TABLE event TYPE option<int>;
DEFINE FIELD event.typicalAgeRange ON TABLE event TYPE option<string>;
DEFINE FIELD event.organizer ON TABLE event TYPE option<record(organization)>;
DEFINE FIELD event.sponsor ON TABLE event TYPE option<record(organization) | record(person)>;
DEFINE FIELD event.location ON TABLE event TYPE option<record(place) | record(postal_address)>;
DEFINE FIELD event.performer ON TABLE event TYPE option<array<record(organization) | record(person)>>;
DEFINE FIELD event.offers ON TABLE event TYPE option<array<record(offer)>>;

// =============================================================================

/**
 * CreativeWork - Schema.org CreativeWork type
 */
DEFINE TABLE creative_work SCHEMAFULL EXTENDS thing;

DEFINE FIELD creative_work.headline ON TABLE creative_work TYPE option<string>;
DEFINE FIELD creative_work.alternativeHeadline ON TABLE creative_work TYPE option<string>;
DEFINE FIELD creative_work.dateCreated ON TABLE creative_work TYPE option<datetime>;
DEFINE FIELD creative_work.datePublished ON TABLE creative_work TYPE option<datetime>;
DEFINE FIELD creative_work.dateModified ON TABLE creative_work TYPE option<datetime>;
DEFINE FIELD creative_work.copyrightYear ON TABLE creative_work TYPE option<int>;
DEFINE FIELD creative_work.copyrightHolder ON TABLE creative_work TYPE option<record(organization) | record(person)>;
DEFINE FIELD creative_work.license ON TABLE creative_work TYPE option<string>;
DEFINE FIELD creative_work.version ON TABLE creative_work TYPE option<string | int>;
DEFINE FIELD creative_work.timeRequired ON TABLE creative_work TYPE option<duration>;
DEFINE FIELD creative_work.encoding ON TABLE creative_work TYPE option<array<record(media_object)>>;
DEFINE FIELD creative_work.fileFormat ON TABLE creative_work TYPE option<array<string>>;
DEFINE FIELD creative_work.contentRating ON TABLE creative_work TYPE option<string>;
DEFINE FIELD creative_work.aggregateRating ON TABLE creative_work TYPE option<record(aggregate_rating)>;
DEFINE FIELD creative_work.review ON TABLE creative_work TYPE option<array<record(review)>>;

// Creator/author fields
DEFINE FIELD creative_work.author ON TABLE creative_work TYPE option<array<record(person) | record(organization)>>;
DEFINE FIELD creative_work.contributor ON TABLE creative_work TYPE option<array<record(person) | record(organization)>>;
DEFINE FIELD creative_work.creator ON TABLE creative_work TYPE option<record(person) | record(organization)>;
DEFINE FIELD creative_work.editor ON TABLE creative_work TYPE option<array<record(person)>>;
DEFINE FIELD creative_work.publisher ON TABLE creative_work TYPE option<record(organization)>;
DEFINE FIELD creative_work.provider ON TABLE creative_work TYPE option<record(organization) | record(person)>;

// =============================================================================

/**
 * MediaObject - Schema.org MediaObject type
 */
DEFINE TABLE media_object SCHEMAFULL EXTENDS thing;

DEFINE FIELD media_object.contentUrl ON TABLE media_object TYPE option<string>;
DEFINE FIELD media_object.embedUrl ON TABLE media_object TYPE option<string>;
DEFINE FIELD media_object.uploadDate ON TABLE media_object TYPE option<datetime>;
DEFINE FIELD media_object.contentSize ON TABLE media_object TYPE option<string>;
DEFINE FIELD media_object.contentDuration ON TABLE media_object TYPE option<duration>;
DEFINE FIELD media_object.encodingFormat ON TABLE media_object TYPE option<string>;
DEFINE FIELD media_object.bitrate ON TABLE media_object TYPE option<string>;

// =============================================================================

/**
 * ImageObject - Schema.org ImageObject type
 */
DEFINE TABLE image_object SCHEMAFULL EXTENDS media_object;

DEFINE FIELD image_object.caption ON TABLE image_object TYPE option<string>;
DEFINE FIELD image_object.thumbnail ON TABLE image_object TYPE option<record(image_object)>;
DEFINE FIELD image_object.exifData ON TABLE image_object TYPE option<string>;
DEFINE FIELD image_object.representativeOfPage ON TABLE image_object TYPE option<bool>;

// =============================================================================

/**
 * VideoObject - Schema.org VideoObject type
 */
DEFINE TABLE video_object SCHEMAFULL EXTENDS media_object;

DEFINE FIELD video_object.caption ON TABLE video_object TYPE option<string>;
DEFINE FIELD video_object.thumbnail ON TABLE video_object TYPE option<record(image_object)>;
DEFINE FIELD video_object.videoFrameSize ON TABLE video_object TYPE option<string>;
DEFINE FIELD video_object.videoQuality ON TABLE video_object TYPE option<string>;
DEFINE FIELD video_object.actor ON TABLE video_object TYPE option<array<record(person)>>;
DEFINE FIELD video_object.director ON TABLE video_object TYPE option<record(person)>;
DEFINE FIELD video_object.musicBy ON TABLE video_object TYPE option<record(person) | record(organization)>;

// =============================================================================

/**
 * AudioObject - Schema.org AudioObject type
 */
DEFINE TABLE audio_object SCHEMAFULL EXTENDS media_object;

DEFINE FIELD audio_object.transcript ON TABLE audio_object TYPE option<string>;
DEFINE FIELD audio_object.embedUrl ON TABLE audio_object TYPE option<string>;
DEFINE FIELD audio_object.caption ON TABLE audio_object TYPE option<array<record(media_object)>>;

// =============================================================================

/**
 * OpeningHoursSpecification - Schema.org OpeningHoursSpecification type
 */
DEFINE TABLE opening_hours_specification SCHEMAFULL EXTENDS thing;

DEFINE FIELD opening_hours_specification.dayOfWeek ON TABLE opening_hours_specification TYPE option<DayOfWeek>;
DEFINE FIELD opening_hours_specification.opens ON TABLE opening_hours_specification TYPE option<string>;
DEFINE FIELD opening_hours_specification.closes ON TABLE opening_hours_specification TYPE option<string>;
DEFINE FIELD opening_hours_specification.validFrom ON TABLE opening_hours_specification TYPE option<datetime>;
DEFINE FIELD opening_hours_specification.validThrough ON TABLE opening_hours_specification TYPE option<datetime>;

// =============================================================================

/**
 * QuantitativeValue - Schema.org QuantitativeValue type
 */
DEFINE TABLE quantitative_value SCHEMAFULL EXTENDS thing;

DEFINE FIELD quantitative_value.value ON TABLE quantitative_value TYPE option<float | int>;
DEFINE FIELD quantitative_value.minValue ON TABLE quantitative_value TYPE option<float | int>;
DEFINE FIELD quantitative_value.maxValue ON TABLE quantitative_value TYPE option<float | int>;
DEFINE FIELD quantitative_value.unitCode ON TABLE quantitative_value TYPE option<string>;
DEFINE FIELD quantitative_value.unitText ON TABLE quantitative_value TYPE option<string>;
DEFINE FIELD quantitative_value.valueReference ON TABLE quantitative_value TYPE option<record(quantitative_value)>;

// =============================================================================

/**
 * MonetaryAmount - Schema.org MonetaryAmount type
 */
DEFINE TABLE monetary_amount SCHEMAFULL EXTENDS thing;

DEFINE FIELD monetary_amount.currency ON TABLE monetary_amount TYPE option<string>;
DEFINE FIELD monetary_amount.value ON TABLE monetary_amount TYPE option<float | int>;
DEFINE FIELD monetary_amount.valueAddedTaxIncluded ON TABLE monetary_amount TYPE option<bool>;
DEFINE FIELD monetary_amount.minPrice ON TABLE monetary_amount TYPE option<float>;
DEFINE FIELD monetary_amount.maxPrice ON TABLE monetary_amount TYPE option<float>;

// =============================================================================

/**
 * PriceSpecification - Schema.org PriceSpecification type
 */
DEFINE TABLE price_specification SCHEMAFULL EXTENDS thing;

DEFINE FIELD price_specification.price ON TABLE price_specification TYPE option<float | int>;
DEFINE FIELD price_specification.priceCurrency ON TABLE price_specification TYPE option<string>;
DEFINE FIELD price_specification.validFrom ON TABLE price_specification TYPE option<datetime>;
DEFINE FIELD price_specification.validThrough ON TABLE price_specification TYPE option<datetime>;
DEFINE FIELD price_specification.valueAddedTaxIncluded ON TABLE price_specification TYPE option<bool>;
DEFINE FIELD price_specification.minPrice ON TABLE price_specification TYPE option<float>;
DEFINE FIELD price_specification.maxPrice ON TABLE price_specification TYPE option<float>;

// =============================================================================

// =============================================================================
// GRAPH EDGES - Schema.org relationships (embedded graph)
// =============================================================================

/**
 * SurrealDB's graph edges are embedded in the tables
 * Using RELATES for edge definitions
 * 
 * Edge types follow Schema.org relationship names:
 * - knows, knowsLanguage
 * - spouse, parent, child, sibling, colleague
 * - alumniOf, memberOf, worksFor
 * - employee, member, subOrganization
 * - offers, brand, manufacturer, model
 * - relatedTo, similarTo
 * - organizer, performer, sponsor, location
 * - author, editor, contributor, creator
 * - linksTo, mentions, hasPart
 */

// =============================================================================
// TIME-SERIES - Temporal data tables
// =============================================================================

/**
 * Price history time-series
 */
DEFINE TABLE product_price_history 
  SCHEMAFULL
  TYPE time SERIES compression gorilla;

DEFINE FIELD product_price_history.product ON TABLE product_price_history TYPE record(product);
DEFINE FIELD product_price_history.offer ON TABLE product_price_history TYPE option<record(offer)>;
DEFINE FIELD product_price_history.price ON TABLE product_price_history TYPE float;
DEFINE FIELD product_price_history.currency ON TABLE product_price_history TYPE string;
DEFINE INDEX product_price_history.ts ON TABLE product_price_history FIELDS _time UNIQUE;

/**
 * Inventory time-series
 */
DEFINE TABLE inventory_history 
  SCHEMAFULL 
  TYPE time SERIES compression gorilla;

DEFINE FIELD inventory_history.product ON TABLE inventory_history TYPE record(product);
DEFINE FIELD inventory_history.offer ON TABLE inventory_history TYPE option<record(offer)>;
DEFINE FIELD inventory_history.inventoryLevel ON TABLE inventory_history TYPE int;
DEFINE FIELD inventory_history.availability ON TABLE inventory_history TYPE ItemAvailability;
DEFINE INDEX inventory_history.ts ON TABLE inventory_history FIELDS _time UNIQUE;

/**
 * Rating history time-series
 */
DEFINE TABLE rating_history 
  SCHEMAFULL 
  TYPE time SERIES compression gorilla;

DEFINE FIELD rating_history.entity ON TABLE rating_history TYPE record(thing);
DEFINE FIELD rating_history.ratingValue ON TABLE rating_history TYPE float;
DEFINE FIELD rating_history.ratingCount ON TABLE rating_history TYPE int;
DEFINE INDEX rating_history.ts ON TABLE rating_history FIELDS _time UNIQUE;

/**
 * Event attendance time-series
 */
DEFINE TABLE event_attendance_history 
  SCHEMAFULL 
  TYPE time SERIES compression gorilla;

DEFINE FIELD event_attendance_history.event ON TABLE event_attendance_history TYPE record(event);
DEFINE FIELD event_attendance_history.attendeeCount ON TABLE event_attendance_history TYPE int;
DEFINE FIELD event_attendance_history.capacity ON TABLE event_attendance_history TYPE int;
DEFINE INDEX event_attendance_history.ts ON TABLE event_attendance_history FIELDS _time UNIQUE;

/**
 * Web analytics time-series
 */
DEFINE TABLE page_view_history 
  SCHEMAFULL 
  TYPE time SERIES compression gorilla;

DEFINE FIELD page_view_history.entity ON TABLE page_view_history TYPE record(thing);
DEFINE FIELD page_view_history.pageViews ON TABLE page_view_history TYPE int;
DEFINE FIELD page_view_history.uniqueVisitors ON TABLE page_view_history TYPE int;
DEFINE FIELD page_view_history.engagementScore ON TABLE page_view_history TYPE float;
DEFINE INDEX page_view_history.ts ON TABLE page_view_history FIELDS _time UNIQUE;

// =============================================================================
// KEY-VALUE STORE - For caching sessions
// =============================================================================

/**
 * SurrealDB can use table as key-value store
 */
DEFINE TABLE entity_cache TYPE KV SCHEMALESS;

DEFINE FIELD entity_cache._entity_id ON TABLE entity_cache TYPE string;
DEFINE FIELD entity_cache._expires_at ON TABLE entity_cache TYPE option<datetime>;

DEFINE INDEX entity_cache.key ON TABLE entity_cache FIELDS _key UNIQUE;

// =============================================================================
// SAMPLE DATA - Example inserts
// =============================================================================

// Insert a Person
INSERT INTO person:john_doe {
  id: "https://example.com/people/john-doe",
  name: "John Doe",
  givenName: "John",
  familyName: "Doe",
  email: "john@example.com",
  jobTitle: "Software Engineer",
  worksFor: [organization:acme_corp],
  address: postal_address:john_home
};

INSERT INTO postal_address:john_home {
  streetAddress: "123 Main Street",
  addressLocality: "San Francisco",
  addressRegion: "California",
  addressCountry: "US",
  postalCode: "94102"
};

// Insert an Organization
INSERT INTO organization:acme_corp {
  id: "https://example.com/orgs/acme-corp",
  legalName: "Acme Corporation",
  dba: "Acme",
  email: "contact@acme.com",
  telephone: "+1-555-0123",
  address: postal_address:acme_hq
};

INSERT INTO postal_address:acme_hq {
  streetAddress: "456 Enterprise Way",
  addressLocality: "San Francisco", 
  addressRegion: "California",
  addressCountry: "US",
  postalCode: "94107"
};

// Insert a Product with Offer
INSERT INTO product:super_widget {
  id: "https://example.com/products/super-widget",
  name: "Super Widget 3000",
  sku: "SW-3000-BLK",
  gtin: "01234567890123",
  brand: brand:acme_brand,
  color: "Black",
  itemCondition: "NewCondition",
  manufacturer: organization:acme_corp,
  offers: [offer:super_widget_sale],
  aggregateRating: aggregate_rating:widget_rating
};

INSERT INTO brand:acme_brand {
  id: "https://example.com/brands/acme",
  name: "ACME",
  logo: "https://example.com/images/acme-logo.png"
};

INSERT INTO offer:super_widget_sale {
  name: "Super Widget 3000 Sale",
  price: 99.99,
  priceCurrency: "USD",
  itemOffered: product:super_widget,
  seller: organization:acme_corp,
  availability: "InStock",
  validFrom: "2024-01-01T00:00:00Z"
};

INSERT INTO aggregate_rating:widget_rating {
  id: "https://example.com/ratings/super-widget",
  ratingValue: 4.5,
  bestRating: 5.0,
  worstRating: 1.0,
  ratingCount: 128
};

// Insert time-series price data
INSERT INTO product_price_history:_ {
  _time: "2024-01-01T00:00:00Z",
  product: product:super_widget,
  offer: offer:super_widget_sale,
  price: 129.99,
  currency: "USD"
};

INSERT INTO product_price_history:_ {
  _time: "2024-02-01T00:00:00Z",
  product: product:super_widget,
  offer: offer:super_widget_sale,
  price: 119.99,
  currency: "USD"
};

// =============================================================================
// SAMPLE QUERIES - SurrealQL examples
// =============================================================================

/* 
 * Basic SELECT - get all products under $100
 */
SELECT product {
  id: product.id,
  name: product.name,
  price: product.offers[].price
}
FROM product
WHERE product.offers[?WHERE price < 100]
RETURN product.name, product.offers[?WHERE price < 100].price;

/*
 * Full-text search on products
 */
SELECT name, description 
FROM product 
WHERE name @@ "widget" OR description @@ "widget"
ORDER BY _created_at DESC
LIMIT 10;

/*
 * Graph traversal - employee's colleagues
 */
SELECT 
  person.name,
  ->worksFor->organization.name AS company,
  <-employee<-person.name AS co_worker
FROM person:john_doe
WHERE ->knows;

/*
 * Graph traversal - products in same category
 */
SELECT 
  p.name,
  p.offers[].price,
  p.aggregateRating.ratingValue AS rating
FROM product AS p
WHERE p.category CONTAINS "Electronics"
ORDER BY p.aggregateRating.ratingValue DESC;

/*
 * Time-series - price history for a product
 */
SELECT _time, price, currency
FROM product_price_history
WHERE product = product:super_widget
ORDER BY _time ASC
LIMIT 30;

/*
 * Time-series - average rating trend
 */
SELECT 
  array::group::_time AS date,
  math::mean(ratingValue) AS avg_rating
FROM rating_history
WHERE _time > "2024-01-01"
GROUP BY time::epoch(_time / 86400) * 86400
ORDER BY date;

/*
 * Multi-model query - Product with graph + time-series
 */
SELECT 
  p.name,
  p.offers[0].price,
  p.offers[0].priceCurrency,
  
  // Related products via graph
  p.isRelatedTo.name,
  
  // Recent price change
  (SELECT _time, price FROM product_price_history
   WHERE product = p
   ORDER BY _time DESC
   LIMIT 1).price AS latest_price
FROM product AS p
WHERE p.itemCondition = "NewCondition"
RETURN p.name, p.offers[0].price, p.isRelatedTo.name, latest_price;

// =============================================================================
// USER & PERMISSIONS - Database security
// =============================================================================

DEFINE USER admin ON NAMESPACE SCHEMAFULL 
  PASSWORD "secure-password-here" 
  ROLE OWNER;

DEFINE USER readonly ON NAMESPACE SCHEMAFULL 
  PASSWORD "readonly-password" 
  ROLE SELECT;

DEFINE USER readwrite ON NAMESPACE SCHEMAFULL 
  PASSWORD "readwrite-password" 
  ROLE SELECT, UPDATE, CREATE, DELETE;

// Grant permissions
GRANT SELECT ON TABLE thing TO readonly;
GRANT ALL ON TABLE thing TO readwrite;
GRANT ALL ON TABLE * TO admin;

// =============================================================================
// EXPORTS - For TypeScript type generation
// =============================================================================

/*
-- To generate TypeScript types from SurrealDB schema:
-- RUN DEFINE SCHEMA EXPORT AS typescript FILE ./schema-org.types.ts;
*/

// Or query the schema programmatically
// DEFINE TABLE $schema RETURN SCHEMAFULL;
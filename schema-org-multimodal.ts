/**
 * Multi-Modal Database Schema for Schema.org
 * 
 * This schema is designed for multi-model databases like ArangoDB, Cosmos DB, or similar
 * that support multiple data models: document, graph, key-value, and time-series.
 * 
 * It provides collections/graphs for different access patterns.
 */

// =============================================================================
// DOCUMENT STORE - Primary Schema.org entity storage
// =============================================================================

/**
 * Documents collection - Stores all Schema.org typed entities as JSON documents
 * Use for: CRUD operations, querying, filtering
 */
interface schema_documents {
  // Internal metadata
  _key: string,                    // Auto-generated unique key
  _id: string,                    // Full collection/key
  _rev: string,                   // Revision ID for MVCC
  
  // Schema.org core properties (Thing)
  "@context": "https://schema.org",   // Schema.org context
  "@type": string,                // Schema.org type (e.g., "Product", "Person")
  "@id": string,                 // Unique identifier (URL or generated)
  
  // Common properties (Thing)
  name?: string,
  description?: string,
  alternateName?: string[],
  disambiguatingDescription?: string,
  url?: string,
  image?: string | {
    "@type": "ImageObject",
    url?: string,
    caption?: string,
  },
  
  // Access control
  tenant_id?: string,            // Multi-tenant isolation
  created_at: number,           // Unix timestamp
  created_by?: string,
  updated_at: number,
  updated_by?: string,
  
  // Full-text search
  _fts?: string,                // Concatenated searchable text
  _fts_boost?: number,           // Search boosting score
  
  // Type-specific properties (discriminated by @type)
  // --- Person ---
  "Person"?: {
    givenName?: string,
    familyName?: string,
    additionalName?: string[],
    email?: string,
    telephone?: string,
    jobTitle?: string,
    birthDate?: string,
    deathDate?: string,
    gender?: string,
    nationality?: string,
    address?: schema_documents,        // PostalAddress reference
    memberOf?: string[],           // Organization references
    worksFor?: string[],          // Organization references
    knowsLanguage?: string[],
    award?: string[],
    alumniOf?: string[],          // EducationalOrganization refs
    spouse?: schema_documents,
    parent?: schema_documents[],
    child?: schema_documents[],
    sibling?: schema_documents[],
    colleague?: string[],
    follow?: string[],
  },
  
  // --- Organization ---
  "Organization"?: {
    LegalName?: string,
    dto?: string,                // "doing business as" / trading name
    logo?: string,
    foundingDate?: string,
    foundingLocation?: schema_documents,
    dissolutionDate?: string,
    numberOfEmployees?: {
      "@type": "QuantitativeValue",
      minValue?: number,
      maxValue?: number,
      value?: number,
    },
    member?: string[],           // Person references
    memberOf?: string[],
    employee?: string[],
    department?: string[],
    parentOrganization?: string,
    subOrganization?: string[],
    areaServed?: string | schema_documents,
    availableService?: string[],
    keyword?: string[],
    contactPoint?: schema_documents[],
  },
  
  // --- Place ---
  "Place"?: {
    address?: schema_documents,
    geo?: schema_documents,       // GeoCoordinates reference
    hasMap?: string,
    isAccessibleForFree?: boolean,
    openingHoursSpecification?: schema_documents[],
    telephone?: string,
    latitude?: number,
    longitude?: number,
    containedInPlace?: string,
    containsPlace?: string[],
    photos?: string[],
  },
  
  // --- Product ---
  "Product"?: {
    brand?: string | schema_documents,
    manufacturer?: string,
    model?: string | schema_documents,
    sku?: string,
    gtin?: string,
    gtin12?: string,
    gtin13?: string,
    gtin14?: string,
    mpn?: string,
    color?: string,
    weight?: schema_documents,
    height?: schema_documents,
    width?: schema_documents,
    depth?: schema_documents,
    itemCondition?: OfferItemCondition,
    brand?: schema_documents,
    offers?: schema_documents[],
    aggregateRating?: schema_documents,
    review?: schema_documents[],
    isRelatedTo?: string[],
    isSimilarTo?: string[],
    countryOfOrigin?: string,
  },
  
  // --- Offer ---
  "Offer"?: {
    price?: number,
    priceCurrency?: string,
    minPrice?: number,
    maxPrice?: number,
    priceType?: string,
    availability?: ItemAvailability,
    availabilityStarts?: string,
    availabilityEnds?: string,
    validFrom?: string,
    validThrough?: string,
    itemOffered?: string,
    seller?: string,
    addOn?: string,
    deliveryLeadTime?: schema_documents,
    categorizes?: string,
    availableAtOrFrom?: string,
    mpn?: string,
    asin?: string,
  },
  
  // --- Event ---
  "Event"?: {
    startDate?: string,
    endDate?: string,
    duration?: string,
    eventStatus?: EventStatusType,
    eventAttendanceMode?: EventAttendanceModeEnumeration,
    location?: string | schema_documents,
    subLocation?: schema_documents,
    organizer?: string,
    performer?: string | string[],
    performerIn?: schema_documents[],
    sponsor?: string | schema_documents,
    offers?: schema_documents[],
    maximumAttendeeCapacity?: number,
    typicalAgeRange?: string,
    previousEvent?: string,
    nextEvent?: string,
  },
  
  // --- CreativeWork ---
  "CreativeWork"?: {
    headline?: string,
    alternativeHeadline?: string,
    datePublished?: string,
    dateCreated?: string,
    dateModified?: string,
    author?: string[],
    editor?: string[],
    contributor?: string[],
    creator?: string,
    publisher?: string,
    provider?: string,
    about?: string,
    associatedMedia?: string[],
    contentRating?: string,
    encoding?: string,
    fileFormat?: string,
    timeRequired?: string,
    commentCount?: number,
    citation?: string[],
    license?: string,
    conditionsOfAccess?: string,
  },
  
  // --- PostalAddress ---
  "PostalAddress"?: {
    streetAddress?: string,
    addressLocality?: string,
    addressRegion?: string,
    addressCountry?: string,
    postalCode?: string,
    postOfficeBoxNumber?: string,
  },
  
  // --- GeoCoordinates ---
  "GeoCoordinates"?: {
    latitude?: number,
    longitude?: number,
    elevation?: number,
    address?: string,
    addressCountry?: string,
    postalCode?: string,
  },
  
  // --- Rating & AggregateRating ---
  "AggregateRating"?: {
    ratingValue?: number,
    bestRating?: number,
    worstRating?: number,
    ratingCount?: number,
    reviewCount?: number,
    ratingExplanation?: string,
  },
  
  // --- OpeningHoursSpecification ---
  "OpeningHoursSpecification"?: {
    dayOfWeek?: DayOfWeek | string[],
    opens?: string,
    closes?: string,
    validFrom?: string,
    validThrough?: string,
  },
  
  // --- QuantitativeValue ---
  "QuantitativeValue"?: {
    value?: number,
    minValue?: number,
    maxValue?: number,
    unitCode?: string,
    unitText?: string,
    valueReference?: string,
  },
  
  // --- MonraryAmount ---
  "MonetaryAmount"?: {
    currency?: string,
    value?: number,
    valueAddedTaxIncluded?: boolean,
    priceType?: string,
  },
}

type OfferItemCondition = 
  | "NewCondition" 
  | "RefurbishedCondition" 
  | "UsedCondition" 
  | "DamagedCondition" 
  | "DiscontinuedCondition";

type ItemAvailability = 
  | "InStock" 
  | "InStoreOnly" 
  | "OnlineOnly" 
  | "OutOfStock" 
  | "PreOrder" 
  | "BackOrder" 
  | "Discontinued" 
  | "LimitedAvailability" 
  | "SoldOut";

type EventStatusType = 
  | "EventScheduled" 
  | "EventCancelled" 
  | "EventMovedOnline" 
  | "EventPostponed" 
  | "EventRescheduled";

type EventAttendanceModeEnumeration = 
  | "OfflineEventAttendanceMode" 
  | "OnlineEventAttendanceMode" 
  | "MixedEventAttendanceMode";

type DayOfWeek = 
  | "Monday" 
  | "Tuesday" 
  | "Wednesday" 
  | "Thursday" 
  | "Friday" 
  | "Saturday" 
  | "Sunday";

// =============================================================================
// GRAPH EDGES - Schema.org relationships for graph traversal
// =============================================================================

/**
 * Graph edges collection - Typed relationships between entities
 * Use for: Graph queries, traversals, path finding
 */
interface schema_edges {
  _key: string,
  _id: string,
  _from: string,              // Source entity _id
  _to: string,                // Target entity _id
  _rev: string,
  _type: string,              // Edge type
  
  // Relationship metadata
  relationship_type: string, // "knows", "member", "worksFor", etc.
  
  // Edge properties (optional)
  startDate?: string,
  endDate?: string,
  validFrom?: string,
  validThrough?: string,
  
  // Weight for path finding
  weight?: number,
  
  // Role in relationship
  role?: string,
  name?: string,
  
  // Bidirectional flag
  bidirectional?: boolean,
  
  // Tenant isolation
  tenant_id?: string,
  
  // Timestamps
  created_at: number,
}

/**
 * Common Schema.org edge types (relationships)
 */
const EDGE_TYPES = {
  // Person relationships
  KNOWS: "knows",
  KNOWS_LANGUAGE: "knowsLanguage",
  SPROUSE: "spouse",
  PARENT: "parent",
  CHILD: "child",
  SIBLING: "sibling",
  COLLEAGUE: "colleague",
  ALUMNI_OF: "alumniOf",
  MEMBER_OF: "memberOf",
  WORKS_FOR: "worksFor",
  
  // Organization relationships
  EMPLOYEE: "employee",
  MEMBER: "member",
  SUB_ORGANIZATION: "subOrganization",
  DEPARTMENT: "department",
  OFFERS: "offers",
  
  // Place relationships
  LOCATED_IN: "locatedIn",
  CONTAINED_IN: "containedIn",
  CONTAINS: "contains",
  OPENES_IN: "opensIn",
  
  // Product relationships  
  OFFERS: "offers",
  BRAND: "brand",
  MANUFACTURER: "manufacturer",
  MODEL: "model",
  RELATED_TO: "relatedTo",
  SIMILAR_TO: "similarTo",
  REVIEWED_IN: "reviewedIn",
  
  // Event relationships
  ORGANIZER: "organizer",
  PERFORMER: "performer",
  SPONSOR: "sponsor",
  LOCATION: "location",
  SUB_LOCATION: "subLocation",
  
  // Creative Work relationships
  AUTHOR: "author",
  EDITOR: "editor",
  CONTRIBUTOR: "contributor",
  CREATOR: "creator",
  PUBLISHER: "provider",
  ABOUT: "about",
  ASSOCIATED_MEDIA: "associatedMedia",
  CITATION: "citation",
  MENTION: "mentions",
  
  // WebContent relationships
  LINK: "linksTo",
  MENTIONS: "mentions",
  HAS_PART: "hasPart",
  IS_PART_OF: "isPartOf",
}

// =============================================================================
// KEY-VALUE STORE - Fast lookups by entity ID
// =============================================================================

/**
 * Key-value store - Fast O(1) lookups by entity ID/URL
 * Use for: Cache, sessions, direct lookups by URL
 */
interface schema_kv {
  _key: string,                    // Entity @id (URL-encoded)
  
  // Entity reference
  _id: string,                    // Document _id reference
  _type: string,                  // Schema.org @type
  
  // Cached data
  name: string,
  description?: string,
  image?: string,
  
  // Lookups
  primary_url: string,            // Primary URL
  
  // Quick flags for filtering
  is_person?: boolean,
  is_organization?: boolean,
  is_place?: boolean,
  is_product?: boolean,
  is_event?: boolean,
  is_creative_work?: boolean,
  
  // Timestamp
  cached_at: number,
  expires_at?: number,
  
  // Tenant
  tenant_id?: string,
}

// =============================================================================
// TIME-SERIES - Temporal data (prices, ratings, availability)
// =============================================================================

/**
 * Time-series collection - Temporal properties of entities
 * Use for: Historical queries, analytics, trends
 */
interface schema_timeseries {
  _key: string,                    // Composite: entityId_timestamp
  
  // Entity reference
  _id: string,                    // Document _id reference
  _type: string,                  // Schema.org type of parent entity
  
  // Timestamp (required for time-series)
  timestamp: number,               // Unix timestamp (ms)
  timestamp_iso: string,          // ISO 8601 timestamp
  
  // Time-series type
  series_type: string,            // "price", "rating", "inventory", etc.
  
  // Value (depending on series_type)
  value?: number,
  value_num?: number,
  value_str?: string,
  
  // Additional metrics
  currency?: string,
  quantity?: number,
  
  // Aggregation metadata
  aggregation?: string,            // "hourly", "daily", "weekly"
  sample_size?: number,
  
  // Tenant
  tenant_id?: string,
}

/**
 * Common time-series types for Schema.org
 */
const SERIES_TYPES = {
  // Product/Offer time series
  PRICE: "price",
  INVENTORY: "inventory",
  AVAILABILITY: "availability",
  DEMAND: "demand",
  
  // Rating time series
  RATING: "rating",
  REVIEW_SENTIMENT: "reviewSentiment",
  
  // Event time series
  ATTENDEE_COUNT: "attendeeCount",
  TICKET_AVAILABILITY: "ticketAvailability",
  
  // Place time series
  POPULARITY: "popularity",
  OCCUPANCY: "occupancy",
  
  // Organization time series
  EMPLOYEE_COUNT: "employeeCount",
  REVENUE: "revenue",
  
  // Web traffic
  PAGE_VIEWS: "pageViews",
  ENGAGEMENT: "engagement",
}

// =============================================================================
// FULL-TEXT SEARCH INDEX - Fuzzy search across entities
// =============================================================================

/**
 * Full-text search analyzer configurations
 */
interface schema_fts_analyzers {
  // Default analyzer: tokenizes and stemming
  default: {
    type: "text",
    stopwords: "_english_",
    case: "lower",
  },
  
  // Exact match analyzer for codes (SKU, GTIN, etc.)
  exact: {
    type: "identity",
  },
  
  // Autocomplete analyzer
  autocomplete: {
    type: "text",
    mode: "prefix",
    case: "lower",
  },
  
  // Address analyzer
  address: {
    type: "text",
    case: "lower",
    stopwords: "_english_",
  },
}

/**
 * Indexed fields for full-text search
 */
const FTS_INDEXED_FIELDS = [
  // Primary search
  "name^5",                     // Boost name matches
  "description^3",
  "alternateName^2",
  
  // Category/codified searches  
  "sku^3",
  "gtin^3",
  "mpn^3",
  "asin^3",
  
  // Address fields
  "address.streetAddress",
  "address.addressLocality^2",
  "address.addressRegion^2",
  "address.postalCode^2",
  "address.addressCountry",
  
  // Organization fields
  "brand.name^2",
  "department.name",
  
  // Person fields
  "givenName^3",
  "familyName^3",
  "jobTitle^2",
  
  // Product/Event
  "category",
  "keywords",
]

// =============================================================================
// GRAPH VIEWS - Pre-computed graph traversals
// =============================================================================

/**
 * Graph views for common traversal patterns
 * These are materialised views for fast graph queries
 */
interface schema_graph_views {
  // Person social graph
  person_network: {
    person_id: string,
    knows_direct: number,        // Direct connections
    knows_transitive: number,   // Network size (2 hops)
    colleagues: string[],        // Same organization
    same_location: string[],     // Same city/country
  },
  
  // Organization hierarchy
  org_hierarchy: {
    org_id: string,
    parent_path: string[],       // Path to root
    child_count: number,     // Direct subsidiaries
    total_employees: number, // All employees in tree
  },
  
  // Product relationships
  product_graph: {
    product_id: string,
    related_products: string[],
    same_brand: string[],
    same_category: string[],
    alternative_offers: string[],
  },
  
  // Event relations
  event_network: {
    event_id: string,
    series_parent?: string,
    series_next?: string,
    series_previous?: string,
    similar_events: string[],
  },
}

// =============================================================================
// INVERTED INDEX - Fast filtering by values
// =============================================================================

/**
 * Inverted indexes for fast filtering by reference values
 * Maps value -> entities that have that value
 */
interface schema_inverted_index {
  // Key: property value (e.g., "New York", "Electronics")
  _key: string,
  
  // Property path (e.g., "address.addressLocality", "category")
  property_path: string,
  
  // Count of entities with this value
  entity_count: number,
  
  // Entity references
  entities: {
    _id: string,
    _type: string,
    score?: number,             // TF-IDF or similar
  }[],
  
  // Tenant
  tenant_id?: string,
}

/**
 * Commonly indexed properties for filtering
 */
const INVERTED_INDEX_PROPERTIES = [
  // Category filters
  "@type",
  "category",
  "keywords",
  
  // Location filters
  "address.addressCountry",
  "address.addressRegion", 
  "address.addressLocality",
  "address.postalCode",
  
  // Organization filters
  "brand.@id",
  "manufacturer.@id",
  "parentOrganization.@id",
  
  // Product filters  
  "itemCondition",
  "availability",
  "productGroup.@id",
  
  // Date filters
  "startDate",
  "endDate",
  "datePublished",
]

// =============================================================================
// MATERIALIZED VIEWS - Pre-computed aggregations
// =============================================================================

/**
 * Materialized views for common aggregation queries
 */
interface schema_materialized_views {
  // Type distribution
  type_counts: {
    "@type": string,
    count: number,
    updated_at: number,
  }[],
  
  // Category aggregation
  by_category: {
    category: string,
    count: number,
    avg_rating?: number,
    min_price?: number,
    max_price?: number,
  }[],
  
  // Location aggregation
  by_location: {
    country: string,
    region?: string,
    locality?: string,
    count: number,
  }[],
  
  // Time-based aggregation  
  by_date: {
    date: string,
    new_entities: number,
    updates: number,
  }[],
  
  // Rating distribution
  rating_distribution: {
    type: string,
    "1star": number,
    "2star": number,
    "3star": number,
    "4star": number,
    "5star": number,
    avg_rating: number,
  }[],
}

// =============================================================================
// MULTI-TENANT INDEXING - Tenant isolation
// =============================================================================

/**
 * Tenant-specific indexes
 */
interface schema_tenant_indexes {
  tenant_id: string,
  
  // Public index (shared data)
  public_collection: string,
  public_edges: string,
  
  // Private index (tenant data)
  private_collection: string,
  private_edges: string,
  
  // Full-text index
  fts_index: string,
  
  // Graph analysis
  graph_views: string[],
  
  // Time-series bucket
  timeseries_bucket: string,
  
  // Last updated
  last_indexed: number,
}

// =============================================================================
// AQL EXAMPLE QUERIES - Sample queries for each modality
// =============================================================================

/**
 * Example AQL (ArangoDB Query Language) queries
 */
const DOCUMENT_QUERIES = {
  // Find all Products under $50
  find_cheap_products: `
    FOR p IN schema_documents
      FILTER p.@type == "Product"
      FOR offer IN p.offers
        FILTER offer.price < 50
        RETURN { product: p.name, price: offer.price }
  `,
  
  // Find organizations in a city
  find_orgs_by_city: `
    FOR org IN schema_documents
      FILTER org.@type == "Organization"
      FILTER org.address.addressLocality == @city
      RETURN org
  `,
  
  // Full-text search
  fts_search: `
    FOR d IN schema_documents
      SEARCH ANALYZER(d.name TOKENS(@query, "default")) 
        || ANALYZER(d.description TOKENS(@query, "default"))
      RETURN d
  `,
}

/**
 * Example graph queries
 */
const GRAPH_QUERIES = {
  // Find all colleagues of a person
  find_colleagues: `
    FOR v, e, p IN 1..2 OUTBOUND @personId schema_edges
      FILTER e.relationship_type == "worksFor" 
         || e.relationship_type == "colleague"
      RETURN { vertex: v, edge: e }
  `,
  
  // Find product alternatives
  find_alternatives: `
    FOR v, e, p IN 1..1 ANY @productId schema_edges
      FILTER e.relationship_type == "relatedTo" 
         || e.relationship_type == "similarTo"
      RETURN v
  `,
  
  // Organization hierarchy
  org_hierarchy: `
    FOR v, e, p IN 1..10 OUTBOUND @orgId schema_edges
      FILTER e.relationship_type == "subOrganization"
      RETURN { org: v.name, path: p[*].name }
  `,
}

/**
 * Example time-series queries
 */
const TIMESERIES_QUERIES = {
  // Price history for a product
  price_history: `
    FOR t IN schema_timeseries
      FILTER t._id == @productId
      FILTER t.series_type == "price"
      SORT t.timestamp DESC
      LIMIT 30
      RETURN { date: t.timestamp_iso, price: t.value }
  `,
  
  // Average rating over time
  rating_trend: `
    FOR t IN schema_timeseries
      FILTER t._type == "AggregateRating"
      FILTER t.timestamp >= @startDate
      COLLECT date = DATE_FORMAT(t.timestamp, "%Y-%m-%d") 
        INTO dayData
      RETURN { 
        date, 
        avgRating: AVERAGE(dayData[*].value),
        count: LENGTH(dayData)
      }
  `,
}

// =============================================================================
// EXPORT ALL SCHEMA DEFINITIONS
// =============================================================================

export type {
  // Document store
  schema_documents,
  
  // Graph edges
  schema_edges,
  
  // Key-value
  schema_kv,
  
  // Time-series
  schema_timeseries,
  
  // Materialized views
  schema_materialized_views,
}

export const {
  // Edge type definitions
  EDGE_TYPES,
  
  // Series type definitions
  SERIES_TYPES,
  
  // FTS configuration
  schema_fts_analyzers,
  FTS_INDEXED_FIELDS,
  
  // Inverted index
  INVERTED_INDEX_PROPERTIES,
}
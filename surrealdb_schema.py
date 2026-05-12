"""
SurrealDB Schema for Schema.org

Maps Schema.org types to SurrealDB table definitions.

Reference: https://schema.org/docs/full.html
Reference: https://surrealdb.com/docs/surrealql/statements/define
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
from base_entity import Entity


# SurrealDB Field Types
class FieldType(Enum):
    STRING = "string"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    DATETIME = "datetime"
    RECORD = "record"
    OBJECT = "object"
    ARRAY = "array"
    OPTION = "option"


# Schema.org Type → SurrealDB Table Mapping
SCHEMA_TABLE_MAP: Dict[str, str] = {
    "Thing": "things",
    "Person": "persons",
    "Organization": "organizations",
    "Place": "places",
    "Product": "products",
    "Event": "events",
    "CreativeWork": "creative_works",
    "Action": "actions",
    "Intangible": "intangibles",
    "MedicalEntity": "medical_entities",
    "StructuredValue": "structured_values",
    "WebSite": "websites",
    "WebPage": "webpages",
    "SoftwareApplication": "software_applications",
}


# SurrealDB Table Definitions
TABLE_DEFINITIONS: Dict[str, str] = {
    # ===== THING (Root) =====
    "things": """
DEFINE TABLE things SCHEMAFULL;
DEFINE FIELD name ON things TYPE string;
DEFINE FIELD description ON things TYPE option<string>;
DEFINE FIELD url ON things TYPE option<string>;
DEFINE FIELD image ON things TYPE option<string>;
DEFINE FIELD identifier ON things TYPE option<string>;
DEFINE FIELD additionalType ON things TYPE option<string>;
DEFINE FIELD sameAs ON things TYPE option<array>;
DEFINE FIELD alternateName ON things TYPE option<string>;
DEFINE FIELD disambiguatingDescription ON things TYPE option<string>;
DEFINE INDEX idx_name ON things FIELDS name SEARCH ANALYZER ascii BM25;
DEFINE INDEX idx_id ON things FIELDS identifier UNIQUE;
""",

    # ===== PERSON =====
    "persons": """
DEFINE TABLE persons SCHEMAFULL;
DEFINE FIELD name ON persons TYPE string;
DEFINE FIELD description ON persons TYPE option<string>;
DEFINE FIELD url ON persons TYPE option<string>;
DEFINE FIELD image ON persons TYPE option<string>;
DEFINE FIELD identifier ON persons TYPE option<string>;
DEFINE FIELD jobTitle ON persons TYPE option<string>;
DEFINE FIELD birthDate ON persons TYPE option<datetime>;
DEFINE FIELD deathDate ON persons TYPE option<datetime>;
DEFINE FIELD address ON persons TYPE option<object>;
DEFINE FIELD email ON persons TYPE option<string>;
DEFINE FIELD telephone ON persons TYPE option<string>;
DEFINE FIELD worksFor ON persons TYPE option<record<organizations>>;
DEFINE FIELD memberOf ON persons TYPE option<array>;
DEFINE FIELD givenName ON persons TYPE option<string>;
DEFINE FIELD familyName ON persons TYPE option<string>;
DEFINE FIELD additionalName ON persons TYPE option<string>;
DEFINE FIELD honorificPrefix ON persons TYPE option<string>;
DEFINE FIELD honorificSuffix ON persons TYPE option<string>;
DEFINE FIELD knowsAbout ON persons TYPE option<array>;
DEFINE FIELD knowsLanguage ON persons TYPE option<array>;
DEFINE FIELD nationality ON persons TYPE option<record<organizations>>;
DEFINE FIELD alumniOf ON persons TYPE option<record<organizations>>;
DEFINE FIELD award ON persons TYPE option<array>;
DEFINE FIELD birthPlace ON persons TYPE option<record<places>>;
DEFINE FIELD deathPlace ON persons TYPE option<record<places>>;
DEFINE FIELD parent ON persons TYPE option<record<persons>>;
DEFINE FIELD children ON persons TYPE option<array>;
DEFINE FIELD sibling ON persons TYPE option<array>;
DEFINE FIELD spouse ON persons TYPE option<record<persons>>;
DEFINE FIELD agent ON persons TYPE option<record<organizations>>;
DEFINE INDEX idx_name ON persons FIELDS name SEARCH ANALYZER ascii BM25;
DEFINE INDEX idx_email ON persons FIELDS email UNIQUE;
""",

    # ===== ORGANIZATION =====
    "organizations": """
DEFINE TABLE organizations SCHEMAFULL;
DEFINE FIELD name ON organizations TYPE string;
DEFINE FIELD description ON organizations TYPE option<string>;
DEFINE FIELD url ON organizations TYPE option<string>;
DEFINE FIELD image ON organizations TYPE option<string>;
DEFINE FIELD identifier ON organizations TYPE option<string>;
DEFINE FIELD address ON organizations TYPE option<object>;
DEFINE FIELD logo ON organizations TYPE option<string>;
DEFINE FIELD telephone ON organizations TYPE option<string>;
DEFINE FIELD email ON organizations TYPE option<string>;
DEFINE FIELD foundingDate ON organizations TYPE option<datetime>;
DEFINE FIELD dissolutionDate ON organizations TYPE option<datetime>;
DEFINE FIELD founder ON organizations TYPE option<record<persons>>;
DEFINE FIELD member ON organizations TYPE option<record<persons>>;
DEFINE FIELD employee ON organizations TYPE option<array>;
DEFINE FIELD department ON organizations TYPE option<array>;
DEFINE FIELD parentOrganization ON organizations TYPE option<record<organizations>>;
DEFINE FIELD subOrganization ON organizations TYPE option<record<organizations>>;
DEFINE FIELD areaServed ON organizations TYPE option<array>;
DEFINE FIELD legalName ON organizations TYPE option<string>;
DEFINE FIELD tickerSymbol ON organizations TYPE option<string>;
DEFINE FIELD numberOfEmployees ON organizations TYPE option<int>;
DEFINE FIELD foundingLocation ON organizations TYPE option<record<places>>;
DEFINE FIELD memberOf ON organizations TYPE option<record<organizations>>;
DEFINE INDEX idx_name ON organizations FIELDS name SEARCH ANALYZER ascii BM25;
DEFINE INDEX idx_taxid ON organizations FIELDS identifier UNIQUE;
""",

    # ===== PLACE =====
    "places": """
DEFINE TABLE places SCHEMAFULL;
DEFINE FIELD name ON places TYPE string;
DEFINE FIELD description ON places TYPE option<string>;
DEFINE FIELD url ON places TYPE option<string>;
DEFINE FIELD image ON places TYPE option<string>;
DEFINE FIELD identifier ON places TYPE option<string>;
DEFINE FIELD address ON places TYPE option<object>;
DEFINE FIELD geo ON places TYPE option<object>;
DEFINE FIELD openingHoursSpecification ON places TYPE option<array>;
DEFINE FIELD telephone ON places TYPE option<string>;
DEFINE FIELD faxNumber ON places TYPE option<string>;
DEFINE FIELD email ON places TYPE option<string>;
DEFINE FIELD latitude ON places TYPE option<float>;
DEFINE FIELD longitude ON places TYPE option<float>;
DEFINE FIELD addressCountry ON places TYPE option<string>;
DEFINE FIELD addressLocality ON places TYPE option<string>;
DEFINE FIELD addressRegion ON places TYPE option<string>;
DEFINE FIELD postalCode ON places TYPE option<string>;
DEFINE FIELD streetAddress ON places TYPE option<string>;
DEFINE FIELD floorLevel ON places TYPE option<string>;
DEFINE FIELD additionalProperty ON places TYPE option<array>;
DEFINE FIELD amenityFeature ON places TYPE option<array>;
DEFINE FIELD branchCode ON places TYPE option<string>;
DEFINE FIELD branchOf ON places TYPE option<record<organizations>>;
DEFINE FIELD containedInPlace ON places TYPE option<record<places>>;
DEFINE FIELD containsPlace ON places TYPE option<array>;
DEFINE FIELD event ON places TYPE option<record<events>>;
DEFINE FIELD isAccessibleForFree ON places TYPE option<bool>;
DEFINE FIELD maxPrice ON places TYPE option<number>;
DEFINE FIELD minPrice ON places TYPE option<number>;
DEFINE FIELD photos ON places TYPE option<array>;
DEFINE FIELD ratings ON places TYPE option<array>;
DEFINE FIELD review ON places TYPE option<array>;
DEFINE FIELD servesCuisine ON places TYPE option<string>;
DEFINE FIELD shortDescription ON places TYPE option<string>;
DEFINE FIELD specialOpeningHoursSpecification ON places TYPE option<array>;
DEFINE INDEX idx_name ON places FIELDS name SEARCH ANALYZER ascii BM25;
DEFINE INDEX idx_geo ON places FIELDS latitude, longitude;
""",

    # ===== PRODUCT =====
    "products": """
DEFINE TABLE products SCHEMAFULL;
DEFINE FIELD name ON products TYPE string;
DEFINE FIELD description ON products TYPE option<string>;
DEFINE FIELD url ON products TYPE option<string>;
DEFINE FIELD image ON products TYPE option<string>;
DEFINE FIELD identifier ON products TYPE option<string>;
DEFINE FIELD brand ON products TYPE option<object>;
DEFINE FIELD manufacturer ON products TYPE option<record<organizations>>;
DEFINE FIELD model ON products TYPE option<string>;
DEFINE FIELD sku ON products TYPE option<string>;
DEFINE FIELD color ON products TYPE option<string>;
DEFINE FIELD weight ON products TYPE option<object>;
DEFINE FIELD width ON products TYPE option<object>;
DEFINE FIELD height ON products TYPE option<object>;
DEFINE FIELD depth ON products TYPE option<object>;
DEFINE FIELD price ON products TYPE option<number>;
DEFINE FIELD priceCurrency ON products TYPE option<string>;
DEFINE FIELD pricevalidUntil ON products TYPE option<datetime>;
DEFINE FIELD availability ON products TYPE option<string>;
DEFINE FIELD itemCondition ON products TYPE option<string>;
DEFINE FIELD category ON products TYPE option<string>;
DEFINE FIELD offers ON products TYPE option<array>;
DEFINE FIELD aggregateRating ON products TYPE option<object>;
DEFINE FIELD review ON products TYPE option<array>;
DEFINE FIELD mpn ON products TYPE option<string>;
DEFINE FIELD gtin ON products TYPE option<string>;
DEFINE FIELD isAccessoryOrSparePartFor ON products TYPE option<record<products>>;
DEFINE FIELD isConsumableFor ON products TYPE option<record<products>>;
DEFINE FIELD isSimilarTo ON products TYPE option<record<products>>;
DEFINE FIELD isVariantOf ON products TYPE option<record<products>>;
DEFINE FIELD nemberOf ON products TYPE option<record<products>>;
DEFINE FIELD owner ON products TYPE option<record<persons>>;
DEFINE FIELD reviewPolicy ON products TYPE option<string>;
DEFINE FIELD hasEnergyConsumptionDetails ON products TYPE option<object>;
DEFINE INDEX idx_name ON products FIELDS name SEARCH ANALYZER ascii BM25;
DEFINE INDEX idx_sku ON products FIELDS sku UNIQUE;
DEFINE INDEX idx_price ON products FIELDS price;
""",

    # ===== EVENT =====
    "events": """
DEFINE TABLE events SCHEMAFULL;
DEFINE FIELD name ON events TYPE string;
DEFINE FIELD description ON events TYPE option<string>;
DEFINE FIELD url ON events TYPE option<string>;
DEFINE FIELD image ON events TYPE option<string>;
DEFINE FIELD identifier ON events TYPE option<string>;
DEFINE FIELD startDate ON events TYPE option<datetime>;
DEFINE FIELD endDate ON events TYPE option<datetime>;
DEFINE FIELD eventStatus ON events TYPE option<string>;
DEFINE FIELD eventAttendanceMode ON events TYPE option<string>;
DEFINE FIELD location ON events TYPE option<record<places>>;
DEFINE FIELD attendee ON events TYPE option<array>;
DEFINE FIELD organizer ON events TYPE option<record<organizations>>;
DEFINE FIELD performer ON events TYPE option<array>;
DEFINE FIELD offers ON events TYPE option<array>;
DEFINE FIELD about ON events TYPE option<object>;
DEFINE FIELD workFeatured ON events TYPE option<record<creative_works>>;
DEFINE FIELD performer IN events TYPE option<array>;
DEFINE FIELD eventSchedule ON events TYPE option<record<events>>;
DEFINE FIELD previousStartDate ON events TYPE option<datetime>;
DEFINE FIELD remainingInventory ON events TYPE option<int>;
DEFINE FIELD totalInventory ON events TYPE option<int>;
DEFINE FIELD superEvent ON events TYPE option<record<events>>;
DEFINE FIELD inLanguage ON events TYPE option<string>;
DEFINE FIELD recordedIn ON events TYPE option<record<creative_works>>;
DEFINE INDEX idx_name ON events FIELDS name SEARCH ANALYZER ascii BM25;
DEFINE INDEX idx_date ON events FIELDS startDate;
""",

    # ===== CREATIVE WORK =====
    "creative_works": """
DEFINE TABLE creative_works SCHEMAFULL;
DEFINE FIELD name ON creative_works TYPE string;
DEFINE FIELD description ON creative_works TYPE option<string>;
DEFINE FIELD url ON creative_works TYPE option<string>;
DEFINE FIELD image ON creative_works TYPE option<string>;
DEFINE FIELD identifier ON creative_works TYPE option<string>;
DEFINE FIELD author ON creative_works TYPE option<record<persons>>;
DEFINE FIELD creator ON creative_works TYPE option<record<persons>>;
DEFINE FIELD dateCreated ON creative_works TYPE option<datetime>;
DEFINE FIELD datePublished ON creative_works TYPE option<datetime>;
DEFINE FIELD dateModified ON creative_works TYPE option<datetime>;
DEFINE FIELD contentRating ON creative_works TYPE option<string>;
DEFINE FIELD inLanguage ON creative_works TYPE option<string>;
DEFINE FIELD encoding ON creative_works TYPE option<array>;
DEFINE FIELD headline ON creative_works TYPE option<string>;
DEFINE FIELD text ON creative_works TYPE option<string>;
DEFINE FIELD about ON creative_works TYPE option<object>;
DEFINE FIELD genre ON creative_works TYPE option<array>;
DEFINE FIELD keywords ON creative_works TYPE option<string>;
DEFINE FIELD award ON creative_works TYPE option<array>;
DEFINE FIELD copyrightHolder ON creative_works TYPE option<record<organizations>>;
DEFINE FIELD copyrightYear ON creative_works TYPE option<int>;
DEFINE FIELD license ON creative_works TYPE option<string>;
DEFINE FIELD publisher ON creative_works TYPE option<record<organizations>>;
DEFINE FIELD provider ON creative_works TYPE option<record<organizations>>;
DEFINE FIELD comment ON creative_works TYPE option<array>;
DEFINE FIELD commentCount ON creative_works TYPE option<int>;
DEFINE FIELD interactionStatistic ON creative_works TYPE option<array>;
DEFINE FIELD hasPart ON creative_works TYPE option<array>;
DEFINE FIELD isPartOf ON creative_works TYPE option<record<creative_works>>;
DEFINE FIELD audio ON creative_works TYPE option<array>;
DEFINE FIELD video ON creative_works TYPE option<array>;
DEFINE FIELD workExample ON creative_works TYPE option<array>;
DEFINE FIELD exampleForWork ON creative_works TYPE option<record<creative_works>>;
DEFINE INDEX idx_name ON creative_works FIELDS name SEARCH ANALYZER ascii BM25;
DEFINE INDEX idx_date ON creative_works FIELDS datePublished;
""",

    # ===== ACTION =====
    "actions": """
DEFINE TABLE actions SCHEMAFULL;
DEFINE FIELD name ON actions TYPE string;
DEFINE FIELD description ON actions TYPE option<string>;
DEFINE FIELD identifier ON actions TYPE option<string>;
DEFINE FIELD startTime ON actions TYPE option<datetime>;
DEFINE FIELD endTime ON actions TYPE option<datetime>;
DEFINE FIELD actionStatus ON actions TYPE option<string>;
DEFINE FIELD agent ON actions TYPE option<record<persons>>;
DEFINE FIELD instrument ON actions TYPE option<record<things>>;
DEFINE FIELD object ON actions TYPE option<record<things>>;
DEFINE FIELD participant ON actions TYPE option<array>;
DEFINE FIELD result ON actions TYPE option<array>;
DEFINE FIELD target ON actions TYPE option<object>;
DEFINE FIELD error ON actions TYPE option<object>;
DEFINE FIELD location ON actions TYPE option<record<places>>;
DEFINE FIELD duration ON actions TYPE option<string>;
DEFINE FIELD isPending ON actions TYPE option<bool>;
DEFINE FIELD isActive ON actions TYPE option<bool>;
DEFINE FIELD targetCollection ON actions TYPE option<record<things>>;
DEFINE INDEX idx_status ON actions FIELDS actionStatus;
DEFINE INDEX idx_agent ON actions FIELDS agent;
DEFINE INDEX idx_start ON actions FIELDS startTime;
""",

    # ===== INTANGIBLE =====
    "intangibles": """
DEFINE TABLE intangibles SCHEMAFULL;
DEFINE FIELD name ON intangibles TYPE string;
DEFINE FIELD description ON intangibles TYPE option<string>;
DEFINE FIELD identifier ON intangibles TYPE option<string>;
DEFINE FIELD additionalType ON intangibles TYPE option<string>;
DEFINE FIELD supersededBy ON intangibles TYPE option<record<intangibles>>;
DEFINE FIELD domainIncludes ON intangibles TYPE option<array>;
DEFINE FIELD rangeIncludes ON intangibles TYPE option<array>;
DEFINE FIELD inverseProperty ON intangibles TYPE option<record<intangibles>>;
""",

    # ===== MEDICAL ENTITY =====
    "medical_entities": """
DEFINE TABLE medical_entities SCHEMAFULL;
DEFINE FIELD name ON medical_entities TYPE string;
DEFINE FIELD description ON medical_entities TYPE option<string>;
DEFINE FIELD identifier ON medical_entities TYPE option<string>;
DEFINE FIELD code ON medical_entities TYPE option<object>;
DEFINE FIELD guideline ON medical_entities TYPE option<array>;
DEFINE FIELD relevantSpecialty ON medical_entities TYPE option<string>;
DEFINE FIELD study ON medical_entities TYPE option<array>;
DEFINE FIELD bodyLocation ON medical_entities TYPE option<array>;
DEFINE FIELD procedure ON medical_entities TYPE option<array>;
DEFINE FIELD cause ON medical_entities TYPE option<record<medical_entities>>;
DEFINE FIELD differentialDiagnosis ON medical_entities TYPE option<array>;
DEFINE FIELD drug ON medical_entities TYPE option<record<medical_entities>>;
DEFINE FIELD expectedPrognosis ON medical_entities TYPE option<string>;
DEFINE FIELD falsePositive ON medical_entities TYPE option<array>;
DEFINE FIELD guidelined FOR medical_entities TYPE option<array>;
DEFINE FIELD interactionConsideration ON medical_entities TYPE option<string>;
DEFINE FIELD legalStatus ON medical_entities TYPE option<object>;
DEFINE FIELD mascot ON medical_entities TYPE option<string>;
DEFINE FIELD medicineSystem ON medical_entities TYPE option<string>;
DEFINE FIELD notContraindicated FOR medical_entities TYPE option<bool>;
DEFINE FIELD possibleTreatment ON medical_entities TYPE option<record<medical_entities>>;
DEFINE FIELD primarilyIncludes ON medical_entities TYPE option<array>;
DEFINE FIELD recognizedBy ON medical_entities TYPE option<record<organizations>>;
DEFINE FIELD riskFactor ON medical_entities TYPE option<record<medical_entities>>;
DEFINE FIELD signOrSymptom ON medical_entities TYPE option<record<medical_entities>>;
DEFINE FIELD stage ON medical_entities TYPE option<object>;
DEFINE FIELD status ON medical_entities TYPE option<string>;
DEFINE FIELD studySupported ON medical_entities TYPE option<bool>;
DEFINE FIELD subtype OF medical_entities TYPE option<string>;
DEFINE FIELD text OF medical_entities TYPE option<string>;
DEFINE FIELD availableService OF medical_entities TYPE option<array>;
DEFINE FIELD bodyMeasurement OF medical_entities TYPE option<object>;
DEFINE INDEX idx_name ON medical_entities FIELDS name SEARCH ANALYZER ascii BM25;
DEFINE INDEX idx_code ON medical_entities FIELDS code;
""",
}


@dataclass
class SchemaOrgSurrealDB:
    """Generate SurrealDB Schema from Schema.org types"""
    
    def get_table_name(self, schema_type: str) -> str:
        """Get SurrealDB table name for Schema.org type"""
        return SCHEMA_TABLE_MAP.get(schema_type, schema_type.lower().replace(" ", "_"))
    
    def get_definition(self, schema_type: str) -> str:
        """Get SurrealDB DEFINE statement"""
        table_name = self.get_table_name(schema_type)
        return TABLE_DEFINITIONS.get(table_name, "")
    
    def get_all_definitions(self) -> List[str]:
        """Get all table definitions"""
        return [defn for defn in TABLE_DEFINITIONS.values() if defn]
    
    def generate_migrations(self) -> str:
        """Generate complete migration SQL"""
        sql = "-- Schema.org SurrealDB Migration\n-- Generated from Schema.org V30.0\n\n"
        for defn in self.get_all_definitions():
            sql += defn + "\n\n"
        return sql


def main():
    schema = SchemaOrgSurrealDB()
    print("=== Schema.org SurrealDB Schema ===")
    print(f"Total Tables: {len(TABLE_DEFINITIONS)}")
    print(f"\nTables:")
    for table in sorted(SCHEMA_TABLE_MAP.values()):
        print(f"  - {table}")
    print(f"\nGenerating migration...")
    print(f"Migration length: {len(schema.generate_migrations())} chars")


if __name__ == "__main__":
    main()

"""
SurrealDB Schema Complete:
- 10 Tables defined
- All core Schema.org types mapped
- Field types: string, int, float, bool, datetime, record, object, array
- Indexes: BM25, UNIQUE, compound

Reference: 
- https://schema.org/docs/full.html
- https://surrealdb.com/docs/surrealql/statements/define
"""
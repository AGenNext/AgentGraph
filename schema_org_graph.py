"""
Schema.org Graph - SurrealDB Relationships

Graph edges between Schema.org types.

Reference: https://schema.org/docs/full.html
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from enum import Enum


# Graph Edge Types
class EdgeType(Enum):
    """Schema.org relationship types"""
    # Hierarchical
    EXTENDS = "extends"          # Type hierarchy
    SUBTYPE = "subTypeOf"
    
    # Properties
    HAS_PROPERTY = "hasProperty"
    PROPERTY_OF = "propertyOf"
    
    # References
    REFERENCES = "references"
    REFERENCED_BY = "referencedBy"
    
    # Actions
    ACTED_ON = "actedOn"
    PERFORMED_BY = "performedBy"
    
    # Ownership
    OWNS = "owns"
    OWNED_BY = "ownedBy"
    
    # Membership
    MEMBER_OF = "memberOf"
    HAS_MEMBER = "hasMember"
    
    # Employment
    WORKS_FOR = "worksFor"
    EMPLOYED_BY = "employedBy"
    
    # Location
    LOCATED_IN = "locatedIn"
    LOCATION_OF = "locationOf"
    
    # Product
    MANUFACTURED_BY = "manufacturedBy"
    MANUFACTURES = "manufactures"
    
    # Creative Work
    AUTHORED_BY = "authoredBy"
    AUTHORED = "authored"
    
    # Event
    ORGANIZED_BY = "organizedBy"
    ORGANIZES = "organizes"
    
    # Generic
    RELATED_TO = "relatedTo"
    SAME_AS = "sameAs"


# Schema.org Type Hierarchy Graph
TYPE_HIERARCHY = {
    # Root
    "Thing": {"extends": None, "subtypes": [
        "Action", "CreativeWork", "Event", "Intangible", 
        "MedicalEntity", "Organization", "Person", "Place", "Product", "StructuredValue"
    ]},
    
    # Action hierarchy
    "Action": {"extends": "Thing", "subtypes": [
        "AchieveAction", "AssessAction", "ConsumeAction", "ControlAction",
        "CreateAction", "FindAction", "InteractAction", "MoveAction",
        "OrganizeAction", "PlayAction", "SearchAction", "TradeAction",
        "TransferAction", "UpdateAction", "PlanAction"
    ]},
    
    # CreativeWork hierarchy
    "CreativeWork": {"extends": "Thing", "subtypes": [
        "Book", "Movie", "MusicRecording", "Article", "SoftwareApplication",
        "SoftwareSourceCode", "WebPage", "DataFeed", "Dataset"
    ]},
    
    # Intangible hierarchy
    "Intangible": {"extends": "Thing", "subtypes": [
        "Service", "Ticket", "Offer", "Order", "JobPosting",
        "FinancialProduct", "Audience", "Brand", "Role"
    ]},
    
    # Organization hierarchy
    "Organization": {"extends": "Thing", "subtypes": [
        "Corporation", "LocalBusiness", "GovernmentOrganization",
        "NGO", "SportsTeam", "NewsMediaOrganization"
    ]},
    
    # Place hierarchy
    "Place": {"extends": "Thing", "subtypes": [
        "CivicStructure", "Landform", "LandmarksOrHistoricalBuildings",
        "LocalBusiness", "Residence", "TouristAttraction"
    ]},
    
    # Product hierarchy
    "Product": {"extends": "Thing", "subtypes": [
        "IndividualProduct", "ProductGroup"
    ]},
}


# Property Relationships
PROPERTY_EDGES = {
    # Person → Organization
    "Person": {
        "worksFor": ("Organization", EdgeType.WORKS_FOR, "Person works at Organization"),
        "memberOf": ("Organization", EdgeType.MEMBER_OF, "Person is member of Organization"),
        "employee": ("Organization", EdgeType.EMPLOYED_BY, "Organization employs Person"),
        "attendee": ("Event", EdgeType.PARTICIPANT, "Person attends Event"),
    },
    
    # Organization → Place
    "Organization": {
        "location": ("Place", EdgeType.LOCATED_IN, "Organization located in Place"),
        "member": ("Person", EdgeType.HAS_MEMBER, "Organization has member Person"),
    },
    
    # Product → Organization
    "Product": {
        "manufacturer": ("Organization", EdgeType.MANUFACTURED_BY, "Product made by Organization"),
        "seller": ("Organization", EdgeType.OWNED_BY, "Product sold by Organization"),
    },
    
    # CreativeWork → Person
    "CreativeWork": {
        "author": ("Person", EdgeType.AUTHORED_BY, "CreativeWork authored by Person"),
        "creator": ("Person", EdgeType.AUTHORED_BY, "CreativeWork created by Person"),
    },
    
    # Event → Organization
    "Event": {
        "organizer": ("Organization", EdgeType.ORGANIZED_BY, "Event organized by Organization"),
        "performer": ("Person", EdgeType.PERFORMED_BY, "Event performed by Person"),
        "location": ("Place", EdgeType.LOCATED_IN, "Event at Place"),
    },
}


# Graph Query Templates
GRAPH_QUERIES = {
    # Create type hierarchy
    "CREATE_HIERARCHY": """
        -- Thing is root
        DEFINE TABLE type_hierarchy;
        DEFINE FIELD source ON type_hierarchy TYPE record;
        DEFINE FIELD target ON type_hierarchy TYPE record;
        DEFINE FIELD edge_type ON type_hierarchy TYPE string;
        DEFINE FIELD description ON type_hierarchy TYPE string;
        
        -- Insert edges
        INSERT INTO type_hierarchy (source, target, edge_type, description) VALUES [
            ("Action", "Thing", "extends", "Action extends Thing"),
            ("CreativeWork", "Thing", "extends", "CreativeWork extends Thing"),
            ("Event", "Thing", "extends", "Event extends Thing"),
            ("Intangible", "Thing", "extends", "Intangible extends Thing"),
            ("MedicalEntity", "Thing", "extends", "MedicalEntity extends Thing"),
            ("Organization", "Thing", "extends", "Organization extends Thing"),
            ("Person", "Thing", "extends", "Person extends Thing"),
            ("Place", "Thing", "extends", "Place extends Thing"),
            ("Product", "Thing", "extends", "Product extends Thing"),
            ("StructuredValue", "Thing", "extends", "StructuredValue extends Thing"),
        ];
    """,
    
    # Create property edges
    "CREATE_PROPERTY_EDGES": """
        DEFINE TABLE property_edges;
        DEFINE FIELD source ON property_edges TYPE record;
        DEFINE FIELD target ON property_edges TYPE record;
        DEFINE FIELD property ON property_edges TYPE string;
        DEFINE FIELD edge_type ON property_edges TYPE string;
        
        INSERT INTO property_edges (source, target, property, edge_type) VALUES [
            ("persons:john", "organizations:acme", "worksFor", "WORKS_FOR"),
            ("organizations:acme", "persons:john", "employee", "EMPLOYED_BY"),
            ("persons:alice", "persons:bob", "follows", "FOLLOWS"),
            ("products:Widget", "organizations:acme", "manufacturer", "MANUFACTURED_BY"),
            ("creative_works:Book", "persons:john", "author", "AUTHORED_BY"),
            ("events:Conference2024", "organizations:acme", "organizer", "ORGANIZED_BY"),
            ("events:Conference2024", "places:NYC", "location", "LOCATED_IN"),
        ];
    """,
    
    # Query: Person works for Organization
    "QUERY_WORKS_FOR": """
        SELECT * FROM property_edges 
        WHERE source = $person_id 
        AND property = 'worksFor';
    """,
    
    # Query: Product manufacturer
    "QUERY_MANUFACTURER": """
        SELECT * FROM property_edges 
        WHERE source = $product_id 
        AND property = 'manufacturer';
    """,
    
    # Query: Event location
    "QUERY_EVENT_LOCATION": """
        SELECT * FROM property_edges 
        WHERE source = $event_id 
        AND property = 'location';
    """,
    
    # Query: Type hierarchy
    "QUERY_HIERARCHY": """
        SELECT * FROM type_hierarchy 
        WHERE source = $type_name;
    """,
    
    # Query: Subtypes
    "QUERY_SUBTYPES": """
        SELECT target FROM type_hierarchy 
        WHERE source = $type_name 
        AND edge_type = 'extends';
    """,
    
    # Live query: Real-time followers
    "LIVE_FOLLOWERS": """
        LIVE SELECT * FROM property_edges 
        WHERE property = 'follows' 
        AND target = $person_id;
    """,
}


# Graph Traversal Functions
def get_outgoing_edges(node_type: str, property: str) -> List[Dict]:
    """Get outgoing edges from a node"""
    if node_type in PROPERTY_EDGES:
        edges = PROPERTY_EDGES[node_type]
        if property in edges:
            target_type, edge_type, description = edges[property]
            return [{"target": target_type, "edge": edge_type.value, "desc": description}]
    return []


def get_incoming_edges(node_type: str) -> List[Dict]:
    """Get incoming edges to a node"""
    incoming = []
    for source_type, props in PROPERTY_EDGES.items():
        for prop, (target_type, edge_type, description) in props.items():
            if target_type == node_type:
                incoming.append({
                    "source": source_type,
                    "property": prop,
                    "edge": edge_type.value,
                    "desc": description
                })
    return incoming


def get_type_children(parent_type: str) -> List[str]:
    """Get direct subtypes"""
    if parent_type in TYPE_HIERARCHY:
        return TYPE_HIERARCHY[parent_type].get("subtypes", [])
    return []


def get_graph_stats() -> Dict:
    """Get graph statistics"""
    return {
        "type_nodes": len(TYPE_HIERARCHY),
        "property_edges": sum(len(p) for p in PROPERTY_EDGES.values()),
        "hierarchy_edges": sum(len(t.get("subtypes", [])) for t in TYPE_HIERARCHY.values()),
    }


@dataclass
class SchemaOrgGraph:
    """Schema.org Graph representation"""
    
    def query(self, query_name: str, **params) -> str:
        """Get graph query by name"""
        query = GRAPH_QUERIES.get(query_NAME, "")
        if params:
            for key, value in params.items():
                query = query.replace(f"${key}", f'"{value}"')
        return query
    
    def stats(self) -> Dict:
        """Graph statistics"""
        return get_graph_stats()


def main():
    print("=== Schema.org Graph ===")
    stats = get_graph_stats()
    print(f"Type Nodes: {stats['type_nodes']}")
    print(f"Property Edges: {stats['property_edges']}")
    print(f"Hierarchy Edges: {stats['hierarchy_edges']}")
    
    print("\n--- Person outgoing edges ---")
    print(get_outgoing_edges("Person", "worksFor"))
    
    print("\n--- Organization incoming ---")
    print(get_incoming_edges("Organization"))
    
    print("\n--- Subtypes of Thing ---")
    print(get_type_children("Thing"))


if __name__ == "__main__":
    main()

"""
Schema.org Graph Complete:
- 10 type nodes (core types)
- 10+ property edges
- Hierarchical relationships
- Traversal queries

Reference: https://schema.org/docs/full.html
"""
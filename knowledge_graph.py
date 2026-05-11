"""
Wikipedia Knowledge Graph Builder

This module builds a knowledge graph from Wikipedia data:
- Fetch person data from Wikipedia API
- Extract structured entities
- Build relationships
- Store in graph format

Reference:
- Wikipedia API: https://www.mediawiki.org/wiki/API:Main_page
- WikiData: https://www.wikidata.org/wiki/Wikidata:Main_Page
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Set
from datetime import datetime
from enum import Enum
import urllib.request
import urllib.parse
import json


# =============================================================================
# KNOWLEDGE GRAPH TYPES
# =============================================================================

class NodeType(Enum):
    """Types of nodes in knowledge graph"""
    PERSON = "Person"
    ORGANIZATION = "Organization"
    PLACE = "Place"
    EVENT = "Event"
    WORK = "CreativeWork"
    CONCEPT = "Concept"


class RelationshipType(Enum):
    """Types of relationships"""
    # Person relationships
    SPOUSE = "spouse"
    CHILD = "child"
    PARENT = "parent"
    SIBLING = "sibling"
    COLLEAGUE = "colleague"
    FRIEND = "friend"
    
    # Work relationships
    EMPLOYEE = "employee"
    EMPLOYER = "employer"
    FOUNDER = "founder"
    PARTNER = "partner"
    
    # Other
    LOCATED_IN = "locatedIn"
    PARTICIPATED_IN = "participatedIn"
    WORKED_WITH = "workedWith"
    KNOWN_FOR = "knownFor"


@dataclass
class WikiNode:
    """A node in the knowledge graph"""
    id: str
    node_type: NodeType
    name: str
    description: Optional[str] = None
    
    # Properties
    properties: Dict[str, Any] = field(default_factory=dict)
    
    # Wikipedia data
    wiki_title: Optional[str] = None
    wiki_url: Optional[str] = None
    wiki_id: Optional[str] = None
    
    # Links
    incoming_edges: Set[str] = field(default_factory=set)
    outgoing_edges: Set[str] = field(default_factory=set)
    
    def add_property(self, key: str, value: Any):
        self.properties[key] = value
    
    def to_json(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.node_type.value,
            "name": self.name,
            "description": self.description,
            "properties": self.properties,
            "wiki_title": self.wiki_title,
            "wiki_url": self.wiki_url
        }


@dataclass
class WikiEdge:
    """An edge in the knowledge graph"""
    source_id: str
    target_id: str
    relationship: RelationshipType
    confidence: float = 1.0
    source: str = "wikipedia"
    
    def to_json(self) -> Dict[str, Any]:
        return {
            "source": self.source_id,
            "target": self.target_id,
            "relationship": self.relationship.value,
            "confidence": self.confidence,
            "source": self.source
        }


# =============================================================================
# WIKIPEDIA API CLIENT
# =============================================================================

class WikipediaClient:
    """Client for Wikipedia API"""
    
    BASE_URL = "https://en.wikipedia.org/w/api.php"
    
    def __init__(self):
        self.cache: Dict[str, Dict] = {}
    
    def _make_request(self, params: Dict) -> Dict:
        """Make API request"""
        params["format"] = "json"
        params["origin"] = "*"
        
        url = f"{self.BASE_URL}?{urllib.parse.urlencode(params)}"
        
        # Use cache
        if url in self.cache:
            return self.cache[url]
        
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
                self.cache[url] = data
                return data
        except Exception as e:
            print(f"Error: {e}")
            return {}
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Search Wikipedia"""
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": limit
        }
        
        data = self._make_request(params)
        return data.get("query", {}).get("search", [])
    
    def get_page_summary(self, title: str) -> Dict:
        """Get page summary"""
        params = {
            "action": "query",
            "titles": title,
            "prop": "extracts|info|links",
            "exintro": True,
            "explaintext": True,
            "inprop": "url"
        }
        
        data = self._make_request(params)
        pages = data.get("query", {}).get("pages", {})
        
        for page_id, page in pages.items():
            if page_id != "-1":
                return page
        return {}
    
    def get_page_content(self, title: str) -> Dict:
        """Get full page content"""
        params = {
            "action": "query",
            "titles": title,
            "prop": "revisions",
            "rvprop": "content",
            "rvslots": "main"
        }
        
        data = self._make_request(params)
        pages = data.get("query", {}).get("pages", {})
        
        for page_id, page in pages.items():
            if page_id != "-1":
                return page
        return {}
    
    def get_embedded_in(self, title: str) -> List[Dict]:
        """Get pages that embed this page"""
        params = {
            "action": "query",
            "titles": title,
            "list": "embeddedin",
            "eilimit": 50
        }
        
        data = self._make_request(params)
        return data.get("query", {}).get("embeddedin", [])
    
    def get_links(self, title: str) -> List[str]:
        """Get outgoing links"""
        params = {
            "action": "query",
            "titles": title,
            "prop": "links",
            "pllimit": 100
        }
        
        data = self._make_request(params)
        pages = data.get("query", {}).get("pages", {})
        
        links = []
        for page_id, page in pages.items():
            for link in page.get("links", []):
                links.append(link["title"])
        return links
    
    def get_categories(self, title: str) -> List[str]:
        """Get page categories"""
        params = {
            "action": "query",
            "titles": title,
            "prop": "categories",
            "cllimit": 50
        }
        
        data = self._make_request(params)
        pages = data.get("query", {}).get("pages", {})
        
        categories = []
        for page_id, page in pages.items():
            for cat in page.get("categories", []):
                categories.append(cat["title"].replace("Category:", ""))
        return categories


# =============================================================================
# KNOWLEDGE GRAPH BUILDER
# =============================================================================

class WikipediaKnowledgeGraph:
    """Build knowledge graph from Wikipedia"""
    
    # Person properties to extract
    PERSON_PROPERTIES = [
        "born", "died", "birth_place", "death_place",
        "occupation", "spouse", "children", "parents",
        "education", "employer", "known_for", "awards",
        "nationality", "religion", "party"
    ]
    
    def __init__(self):
        self.wiki_client = WikipediaClient()
        self.nodes: Dict[str, WikiNode] = {}
        self.edges: List[WikiEdge] = []
        self.node_counter = 0
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID"""
        self.node_counter += 1
        return f"wiki_{self.node_counter}"
    
    def _normalize_name(self, name: str) -> str:
        """Normalize Wikipedia title"""
        return name.replace(" ", "_")
    
    def add_person(self, name: str, fetch_details: bool = True) -> WikiNode:
        """Add a person node"""
        node_id = self._generate_id(name)
        wiki_title = self._normalize_name(name)
        
        node = WikiNode(
            id=node_id,
            node_type=NodeType.PERSON,
            name=name,
            wiki_title=wiki_title,
            wiki_url=f"https://en.wikipedia.org/wiki/{wiki_title}"
        )
        
        # Fetch details if requested
        if fetch_details:
            summary = self.wiki_client.get_page_summary(wiki_title)
            if summary:
                node.description = summary.get("extract", "")[:500]
                node.wiki_id = str(summary.get("pageid", ""))
                
                # Extract infobox data
                self._extract_infobox_data(node, summary)
        
        self.nodes[node_id] = node
        return node
    
    def _extract_infobox_data(self, node: WikiNode, summary: Dict):
        """Extract data from infobox"""
        # Store basic properties
        if summary.get("description"):
            node.add_property("description", summary["description"])
        
        # Extract from categories
        categories = self.wiki_client.get_categories(node.wiki_title)
        for cat in categories:
            if "birth" in cat.lower():
                node.add_property("category", cat)
            elif "occupation" in cat.lower():
                node.add_property("occupation_category", cat)
    
    def add_relationship(
        self, 
        source: str, 
        target: str, 
        rel_type: RelationshipType,
        confidence: float = 1.0
    ):
        """Add relationship between nodes"""
        edge = WikiEdge(
            source_id=source,
            target_id=target,
            relationship=rel_type,
            confidence=confidence
        )
        self.edges.append(edge)
        
        # Update node edges
        if source in self.nodes:
            self.nodes[source].outgoing_edges.add(target)
        if target in self.nodes:
            self.nodes[target].incoming_edges.add(source)
    
    def build_from_wikipedia(self, seed_person: str, depth: int = 2) -> int:
        """
        Build knowledge graph from Wikipedia person
        depth: how many levels of links to follow
        """
        visited = set()
        queue = [(seed_person, 0)]
        
        while queue:
            name, level = queue.pop(0)
            
            if name in visited or level > depth:
                continue
            
            visited.add(name)
            
            # Add person
            person = self.add_person(name)
            
            # Get related pages
            try:
                links = self.wiki_client.get_links(self._normalize_name(name))
                
                # Add related people
                for link in links[:20]:  # Limit
                    # Check if it's a person-related link
                    if self._is_person_related(link):
                        queue.append((link, level + 1))
                        
                        # Add node
                        related = self.add_person(link, fetch_details=False)
                        
                        # Add relationship
                        self.add_relationship(
                            person.id,
                            related.id,
                            RelationshipType.KNOWN_FOR
                        )
            except Exception as e:
                print(f"Error processing {name}: {e}")
        
        return len(self.nodes)
    
    def _is_person_related(self, title: str) -> bool:
        """Check if title is person-related"""
        person_indicators = [
            "born", "died", "actor", "singer", "writer", "politician",
            "scientist", "athlete", "director", "producer", "artist"
        ]
        title_lower = title.lower()
        return any(indicator in title_lower for indicator in person_indicators)
    
    def search_person(self, query: str) -> List[WikiNode]:
        """Search for person"""
        results = self.wiki_client.search(f"{query} born")
        
        persons = []
        for result in results[:10]:
            name = result["title"]
            person = self.add_person(name)
            persons.append(person)
        
        return persons
    
    def get_person_connections(self, person_id: str) -> Dict[str, List[WikiNode]]:
        """Get all connections for a person"""
        if person_id not in self.nodes:
            return {}
        
        person = self.nodes[person_id]
        
        connections = {
            "outgoing": [],
            "incoming": []
        }
        
        for edge in self.edges:
            if edge.source_id == person_id:
                if edge.target_id in self.nodes:
                    connections["outgoing"].append(self.nodes[edge.target_id])
            elif edge.target_id == person_id:
                if edge.source_id in self.nodes:
                    connections["incoming"].append(self.nodes[edge.source_id])
        
        return connections
    
    def to_json(self) -> Dict[str, Any]:
        """Export to JSON"""
        return {
            "nodes": [n.to_json() for n in self.nodes.values()],
            "edges": [e.to_json() for e in self.edges],
            "metadata": {
                "total_nodes": len(self.nodes),
                "total_edges": len(self.edges),
                "generated_at": datetime.now().isoformat()
            }
        }
    
    def to_jsonld(self) -> List[Dict]:
        """Export as JSON-LD"""
        graph = []
        
        for node in self.nodes.values():
            entity = {"@type": node.node_type.value}
            
            if node.id:
                entity["@id"] = node.id
            if node.name:
                entity["name"] = node.name
            if node.description:
                entity["description"] = node.description
            
            # Add properties
            for key, value in node.properties.items():
                entity[key] = value
            
            graph.append(entity)
        
        return graph


# =============================================================================
# PRE-BUILT KNOWLEDGE GRAPHS
# =============================================================================

class FamousPeopleGraph(WikipediaKnowledgeGraph):
    """Pre-built graphs for famous people"""
    
    def build_tech_ceo_graph(self):
        """Build graph of tech CEOs"""
        ceos = [
            "Elon Musk", "Tim Cook", "Satya Nadella", "Mark Zuckerberg",
            "Jeff Bezos", "Larry Page", "Sergey Brin", "Steve Jobs",
            "Bill Gates", " Sundar Pichai", "Sam Altman", "Marc Benioff"
        ]
        
        for ceo in ceos:
            self.add_person(ceo)
    
    def build_actors_graph(self):
        """Build graph of famous actors"""
        actors = [
            "Leonardo DiCaprio", "Robert De Niro", "Al Pacino",
            "Tom Hanks", "Brad Pitt", "Johnny Depp", "Will Smith",
            "Denzel Washington", "Morgan Freeman", "Samuel L. Jackson"
        ]
        
        for actor in actors:
            self.add_person(actor)
    
    def build_scientists_graph(self):
        """Build graph of famous scientists"""
        scientists = [
            "Albert Einstein", "Isaac Newton", "Stephen Hawking",
            "Marie Curie", "Charles Darwin", "Nikola Tesla",
            "Galileo Galilei", "Carl Sagan", "Neil deGrasse Tyson"
        ]
        
        for scientist in scientists:
            self.add_person(scientist)


# =============================================================================
# USAGE EXAMPLE
# =============================================================================

def main():
    """Example: Build knowledge graph from Wikipedia"""
    
    print("=== Wikipedia Knowledge Graph ===\n")
    
    # Create graph
    graph = WikipediaKnowledgeGraph()
    
    # Build from a seed person
    print("Building graph from Elon Musk...")
    graph.build_from_wikipedia("Elon Musk", depth=1)
    
    print(f"\nNodes: {len(graph.nodes)}")
    print(f"Edges: {len(graph.edges)}")
    
    # Show some nodes
    print("\nSample nodes:")
    for i, node in enumerate(list(graph.nodes.values())[:5]):
        print(f"  {i+1}. {node.name} ({node.node_type.value})")
    
    # Export
    print("\n--- JSON Export ---")
    json_data = graph.to_json()
    print(f"Total: {json_data['metadata']['total_nodes']} nodes, {json_data['metadata']['total_edges']} edges")
    
    # Search
    print("\n--- Search ---")
    results = graph.search_person("Musk")
    print(f"Found: {len(results)} results")


if __name__ == "__main__":
    main()


"""
Wikipedia Knowledge Graph Builder

Usage:

    # Build from Wikipedia person
    graph = WikipediaKnowledgeGraph()
    graph.build_from_wikipedia("Elon Musk", depth=2)
    
    # Get connections
    connections = graph.get_person_connections(person_id)
    
    # Export
    print(graph.to_jsonld())

References:
    - Wikipedia API: https://www.mediawiki.org/wiki/API:Main_page
    - WikiData: https://www.wikidata.org/wiki/Wikidata:Main_Page
    - Schema.org: https://schema.org
"""
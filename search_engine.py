"""
Search Engine

Full-text search and query engine:
- Search all databases
- Filters, Facets
- Ranking, Scoring
- Autocomplete, Suggestions

Reference:
- Elasticsearch: https://www.elastic.co/guide/
- Meilisearch: https://www.meilisearch.com/
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Callable
from datetime import datetime
from enum import Enum
import re


# =============================================================================
# SEARCH TYPES
# =============================================================================

class SearchType(Enum):
    """Search types"""
    EXACT = "exact"
    FUZZY = "fuzzy"
    PHRASE = "phrase"
    WILDCARD = "wildcard"
    REGEX = "regex"
    BOOLEAN = "boolean"


class Operator(Enum):
    """Boolean operators"""
    AND = "AND"
    OR = "OR"
    NOT = "NOT"


class SortOrder(Enum):
    """Sort order"""
    ASC = "asc"
    DESC = "desc"


@dataclass
class SearchResult:
    """Search result"""
    id: str
    score: float = 0.0
    
    data: Dict[str, Any] = field(default_factory=dict)
    
    highlights: List[str] = field(default_factory=list)
    
    faceted: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchQuery:
    """Search query"""
    query: str
    
    search_type: SearchType = SearchType.FUZZY
    
    # Filters
    filters: Dict[str, Any] = field(default_factory=dict)
    facet_filters: List[Dict] = field(default_factory=list)
    
    # Pagination
    page: int = 1
    page_size: int = 10
    
    # Sorting
    sort_by: Optional[str] = None
    sort_order: SortOrder = SortOrder.DESC
    
    # Fields
    fields: List[str] = field(default_factory=list)
    
    # Highlight
    highlight: bool = True
    highlight_tags: List[str] = field(default_factory=list)


# =============================================================================
# SEARCH ENGINE
# =============================================================================

class SearchEngine:
    """Full-text search engine"""
    
    def __init__(self):
        self.documents: Dict[str, Dict[str, Any]] = {}
        self.inverted_index: Dict[str, List[str]] = {}
        self.facets: Dict[str, Dict[str, int]] = {}
        self.stemmer = Stemmer()
    
    def index(self, doc_id: str, document: Dict[str, Any]):
        """Index a document"""
        self.documents[doc_id] = document
        
        # Build inverted index
        text = self._extract_text(document)
        tokens = self._tokenize(text)
        
        for token in tokens:
            if token not in self.inverted_index:
                self.inverted_index[token] = []
            self.inverted_index[token].append(doc_id)
        
        # Build facets
        for field, value in document.items():
            if isinstance(value, str):
                if field not in self.facets:
                    self.facets[field] = {}
                self.facets[field][value] = self.facets[field].get(value, 0) + 1
    
    def _extract_text(self, document: Dict) -> str:
        """Extract searchable text"""
        parts = []
        for value in document.values():
            if isinstance(value, str):
                parts.append(value)
            elif isinstance(value, (list, tuple)):
                parts.extend([str(v) for v in value])
        return " ".join(parts)
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text"""
        text = text.lower()
        tokens = re.findall(r'\w+', text)
        
        # Apply stemming
        tokens = [self.stemmer.stem(t) for t in tokens]
        
        return list(set(tokens))
    
    def search(self, query: SearchQuery) -> List[SearchResult]:
        """Search documents"""
        results = []
        
        # Get matching documents
        matching_docs = set()
        
        query_tokens = self._tokenize(query.query)
        
        if query.search_type == SearchType.EXACT:
            # Exact match
            for doc_id, doc in self.documents.items():
                if query.query.lower() in str(doc).lower():
                    matching_docs.add(doc_id)
        
        elif query.search_type == SearchType.WILDCARD:
            # Wildcard
            pattern = query.query.replace("*", ".*").replace("?", ".")
            regex = re.compile(pattern, re.IGNORECASE)
            for doc_id, doc in self.documents.items():
                if regex.search(str(doc)):
                    matching_docs.add(doc_id)
        
        elif query.search_type == SearchType.REGEX:
            # Regex
            regex = re.compile(query.query, re.IGNORECASE)
            for doc_id, doc in self.documents.items():
                if regex.search(str(doc)):
                    matching_docs.add(doc_id)
        
        else:
            # Fuzzy/standard - use inverted index
            for token in query_tokens:
                if token in self.inverted_index:
                    matching_docs.update(self.inverted_index[token])
        
        # Calculate scores
        query_length = len(query_tokens)
        
        for doc_id in matching_docs:
            doc = self.documents[doc_id]
            
            # Calculate score
            score = 0.0
            if query_tokens:
                doc_tokens = self._tokenize(self._extract_text(doc))
                matches = len(set(query_tokens) & set(doc_tokens))
                score = matches / query_length
            
            # Apply filters
            if query.filters:
                if not self._matches_filters(doc, query.filters):
                    continue
            
            # Create result
            result = SearchResult(
                id=doc_id,
                score=score,
                data=doc,
                highlights=self._highlight(doc, query.query)
            )
            results.append(result)
        
        # Sort results
        results.sort(key=lambda r: r.score, reverse=True)
        
        # Apply pagination
        start = (query.page - 1) * query.page_size
        end = start + query.page_size
        results = results[start:end]
        
        return results
    
    def _matches_filters(self, doc: Dict, filters: Dict) -> bool:
        """Check if document matches filters"""
        for field, value in filters.items():
            if field not in doc:
                return False
            if isinstance(value, list):
                if doc[field] not in value:
                    return False
            elif doc[field] != value:
                return False
        return True
    
    def _highlight(self, document: Dict, query: str) -> List[str]:
        """Highlight matching terms"""
        highlights = []
        
        for field, value in document.items():
            if isinstance(value, str):
                if query.lower() in value.lower():
                    highlighted = value.replace(
                        query, f"<em>{query}</em>"
                    )
                    highlights.append(f"{field}: {highlighted}")
        
        return highlights
    
    def facets(self, field: str) -> Dict[str, int]:
        """Get facet counts"""
        return self.facets.get(field, {})
    
    def autocomplete(self, prefix: str, limit: int = 5) -> List[str]:
        """Autocomplete suggestions"""
        suggestions = []
        prefix = prefix.lower()
        
        for token in self.inverted_index.keys():
            if token.startswith(prefix):
                suggestions.append(token)
        
        return suggestions[:limit]
    
    def searchAll(self, query: str) -> Dict[str, Any]:
        """Search across all indexed documents"""
        
        sq = SearchQuery(query=query)
        results = self.search(sq)
        
        return {
            "query": query,
            "total": len(results),
            "results": [r.data for r in results[:10]]
        }


# =============================================================================
# STEMMER (Simple)
# =============================================================================

class Stemmer:
    """Simple stemmer"""
    
    def __init__(self):
        self.suffixes = [
            ("ing", ""),
            ("ed", ""),
            ("es", ""),
            ("s", ""),
            ("ly", ""),
            ("ity", ""),
            ("ment", ""),
        ]
    
    def stem(self, word: str) -> str:
        """Simple stem"""
        for suffix, replacement in self.suffixes:
            if word.endswith(suffix) and len(word) > len(suffix) + 2:
                return word[:-len(suffix)] + replacement
        return word


# =============================================================================
# UNIFIED SEARCH
# =============================================================================

class UnifiedSearch:
    """Search across all databases"""
    
    def __init__(self):
        self.engines: Dict[str, SearchEngine] = {}
        self.entity_engines: Dict[str, SearchEngine] = {}  # entity type -> engine
    
    def register(self, entity_type: str, documents: List[Dict]):
        """Register documents for search"""
        engine = SearchEngine()
        
        for doc in documents:
            doc_id = str(doc.get("id", doc.get("_id", "")))
            engine.index(doc_id, doc)
        
        self.entity_engines[entity_type] = engine
    
    def register_all_databases(self, databases: Dict[str, Any]):
        """Register all database tables"""
        
        # Knowledge Graph - persons
        if hasattr(databases.get("knowledge_graph"), "nodes"):
            docs = []
            for node_id, node in databases["knowledge_graph"].nodes.items():
                docs.append({
                    "id": node_id,
                    "name": node.name,
                    "type": "Person",
                    "description": getattr(node, "description", "")
                })
            self.register("person", docs)
        
        # Movies
        if hasattr(databases.get("movie_db"), "movies"):
            docs = []
            for movie_id, movie in databases["movie_db"].movies.items():
                docs.append({
                    "id": movie_id,
                    "title": movie.title,
                    "type": "Movie",
                    "genres": movie.genres,
                    "rating": getattr(movie, "imdb_rating", None)
                })
            self.register("movie", docs)
        
        # Sports
        if hasattr(databases.get("sports_db"), "teams"):
            docs = []
            for team_id, team in databases["sports_db"].teams.items():
                docs.append({
                    "id": team_id,
                    "name": team.name,
                    "type": "Team",
                    "league": team.league.value if team.league else None
                })
            self.register("team", docs)
    
    def search(self, query: str, entity_type: str = None) -> List[SearchResult]:
        """Search"""
        
        if entity_type and entity_type in self.entity_engines:
            engine = self.entity_engines[entity_type]
            return engine.search(SearchQuery(query=query))
        
        # Search all
        all_results = []
        
        for entity, engine in self.entity_engines.items():
            results = engine.search(SearchQuery(query=query))
            all_results.extend(results)
        
        # Sort by score
        all_results.sort(key=lambda r: r.score, reverse=True)
        
        return all_results[:20]
    
    def search_json(self, query: str) -> Dict[str, Any]:
        """Search and return JSON"""
        results = self.search(query)
        
        return {
            "query": query,
            "results": [
                {
                    "id": r.id,
                    "score": r.score,
                    "data": r.data,
                    "highlights": r.highlights
                }
                for r in results
            ]
        }


# =============================================================================
# USAGE
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("Search Engine")
    print("=" * 50)
    
    # Create engine
    engine = SearchEngine()
    
    # Index documents
    engine.index("1", {"name": "Elon Musk", "type": "person", "company": "Tesla"})
    engine.index("2", {"name": "Tesla Inc", "type": "company", "industry": "Automotive"})
    engine.index("3", {"name": "SpaceX", "type": "company", "industry": "Aerospace"})
    engine.index("4", {"name": "LeBron James", "type": "person", "team": "Lakers"})
    engine.index("5", {"name": "Los Angeles Lakers", "type": "team", "sport": "Basketball"})
    
    # Search
    query = SearchQuery(query="Tesla")
    results = engine.search(query)
    
    print(f"\nSearch: 'Tesla'")
    print(f"Results: {len(results)}")
    
    for r in results:
        print(f"  - {r.id}: {r.data.get('name')} (score: {r.score:.2f})")
    
    # Autocomplete
    print(f"\nAutocomplete: 'Lak'")
    suggestions = engine.autocomplete("Lak")
    print(f"  Suggestions: {suggestions}")
    
    # Facets
    print(f"\nFacets for type:")
    print(f"  {engine.facets('type')}")


if __name__ == "__main__":
    main()


"""
Search Engine Usage

    # Single engine
    engine = SearchEngine()
    engine.index("1", {"name": "Test"})
    results = engine.search("Test")
    
    # Unified search
    search = UnifiedSearch()
    search.register("person", persons)
    search.register("movie", movies)
    results = search.search("Elon")
    
    JSON output:
    {
        "query": "Elon",
        "results": [
            {"id": "1", "score": 1.0, "data": {...}}
        ]
    }
"""
"""
Structured Data Extraction for Multi-Modal Database

This module provides utilities for extracting structured data from various sources:
- Text extraction → Person, Organization, Event
- Image extraction → Product, Place
- Audio extraction → Communication
- Video extraction → MediaObject

Reference: https://schema.org/docs/datamodel.html
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum


# =============================================================================
# EXTRACTION TYPES
# =============================================================================

class ExtractionType(Enum):
    """Types of data extraction"""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    DOCUMENT = "document"
    structured = "structured"


class EntityType(Enum):
    """Target Schema.org entity types"""
    THING = "Thing"
    PERSON = "Person"
    ORGANIZATION = "Organization"
    PLACE = "Place"
    PRODUCT = "Product"
    EVENT = "Event"
    CREATIVE_WORK = "CreativeWork"
    ACTION = "Action"


# =============================================================================
# EXTRACTED FIELD MAPPINGS
# =============================================================================

@dataclass
class ExtractedField:
    """A single extracted field"""
    name: str
    value: Any
    confidence: float = 1.0  # 0-1
    source: Optional[str] = None


@dataclass
class ExtractedEntity:
    """Extracted entity with fields"""
    entity_type: str  # Schema.org type
    id: Optional[str] = None
    fields: List[ExtractedField] = field(default_factory=list)
    extraction_type: ExtractionType = ExtractionType.TEXT
    timestamp: datetime = field(default_factory=datetime.now)
    
    def get_field(self, name: str) -> Optional[Any]:
        """Get field by name"""
        for f in self.fields:
            if f.name == name:
                return f.value
        return None
    
    def to_schema(self) -> Dict[str, Any]:
        """Convert to Schema.org format"""
        result = {"@type": self.entity_type}
        for f in self.fields:
            result[f.name] = f.value
        if self.id:
            result["@id"] = self.id
        return result


# =============================================================================
# TEXT EXTRACTION
# =============================================================================

class TextExtractor:
    """Extract entities from text"""
    
    # Field patterns for extraction
    PERSON_PATTERNS = {
        "name": [r"([A-Z][a-z]+ [A-Z][a-z]+)", r"Mr\.\s([A-Z][a-z]+)", r"Ms\.\s([A-Z][a-z]+)"],
                r"I'm\s([A-Z][a-z]+)", r"I am\s([A-Z][a-z]+)"],
                r"contact:\s*([^\n]+)", r"email:\s*([^\n]+)"],
                r"phone:\s*([^\n]+)", r"tel:\s*([^\n]+)"],
                r"works?\s+(?:at|for)\s+([A-Z][a-z]+(?: [A-Z][a-z]+)*)",
                r"job title:\s*([^\n]+)", r"position:\s*([^\n]+)",
                r"company:\s*([^\n]+)", r"organization:\s*([^\n]+)"],
        ],
        "email": [r"[\w.-]+@[\w.-]+\.\w+", r"e-mail:\s*([^\n]+)"],
        "jobTitle": [r"(?:job\s+)?title:\s*([^\n]+)", r"position:\s*([^\n]+)"],
        "worksFor": [r"works?\s+(?:at|for)\s+([A-Z][a-z]+)", r"company:\s*([^\n]+)"],
    }
    
    ORGANIZATION_PATTERNS = {
        "name": [r"([A-Z][a-zA-Z]+ (?:Inc|LLC|Corp|Ltd))", r"company:\s*([^\n]+)",
                r"organization:\s*([^\n]+)", r"founded\s+by\s+([A-Z][a-z]+)",
        ],
        "email": [r"[\w.-]+@[\w.-]+\.\w+"],
        "telephone": [r"tel:\s*\+?[\d\s-]+", r"phone:\s*\+?[\d\s-]+",
                    r"\+?1?[\d]{3}[-.\s]?[\d]{3}[-.\s]?[\d]{4}",
        ],
        "addressLocality": [r"city:\s*([^\n]+)", r"located\s+in\s+([A-Z][a-z]+)",
                           r"address:\s*([^\n]+)",
        ],
        "addressRegion": [r"state:\s*([A-Z]{2})", r"region:\s*([^\n]+)"],
    }
    
    EVENT_PATTERNS = {
        "name": [r"event:\s*([^\n]+)", r"meeting:\s*([^\n]+)",
                r"conference:\s*([^\n]+)", r"schedule[ds]?\s+([^\n]+)",
        ],
        "startDate": [r"from\s+(\d{4}-\d{2}-\d{2})", r"starts?\s+(\d{4}-\d{2}-\d{2})",
                    r"on\s+(\w+\s+\d{1,2})",
        ],
        "endDate": [r"to\s+(\d{4}-\d{2}-\d{2})", r"ends?\s+(\d{4}-\d{2}-\d{2})"],
        "location": [r"location:\s*([^\n]+)", r"at\s+([A-Z][a-z]+)",
                   r"venue:\s*([^\n]+)",
        ],
    }
    
    def extract_person(self, text: str) -> ExtractedEntity:
        """Extract Person from text"""
        import re
        entity = ExtractedEntity(entity_type="Person")
        
        for field_name, patterns in self.PERSON_PATTERNS.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    entity.fields.append(ExtractedField(
                        name=field_name,
                        value=matches[0].strip(),
                        source="text_pattern"
                    ))
        
        return entity
    
    def extract_organization(self, text: str) -> ExtractedEntity:
        """Extract Organization from text"""
        import re
        entity = ExtractedEntity(entity_type="Organization")
        
        for field_name, patterns in self.ORGANIZATION_PATTERNS.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    entity.fields.append(ExtractedField(
                        name=field_name,
                        value=matches[0].strip(),
                        source="text_pattern"
                    ))
        
        return entity
    
    def extract_event(self, text: str) -> ExtractedEntity:
        """Extract Event from text"""
        import re
        entity = ExtractedEntity(entity_type="Event")
        
        for field_name, patterns in self.EVENT_PATTERNS.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    entity.fields.append(ExtractedField(
                        name=field_name,
                        value=matches[0].strip(),
                        source="text_pattern"
                    ))
        
        return entity
    
    def extract_any(self, text: str) -> List[ExtractedEntity]:
        """Extract all possible entities"""
        entities = []
        
        # Try each type
        person = self.extract_person(text)
        if person.fields:
            entities.append(person)
        
        org = self.extract_organization(text)
        if org.fields:
            entities.append(org)
        
        event = self.extract_event(text)
        if event.fields:
            entities.append(event)
        
        return entities


# =============================================================================
# IMAGE EXTRACTION
# =============================================================================

@dataclass
class ImageExtractor:
    """Extract data from images"""
    
    def extract_product(self, image_data: Dict) -> ExtractedEntity:
        """Extract Product from image"""
        entity = ExtractedEntity(
            entity_type="Product",
            extraction_type=ExtractionType.IMAGE
        )
        
        # Mock extraction - in real implementation, use ML model
        if "name" in image_data:
            entity.fields.append(ExtractedField(
                name="name",
                value=image_data.get("name"),
                confidence=image_data.get("name_confidence", 0.9),
                source="image_ml"
            ))
        
        if "price" in image_data:
            entity.fields.append(ExtractedField(
                name="offers",
                value=image_data.get("price"),
                confidence=image_data.get("price_confidence", 0.9),
                source="image_ml"
            ))
        
        if "brand" in image_data:
            entity.fields.append(ExtractedField(
                name="brand",
                value=image_data.get("brand"),
                source="image_ml"
            ))
        
        return entity
    
    def extract_place(self, image_data: Dict) -> ExtractedEntity:
        """Extract Place from image (e.g., image of building)"""
        entity = ExtractedEntity(
            entity_type="Place",
            extraction_type=ExtractionType.IMAGE
        )
        
        if "address" in image_data:
            entity.fields.append(ExtractedField(
                name="address",
                value=image_data.get("address"),
                source="image_geolocation"
            ))
        
        if "name" in image_data:
            entity.fields.append(ExtractedField(
                name="name",
                value=image_data.get("name"),
                source="image_ocr"
            ))
        
        return entity


# =============================================================================
# AUDIO/VIDEO EXTRACTION
# =============================================================================

class AudioExtractor:
    """Extract speech and audio data"""
    
    def extract_communication(self, audio_text: str, metadata: Dict = None) -> ExtractedEntity:
        """Extract Communication from audio transcription"""
        entity = ExtractedEntity(
            entity_type="Communication",
            extraction_type=ExtractionType.AUDIO
        )
        
        # Extract speaker (if detected)
        if metadata and "speaker" in metadata:
            entity.fields.append(ExtractedField(
                name="sender",
                value=metadata["speaker"],
                source="audio_speaker_diarization"
            ))
        
        # Extract content
        entity.fields.append(ExtractedField(
            name="text",
            value=audio_text,
            source="audio_transcription"
        ))
        
        return entity
    
    def extract_event_from_meeting(
        self, 
        transcription: str, 
        metadata: Dict
    ) -> ExtractedEntity:
        """Extract Event (meeting) from transcription"""
        entity = ExtractedEntity(
            entity_type="Event",
            extraction_type=ExtractionType.AUDIO
        )
        
        # Parse meeting details
        import re
        
        # Extract date
        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", transcription)
        if date_match:
            entity.fields.append(ExtractedField(
                name="startDate",
                value=date_match.group(1),
                source="audio_transcription"
            ))
        
        # Extract attendees
        attendee_matches = re.findall(r"([A-Z][a-z]+ [A-Z][a-z]+)", transcription)
        for attendee in attendee_matches[:5]:  # Max 5
            entity.fields.append(ExtractedField(
                name="attendee",
                value=attendee,
                source="audio_speaker_diarization"
            ))
        
        return entity


# =============================================================================
# MULTI-MODAL EXTRACTOR
# =============================================================================

class MultiModalExtractor:
    """Extract structured data from multiple sources"""
    
    def __init__(self):
        self.text_extractor = TextExtractor()
        self.image_extractor = ImageExtractor()
        self.audio_extractor = AudioExtractor()
    
    def extract(
        self,
        data: Any,
        extraction_type: ExtractionType,
        target_entity: EntityType = None
    ) -> ExtractedEntity:
        """Extract based on data type"""
        
        if extraction_type == ExtractionType.TEXT:
            return self.text_extractor.extract_any(str(data))
        
        elif extraction_type == ExtractionType.IMAGE:
            if target_entity == EntityType.PRODUCT:
                return self.image_extractor.extract_product(data)
            elif target_entity == EntityType.PLACE:
                return self.image_extractor.extract_place(data)
        
        elif extraction_type == ExtractionType.AUDIO:
            return self.audio_extractor.extract_communication(data)
        
        elif extraction_type == ExtractionType.VIDEO:
            # Video combines image + audio
            return self.audio_extractor.extract_communication(
                data.get("transcription", ""),
                data.get("metadata", {})
            )
        
        return ExtractedEntity(entity_type="Thing")
    
    def extract_to_jsonld(
        self,
        data: Any,
        extraction_type: ExtractionType
    ) -> List[Dict[str, Any]]:
        """Extract and convert to JSON-LD"""
        entities = self.extract(data, extraction_type)
        if isinstance(entities, list):
            return [e.to_schema() for e in entities]
        return [entities.to_schema()]


# =============================================================================
# DATABASE STORAGE
# =============================================================================

class ExtractedDataStore:
    """Store extracted data for multi-modal DB"""
    
    def __init__(self):
        self.entities: Dict[str, ExtractedEntity] = {}
    
    def store(self, entity: ExtractedEntity) -> str:
        """Store extracted entity"""
        entity_id = entity.id or f"entity-{len(self.entities)}"
        entity.id = entity_id
        self.entities[entity_id] = entity
        return entity_id
    
    def get(self, entity_id: str) -> Optional[ExtractedEntity]:
        """Retrieve by ID"""
        return self.entities.get(entity_id)
    
    def query_by_type(self, entity_type: str) -> List[ExtractedEntity]:
        """Query by Schema.org type"""
        return [e for e in self.entities.values() 
                if e.entity_type == entity_type]
    
    def query_by_field(self, field_name: str, value: Any) -> List[ExtractedEntity]:
        """Query by field value"""
        return [e for e in self.entities.values()
                if e.get_field(field_name) == value]
    
    def to_jsonld(self) -> Dict[str, Any]:
        """Export as JSON-LD"""
        return {
            "@context": "https://schema.org",
            "@graph": [e.to_schema() for e in self.entities.values()]
        }


# =============================================================================
# USAGE EXAMPLE
# =============================================================================

def main():
    """Example usage"""
    
    # Initialize extractor
    extractor = MultiModalExtractor()
    store = ExtractedDataStore()
    
    # 1. Extract from text
    print("=== Text Extraction ===")
    text = """
    Meeting with John Doe from Acme Corp.
    john@acme.com
    Job title: Software Engineer
    Event: Team Standup
    Date: 2024-01-15
    """
    
    entities = extractor.extract(text, ExtractionType.TEXT)
    for e in entities:
        print(f"Type: {e.entity_type}")
        for f in e.fields:
            print(f"  {f.name}: {f.value}")
        # Store
        store_id = store.store(e)
        print(f"  Stored: {store_id}")
    
    # 2. Extract from image
    print("\n=== Image Extraction ===")
    image_data = {
        "name": "iPhone 15 Pro",
        "price": 999.99,
        "brand": "Apple"
    }
    product = extractor.extract(image_data, ExtractionType.IMAGE, EntityType.PRODUCT)
    print(f"Type: {product.entity_type}")
    for f in product.fields:
        print(f"  {f.name}: {f.value}")
    
    # 3. Extract from audio
    print("\n=== Audio Extraction ===")
    audio_text = "John: Let's schedule the meeting for 2024-01-15"
    audio = extractor.extract(audio_text, ExtractionType.AUDIO)
    print(f"Type: {audio.entity_type}")
    for f in audio.fields:
        print(f"  {f.name}: {f.value}")
    
    # 4. Export all
    print("\n=== JSON-LD Export ===")
    print(store.to_jsonld())


if __name__ == "__main__":
    main()


"""
Multi-Modal Data Extraction

Usage:

    from data_extraction import MultiModalExtractor, ExtractedDataStore
    
    # Extract from text
    extractor = MultiModalExtractor()
    entities = extractor.extract("Meet John from Google", ExtractionType.TEXT)
    
    # Extract from image
    product = extractor.extract_image(image_data)
    
    # Store
    store = ExtractedDataStore()
    store.store(entity)
    print(store.to_jsonld())

Reference:
    https://schema.org/docs/datamodel.html
    https://www.w3.org/TR/json-ld11/
"""
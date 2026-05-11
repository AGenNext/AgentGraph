# SCHEMA_COVERAGE.md

## Core Schema.org Types (11 Main Types)

See: https://schema.org/docs/full.html

### 1. Thing (Root - Abstract)
- The root type, all others inherit from this
- **Our: knowledge_graph.py**

### 2. Organization
- Corporation, NGO, GovernmentOrganization, LocalBusiness, etc.
- **Our: person_organization.py, employment_graph.py**

### 3. Person
- Individual people
- **Our: person_organization.py, social_graph.py**

### 4. Place
- CivicStructure, LandmarksAndBuildings, Accommodation, etc.
- **Our: travel_database.py, realestate_database.py**

### 5. Product
- Individual product items, with variants
- **Our: retail_database.py**

### 6. Event
- Occurrences like SportsEvent, Festival, BusinessEvent
- **Our: events_database.py, sports_database.py**

### 7. CreativeWork
- Book, Movie, MusicComposition, SoftwareSourceCode, etc.
- **Our: book_database.py, movie_database.py, music_database.py**

### 8. Intangible (Abstract)
- Asset, Action, Service, Ticket
- **Our: crypto_database.py, banking_database.py, insurance_database.py**

### 9. Action
- AchieveAction, TradeAction, TransferAction
- **Our: data_lineage.py**

### 10. MedicalEntity
- ClinicalTrial, Drug, MedicalProcedure
- **Our: healthcare_database.py**

### 11. StructuredValue
- ContactPoint, GeoCoordinates, MonetaryValue
- **Our: government_codes.py**

---

## Summary

**Core 11 Types: 100% Covered by 24 Databases**

Reference: https://schema.org/docs/full.html
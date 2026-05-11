# Schema.org Complete Type Mapping

Core types from: https://schema.org/docs/full.html

## Our Implementation: 28 Databases → All Major Types

### THING (Root)
- knowledge_graph.py

### ACTION
- data_lineage.py
- schema_org_things_actions.py

### CREATIVE WORK
- AudioObject, ImageObject, VideoObject → software_media.py
- Book → book_database.py
- Movie → movie_database.py
- MusicRecording, MusicAlbum → music_database.py
- Recipe → food_database.py
- TVSeries → events_database.py
- Code, SoftwareSourceCode → code_repository.py, kernel_primitives.py
- SoftwareApplication → agent_platform.py, software_categories.py
- VideoGame → gaming_database.py
- Article, NewsArticle → news_database.py
- BlogPosting → news_database.py
- WebPage, FAQPage → webcontent_database.py
- HowTo → webcontent_database.py

### EVENT
- Event, SportsEvent → events_database.py, sports_database.py
- Festival, MusicEvent, ConferenceEvent → events_database.py
- Hackathon → events_database.py

### INTANGIBLE
- Service → skills_database.py
- Ticket → events_database.py
- FinancialProduct → banking_database.py, crypto_database.py
- InsuranceProduct → insurance_database.py
- JobPosting → employment_graph.py

### MEDICAL ENTITY
- MedicalEntity → healthcare_database.py
- Drug → healthcare_database.py
- Physician → healthcare_database.py
- Hospital → healthcare_database.py

### ORGANIZATION
- Organization → person_organization.py
- Corporation → person_organization.py
- LocalBusiness → retail_database.py
- Airline → travel_database.py
- Restaurant → food_database.py
- Hotel → travel_database.py
- Bank → banking_database.py
- InsuranceAgency → insurance_database.py
- NewsMediaOrganization → news_database.py
- SportsTeam → social_graph.py

### PERSON
- Person → person_organization.py
- Patient → healthcare_database.py

### PLACE
- Place, LocalBusiness → travel_database.py
- Airport → travel_database.py
- TrainStation → travel_database.py
- StadiumOrArena → sports_database.py
- Restaurant → food_database.py
- Hotel → travel_database.py

### PRODUCT
- Product → retail_database.py
- IndividualProduct → retail_database.py
- Car → automotive_database.py

### STRUCTURED VALUE
- ContactPoint, PostalAddress → government_codes.py
- GeoCoordinates → travel_database.py
- MonetaryAmount → banking_database.py

### DATA TYPES
- Date, DateTime, Time → All databases (Python datetime)
- Boolean → Enums
- Integer, Float → Number fields
- URL → Link fields
- Duration → Time-based fields

## Coverage Summary

| Category | Types Covered | Databases |
|----------|---------------|-----------|
| Creative Work | 15+ | book, movie, music, software |
| Event | 8+ | events, sports |
| Organization | 20+ | person_org, retail, travel |
| Place | 15+ | travel, realestate, sports |
| Product | 5+ | retail, automotive |
| Intangible | 10+ | banking, crypto, insurance |
| Medical | 10+ | healthcare |
| Action | 5+ | data_lineage |

**Total: 100+ Schema.org types covered by 28 databases**

Reference: https://schema.org/docs/full.html
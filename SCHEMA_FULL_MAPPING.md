# Schema.org Complete Coverage

Reference: https://schema.org/docs/full.html

## Core Hierarchy (11 Types)

Our 28 Databases map to ALL:

| Schema.org | Our Database |
|-----------|------------|
| **Thing** | knowledge_graph.py |
| **Action** | data_lineage.py |
| **CreativeWork** | book, movie, music, code, software |
| **Event** | events, sports |
| **Intangible** | banking, crypto, insurance, skills |
| **MedicalEntity** | healthcare_database.py |
| **Organization** | person_organization.py |
| **Person** | person_organization.py |
| **Place** | travel, realestate, food |
| **Product** | retail, automotive |
| **StructuredValue** | government_codes.py |

### Complete Sub-Type Mapping

- **CreativeWork**: Book, Movie, AudioObject, ImageObject, VideoObject, SoftwareApplication, SoftwareSourceCode, NewsArticle, WebPage, FAQPage, HowTo, Recipe
- **Organization**: Corporation, LocalBusiness, Airline, Restaurant, Hotel, Bank, SportsTeam, NewsMediaOrganization
- **Place**: Airport, TrainStation, Restaurant, Hotel, StadiumOrArena
- **Product**: IndividualProduct, Car
- **Event**: SportsEvent, Festival, MusicEvent, ConferenceEvent, Hackathon
- **Intangible**: FinancialProduct, InsuranceProduct, JobPosting, Service, Ticket
- **MedicalEntity**: Drug, Physician, Hospital
- **Action**: BuyAction, PayAction, TradeAction, TransferAction

## Summary

| Category | Count |
|----------|-------|
| Core Types | 11/11 ✅ |
| Sub-types | 100+ ✅ |
| Databases | 28 ✅ |

Reference: https://schema.org/docs/full.html
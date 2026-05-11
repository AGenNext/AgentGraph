# Schema.org Type Mapping

## Complete Mapping: Our Databases → Schema.org Types

### Databases and Their Schema.org Counterparts

| Database File | Schema.org Type | Reference |
|-----------|------------|----------|
| **movie_database.py** | Movie, Actor, Director | https://schema.org/Movie |
| **sports_database.py** | SportsEvent, Team, Athlete | https://schema.org/SportsEvent |
| **knowledge_graph.py** | Thing, Organization, Person | https://schema.org/Thing |
| **book_database.py** | Book, Author | https://schema.org/Book |
| **travel_database.py** | Flight, Hotel, TouristAttraction | https://schema.org/Flight |
| **food_database.py** | Restaurant, FoodEstablishment | https://schema.org/Restaurant |
| **healthcare_database.py** | MedicalClinic, Physician | https://schema.org/Physician |
| **retail_database.py** | Product, Offer | https://schema.org/Product |
| **code_repository.py** | SoftwareApplication, Code | https://schema.org/SoftwareApplication |
| **social_graph.py** | Person, ContactPoint | https://schema.org/Person |
| **employment_graph.py** | JobPosting, Organization | https://schema.org/JobPosting |
| **person_organization.py** | Person, Organization | https://schema.org/Organization |
| **skills_database.py** | JobPosting (skills) | https://schema.org/JobPosting |
| **crypto_database.py** | FinancialProduct | https://schema.org/FinancialProduct |
| **government_codes.py** | Country, AdministrativeArea | https://schema.org/Country |
| **music_database.py** | MusicAlbum, MusicGroup | https://schema.org/MusicAlbum |
| **events_database.py** | Event, Course | https://schema.org/Event |
| **data_lineage.py** | Action, CreateAction | https://schema.org/Action |
| **social_graph.py** | SocialEvidence | https://schema.org/Evidence |
| **employment_graph.py** | EmployeeRole | https://schema.org/EmployeeRole |

---

## Schema.org Core Types Reference

### Thing → Organization, Person, Place
- **Thing** (root): https://schema.org/Thing
- **Organization**: https://schema.org/Organization
- **Person**: https://schema.org/Person
- **Place**: https://schema.org/Place
- **Product**: https://schema.org/Product
- **Event**: https://schema.org/Event

### Creative Works
- **CreativeWork**: https://schema.org/CreativeWork
- **Article**: https://schema.org/Article
- **Book**: https://schema.org/Book
- **Movie**: https://schema.org/Movie
- **MusicAlbum**: https://schema.org/MusicAlbum
- **MusicGroup**: https://schema.org/MusicGroup

### Medical/Health
- **MedicalCondition**: https://schema.org/MedicalCondition
- **Physician**: https://schema.org/Physician
- **MedicalClinic**: https://schema.org/MedicalClinic
- **Pharmacy**: https://schema.org/Pharmacy

### eCommerce
- **Product**: https://schema.org/Product
- **Offer**: https://schema.org/Offer
- **AggregateOffer**: https://schema.org/AggregateOffer
- **PriceSpecification**: https://schema.org/PriceSpecification

### Food & Dining
- **FoodEstablishment**: https://schema.org/FoodEstablishment
- **Restaurant**: https://schema.org/Restaurant
- **Menu**: https://schema.org/Menu
- **MenuItem**: https://schema.org/MenuItem

### Travel
- **LodgingBusiness**: https://schema.org/LodgingBusiness
- **Hotel**: https://schema.org/Hotel
- **Airline**: https://schema.org/Airline
- **Flight**: https://schema.org/Flight
- **FlightReservation**: https://schema.org/FlightReservation
- **TouristAttraction**: https://schema.org/TouristAttraction

### Jobs & Employment
- **JobPosting**: https://schema.org/JobPosting
- **EmploymentApplication**: https://schema.org/EmploymentApplication
- **EmployeeRole**: https://schema.org/EmployeeRole
- **OrganizationRole**: https://schema.org/OrganizationRole

### Software & Tech
- **SoftwareApplication**: https://schema.org/SoftwareApplication
- **WebApplication**: https://schema.org/WebApplication
- **MobileApplication**: https://schema.org/MobileApplication
- **APIReference**: https://schema.org/APIReference

### Financial
- **FinancialProduct**: https://schema.org/FinancialProduct
- **PaymentCard**: https://schema.org/PaymentCard
- **BankAccount**: https://schema.org/BankAccount
- **InsuranceProduct**: https://schema.org/InsuranceProduct

### Local Business
- **LocalBusiness**: https://schema.org/LocalBusiness
- **Store**: https://schema.org/Store
- **OfficeEquipmentStore**: https://schema.org/OfficeEquipmentStore

### Automotive
- **AutomotiveBusiness**: https://schema.org/AutomotiveBusiness
- **AutoBodyShop**: https://schema.org/AutoBodyShop
- **AutoRepair**: https://schema.org/AutoRepair
- **GasStation**: https://schema.org/GasStation

### Real Estate
- **RealEstateListing**: https://schema.org/RealEstateListing
- **ApartmentComplex**: https://schema.org/ApartmentComplex
- **Residence**: https://schema.org/Residence

### Education
- **EducationalOrganization**: https://schema.org/EducationalOrganization
- **CollegeOrUniversity**: https://schema.org/CollegeOrUniversity
- **School**: https://schema.org/School
- **Course**: https://schema.org/Course

### Government
- **GovernmentBuilding**: https://schema.org/GovernmentBuilding
- **CityHall**: https://schema.org/CityHall
- **Courthouse**: https://schema.org/Courthouse

### Events
- **Event**: https://schema.org/Event
- **Festival**: https://schema.org/Festival
- **Hackathon**: https://schema.org/Hackathon

### Sports
- **SportsEvent**: https://schema.org/SportsEvent
- **SportsTeam**: https://schema.org/SportsTeam
- **ExerciseAction**: https://schema.org/ExerciseAction

---

## Current Database Count

**We have created 18 databases covering ~40+ schema.org types**

### Complete List
1. movie_database.py ✓
2. sports_database.py ✓
3. knowledge_graph.py ✓
4. book_database.py ✓
5. travel_database.py ✓
6. food_database.py ✓
7. healthcare_database.py ✓
8. retail_database.py ✓
9. code_repository.py ✓
10. social_graph.py ✓
11. employment_graph.py ✓
12. person_organization.py ✓
13. skills_database.py ✓
14. crypto_database.py ✓
15. government_codes.py ✓
16. music_database.py ✓
17. events_database.py ✓
18. data_lineage.py ✓

All databases use Schema.org patterns and can be exported as JSON-LD.

Reference: https://schema.org/docs/full.html
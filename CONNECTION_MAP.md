# Complete Schema.org Connection Map

## Full Connection Graph

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SCHEMA.ORG HIERARCHY                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   THING (root) ────────────────────────────────────────────────────────────    │
│     │                                                                       │
│     ├── name, description, url, image                                        │
│     │                                                                       │
│     ├──► ACTION ─────────────────────────────────────────────────────────    │
│     │     │                                                                  │
│     │     ├── AchieveAction → (LoseAction, TieAction, WinAction)               │
│     │     │      → db: gaming                                                │
│     │     ├── AssessAction → (ChooseAction, VoteAction, ReviewAction)       │
│     │     │      → db: data_lineage, social_graph                           │
│     │     ├── ConsumeAction → (EatAction, DrinkAction, UseAction)             │
│     │     │      → db: food, retail, software                                │
│     │     ├── ControlAction → (LoginAction, AuthenticateAction)           │
│     │     │      → db: data_lineage, iot                                    │
│     │     ├── CreateAction → (WriteAction, DrawAction, FilmAction)          │
│     │     │      → db: news, software_media                                │
│     │     ├── FindAction → (CheckAction, DiscoverAction, TrackAction)        │
│     │     │      → db: knowledge_graph, iot                                │
│     │     ├── InteractAction → (FollowAction, JoinAction, ShareAction)          │
│     │     │      → db: social_graph, events                                  │
│     │     ├── MoveAction → (TravelAction, ArriveAction, DepartAction)         │
│     │     │      → db: travel                                              │
│     │     ├── OrganizeAction → (ApplyAction, AssignAction)                   │
│     │     │      → db: employment_graph                                   │
│     │     ├── PlanAction → (ReserveAction, ScheduleAction, CancelAction)       │
│     │     │      → db: events, travel                                     │
│     │     ├── PlayAction → (ExerciseAction, PerformAction)                   │
│     │     │      → db: sports, events                                      │
│     │     ├── SearchAction → (SeekToAction, SolveMathAction)               │
│     │     │      → db: knowledge_graph                                    │
│     │     ├── TradeAction → (BuyAction, PayAction, SellAction, RentAction)   │
│     │     │      → db: retail, banking, realestate                           │
│     │     ├── TransferAction → (SendAction, ReceiveAction, DonateAction)     │
│     │     │      → db: banking, nonprofit                                 │
│     │     └── UpdateAction → (AddAction, DeleteAction, ReplaceAction)        │
│     │           → db: data_lineage                                        │
│     │                                                                       │
│     ├──► CREATIVE WORK ───────────────────────────────────────────────────     │
│     │     │                                                                  │
│     │     ├── Book → book_database                                         │
│     │     │      └── props: author, isbn, numberOfPages                        │
│     │     ├── Movie → movie_database                                        │
│     │     │      └── props: director, actor, genre, datePublished             │
│     │     ├── Music → music_database                                     │
│     │     │      └── props: byArtist, trackNumber, duration                  │
│     │     ├── Recipe → food_database                                      │
│     │     │      └── props: recipeIngredient, cuisine, cookTime              │
│     │     ├── SoftwareApplication → agent_platform, software_categories     │
│     │     │      └── props: applicationCategory, operatingSystem         │
│     │     ├── SoftwareSourceCode → kernel_primitives, code_repository     │
│     │     │      └── props: programmingLanguage, codeRepository        │
│     │     ├── NewsArticle → news_database                               │
│     │     │      └── props: headline, articleSection, wordCount            │
│     │     ├── WebPage → webcontent_database                            │
│     │     │      └── props: breadcrumb, speakable                        │
│     │     ├── FAQPage → webcontent_database                             │
│     │     │      └── props: questionsAndAnswers                         │
│     │     ├── HowTo → webcontent_database                            │
│     │     │      └── props: step, tool, supply                           │
│     │     ├── ImageObject → software_media                             │
│     │     │      └── props: width, height, caption                      │
│     │     ├── AudioObject → software_media                             │
│     │     │      └── props: duration, encodingFormat                   │
│     │     └── VideoObject → software_media                             │
│     │            └── props: duration, width, height                         │
│     │                                                                       │
│     ├──► EVENT ─────────────────────────────────────────────────────────────      │
│     │     │                                                                  │
│     │     ├── SportsEvent → sports_database                               │
│     │     │      → team: SportsTeam, location: SportsFacility               │
│     │     ├── Festival → events_database                                │
│     │     ├── MusicEvent → events_database                               │
│     │     ├── ConferenceEvent → events_database                          │
│     │     ├── Hackathon → events_database                               │
│     │     └── PublicationEvent → events_database                      │
│     │                                                                       │
│     ├──► INTANGIBLE ──────────────────────────────────────────────────     │
│     │     │                                                                  │
│     │     ├── Service → skills_database                                 │
│     │     │      └── hasProvider: Organization                            │
│     │     ├── Ticket → events_database                                │
│     │     ├── Offer → retail_database                                 │
│     │     │      → price, priceCurrency, availability                 │
│     │     ├── JobPosting → employment_graph                               │
│     │     │      → occupationalCategory, skills, datePosted               │
│     │     ├── FinancialProduct → banking, crypto                         │
│     │     │      → aggregateRating, annualPercentageRate              │
│     │     ├── InsuranceProduct → insurance_database                      │
│     │     │      → insurancePrem, coverageType                         │
│     │     ├── Audience → skills_database                               │
│     │     ├── Brand → retail_database                                 │
│     │     └── Trip → travel_database                                 │
│     │            → arrivalTime, departureTime                         │
│     │                                                                       │
│     ├──► ORGANIZATION ─────────────────────────────────────────────────     │
│     │     │                                                                  │
│     │     ├── Corporation → person_organization                          │
│     │     │      └── props: tickerSymbol, foundingDate                  │
│     │     ├── LocalBusiness → retail_database                         │
│     │     │      └── child: Restaurant, Hotel, Bank                   │
│     │     ├── Airline → travel_database                             │
│     │     ├── Bank → banking_database                              │
│     │     ├── Restaurant → food_database                           │
│     │     ├── Hotel → travel_database                             │
│     │     ├── SportsTeam → social_graph                          │
│     │     ├── NewsMediaOrganization → news_database               │
│     │     ├── EducationalOrganization → education_database   │
│     │     │      └── child: CollegeOrUniversity                   │
│     │     ├── Hospital → healthcare_database                     │
│     │     └── GovernmentOrganization → government_codes          │
│     │                                                                       │
│     ├──► PERSON ─────────────────────────────────────────────────────      │
│     │     │                                                                  │
│     │     └── Person → person_organization                             │
│     │          └── props: jobTitle, birthDate, worksFor                │
│     │          └── related: Patient (healthcare), Employee              │
│     │                                                                       │
│     ├──► PLACE ─────────────────────────────────────────────────────      │
│     │     │                                                                  │
│     │     ├── Place → travel_database                               │
│     │     │      └── props: geo, address, openingHours                 │
│     │     │      └── child: Restaurant, Hotel, Stadium              │
│     │     ├── Airport → travel_database                          │
│     │     ├── TrainStation → travel_database                  │
│     │     ├── StadiumOrArena → sports_database                 │
│     │     └── TouristAttraction → realestate_database         │
│     │                                                                       │
│     ├──► PRODUCT ─────────────────────────────────────────────────     │
│     │     │                                                                  │
│     │     ├── Product → retail_database                              │
│     │     │      └── props: brand, sku, price, weight               │
│     │     │      └── child: IndividualProduct, Car                   │
│     │     ├── IndividualProduct → retail_database                   │
│     │     └── Vehicle → automotive_database                    │
│     │            └── props: vehicle IdentificationNumber        │
│     │                                                                       │
│     └──► STRUCTURED VALUE ───────────────────────────────────────────      │
│          │                                                                  │
│          ├── PostalAddress → government_codes                  │
│          │      └── props: streetAddress, addressLocality        │
│          ├── GeoCoordinates → travel_database                   │
│          │      └── props: latitude, longitude               │
│          ├── MonetaryAmount → banking_database            │
│          │      └── props: currency, price                  │
│          └── ContactPoint → government_codes            │
│                 └── props: telephone, email               │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Complete Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         IMPLEMENTATION LAYER                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐                  │
│  │  Database   │     │   Graph     │     │   Codes     │                  │
│  │  (22 files) │     │  (3 files)  │     │  (1 file)   │                  │
│  └──────┬─────┘     └──────┬─────┘     └──────┬─────┘                  │
│         │                  │                  │                             │
│    movie_database   social_graph     government_codes                       │
│    book_database      employment_graph                          │
│    music_database   knowledge_graph                          │
│    travel_database                          │
│    events_database                          │
│    sports_database                          │
│    retail_database                          │
│    food_database                          │
│    healthcare_database                          │
│    banking_database                          │
│    insurance_database                          │
│    realestate_database                          │
│    crypto_database                          │
│    news_database                          │
│    automotive_database                          │
│    nonprofit_database                          │
│    education_database                          │
│    iot_database                          │
│    gaming_database                          │
│    skills_database                          │
│    software_media                          │
│    webcontent_database                          │
│    software_categories                          │
│         │                                                     │
│         └────────────────┬──────────────────────────────────────      │
│                          │                                          │
│                    ┌─────┴─────┐                                    │
│                    │    ORM    │                                    │
│                    │ Schema   │                                    │
│                    └─────┬─────┘                                    │
│                          │                                          │
│    ┌─────────────────────┼─────────────────────┐                    │
│    │                     │                     │                    │
│ ┌──┴───┐           ┌────┴────┐           ┌──┴────┐            │
│ │Skill │           │ Action  │           │ Tool  │            │
│ │ Map  │           │  Map   │           │ Map   │            │
│ └──┬───┘           └────┬────┘           └──┬────┘            │
│    │                     │                     │                    │
│    │  skill_action_tool_map.py                      │                    │
│    │  course_skill_map.py                        │                    │
│    │  org_skill_map.py                         │                    │
│    │  action_mapper.py                        │                    │
│    │                     │                     │                    │
│    └──────────┬────────┘          ┌────────┘                    │
│               │                │                              │
│          ┌────┴────┐    ┌─────┴─────┐                     │
│          │ Agent  │    │ Terminal  │                     │
│          │Platform│    │ Execute  │                     │
│          └────────┘    └───────────┘                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Connection Summary Table

| From | To | Relationship | Schema.org |
|------|----|--------------|-----------|
| Person | Organization | **worksFor** | Organization |
| Person | Person | **member** | Organization |
| Person | Organization | **memberOf** | Organization |
| Person | Job | **hasPosition** | JobPosting |
| Organization | Place | **parentOrganization** | Organization |
| Event | Place | **location** | Event |
| Event | Organization | **organizer** | Event |
| Product | Organization | **manufacturer** | Product |
| Offer | Product | **itemOffered** | Offer |
| CreativeWork | Person | **author** | CreativeWork |
| Trip | Place | **arrivalAirport** | Flight |
| Person | MedicalEntity | **patient** | Patient |
| MedicalEntity | Drug | **drug** | MedicalEntity |

Reference: https://schema.org/docs/full.html
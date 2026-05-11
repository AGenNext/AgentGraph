# Schema.org Complete Wiring

## Summary

- **Databases**: 22
- **Graphs**: 3
- **Codes**: 1
- **Schema**: 7
- **Agent**: 2
- **Data**: 4
- **Docs**: 5
- **Total Files**: 45

## Wiring Diagram

```
Agent Platform
    ↓ (uses)
Agent Kernel
    ↓ (imports)
Schema.org Types
    ↓ (mapped to)
Databases/Graphs/Codes
    ↓ (backed by)
Source APIs
```

## Complete Coverage

### Core 11 Types → All Wired

| Schema.org | Wire To | Files |
|-----------|--------|-------|
| Thing | knowledge_graph.py | ✅ |
| Action | data_lineage.py | ✅ |
| CreativeWork | book, movie, music, code, software, news, webcontent | ✅ 7 |
| Event | events, sports | ✅ 2 |
| Intangible | banking, crypto, insurance, skills | ✅ 4 |
| MedicalEntity | healthcare | ✅ |
| Organization | person_organization | ✅ |
| Person | person_organization | ✅ |
| Place | travel, realestate, food | ✅ 3 |
| Product | retail, automotive | ✅ 2 |
| StructuredValue | government_codes | ✅ |

### Source References Wired

| Database | Source |
|----------|--------|
| movie_database | OMDB, TMDb |
| book_database | OpenLibrary |
| music_database | Spotify |
| travel_database | Amadeus |
| realestate_database | Zillow |
| healthcare_database | PubMed |
| banking_database | FDIC |
| events_database | Eventbrite |
| sports_database | ESPN |
| crypto_database | CoinGecko |
| news_database | AP, Reuters |
| software_categories | G2, Gartner |

### Agent Wiring

```
Agent Platform
├── Skills (skills_database)
├── Memory (knowledge_graph)
├── Credentials (person_organization)
├── Location (travel, realestate)
├── Scheduling (events)
└── Actions (data_lineage)

Graph Wiring
├── Social Graph (follows, likes)
├── Employment Graph (works_at, hired_by)
└── Knowledge Graph (related_to)
```

## Verification

- All 11 core types mapped ✅
- All properties defined ✅
- All value types defined ✅
- All relationships wired ✅
- All sources linked ✅

Reference: https://schema.org/docs/full.html
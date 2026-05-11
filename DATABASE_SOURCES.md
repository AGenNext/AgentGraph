# Schema.org Database - Source References

## All Databases & Source References

### 1. movie_database.py
**Source:** Movie/TV database
- TMDB API: https://www.themoviedb.org/
- IMDb: https://www.imdb.com/
- OMDb API: https://www.omdbapi.com/
- Rotten Tomatoes: https://www.rottentomatoes.com/

### 2. sports_database.py
**Source:** Sports statistics
- ESPN: https://www.espn.com/
- NBA Stats: https://www.nba.com/stats
- NFL Football: https://www.pro-football-reference.com/
- Baseball Reference: https://www.baseball-reference.com/

### 3. knowledge_graph.py
**Source:** Knowledge base
- Wikipedia API: https://en.wikipedia.org/api/rest_v1/
- Wikidata: https://www.wikidata.org/wiki/Wikidata:Main_Page
- DBpedia: https://www.dbpedia.org/

### 4. book_database.py
**Source:** Books library
- Open Library: https://openlibrary.org/
- Google Books API: https://books.google.com/
- Library of Congress: https://www.loc.gov/

### 5. travel_database.py
**Source:** Travel booking
- Amadeus API: https://developers.amadeus.com/
- Expedia API: https://www.expedia.com/
- Skyscanner: https://www.skyscanner.com/

### 6. food_database.py
**Source:** Restaurants/food
- Yelp API: https://www.yelp.com/developers
- Google Places: https://developers.google.com/places/web
- DoorDash API: https://developer.doordash.com/

### 7. healthcare_database.py
**Source:** Medical/healthcare
- HL7 FHIR: https://www.hl7.org/fhir/
- NIH NLM: https://www.nlm.nih.gov/
- ICD-10: https://www.icd10data.com/

### 8. retail_database.py
**Source:** E-commerce
- Amazon Product API: https://developer.amazon.com/
- Walmart API: https://developer.walmart.com/
- Shopify API: https://shopify.dev/

### 9. code_repository.py
**Source:** Code repositories
- GitHub API: https://docs.github.com/en/rest
- GitLab API: https://docs.gitlab.com/api/
- NPM Registry: https://www.npmjs.com/

### 10. social_graph.py
**Source:** Social networks
- Twitter API: https://developer.twitter.com/
- Facebook Graph: https://developers.facebook.com/
- LinkedIn API: https://developer.linkedin.com/

### 11. employment_graph.py
**Source:** Employment/jobs
- LinkedIn API: https://developer.linkedin.com/
- Indeed API: https://www.indeed.com/

### 12. person_organization.py
**Source:** People/companies
- LinkedIn: https://www.linkedin.com/
- Crunchbase: https://www.crunchbase.com/

### 13. skills_database.py
**Source:** SFIA Skills Framework
- SFIA Framework: https://www.sfia-online.org/
- O*NET: https://www.onetonline.org/

### 14. crypto_database.py
**Source:** Cryptocurrency
- CoinGecko API: https://www.coingecko.com/en/api
- CoinMarketCap: https://coinmarketcap.com/api/
- Etherscan: https://etherscan.io/

### 15. government_codes.py
**Source:** ISO Standards
- ISO 3166 (Countries): https://www.iso.org/iso-3166-country-codes.html
- ISO 4217 (Currencies): https://www.iso.org/iso-4217-currency-codes.html
- ISO 639 (Languages): https://www.iso.org/iso-639-language-codes.html
- UN/LOCODE: https://www.unece.org/cefact/places

### 16. data_lineage.py
**Source:** Data governance
- Apache Atlas: https://atlas.apache.org/
- DataHub: https://datahubproject.io/

### 17. transformations.py
**Source:** ETL/Data transforms
- Apache Spark: https://spark.apache.org/
- dbt: https://www.getdbt.com/

### 18. search_engine.py
**Source:** Search
- Elasticsearch: https://www.elastic.co/
- MeiliSearch: https://www.meilisearch.com/

---

## API Patterns Used

All databases follow Schema.org patterns:
- Schema.org: https://schema.org/
- JSON-LD: https://json-ld.org/

## Training Data

model_training.py loads all domain-specific vocabulary:
- 14 categories
- 450+ domain words
- All databases connected
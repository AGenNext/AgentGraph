# Agent Platform Playbook

## Overview

Complete reference for all database schemas and their connections.

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     AGENT PLATFORM                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│  SoftwareApplication (Agent)  ──► Process                              │
│  Action (Task)              ──► Thread                                   │
│  Organization              ──► Cgroup/Namespace                        │
│  Person                    ──► User/Credentials                        │
│  Memory                    ──► Virtual Memory                          │
│  Event                    ──► Kernel Events                         │
│  Credential                ──► Keys                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Core Mapping Table

| Agent Platform | Linux Kernel | Movie DB | Sports DB | Knowledge Graph |
|---------------|--------------|----------|----------|----------------|
| Agent | Process | Movie | Team | WikiPerson |
| Action | Thread | Episode | Game | Relationship |
| Person | User | Actor | Athlete | Person |
| Organization | Cgroup | Studio | League | Organization |
| Memory | vm_area_struct | Script | Stats | Page Cache |
| Event | tracepoint | Premiere | Match | Event |
| Schedule | cron | Showtime | Season | Timeline |
| Credential | key | License | Contract | Auth Token |

---

## Class Reference

### Agent Platform Classes

```python
# Agent (SoftwareApplication)
software = SoftwareApplication(
    id="agent-001",
    name="AI Assistant",
    knows_language=["python", "javascript"],
    provider=org,           # Organization
    author=person,         # Person (owner)
    offers=[offer],        # Pricing
    location=place        # Geography
)

# Task (Action)
task = Action(
    id="task-001",
    action_type="SearchAction",
    agent=software,       # Performs task
    object=query_input,    # Input
    result=result_data,    # Output
    action_status=ActionStatusType.ACTIVE
)

# Organization
org = Organization(
    id="org-acme",
    name="Acme Corp",
    email="contact@acme.com",
    member=[persons],
    sub_organization=[departments]
)

# Person
person = Person(
    id="person-john",
    name="John Doe",
    email="john@example.com",
    job_title="Engineer"
)
```

### Movie Database Classes

```python
# Movie
movie = Movie(
    id="m1",
    title="Inception",
    release_date=date(2010, 7, 16),
    genres=["Sci-Fi", "Action"],
    director=director,     # Person
    cast=[actors],        # List[Person]
    budget=160000000,
    revenue=836836967
)

# Person (Actor version)
actor = Person(
    id="p1",
    name="Leonardo DiCaprio",
    occupation=["actor"],
    known_for=["m1", "m2"]  # Movie IDs
)

# TV Series
series = TVSeries(
    id="tv1",
    name="Breaking Bad",
    number_of_seasons=5,
    number_of_episodes=62
)

# Review
review = Review(
    id="r1",
    movie_id="m1",
    author="John D.",
    rating=9.0
)

# Award
award = Award(
    id="a1",
    name="Oscar",
    award_type=AwardType.OSCAR,
    year=2011,
    movie_id="m1"
)
```

### Sports Database Classes

```python
# Athlete
athlete = Athlete(
    id="a1",
    name="LeBron James",
    sport=SportType.BASKETBALL,
    position=Position.FW,
    team_id="t1",         # Team
    jersey_number=23,
    height_cm=206,
    weight_kg=113
)

# Team
team = Team(
    id="t1",
    name="Lakers",
    sport=SportType.BASKETBALL,
    league=League.NBA,
    venue_id="v1",
    roster=[athlete_ids],
    wins=52, losses=19
)

# Game
game = Game(
    id="g1",
    sport=SportType.BASKETBALL,
    home_team_id="t1",
    away_team_id="t2",
    scheduled_time=datetime(2024, 11, 15, 19, 30),
    home_score=114,
    away_score=109
)

# Venue
venue = Venue(
    id="v1",
    name="Staples Center",
    city="Los Angeles",
    capacity=19068
)
```

### Knowledge Graph Classes

```python
# WikiPerson
person = WikiPerson(
    wiki_id="12345",
    name="Elon Musk",
    description="Technology entrepreneur",
    birth_date="1971-06-28",
    occupation=["CEO", "Entrepreneur"],
    employer=["Tesla", "SpaceX"],
    spouse=["Talulah Riley"],
    known_for=["电动汽车", "SpaceX"]
)

# Relationship
rel = Relationship(
    source_id="person_1",
    target_id="person_2",
    relationship=RelationshipType.EMPLOYER
)

# Knowledge Graph
graph = KnowledgeGraph()
graph.fetch_person("Elon Musk")
graph.build_from_seed("Elon Musk", depth=2)
```

### Kernel Primitives Classes

```python
# Agent → Process
process = AgentProcess(
    agent_id="agent-001",
    name="ai-assistant",
    pid=12345,
    uid=1000,
    state="RUNNING",
    capabilities=["CAP_SYS_ADMIN"],
    cgroup_path="/sys/fs/cgroup/agent-001"
)

# Task → Thread
thread = AgentTask(
    task_id="task-001",
    action_type="SearchAction",
    tid=12346,
    priority=0,
    state="RUNNING"
)

# Organization → Cgroup
cgroup = OrganizationCgroup(
    org_id="org-acme",
    name="acme-corp",
    cgroup_path="/sys/fs/cgroup/acme",
    cpu_shares=1024,
    memory_limit_mb=4096
)

# Person → User
user = PersonUser(
    person_id="person-john",
    name="John Doe",
    uid=1000,
    gid=1000,
    permitted_capabilities=["CAP_NET_BIND_SERVICE"]
)
```

---

## Common Enumerations

### By Database

```python
# Agent Platform
ActionStatusType: POTENTIAL, ACTIVE, COMPLETED, FAILED
ItemAvailability: IN_STOCK, ONLINE_ONLY, OUT_OF_STOCK
IndustryCategory: TECHNOLOGY, HEALTHCARE, FINANCE, etc.
SkillCategory: DATA_READ, WEB_SEARCH, CODE_EXECUTE, etc.
SoftwareCategory: AI_AGENT, PRODUCTIVITY, DEVELOPMENT, etc.

# Movie Database
MediaType: MOVIE, TV_SHOW, DOCUMENTARY, ANIMATION
RatingSystem: G, PG, PG_13, R, NC_17
Genre: ACTION, COMEDY, DRAMA, HORROR, etc.
AwardType: OSCAR, GOLDEN_GLOBE, BAFTA, EMMY

# Sports Database
SportType: FOOTBALL, BASEBALL, BASKETBALL, SOCCER, etc.
League: NFL, NBA, MLB, NHL, MLS, EPL, etc.
Position: QB, RB, WR, PG, SG, etc.
EventStatus: SCHEDULED, IN_PROGRESS, COMPLETED
Outcome: HOME_WIN, AWAY_WIN, DRAW

# Knowledge Graph
NodeType: PERSON, ORGANIZATION, PLACE, EVENT, WORK, CONCEPT
RelationshipType: SPOUSE, CHILD, PARENT, EMPLOYER, etc.

# Kernel Primitives
KernelPrimitive: PROCESS, THREAD, CGROUP, NAMESPACE, SYSCALL
```

---

## JSON-LD Export

### All Databases Export Same Format

```python
# Export
jsonld = {
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "Person", "@id": "p1", "name": "John"},
        {"@type": "SoftwareApplication", "@id": "a1", "name": "AI"},
        {"@type": "Movie", "@id": "m1", "name": "Inception"},
        {"@type": "SportsTeam", "@id": "t1", "name": "Lakers"}
    ]
}
```

---

## Usage Examples

### 1. Agent Platform

```python
platform = AgentPlatform()

# Create org
org = platform.create_organization("org-acme", "Acme Corp")

# Create agent
agent = platform.create_agent("agent-001", "AI Assistant")

# Set owner
platform.set_agent_owner("agent-001", "person-john")

# Create task
task = platform.create_task("task-001", "agent-001", "SearchAction")

# Export
print(platform.to_jsonld())
```

### 2. Movie Database

```python
db = MovieDatabase()

# Add movie
movie = Movie(id="m1", title="Inception", ...)
db.add_movie(movie)

# Add actors
actor = Person(id="p1", name="Leonardo DiCaprio", ...)
db.add_person(actor)

# Link
movie.cast.append(actor)

# Search
results = db.search_movie("Inception")
```

### 3. Sports Database

```python
db = SportsDatabase()

# Add team
team = Team(id="t1", name="Lakers", ...)
db.add_team(team)

# Add player
athlete = Athlete(id="a1", name="LeBron", ...)
db.add_athlete(athlete)

# Link
team.roster.append("a1")

# Get standings
standings = db.get_league_standings(League.NBA)
```

### 4. Knowledge Graph

```python
graph = KnowledgeGraph()

# Fetch from Wikipedia
graph.fetch_person("Elon Musk")

# Build connections
graph.build_from_seed("Elon Musk", depth=2)

# Search
results = graph.search("CEO")
```

### 5. Kernel Mapping

```python
platform = KernelAgentPlatform()

# Create process (from agent)
process = platform.create_agent_process("agent-001", "ai-assistant")

# Create thread (from task)
thread = platform.create_task_thread("task-001", "agent-001")

# Export as /proc format
print(platform.to_proc())
```

---

## Database Connections

### Example: Actor in All Databases

```python
# 1. Agent Platform: Person
person = Person(id="person-leo", name="Leonardo DiCaprio")

# 2. Movie DB: Actor (same person)
actor = Person(id="p1", name="Leonardo DiCaprio", occupation=["actor"])

# 3. Sports DB: Could have athlete (same name)
athlete = Athlete(id="a1", name="Leonardo", sport=SportType.BASKETBALL)

# 4. Knowledge Graph: From Wikipedia
wiki = WikiPerson(wiki_id="123", name="Leonardo DiCaprio")

# 5. Kernel: User (if running as user)
user = PersonUser(uid=501, name="Leonardo")
```

### Example: Movie in All Databases

```python
# 1. Agent Platform: CreativeWork
app = SoftwareApplication(name="movie-app")

# 2. Movie DB: Movie
movie = Movie(title="Titanic", cast=[actors])

# 3. Sports DB: Could be about sports movie
sports_movie = Movie(title="Remember the Titans")

# 4. Kernel: Could be file/process
# - opens file: /path/to/titanic.mp4
# - process: video_player
```

---

## Reference Links

- [Schema.org](https://schema.org)
- [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page)
- [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page)
- [Linux Kernel](https://www.kernel.org/doc/html/latest/)
- [Proc FS](https://www.kernel.org/doc/Documentation/filesystems/proc.txt)
- [Cgroups v2](https://www.kernel.org/doc/admin-guide/cgroup-v2.rst)

---

## File Summary

| File | Classes | Lines | Purpose |
|------|---------|-------|---------|
| agent_platform.py | 20 | 1389 | Agent management |
| movie_database.py | 12 | 822 | Movies/TV/Studios |
| sports_database.py | 15 | 915 | Sports/Teams/Games |
| knowledge_graph.py | 8 | 602 | Wikipedia data |
| kernel_primitives.py | 14 | 906 | Linux mapping |
| data_extraction.py | 5 | 508 | Multi-modal extraction |

**Total: ~4500 lines, 390+ classes**
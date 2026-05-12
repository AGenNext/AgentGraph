"""
Sports Database - Complete Schema.org Implementation

Comprehensive sports database with:
- Athletes, Teams, Coaches
- Leagues, Divisions
- Venues, Stadiums
- Games, Matches
- Statistics, Rankings
- Awards, Contracts

Reference:
- Schema.org: https://schema.org/SportsEvent
- Sports Reference: https://www.sports-reference.com/
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, date, time
from enum import Enum
from base_entity import Entity


# =============================================================================
# ENUMERATIONS
# =============================================================================

class SportType(Enum):
    """Sports"""
    FOOTBALL = "Football"
    BASEBALL = "Baseball"
    BASKETBALL = "Basketball"
    SOCCER = "Soccer"
    HOCKEY = "Hockey"
    TENNIS = "Tennis"
    GOLF = "Golf"
    BOXING = "Boxing"
    MMA = "Mixed Martial Arts"
    WRESTLING = "Wrestling"
    CRICKET = "Cricket"
    RUGBY = "Rugby"
    VOLLEYBALL = "Volleyball"
    AUTO_RACING = "Auto Racing"
    HORSE_RACING = "Horse Racing"
    SWIMMING = "Swimming"
    TRACK_FIELD = "Track and Field"


class League(Enum):
    """Major Leagues"""
    NFL = "NFL"
    NBA = "NBA"
    MLB = "MLB"
    NHL = "NHL"
    MLS = "MLS"
    EPL = "English Premier League"
    LA_LIGA = "La Liga"
    BUNDESLIGA = "Bundesliga"
    SERIE_A = "Serie A"
    LIGUE_1 = "Ligue 1"
    WTA = "WTA"
    ATP = "ATP"
    LPGA = "LPGA"
    PGA = "PGA"


class Position(Enum):
    """Positions"""
    # Football
    QB = "Quarterback"
    RB = "Running Back"
    WR = "Wide Receiver"
    TE = "Tight End"
    OL = "Offensive Line"
    DL = "Defensive Line"
    LB = "Linebacker"
    CB = "Cornerback"
    S = "Safety"
    K = "Kicker"
    P = "Punter"
    
    # Baseball
    PITCHER = "Pitcher"
    CATCHER = "Catcher"
    FIRST_BASE = "First Base"
    SECOND_BASE = "Second Base"
    SHORTSTOP = "Shortstop"
    THIRD_BASE = "Third Base"
    OUTFIELD = "Outfield"
    
    # Basketball
    PG = "Point Guard"
    SG = "Shooting Guard"
    SF = "Small Forward"
    PF = "Power Forward"
    C = "Center"
    
    # Soccer
    GK = "Goalkeeper"
    DEF = "Defender"
    MID = "Midfielder"
    FWD = "Forward"


class EventStatus(Enum):
    """Game status"""
    SCHEDULED = "Scheduled"
    IN_PROGRESS = "InProgress"
    COMPLETED = "Completed"
    POSTPONED = "Postponed"
    CANCELLED = "Cancelled"


class Outcome(Enum):
    """Game outcome"""
    HOME_WIN = "Home Win"
    AWAY_WIN = "Away Win"
    DRAW = "Draw"
    NO_CONTEST = "No Contest"


# =============================================================================
# CORE CLASSES
# =============================================================================

@dataclass
class Entity(Entity):
class Athlete:
    """Athlete/Player"""
    id: str
    name: str
    sport: SportType
    
    # Identity
    birth_date: Optional[date] = None
    birth_place: Optional[str] = None
    nationality: Optional[str] = None
    
    # Physical
    height_cm: Optional[float] = None  # height
    weight_kg: Optional[float] = None
    
    # Career
    position: Optional[Position] = None
    bat_hand: Optional[str] = None  # L/R
    throw_hand: Optional[str] = None
    
    # Current Team
    team_id: Optional[str] = None
    jersey_number: Optional[int] = None
    
    # Stats Career
    games_played: int = 0
    stats: Dict[str, Any] = field(default_factory=dict)
    
    # Salary
    salary: Optional[float] = None
    contract_value: Optional[float] = None
    contract_years: Optional[int] = None
    
    # Image
    photo_url: Optional[str] = None
    
    # Social
    twitter_handle: Optional[str] = None
    instagram: Optional[str] = None
    
    def to_schema(self) -> Dict:
        return {
            "@type": "Person",
            "@id": self.id,
            "name": self.name,
            "jobTitle": self.position.value if self.position else None,
            "birthDate": str(self.birth_date) if self.birth_date else None,
            "nationality": self.nationality
        }


@dataclass
class Entity(Entity):
class Coach:
    """Coach/Trainer"""
    id: str
    name: str
    sport: SportType
    
    # Role
    role: str = "Head Coach"  # Head, Assistant, Position
    title: Optional[str] = None
    
    # Details
    birth_date: Optional[date] = None
    nationality: Optional[str] = None
    
    # Career
    team_id: Optional[str] = None
    experience_years: int = 0
    
    # Record
    wins: int = 0
    losses: int = 0
    ties: int = 0
    
    # Salary
    salary: Optional[float] = None
    
    def win_pct(self) -> float:
        total = self.wins + self.losses + self.ties
        if total == 0:
            return 0.0
        return self.wins / total
    
    def to_schema(self) -> Dict:
        return {
            "@type": "Person",
            "@id": self.id,
            "name": self.name,
            "jobTitle": self.role,
            "worksFor": {"@id": self.team_id} if self.team_id else None
        }


@dataclass
class Entity(Entity):
class Team:
    """Sports Team"""
    id: str
    name: str
    sport: SportType
    
    # Identity
    short_name: Optional[str] = None  # Abbreviation
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    
    # League
    league: Optional[League] = None
    division: Optional[str] = None
    
    # Venue
    venue_id: Optional[str] = None
    
    # Personnel
    coach_id: Optional[str] = None
    owner: Optional[str] = None
    general_manager: Optional[str] = None
    
    # Roster
    roster: List[str] = field(default_factory=list)  # athlete IDs
    
    # Record
    wins: int = 0
    losses: int = 0
    ties: int = 0
    
    # Standings
    rank: int = 0
    playoff_seed: Optional[int] = None
    
    # Finance
    valuation: Optional[float] = None  # in millions
    revenue: Optional[float] = None
    payroll: Optional[float] = None
    
    # Logo
    logo_url: Optional[str] = None
    colors: List[str] = field(default_factory=list)
    
    # Social
    website: Optional[str] = None
    twitter: Optional[str] = None
    
    def win_pct(self) -> float:
        total = self.wins + self.losses + self.ties
        if total == 0:
            return 0.0
        return self.wins / total
    
    def add_player(self, athlete_id: str):
        if athlete_id not in self.roster:
            self.roster.append(athlete_id)
    
    def to_schema(self) -> Dict:
        return {
            "@type": "SportsTeam",
            "@id": self.id,
            "name": self.name,
            "homeLocation": {
                "@type": "Place",
                "address": f"{self.city}, {self.state}"
            },
            "member": [{"@id": pid} for pid in self.roster[:10]]
        }


@dataclass
class Entity(Entity):
class Venue:
    """Stadium/Arena"""
    id: str
    name: str
    
    # Location
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    
    # Geo
    lat: Optional[float] = None
    lon: Optional[float] = None
    
    # Capacity
    capacity: int = 0
    capacity_football: Optional[int] = None
    
    # Features
    roof_type: Optional[str] = None  # open, dome, retractable
    turf_type: Optional[str] = None
    
    # Teams
    home_teams: List[str] = field(default_factory=list)
    
    # Built
    opening_date: Optional[date] = None
    
    # Cost
    construction_cost: Optional[float] = None
    
    def to_schema(self) -> Dict:
        return {
            "@type": "StadiumOrArena",
            "@id": self.id,
            "name": self.name,
            "address": self.address,
            "capacity": self.capacity
        }


@dataclass
class Entity(Entity):
class Game:
    """Game/Match"""
    id: str
    sport: SportType
    
    # Teams
    home_team_id: Optional[str] = None
    away_team_id: Optional[str] = None
    
    # Time
    scheduled_time: Optional[datetime] = None
    start_time: Optional[time] = None
    
    # Status
    status: EventStatus = EventStatus.SCHEDULED
    
    # Score
    home_score: int = 0
    away_score: int = 0
    
    # Period
    period: Optional[str] = None  # Q1, Q2, Q3, Q4, Inning, Half
    time_remaining: Optional[str] = None
    
    # Officials
    referee: Optional[str] = None
    umpire: Optional[str] = None
    
    # Venue
    venue_id: Optional[str] = None
    
    # Broadcast
    tv_network: Optional[str] = None
    tv_channel: Optional[str] = None
    
    # Attendance
    attendance: int = 0
    
    # Note
    notes: Optional[str] = None
    
    def home_win(self) -> bool:
        return self.home_score > self.away_score
    
    def away_win(self) -> bool:
        return self.away_score > self.home_score
    
    def is_final(self) -> bool:
        return self.status == EventStatus.COMPLETED
    
    def to_schema(self) -> Dict:
        return {
            "@type": "SportsEvent",
            "@id": self.id,
            "startDate": self.scheduled_time.isoformat() if self.scheduled_time else None,
            "homeTeam": {"@id": self.home_team_id},
            "awayTeam": {"@id": self.away_team_id},
            "winner": self.home_team_id if self.home_win() else self.away_team_id if self.away_win() else None
        }


@dataclass
class Entity(Entity):
class Season:
    """Season"""
    id: str
    sport: SportType
    league: League
    
    year: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    
    # Games
    games: List[str] = field(default_factory=list)  # game IDs
    
    # Champion
    champion_team_id: Optional[str] = None
    
    # Status
    status: str = "active"  # active, completed
    
    def to_schema(self) -> Dict:
        return {
            "@type": "SportsSeason",
            "@id": self.id,
            "sport": self.sport.value,
            "league": self.league.value,
            "startDate": str(self.start_date) if self.start_date else None
        }


@dataclass
class Entity(Entity):
class StatLine:
    """Player Stats for a Game"""
    id: str
    game_id: str
    athlete_id: str
    
    # Basic
    minutes: int = 0
    points: int = 0
    rebounds: int = 0
    assists: int = 0
    
    # Shooting
    field_goals_made: int = 0
    field_goals_attempted: int = 0
    three_points_made: int = 0
    three_points_attempted: int = 0
    free_throws_made: int = 0
    free_throws_attempted: int = 0
    
    # Other
    steals: int = 0
    blocks: int = 0
    turnovers: int = 0
    personal_fouls: int = 0
    
    def fg_pct(self) -> float:
        if self.field_goals_attempted == 0:
            return 0.0
        return self.field_goals_made / self.field_goals_attempted


@dataclass
class Entity(Entity):
class TeamStatLine:
    """Team Stats"""
    id: str
    team_id: str
    
    # Record
    wins: int = 0
    losses: int = 0
    ties: int = 0
    
    # Offense
    points_for: int = 0  # total points scored
    points_against: int = 0
    
    # Shooting
    field_goal_pct: float = 0.0
    three_point_pct: float = 0.0
    
    # Other
    turnovers: int = 0
    steals: int = 0
    blocks: int = 0


@dataclass
class Entity(Entity):
class Contract:
    """Player Contract"""
    id: str
    athlete_id: str
    team_id: str
    
    value: float
    years: int
    
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    
    guaranteed: bool = True
    
    # Clauses
    no_trade_clause: bool = False
    player_option: bool = False
    team_option: bool = False
    
    def to_schema(self) -> Dict:
        return {
            "@type": "Offer",
            "@id": self.id,
            "price": self.value,
            "validFrom": str(self.start_date) if self.start_date else None,
            "validThrough": str(self.end_date) if self.end_date else None
        }


@dataclass
class Entity(Entity):
class Award:
    """Sports Award"""
    id: str
    name: str  # MVP, ROY, etc.
    sport: SportType
    league: League
    
    year: int
    
    recipient_id: Optional[str] = None  # athlete_id
    recipient_team_id: Optional[str] = None
    
    # Vote details
    votes: Optional[int] = None
    points: Optional[float] = None
    
    def to_schema(self) -> Dict:
        return {
            "@type": "Award",
            "name": self.name,
            "year": self.year
        }


@dataclass
class Entity(Entity):
class Ranking:
    """Team/Athlete Ranking"""
    id: str
    sport: SportType
    league: League
    
    week: int
    year: int
    
    # Ranked entity
    entity_id: str
    entity_type: str  # team, athlete
    
    rank: int
    previous_rank: Optional[int] = None
    
    # Polls
    ap_poll: Optional[int] = None
    coaches_poll: Optional[int] = None
    
    # Points
    points: Optional[float] = None
    first_place_votes: Optional[int] = None
    
    def moved_up(self) -> bool:
        return self.previous_rank and self.rank < self.previous_rank
    
    def moved_down(self) -> bool:
        return self.previous_rank and self.rank > self.previous_rank


# =============================================================================
# SPORTS DATABASE
# =============================================================================

class SportsDatabase:
    """Complete sports database"""
    
    def __init__(self):
        self.athletes: Dict[str, Athlete] = {}
        self.coaches: Dict[str, Coach] = {}
        self.teams: Dict[str, Team] = {}
        self.venues: Dict[str, Venue] = {}
        self.games: Dict[str, Game] = {}
        self.seasons: Dict[str, Season] = {}
        self.stat_lines: Dict[str, StatLine] = {}
        self.team_stats: Dict[str, TeamStatLine] = {}
        self.contracts: Dict[str, Contract] = {}
        self.awards: Dict[str, Award] = {}
        self.rankings: Dict[str, Ranking] = {}
    
    # ---------------------------------------------------------------------
    # Athletes
    # ---------------------------------------------------------------------
    
    def add_athlete(self, athlete: Athlete) -> str:
        self.athletes[athlete.id] = athlete
        return athlete.id
    
    def get_athlete(self, athlete_id: str) -> Optional[Athlete]:
        return self.athletes.get(athlete_id)
    
    def search_athlete(self, query: str) -> List[Athlete]:
        return [a for a in self.athletes.values() 
                if query.lower() in a.name.lower()]
    
    def get_team_roster(self, team_id: str) -> List[Athlete]:
        team = self.teams.get(team_id)
        if not team:
            return []
        return [self.athletes[pid] for pid in team.roster 
                    if pid in self.athletes]
    
    # ---------------------------------------------------------------------
    # Teams
    # ---------------------------------------------------------------------
    
    def add_team(self, team: Team) -> str:
        self.teams[team.id] = team
        return team.id
    
    def get_team(self, team_id: str) -> Optional[Team]:
        return self.teams.get(team_id)
    
    def search_team(self, query: str) -> List[Team]:
        return [t for t in self.teams.values() 
                if query.lower() in t.name.lower()]
    
    def get_teams_by_league(self, league: League) -> List[Team]:
        return [t for t in self.teams.values() 
                if t.league == league]
    
    def get_teams_by_sport(self, sport: SportType) -> List[Team]:
        return [t for t in self.teams.values() 
                if t.sport == sport]
    
    def get_league_standings(self, league: League) -> List[Team]:
        teams = self.get_teams_by_league(league)
        return sorted(teams, key=lambda t: t.win_pct(), reverse=True)
    
    # ---------------------------------------------------------------------
    # Games
    # ---------------------------------------------------------------------
    
    def add_game(self, game: Game) -> str:
        self.games[game.id] = game
        return game.id
    
    def get_game(self, game_id: str) -> Optional[Game]:
        return self.games.get(game_id)
    
    def get_team_games(self, team_id: str) -> List[Game]:
        return [g for g in self.games.values() 
                if g.home_team_id == team_id or g.away_team_id == team_id]
    
    def get_upcoming_games(self, limit: int = 10) -> List[Game]:
        from datetime import datetime
        
        upcoming = [g for g in self.games.values() 
                  if g.status == EventStatus.SCHEDULED 
                  and g.scheduled_time 
                  and g.scheduled_time > datetime.now()]
        
        return sorted(upcoming, key=lambda g: g.scheduled_time)[:limit]
    
    # ---------------------------------------------------------------------
    # Venues
    # ---------------------------------------------------------------------
    
    def add_venue(self, venue: Venue) -> str:
        self.venues[venue.id] = venue
        return venue.id
    
    def get_venue(self, venue_id: str) -> Optional[Venue]:
        return self.venues.get(venue_id)
    
    # ---------------------------------------------------------------------
    # Awards
    # ---------------------------------------------------------------------
    
    def add_award(self, award: Award) -> str:
        self.awards[award.id] = award
        return award.id
    
    def get_athlete_awards(self, athlete_id: str) -> List[Award]:
        return [a for a in self.awards.values() 
                if a.recipient_id == athlete_id]
    
    def get_team_awards(self, team_id: str) -> List[Award]:
        return [a for a in self.awards.values() 
                if a.recipient_team_id == team_id]
    
    # ---------------------------------------------------------------------
    # Contracts
    # ---------------------------------------------------------------------
    
    def add_contract(self, contract: Contract) -> str:
        self.contracts[contract.id] = contract
        return contract.id
    
    def get_active_contracts(self, team_id: str) -> List[Contract]:
        return [c for c in self.contracts.values() 
                if c.team_id == team_id and c.end_date]
    
    # ---------------------------------------------------------------------
    # Export
    # ---------------------------------------------------------------------
    
    def to_jsonld(self) -> Dict:
        graph = []
        
        for team in self.teams.values():
            graph.append(team.to_schema())
        
        for athlete in self.athletes.values():
            graph.append(athlete.to_schema())
        
        for venue in self.venues.values():
            graph.append(venue.to_schema())
        
        for game in self.games.values():
            graph.append(game.to_schema())
        
        return {
            "@context": "https://schema.org",
            "@graph": graph
        }
    
    def to_json(self) -> Dict:
        return {
            "teams": {t.id: {"name": t.name, "league": t.league.value} 
                     for t in self.teams.values()},
            "athletes": {a.id: {"name": a.name, "sport": a.sport.value} 
                        for a in self.athletes.values()},
            "games": {g.id: {"home": g.home_team_id, "away": g.away_team_id,
                           "status": g.status.value} for g in self.games.values()}
        }


# =============================================================================
# SAMPLE DATA
# =============================================================================

def create_sample_database() -> SportsDatabase:
    """Create sample sports database"""
    
    db = SportsDatabase()
    
    # Add venues
    venues = [
        Venue(id="v1", name="MetLife Stadium", city="East Rutherford",
              state="NJ", capacity=82500, roof_type="open"),
        Venue(id="v2", name="Madison Square Garden", city="New York",
              state="NY", capacity=19812, roof_type="dome"),
        Venue(id="v3", name="Fenway Park", city="Boston", state="MA",
              capacity=37755, roof_type="open"),
        Venue(id="v4", name="Staples Center", city="Los Angeles",
              state="CA", capacity=19068, roof_type="dome"),
    ]
    
    for v in venues:
        db.add_venue(v)
    
    # Add teams
    teams = [
        Team(id="t1", name="New York Giants", short_name="NYG", sport=SportType.FOOTBALL,
             city="New York", state="NY", league=League.NFL, venue_id="v1",
             wins=4, losses=12, rank=4, colors=["blue", "red"]),
        Team(id="t2", name="Los Angeles Lakers", short_name="LAL", 
             sport=SportType.BASKETBALL, city="Los Angeles", state="CA",
             league=League.NBA, venue_id="v4", wins=52, losses=19,
             colors=["purple", "gold"]),
        Team(id="t3", name="Boston Red Sox", short_name="BOS", 
             sport=SportType.BASEBALL, city="Boston", state="MA",
             league=League.MLB, venue_id="v3", wins=84, losses=78,
             colors=["red", "blue", "white"]),
        Team(id="t4", name="New York Knicks", short_name="NYK",
             sport=SportType.BASKETBALL, city="New York", state="NY",
             league=League.NBA, venue_id="v2", wins=41, losses=31,
             colors=["orange", "blue"]),
    ]
    
    for t in teams:
        db.add_team(t)
    
    # Add athletes
    athletes = [
        Athlete(id="a1", name="Saquon Barkley", sport=SportType.FOOTBALL,
                position=Position.RB, team_id="t1", jersey_number=26,
                height_cm=180, weight_kg=100, nationality="USA"),
        Athlete(id="a2", name="LeBron James", sport=SportType.BASKETBALL,
                position=Position.FW, team_id="t2", jersey_number=23,
                height_cm=206, weight_kg=113, nationality="USA"),
        Athlete(id="a3", name="Mookie Betts", sport=SportType.BASEBALL,
                position=Position.OUTFIELD, team_id="t3", jersey_number=50,
                height_cm=185, weight_kg=82, nationality="USA"),
        Athlete(id="a4", name="Julius Randle", sport=SportType.BASKETBALL,
                position=Position.PF, team_id="t4", jersey_number=30,
                height_cm=203, weight_kg=113, nationality="USA"),
        Athlete(id="a5", name="Patrick Mahomes", sport=SportType.FOOTBALL,
                position=Position.QB, team_id="t1", jersey_number=15,
                height_cm=188, weight_kg=104, nationality="USA"),
    ]
    
    for a in athletes:
        db.add_athlete(a)
    
    # Add games
    games = [
        Game(id="g1", sport=SportType.FOOTBALL, home_team_id="t1", away_team_id="t2",
             scheduled_time=datetime(2024, 11, 15, 20, 0), status=EventStatus.SCHEDULED,
             venue_id="v1", tv_network="ESPN"),
        Game(id="g2", sport=SportType.BASKETBALL, home_team_id="t2", away_team_id="t4",
             scheduled_time=datetime(2024, 11, 10, 19, 30), status=EventStatus.COMPLETED,
             home_score=114, away_score=109, venue_id="v4"),
    ]
    
    for g in games:
        db.add_game(g)
    
    # Add awards
    awards = [
        Award(id="aw1", name="MVP", sport=SportType.FOOTBALL, league=League.NFL,
              year=2023, recipient_id="a5", votes=490, points=2011),
        Award(id="aw2", name="MVP", sport=SportType.BASKETBALL, league=League.NBA,
              year=2023, recipient_id="a2", votes=86, points=426),
    ]
    
    for a in awards:
        db.add_award(a)
    
    return db


# =============================================================================
# USAGE
# =============================================================================

def main():
    """Example usage"""
    
    print("=" * 50)
    print("Sports Database")
    print("=" * 50)
    
    # Create database
    db = create_sample_database()
    
    # Search teams
    print("\n1. NFL Teams:")
    nfl_teams = db.get_teams_by_sport(SportType.FOOTBALL)
    for t in nfl_teams:
        print(f"   - {t.name} ({t.league.value})")
    
    # Search athletes
    print("\n2. Search Athletes:")
    results = db.search_athlete("LeBron")
    for a in results:
        print(f"   - {a.name} - {a.position.value}")
    
    # Rankings
    print("\n3. NBA Standings:")
    nba_teams = db.get_teams_by_league(League.NBA)
    for t in sorted(nba_teams, key=lambda x: x.win_pct(), reverse=True):
        print(f"   {t.win_pct():.3f} - {t.name}")
    
    # Upcoming games
    print("\n4. Upcoming Games:")
    upcoming = db.get_upcoming_games()
    for g in upcoming:
        print(f"   - {g.scheduled_time} {g.home_team_id} vs {g.away_team_id}")
    
    # Awards
    print("\n5. Recent Awards:")
    for a in db.awards.values():
        print(f"   - {a.name} ({a.year}): {a.league.value}")
    
    # Export
    print("\n6. Export JSON-LD:")
    jsonld = db.to_jsonld()
    print(f"   Total: {len(jsonld['@graph'])} entities")


if __name__ == "__main__":
    main()


"""
Sports Database Usage:

    # Create database
    db = SportsDatabase()
    
    # Add team
    team = Team(id="t1", name="Lakers", sport=SportType.BASKETBALL, ...)
    db.add_team(team)
    
    # Add athlete
    player = Athlete(id="a1", name="LeBron James", sport=SportType.BASKETBALL, ...)
    db.add_athlete(player)
    
    # Search
    teams = db.search_team("Lakers")
    players = db.search_athlete("LeBron")
    standings = db.get_league_standings(League.NBA)
    
    # Export
    print(db.to_jsonld())

References:
    - Schema.org: https://schema.org/SportsEvent
    - Schema.org: https://schema.org/SportsTeam
    - Sports Reference: https://www.sports-reference.com/
"""
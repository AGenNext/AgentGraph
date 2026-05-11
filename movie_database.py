"""
Movie Database - Complete Schema.org Implementation

Comprehensive movie database with:
- Movies, Actors, Directors
- Studios, Genres
- Awards, Reviews
- Showtimes, Tickets
- Relationships

Reference:
- Schema.org: https://schema.org/Movie
- IMDB Data Model
- TMDB API Patterns
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum


# =============================================================================
# ENUMERATIONS
# =============================================================================

class MediaType(Enum):
    """Type of media"""
    MOVIE = "Movie"
    TV_SHOW = "TVSeries"
    DOCUMENTARY = "Documentary"
    SHORT_FILM = "Short"
    ANIMATION = "Animation"


class RatingSystem(Enum):
    """Content rating"""
    G = "G"
    PG = "PG"
    PG_13 = "PG-13"
    R = "R"
    NC_17 = "NC-17"
    TV_Y = "TV-Y"
    TV_G = "TV-G"
    TV_PG = "TV-PG"
    TV_14 = "TV-14"
    TV_MA = "TV-MA"


class Genre(Enum):
    """Movie genres"""
    ACTION = "Action"
    ADVENTURE = "Adventure"
    ANIMATION = "Animation"
    BIOGRAPHY = "Biography"
    COMEDY = "Comedy"
    CRIME = "Crime"
    DOCUMENTARY = "Documentary"
    DRAMA = "Drama"
    FAMILY = "Family"
    FANTASY = "Fantasy"
    HISTORY = "History"
    HORROR = "Horror"
    MUSIC = "Music"
    MYSTERY = "Mystery"
    ROMANCE = "Romance"
    SCI_FI = "Sci-Fi"
    SPORT = "Sport"
    THRILLER = "Thriller"
    WAR = "War"
    WESTERN = "Western"


class AwardType(Enum):
    """Award types"""
    OSCAR = "Oscar"
    GOLDEN_GLOBE = "Golden Globe"
    BAFTA = "BAFTA"
    EMMY = "Emmy"
    GRAMMY = "Grammy"
    PALME_D_OR = "Palme d'Or"
    GOLDEN_BEAR = "Golden Bear"
    CANNES = "Cannes"
    SAG = "SAG"


# =============================================================================
# CORE CLASSES
# =============================================================================

@dataclass
class Person:
    """Person (Actor, Director, etc.)"""
    id: str
    name: str
    biography: Optional[str] = None
    
    # Identity
    birth_date: Optional[date] = None
    birth_place: Optional[str] = None
    death_date: Optional[date] = None
    gender: Optional[str] = None
    
    # Physical
    height_cm: Optional[float] = None
    
    # Career
    occupation: List[str] = field(default_factory=list)  # actor, director, etc.
    known_for: List[str] = field(default_factory=list)  # movie IDs
    
    # Stats
    total_movies: int = 0
    avg_rating: float = 0.0
    
    # Image
    photo_url: Optional[str] = None
    
    def add_movie(self, movie_id: str):
        if movie_id not in self.known_for:
            self.known_for.append(movie_id)
            self.total_movies += 1
    
    def to_schema(self) -> Dict:
        return {
            "@type": "Person",
            "@id": self.id,
            "name": self.name,
            "birthDate": str(self.birth_date) if self.birth_date else None,
            "jobTitle": self.occupation[0] if self.occupation else None
        }


@dataclass
class Movie:
    """Movie"""
    id: str
    title: str
    
    # Identity
    original_title: Optional[str] = None
    tagline: Optional[str] = None
    plot: Optional[str] = None
    release_date: Optional[date] = None
    
    # Classification
    media_type: MediaType = MediaType.MOVIE
    genres: List[str] = field(default_factory=list)
    content_rating: Optional[RatingSystem] = None
    
    # Duration
    runtime_minutes: Optional[int] = None  # in minutes
    
    # Language
    language: List[str] = field(default_factory=list)
    subtitle_language: List[str] = field(default_factory=list)
    
    # Budget/Box Office
    budget: Optional[int] = None  # USD
    revenue: Optional[int] = None
    currency: str = "USD"
    
    # Status
    status: str = "released"  # released, production, announced
    
    # People
    director: Optional[Person] = None
    cast: List[Person] = field(default_factory=list)
    writer: List[Person] = field(default_factory=list)
    producer: List[Person] = field(default_factory=list)
    cinematographer: Optional[Person] = None
    composer: Optional[Person] = None
    editor: Optional[Person] = None
    
    # Studio
    production_company: Optional[str] = None
    distributor: Optional[str] = None
    
    # Rating
    imdb_id: Optional[str] = None
    imdb_rating: Optional[float] = None
    imdb_votes: int = 0
    rotten_tomatoes_score: Optional[int] = None
    
    # Images
    poster_url: Optional[str] = None
    backdrop_url: Optional[str] = None
    
    # Links
    website: Optional[str] = None
    trailer_url: Optional[str] = None
    
    # Awards
    awards: List[Dict] = field(default_factory=list)
    
    # Keywords
    keywords: List[str] = field(default_factory=list)
    
    # Collections
    collection: Optional[str] = None  # franchise
    
    def add_cast(self, person: Person):
        self.cast.append(person)
        person.add_movie(self.id)
    
    def to_schema(self) -> Dict:
        return {
            "@type": "Movie",
            "@id": self.id,
            "name": self.title,
            "description": self.plot,
            "datePublished": str(self.release_date) if self.release_date else None,
            "duration": f"PT{self.runtime_minutes}M" if self.runtime_minutes else None,
            "contentRating": self.content_rating.value if self.content_rating else None,
            "genre": self.genres,
            "actor": [{"@type": "Person", "name": p.name} for p in self.cast[:5]],
            "director": {"@type": "Person", "name": self.director.name} if self.director else None
        }


@dataclass
class TVSeries:
    """TV Series"""
    id: str
    name: str
    
    # Show info
    plot: Optional[str] = None
    release_date: Optional[date] = None
    end_date: Optional[date] = None
    
    # Classification
    genres: List[str] = field(default_factory=list)
    content_rating: Optional[RatingSystem] = None
    
    # Seasons/Episodes
    number_of_seasons: int = 0
    number_of_episodes: int = 0
    
    # Status
    status: str = "returning"  # returning, ended, cancelled
    
    # People
    creator: Optional[Person] = None
    cast: List[Person] = field(default_factory=list)
    
    # Rating
    imdb_rating: Optional[float] = None
    
    # Images
    poster_url: Optional[str] = None
    
    def to_schema(self) -> Dict:
        return {
            "@type": "TVSeries",
            "@id": self.id,
            "name": self.name,
            "description": self.plot,
            "numberOfSeasons": self.number_of_seasons,
            "numberOfEpisodes": self.number_of_episodes
        }


@dataclass
class Season:
    """TV Season"""
    id: str
    series_id: str
    season_number: int
    
    title: Optional[str] = None
    plot: Optional[str] = None
    release_date: Optional[date] = None
    
    number_of_episodes: int = 0
    episodes: List[Dict] = field(default_factory=list)


@dataclass
class Episode:
    """TV Episode"""
    id: str
    series_id: str
    season_number: int
    episode_number: int
    
    title: Optional[str] = None
    plot: Optional[str] = None
    runtime_minutes: Optional[int] = None
    release_date: Optional[date] = None
    
    imdb_rating: Optional[float] = None


@dataclass
class Studio:
    """Production Studio"""
    id: str
    name: str
    
    founding_year: Optional[int] = None
    headquarters: Optional[str] = None
    website: Optional[str] = None
    
    founder: Optional[str] = None
    parent_company: Optional[str] = None
    
    movies: List[str] = field(default_factory=list)  # movie IDs
    
    logo_url: Optional[str] = None
    
    def add_movie(self, movie_id: str):
        self.movies.append(movie_id)
    
    def to_schema(self) -> Dict:
        return {
            "@type": "Organization",
            "@id": self.id,
            "name": self.name,
            "foundingDate": str(self.founding_year) if self.founding_year else None,
            "url": self.website
        }


@dataclass
class Review:
    """Movie Review"""
    id: str
    movie_id: str
    
    author: Optional[str] = None
    rating: Optional[float] = None  # 1-10
    rating_max: float = 10.0
    
    title: Optional[str] = None
    body: Optional[str] = None
    
    source: Optional[str] = None  # imdb, rotten_tomatoes, etc.
    source_url: Optional[str] = None
    
    helpful_count: int = 0
    created_at: Optional[datetime] = None
    
    def to_schema(self) -> Dict:
        return {
            "@type": "Review",
            "@id": self.id,
            "reviewRating": {
                "@type": "Rating",
                "ratingValue": self.rating,
                "bestRating": self.rating_max
            },
            "author": self.author,
            "reviewBody": self.body
        }


@dataclass
class Award:
    """Award/Oscar"""
    id: str
    name: str
    award_type: AwardType
    
    year: Optional[int] = None
    category: Optional[str] = None
    
    movie_id: Optional[str] = None
    person_id: Optional[str] = None
    
    winner: bool = True
    
    def to_schema(self) -> Dict:
        return {
            "@type": "Award",
            "name": f"{self.award_type.value} - {self.category}",
            "year": self.year,
            "winner": self.winner
        }


@dataclass
class Showtime:
    """Theater Showtime"""
    id: str
    movie_id: str
    theater_id: str
    
    show_time: datetime
    
    format_3d: bool = False
    format_imax: bool = False
    format_dolby: bool = False
    
    price: Optional[float] = None
    
    available_seats: int = 0
    total_seats: int = 0
    
    def to_schema(self) -> Dict:
        return {
            "@type": "ScreeningEvent",
            "@id": self.id,
            "startDate": self.show_time.isoformat(),
            "workPresented": {"@id": self.movie_id},
            "location": {"@id": self.theater_id}
        }


@dataclass
class Theater:
    """Movie Theater"""
    id: str
    name: str
    
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    
    lat: Optional[float] = None
    lon: Optional[float] = None
    
    screens: int = 0
    seats_per_screen: int = 0
    
    def to_schema(self) -> Dict:
        return {
            "@type": "CivicStructure",
            "@id": self.id,
            "name": self.name,
            "address": self.address
        }


# =============================================================================
# MOVIE DATABASE
# =============================================================================

class MovieDatabase:
    """Complete movie database"""
    
    def __init__(self):
        self.movies: Dict[str, Movie] = {}
        self.people: Dict[str, Person] = {}
        self.tv_series: Dict[str, TVSeries] = {}
        self.studios: Dict[str, Studio] = {}
        self.reviews: Dict[str, Review] = {}
        self.awards: Dict[str, Award] = {}
        self.showtimes: Dict[str, Showtime] = {}
        self.theaters: Dict[str, Theater] = {}
    
    # ---------------------------------------------------------------------
    # People
    # ---------------------------------------------------------------------
    
    def add_person(self, person: Person) -> str:
        """Add person"""
        self.people[person.id] = person
        return person.id
    
    def get_person(self, person_id: str) -> Optional[Person]:
        return self.people.get(person_id)
    
    def search_person(self, query: str) -> List[Person]:
        query_lower = query.lower()
        return [p for p in self.people.values() 
                if query_lower in p.name.lower()]
    
    # ---------------------------------------------------------------------
    # Movies
    # ---------------------------------------------------------------------
    
    def add_movie(self, movie: Movie) -> str:
        """Add movie"""
        self.movies[movie.id] = movie
        return movie.id
    
    def get_movie(self, movie_id: str) -> Optional[Movie]:
        return self.movies.get(movie_id)
    
    def search_movie(self, query: str) -> List[Movie]:
        query_lower = query.lower()
        return [m for m in self.movies.values() 
                if query_lower in m.title.lower()]
    
    def get_movies_by_genre(self, genre: str) -> List[Movie]:
        return [m for m in self.movies.values() 
                if genre in m.genres]
    
    def get_movies_by_year(self, year: int) -> List[Movie]:
        return [m for m in self.movies.values() 
                if m.release_date and m.release_date.year == year]
    
    def get_movies_by_actor(self, actor_id: str) -> List[Movie]:
        actor = self.people.get(actor_id)
        if not actor:
            return []
        return [m for m in self.movies.values() 
                if actor_id in m.known_for]
    
    def get_top_rated(self, limit: int = 10) -> List[Movie]:
        sorted_movies = sorted(
            self.movies.values(), 
            key=lambda m: m.imdb_rating or 0, 
            reverse=True
        )
        return sorted_movies[:limit]
    
    # ---------------------------------------------------------------------
    # Studios
    # ---------------------------------------------------------------------
    
    def add_studio(self, studio: Studio) -> str:
        self.studios[studio.id] = studio
        return studio.id
    
    def get_studio(self, studio_id: str) -> Optional[Studio]:
        return self.studios.get(studio_id)
    
    # ---------------------------------------------------------------------
    # Reviews
    # ---------------------------------------------------------------------
    
    def add_review(self, review: Review) -> str:
        self.reviews[review.id] = review
        return review.id
    
    def get_movie_reviews(self, movie_id: str) -> List[Review]:
        return [r for r in self.reviews.values() 
                if r.movie_id == movie_id]
    
    # ---------------------------------------------------------------------
    # Awards
    # ---------------------------------------------------------------------
    
    def add_award(self, award: Award) -> str:
        self.awards[award.id] = award
        return award.id
    
    def get_movie_awards(self, movie_id: str) -> List[Award]:
        return [a for a in self.awards.values() 
                if a.movie_id == movie_id]
    
    def get_person_awards(self, person_id: str) -> List[Award]:
        return [a for a in self.awards.values() 
                if a.person_id == person_id]
    
    # ---------------------------------------------------------------------
    # Showtimes
    # ---------------------------------------------------------------------
    
    def add_showtime(self, showtime: Showtime) -> str:
        self.showtimes[showtime.id] = showtime
        return showtime.id
    
    def get_movie_showtimes(self, movie_id: str) -> List[Showtime]:
        return [s for s in self.showtimes.values() 
                if s.movie_id == movie_id]
    
    # ---------------------------------------------------------------------
    # Export
    # ---------------------------------------------------------------------
    
    def to_jsonld(self) -> Dict:
        """Export as JSON-LD"""
        graph = []
        
        # Movies
        for movie in self.movies.values():
            graph.append(movie.to_schema())
        
        # People
        for person in self.people.values():
            graph.append(person.to_schema())
        
        # Studios
        for studio in self.studios.values():
            graph.append(studio.to_schema())
        
        # Reviews
        for review in self.reviews.values():
            graph.append(review.to_schema())
        
        # Awards
        for award in self.awards.values():
            graph.append(award.to_schema())
        
        return {
            "@context": "https://schema.org",
            "@graph": graph
        }
    
    def to_json(self) -> Dict:
        """Export as JSON"""
        return {
            "movies": {
                m.id: {
                    "title": m.title,
                    "release_date": str(m.release_date) if m.release_date else None,
                    "runtime_minutes": m.runtime_minutes,
                    "genres": m.genres,
                    "imdb_rating": m.imdb_rating,
                    "director": m.director.name if m.director else None,
                    "cast": [p.name for p in m.cast]
                }
                for m in self.movies.values()
            },
            "people": {
                p.id: {
                    "name": p.name,
                    "occupation": p.occupation,
                    "total_movies": p.total_movies
                }
                for p in self.people.values()
            }
        }


# =============================================================================
# EXAMPLE DATA
# =============================================================================

def create_sample_database() -> MovieDatabase:
    """Create sample movie database"""
    
    db = MovieDatabase()
    
    # Create people
    actors = [
        Person(id="p1", name="Leonardo DiCaprio", 
                occupation=["actor"], birth_date=1974-11-11),
        Person(id="p2", name="Tom Hanks",
                occupation=["actor"], birth_date=1956-07-09),
        Person(id="p3", name="Robert De Niro",
                occupation=["actor"], birth_date=1943-08-17),
        Person(id="p4", name="Quentin Tarantino",
                occupation=["director", "writer"], birth_date=1963-03-27),
        Person(id="p5", name="Steven Spielberg",
                occupation=["director", "producer"], birth_date=1946-12-18),
    ]
    
    for actor in actors:
        db.add_person(actor)
    
    # Create studios
    studios = [
        Studio(id="s1", name="Warner Bros.", founding_year=1923, 
               headquarters="Burbank, California"),
        Studio(id="s2", name="Universal Pictures", founding_year=1912,
               headquarters="Universal City, California"),
        Studio(id="s3", name="Paramount Pictures", founding_year=1912,
               headquarters="Hollywood, California"),
    ]
    
    for studio in studios:
        db.add_studio(studio)
    
    # Create movies
    movies = [
        Movie(
            id="m1",
            title="Inception",
            release_date=date(2010, 7, 16),
            plot="A thief who steals corporate secrets through dream-sharing technology...",
            runtime_minutes=148,
            genres=["Sci-Fi", "Action", "Thriller"],
            content_rating=RatingSystem.PG_13,
            director=db.people["p4"],
            budget=160000000,
            revenue=836836967,
            imdb_rating=8.8,
            imdb_votes=2200000,
            production_company="Warner Bros."
        ),
        Movie(
            id="m2",
            title="The Godfather",
            release_date=date(1972, 3, 24),
            plot="The aging patriarch of an organized crime dynasty...",
            runtime_minutes=175,
            genres=["Crime", "Drama"],
            content_rating=RatingSystem.R,
            director=None,  # Francis Ford Coppola not in DB
            budget=6000000,
            revenue=246120974,
            imdb_rating=9.2,
            imdb_votes=1800000,
            production_company="Paramount Pictures"
        ),
        Movie(
            id="m3",
            title="Forrest Gump",
            release_date=date(1994, 7, 6),
            plot="The presidencies of Kennedy and Johnson unfold through the life of Forrest Gump...",
            runtime_minutes=142,
            genres=["Drama", "Romance"],
            content_rating=RatingSystem.PG_13,
            director=db.people.get("p5"),  # Simplified
            budget=55000000,
            revenue=678226133,
            imdb_rating=8.8,
            imdb_votes=1900000,
            production_company="Paramount Pictures"
        ),
    ]
    
    # Add cast to movies
    movies[0].cast = [db.people["p1"]]  # Inception - Leo
    movies[1].cast = [db.people["p3"]]  # Godfather - De Niro
    movies[2].cast = [db.people["p2"]]  # Forrest Gump - Tom
    
    for movie in movies:
        db.add_movie(movie)
    
    # Add reviews
    reviews = [
        Review(id="r1", movie_id="m1", author="John D.",
               rating=9.0, title="Mind-bending masterpiece",
               body="One of the best films ever made..."),
        Review(id="r2", movie_id="m2", author="Mike R.",
               rating=10.0, title="The greatest film ever",
               body="A timeless classic..."),
    ]
    
    for review in reviews:
        db.add_review(review)
    
    # Add awards
    awards = [
        Award(id="a1", name="Oscar", award_type=AwardType.OSCAR,
              year=2011, category="Best Picture", movie_id="m1", winner=True),
        Award(id="a2", name="Oscar", award_type=AwardType.OSCAR,
              year=1973, category="Best Picture", movie_id="m2", winner=True),
    ]
    
    for award in awards:
        db.add_award(award)
    
    return db


# =============================================================================
# USAGE
# =============================================================================

def main():
    """Example usage"""
    
    print("=" * 50)
    print("Movie Database")
    print("=" * 50)
    
    # Create database
    db = create_sample_database()
    
    # Search movies
    print("\n1. Search Movies:")
    results = db.search_movie("Godfather")
    for m in results:
        print(f"   - {m.title} ({m.release_date.year})")
    
    # Movies by genre
    print("\n2. Sci-Fi Movies:")
    scifi = db.get_movies_by_genre("Sci-Fi")
    for m in scifi:
        print(f"   - {m.title}")
    
    # Top rated
    print("\n3. Top Rated:")
    top = db.get_top_rated(5)
    for m in top:
        print(f"   - {m.title}: {m.imdb_rating}")
    
    # Get reviews
    print("\n4. Reviews for Inception:")
    reviews = db.get_movie_reviews("m1")
    for r in reviews:
        print(f"   - {r.title}: {r.rating}/10")
    
    # Awards
    print("\n5. Oscar Winners:")
    for a in db.awards.values():
        print(f"   - {a.award_type.value} {a.year}: {a.category}")
    
    # Export
    print("\n6. Export JSON-LD:")
    jsonld = db.to_jsonld()
    print(f"   Total entities: {len(jsonld['@graph'])}")


if __name__ == "__main__":
    main()


"""
Movie Database Usage:

    # Create database
    db = MovieDatabase()
    
    # Add movie
    movie = Movie(id="m1", title="Inception", ...)
    db.add_movie(movie)
    
    # Add person
    actor = Person(id="p1", name="Leonardo DiCaprio", ...)
    db.add_person(actor)
    
    # Search
    results = db.search_movie("Inception")
    results = db.search_person("Leonardo")
    results = db.get_movies_by_genre("Sci-Fi")
    
    # Export
    print(db.to_jsonld())

References:
    - Schema.org Movie: https://schema.org/Movie
    - Schema.org Person: https://schema.org/Person
    - TMDB API: https://www.themoviedb.org/documentation/api
    - IMDB: https://www.imdb.com/
"""
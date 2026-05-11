"""
Music Database - Streaming & Artists

Music database:
- Artists, Albums, Songs
- Playlists, Streaming
- Concerts, Venues
- Charts, Awards

Reference:
- Spotify: https://developer.spotify.com/
- Discogs: https://www.discogs.com/
- MusicBrainz: https://musicbrainz.org/
- Billboard: https://www.billboard.com/

Data Sources:
- Spotify API (metadata, audio features)
- MusicBrainz (comprehensive music database)
- Discogs (releases, vinyl)
- Billboard (charts)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum


# =============================================================================
# TYPES
# =============================================================================

class MusicGenre(Enum):
    Rock = "Rock"
    Pop = "Pop"
    Hip_Hop = "Hip Hop"
    Electronic = "Electronic"
    Jazz = "Jazz"
    Classical = "Classical"
    Country = "Country"
    R_B = "R&B"
    Metal = "Metal"
    Indie = "Indie"


class AlbumType(Enum):
    Studio = "Studio"
    Live = "Live"
    Compilation = "Compilation"
    EP = "EP"
    Single = "Single"


class MediaType(Enum):
    CD = "CD"
    Vinyl = "Vinyl"
    Digital = "Digital"
    Cassette = "Cassette"


# =============================================================================
# ENTITIES
# =============================================================================

@dataclass
class Artist:
    """Artist"""
    id: str
    name: str
    
    genre: MusicGenre = None
    
    bio: str = ""
    
    origin: str = ""  # City, Country
    
    formed_year: Optional[int] = None
    
    members: List[str] = field(default_factory=list)  # Member IDs
    
    image_url: str = ""
    
    spotify_id: str = ""
    
    monthly_listeners: int = 0
    
    followers: int = 0
    
    popularity: int = 0  # 0-100
    
    # Social
    instagram: str = ""
    twitter: str = ""
    website: str = ""


@dataclass
class Album:
    """Album"""
    id: str
    title: str
    
    artist_id: str
    
    album_type: AlbumType = AlbumType.Studio
    
    release_date: Optional[date] = None
    
    genre: MusicGenre = None
    
    label: str = ""
    
    cover_url: str = ""
    
    tracks: int = 0
    
    duration_minutes: int = 0
    
    popularity: int = 0
    
    spotify_id: str = ""
    
    # Charts
    billboard_peak: int = 0
    weeks_on_chart: int = 0


@dataclass
class Song:
    """Song"""
    id: str
    title: str
    
    artist_id: str
    album_id: str = ""
    
    track_number: int = 0
    
    duration_seconds: int = 0
    
    disc_number: int = 1
    
    explicit: bool = False
    
    isrc: str = ""  # International Standard Recording Code
    
    # Audio features
    tempo: float = 0.0
    key: str = ""
    time_signature: int = 4
    danceability: float = 0.0
    energy: float = 0.0
    
    # Streaming
    stream_count: int = 0
    
    popularity: int = 0


@dataclass
class Playlist:
    """Playlist"""
    id: str
    name: str
    
    owner_id: str
    
    description: str = ""
    
    public: bool = True
    
    collaborative: bool = False
    
    image_url: str = ""
    
    total_duration: int = 0
    
    followers: int = 0
    
    songs: List[str] = field(default_factory=list)


@dataclass
class Concert:
    """Concert"""
    id: str
    
    artist_id: str = ""
    
    name: str = ""
    
    venue: str = ""
    city: str = ""
    country: str = ""
    
    date: Optional[date] = None
    
    doors_open: str = ""
    
    price_min: float = 0.0
    price_max: float = 0.0
    
    sold_out: bool = False
    
    capacity: int = 0
    
    attendance: int = 0


@dataclass
class Chart:
    """Chart"""
    id: str
    name: str
    
    chart_type: str = ""  # Hot 100, Billboard 200
    
    country: str = ""
    
    updated_date: Optional[date] = None
    
    entries: List[Dict] = field(default_factory=list)  # {position, artist, song, weeks}


# =============================================================================
# DATABASE
# =============================================================================

class MusicDatabase:
    """Music database"""
    
    def __init__(self):
        self.artists: Dict[str, Artist] = {}
        self.albums: Dict[str, Album] = {}
        self.songs: Dict[str, Song] = {}
        self.playlists: Dict[str, Playlist] = {}
        self.concerts: Dict[str, Concert] = {}
        self.charts: Dict[str, Chart] = {}
        
        # Indexes
        self.albums_by_artist: Dict[str, List[str]] = {}
        self.songs_by_artist: Dict[str, List[str]] = {}
        self.songs_by_album: Dict[str, List[str]] = {}
    
    # Artists
    def add_artist(self, artist: Artist) -> str:
        self.artists[artist.id] = artist
        return artist.id
    
    def get_artist(self, artist_id: str) -> Optional[Artist]:
        return self.artists.get(artist_id)
    
    def search_artists(
        self,
        query: str = None,
        genre: MusicGenre = None
    ) -> List[Artist]:
        results = list(self.artists.values())
        
        if query:
            q = query.lower()
            results = [
                a for a in results
                if q in a.name.lower()
            ]
        
        if genre:
            results = [a for a in results if a.genre == genre]
        
        return results
    
    def get_top_artists(self, limit: int = 10) -> List[Artist]:
        return sorted(
            self.artists.values(),
            key=lambda a: a.monthly_listeners,
            reverse=True
        )[:limit]
    
    # Albums
    def add_album(self, album: Album) -> str:
        self.albums[album.id] = album
        
        # Index
        if album.artist_id not in self.albums_by_artist:
            self.albums_by_artist[album.artist_id] = []
        self.albums_by_artist[album.artist_id].append(album.id)
        
        return album.id
    
    def get_artist_albums(self, artist_id: str) -> List[Album]:
        album_ids = self.albums_by_artist.get(artist_id, [])
        return sorted(
            [self.albums[aid] for aid in album_ids if aid in self.albums],
            key=lambda a: a.release_date or date(1900, 1, 1),
            reverse=True
        )
    
    def search_albums(
        self,
        query: str = None,
        artist_id: str = None
    ) -> List[Album]:
        results = list(self.albums.values())
        
        if query:
            q = query.lower()
            results = [
                a for a in results
                if q in a.title.lower()
            ]
        
        if artist_id:
            results = [a for a in results if a.artist_id == artist_id]
        
        return results
    
    # Songs
    def add_song(self, song: Song) -> str:
        self.songs[song.id] = song
        
        # Index
        if song.artist_id:
            if song.artist_id not in self.songs_by_artist:
                self.songs_by_artist[song.artist_id] = []
            self.songs_by_artist[song.artist_id].append(song.id)
        
        if song.album_id:
            if song.album_id not in self.songs_by_album:
                self.songs_by_album[song.album_id] = []
            self.songs_by_album[song.album_id].append(song.id)
        
        return song.id
    
    def get_artist_songs(self, artist_id: str) -> List[Song]:
        song_ids = self.songs_by_artist.get(artist_id, [])
        return [self.songs[sid] for sid in song_ids if sid in self.songs]
    
    def get_top_songs(self, limit: int = 10) -> List[Song]:
        return sorted(
            self.songs.values(),
            key=lambda s: s.popularity,
            reverse=True
        )[:limit]
    
    # Playlists
    def add_playlist(self, playlist: Playlist) -> str:
        self.playlists[playlist.id] = playlist
        return playlist.id
    
    def get_playlist(self, playlist_id: str) -> Optional[Playlist]:
        return self.playlists.get(playlist_id)
    
    # Charts
    def add_chart(self, chart: Chart) -> str:
        self.charts[chart.id] = chart
        return chart.id
    
    def get_chart(self, chart_id: str) -> Optional[Chart]:
        return self.charts.get(chart_id)
    
    def get_chart_position(self, chart_id: str, song_id: str) -> Optional[int]:
        chart = self.charts.get(chart_id)
        if not chart:
            return None
        
        for entry in chart.entries:
            if entry.get("song_id") == song_id:
                return entry.get("position")
        
        return None
    
    # Stats
    def stats(self) -> Dict:
        return {
            "artists": len(self.artists),
            "albums": len(self.albums),
            "songs": len(self.songs),
            "playlists": len(self.playlists),
            "concerts": len(self.concerts),
            "charts": len(self.charts)
        }


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 50)
    print("Music Database")
    print("=" * 50)
    
    db = MusicDatabase()
    
    # Add artist
    artist = Artist(
        id="a1",
        name="The Beatles",
        genre=MusicGenre.Rock,
        origin="Liverpool, UK",
        monthly_listeners=50_000_000
    )
    db.add_artist(artist)
    
    print(f"\nArtist: {artist.name}")
    print(f"  Genre: {artist.genre.value}")
    print(f"  Listeners: {artist.monthly_listeners:,}")
    
    # Add album
    album = Album(
        id="alb1",
        title="Abbey Road",
        artist_id="a1",
        release_date=date(1969, 9, 26),
        popularity=95
    )
    db.add_album(album)
    
    print(f"\nAlbum: {album.title}")
    
    # Search
    print(f"\nSearch 'Beatles':")
    artists = db.search_artists("Beatles")
    for a in artists:
        print(f"  {a.name}")
    
    print(f"\nStats:")
    stats = db.stats()
    print(f"  {stats}")


if __name__ == "__main__":
    main()
"""
Software & Media Database - Code, Images, Video

Software and media database:
- SoftwareSourceCode, WebApplication
- ImageObject, VideoObject, AudioObject
- MediaObject

Reference:
- Schema.org SoftwareApplication
- Schema.org MediaObject

Schema.org: SoftwareApplication, SoftwareSourceCode, WebApplication
Schema.org: ImageObject, VideoObject, AudioObject

Data Sources:
- GitHub API
- npm Registry
- Docker Hub
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


class MediaType(Enum):
    Image = "Image"
    Video = "Video"
    Audio = "Audio"
    Software = "Software"


@dataclass
class Software:
    id: str
    name: str
    
    description: str = ""
    
    version: str = ""
    
    programming_language: str = ""
    
    url: str = ""
    
    download_url: str = ""
    
    license: str = ""
    
    stars: int = 0
    
    forks: int = 0
    
    dependencies: int = 0


@dataclass
class Media:
    id: str
    name: str
    
    media_type: MediaType = MediaType.Image
    
    url: str = ""
    
    content_url: str = ""
    
    encoding_format: str = ""  # jpeg, mp4, mp3
    
    width: int = 0
    height: int = 0
    
    duration: str = ""


class SoftwareMediaDatabase:
    def __init__(self):
        self.software: Dict[str, Software] = {}
        self.media: Dict[str, Media] = {}
    
    def add_software(self, s: Software) -> str:
        self.software[s.id] = s
        return s.id
    
    def add_media(self, m: Media) -> str:
        self.media[m.id] = m
        return m.id
    
    def get_popular_software(self, limit: int = 10) -> List[Software]:
        return sorted(self.software.values(), key=lambda s: s.stars, reverse=True)[:limit]
    
    def stats(self) -> Dict:
        return {
            "software": len(self.software),
            "media": len(self.media)
        }


def main():
    db = SoftwareMediaDatabase()
    
    s = Software(id="s1", name="FastAPI", programming_language="Python", stars=60000)
    db.add_software(s)
    
    print(f"Software: {s.name}, Stars: {s.stars:,}")
    print(f"Stats: {db.stats()}")


if __name__ == "__main__":
    main()

"""
This covers the missing important Schema.org types:
- SoftwareSourceCode/App (needed for GitHub/developer)
- ImageObject (needed for visual content)
- VideoObject (for videos)
- AudioObject (for podcasts/audio)
"""
"""
Gaming Database - Games & Players

Gaming database:
- Games, Players
- Tournaments, Scores
- Achievements, Items

Reference:
- Twitch: https://dev.twitch.tv/
- Steam: https://steamcommunity.com/dev

Schema.org: VideoGame, GameServer

Data Sources:
- Steam API
- Twitch API
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum
from base_entity import Entity


class GamePlatform(Enum):
    PC = "PC"
    PlayStation = "PlayStation"
    Xbox = "Xbox"
    Nintendo = "Nintendo"
    Mobile = "Mobile"


@dataclass
class Entity(Entity):
class Game:
    id: str
    name: str
    
    platform: GamePlatform = GamePlatform.PC
    
    genre: str = ""
    
    release_date: str = ""
    
    price: float = 0.0
    
    players: int = 0


@dataclass
class Entity(Entity):
class Player:
    id: str
    gamertag: str
    
    platform: GamePlatform = GamePlatform.PC
    
    level: int = 0
    
    score: int = 0


class GamingDatabase:
    def __init__(self):
        self.games: Dict[str, Game] = {}
        self.players: Dict[str, Player] = {}
    
    def add_game(self, g: Game) -> str:
        self.games[g.id] = g
        return g.id
    
    def stats(self) -> Dict:
        return {"games": len(self.games), "players": len(self.players)}


def main():
    db = GamingDatabase()
    g = Game(id="g1", name="Fortnite", price=0)
    db.add_game(g)
    print(f"Game: {g.name}")
    print(f"Stats: {db.stats()}")


if __name__ == "__main__":
    main()
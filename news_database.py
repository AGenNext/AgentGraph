"""
News Database - Publications & Articles

News database:
- NewsArticles, Press Releases
- Publishers, Journalists
- News Categories
- Fact Checks

Reference:
- News Media: https://news.google.com/
- AP: https://apnews.com/
- Reuters: https://www.reuters.com/

Schema.org: NewsArticle, Article, BlogPosting

Data Sources:
- Google News
- AP News API
- Reuters API
- NewsAPI.org
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from base_entity import Entity


class NewsCategory(Enum):
    Politics = "Politics"
    Business = "Business"
    Technology = "Technology"
    Sports = "Sports"
    Entertainment = "Entertainment"
    Science = "Science"
    Health = "Health"
    World = "World"


@dataclass
class Entity(Entity):
class NewsArticle:
    id: str
    headline: str
    
    category: NewsCategory = NewsCategory.World
    
    source: str = ""
    author: str = ""
    
    url: str = ""
    
    published: Optional[datetime] = None
    
    summary: str = ""
    
    fact_check: bool = False
    
    sentiment: str = ""  # Positive, Negative, Neutral


@dataclass
class Entity(Entity):
class Publisher:
    id: str
    name: str
    
    website: str = ""
    
    bias: str = ""  # Left, Center, Right
    
   trust_score: float = 0.0


@dataclass
class Entity(Entity):
class Journalist:
    id: str
    name: str
    
    outlet: str = ""
    
    beat: str = ""  # Specialty area
    
    followers: int = 0


class NewsDatabase:
    def __init__(self):
        self.articles: Dict[str, NewsArticle] = {}
        self.publishers: Dict[str, Publisher] = {}
        self.journalists: Dict[str, Journalist] = {}
    
    def add_article(self, a: NewsArticle) -> str:
        self.articles[a.id] = a
        return a.id
    
    def search_articles(self, category: NewsCategory = None) -> List[NewsArticle]:
        results = self.articles.values()
        if category:
            results = [a for a in results if a.category == category]
        return sorted(results, key=lambda a: a.published or datetime.min, reverse=True)
    
    def search_by_source(self, source: str) -> List[NewsArticle]:
        return [a for a in self.articles.values() if a.source == source]
    
    def add_publisher(self, p: Publisher) -> str:
        self.publishers[p.id] = p
        return p.id
    
    def get_fact_checked(self) -> List[NewsArticle]:
        return [a for a in self.articles.values() if a.fact_check]
    
    def stats(self) -> Dict:
        return {
            "articles": len(self.articles),
            "publishers": len(self.publishers),
            "fact_checks": len(self.get_fact_checked())
        }


def main():
    db = NewsDatabase()
    
    # Add article
    article = NewsArticle(
        id="a1",
        headline="Tech Giants Report Earnings",
        category=NewsCategory.Business,
        source="Reuters",
        fact_check=True
    )
    db.add_article(article)
    
    print(f"Article: {article.headline}")
    print(f"Category: {article.category.value}")
    print(f"Source: {article.source}")
    print(f"Fact Check: {article.fact_check}")
    print(f"Stats: {db.stats()}")


if __name__ == "__main__":
    main()

"""
News Database covers:
- NewsArticle, Article, BlogPosting
- Publishers and journalists
- Fact checking
- News categories
"""
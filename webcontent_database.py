"""
Web Content Database - Pages & Articles

Web content database:
- WebPages, Articles
- FAQs, HowTos
- Breadcrumbs, Navigation
- Reviews, Ratings

Reference:
- Google Structured Data: https://developers.google.com/search/docs/guides/intro-structured-data
- JSON-LD: https://json-ld.org/

Schema.org: WebPage, Article, FAQPage, HowTo, QAPage, BreadcrumbList

Data Sources:
- Google Search Central (documentation)
- Schema.org full hierarchy
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from base_entity import Entity


class ContentType(Enum):
    Article = "Article"
    NewsArticle = "NewsArticle"
    BlogPosting = "BlogPosting"
    FAQPage = "FAQPage"
    HowTo = "HowTo"
    QAPage = "QAPage"
    WebPage = "WebPage"
    AboutPage = "AboutPage"
    ContactPage = "ContactPage"


@dataclass
class Entity(Entity):
class WebPage:
    id: str
    url: str
    
    title: str = ""
    description: str = ""
    
    content_type: ContentType = ContentType.WebPage
    
    author: str = ""
    published: Optional[datetime] = None
    modified: Optional[datetime] = None
    
    keywords: List[str] = field(default_factory=list)
    
    breadcrumb: List[str] = field(default_factory=list)
    
    speakable: bool = False


@dataclass
class Entity(Entity):
class FAQ:
    id: str
    question: str
    answer: str
    
    page_id: str = ""


@dataclass
class Entity(Entity):
class HowToStep:
    id: str
    step_number: int
    name: str = ""
    text: str = ""
    image: str = ""


@dataclass
class Entity(Entity):
class Review:
    id: str
    
    item_name: str = ""
    
    rating: int = 5  # 1-5
    
    review_body: str = ""
    
    author: str = ""
    
    date: Optional[datetime] = None


@dataclass
class Entity(Entity):
class BreadcrumbItem:
    id: str
    name: str
    url: str
    
    position: int = 0


class WebContentDatabase:
    def __init__(self):
        self.pages: Dict[str, WebPage] = {}
        self.faqs: Dict[str, FAQ] = {}
        self.howtos: Dict[str, List[HowToStep]] = {}
        self.reviews: Dict[str, Review] = {}
        self.breadcrumbs: Dict[str, List[BreadcrumbItem]] = {}
    
    def add_page(self, p: WebPage) -> str:
        self.pages[p.id] = p
        return p.id
    
    def search_pages(self, content_type: ContentType) -> List[WebPage]:
        return [p for p in self.pages.values() if p.content_type == content_type]
    
    def add_faq(self, f: FAQ) -> str:
        self.faqs[f.id] = f
        return f.id
    
    def add_review(self, r: Review) -> str:
        self.reviews[r.id] = r
        return r.id
    
    def get_rating_summary(self) -> Dict:
        if not self.reviews:
            return {"average": 0, "count": 0}
        
        total = sum(r.rating for r in self.reviews.values())
        return {"average": total / len(self.reviews), "count": len(self.reviews)}
    
    def stats(self) -> Dict:
        return {
            "pages": len(self.pages),
            "faqs": len(self.faqs),
            "reviews": len(self.reviews),
            "rating": self.get_rating_summary()
        }


def main():
    db = WebContentDatabase()
    
    # Important types
    page = WebPage(
        id="p1",
        url="https://example.com/faq",
        title="FAQ Page",
        content_type=ContentType.FAQPage
    )
    db.add_page(page)
    
    # FAQ
    faq = FAQ(id="f1", question="What is schema.org?", answer="A vocabulary for structured data")
    db.add_faq(faq)
    
    print(f"Content Type: {page.content_type.value}")
    print(f"FAQ: {faq.question}")
    print(f"Stats: {db.stats()}")


if __name__ == "__main__":
    main()

"""
Web Content Database covers:
- WebPage (most used)
- Article, NewsArticle, BlogPosting
- FAQPage, HowTo, QAPage
- BreadcrumbList
- Review

All the most important Schema.org types for web SEO and structured data.
"""
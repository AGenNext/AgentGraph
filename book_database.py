"""
Book Database - Complete Library System

Books database:
- Books, Authors, Publishers
- Categories, Genres
- ISBN, Reviews
- Library management

Reference:
- Amazon/Goodreads style
- Library systems
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum


# =============================================================================
# TYPES
# =============================================================================

class BookFormat(Enum):
    Hardcover = "Hardcover"
    Paperback = "Paperback"
    Ebook = "Ebook"
    Audiobook = "Audiobook"
    Kindle = "Kindle"


class BookGenre(Enum):
    FICTION = "Fiction"
    NONFICTION = "Non-Fiction"
    MYSTERY = "Mystery"
    SCIFI = "Science Fiction"
    FANTASY = "Fantasy"
    ROMANCE = "Romance"
    THRILLER = "Thriller"
    BIOGRAPHY = "Biography"
    HISTORY = "History"
    SELF_HELP = "Self-Help"
    BUSINESS = "Business"
    SCIENCE = "Science"


class BookStatus(Enum):
    Available = "Available"
    Checked_Out = "Checked Out"
    Reserved = "Reserved"
    Lost = "Lost"


# =============================================================================
# BOOKS
# =============================================================================

@dataclass
class Book:
    """Book"""
    id: str
    title: str
    
    author_ids: List[str] = field(default_factory=list)
    
    isbn: str = ""
    isbn13: str = ""
    
    publisher: str = ""
    publish_date: Optional[date] = None
    
    pages: int = 0
    
    format: BookFormat = BookFormat.Paperback
    
    genres: List[BookGenre] = field(default_factory=list)
    
    description: str = ""
    
    language: str = "English"
    
    goodreads_id: str = ""
    amazon_id: str = ""
    
    rating: float = 0.0
    ratings_count: int = 0
    
    # Pricing
    list_price: float = 0.0
    amazon_price: float = 0.0
    
    # Cover
    cover_url: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "isbn": self.isbn,
            "publisher": self.publisher,
            "genres": [g.value for g in self.genres],
            "rating": self.rating
        }


@dataclass
class Author:
    """Author"""
    id: str
    name: str
    
    bio: str = ""
    
    birth_date: Optional[date] = None
    death_date: Optional[date] = None
    
    birthplace: str = ""
    
    website: str = ""
    
    twitter: str = ""
    
    goodreads_id: str = ""
    
    image_url: str = ""
    
    book_count: int = 0
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "book_count": self.book_count
        }


@dataclass
class Publisher:
    """Publisher"""
    id: str
    name: str
    
    founded: Optional[int] = None
    
    headquarters: str = ""
    
    website: str = ""
    
    description: str = ""
    
    book_count: int = 0


@dataclass
class Review:
    """Book review"""
    id: str
    book_id: str
    user_id: str
    
    rating: int = 5  # 1-5
    
    title: str = ""
    content: str = ""
    
    created_at: datetime = field(default_factory=datetime.now)
    
    helpful_count: int = 0


@dataclass
class User:
    """Library user"""
    id: str
    name: str
    
    email: str = ""
    
    membership_date: date = field(default_factory=date.today)
    
    checked_out: List[str] = field(default_factory=list)  # book IDs
    
    reserved: List[str] = field(default_factory=list)
    
    read_list: List[str] = field(default_factory=list)


@dataclass
class Loan:
    """Book loan"""
    id: str
    book_id: str
    user_id: str
    
    checked_out: date = field(default_factory=date.today)
    due_date: Optional[date] = None
    returned: Optional[date] = None
    
    status: BookStatus = BookStatus.Available


# =============================================================================
# DATABASE
# =============================================================================

class BookDatabase:
    """Book database"""
    
    def __init__(self):
        self.books: Dict[str, Book] = {}
        self.authors: Dict[str, Author] = {}
        self.publishers: Dict[str, Publisher] = {}
        self.reviews: Dict[str, Review] = {}
        self.users: Dict[str, User] = {}
        self.loans: Dict[str, Loan] = {}
    
    # Books
    def add_book(self, book: Book) -> str:
        self.books[book.id] = return book.id
    
    def get_book(self, book_id: str) -> Optional[Book]:
        return self.books.get(book_id)
    
    def search_books(
        self,
        query: str = None,
        genre: BookGenre = None,
        author_id: str = None
    ) -> List[Book]:
        results = list(self.books.values())
        
        if query:
            query_lower = query.lower()
            results = [
                b for b in results
                if query_lower in b.title.lower()
                or query_lower in b.description.lower()
            ]
        
        if genre:
            results = [b for b in results if genre in b.genres]
        
        if author_id:
            results = [b for b in results if author_id in b.author_ids]
        
        return results
    
    def get_books_by_author(self, author_id: str) -> List[Book]:
        return [b for b in self.books.values() if author_id in b.author_ids]
    
    def get_books_by_genre(self, genre: BookGenre) -> List[Book]:
        return [b for b in self.books.values() if genre in b.genres]
    
    def get_top_rated(self, limit: int = 10) -> List[Book]:
        return sorted(
            self.books.values(),
            key=lambda b: b.rating,
            reverse=True
        )[:limit]
    
    # Authors
    def add_author(self, author: Author) -> str:
        self.authors[author.id] = return author.id
    
    def get_author(self, author_id: str) -> Optional[Author]:
        return self.authors.get(author_id)
    
    def search_authors(self, query: str) -> List[Author]:
        query_lower = query.lower()
        return [
            a for a in self.authors.values()
            if query_lower in a.name.lower()
        ]
    
    # Reviews
    def add_review(self, review: Review) -> str:
        self.reviews[review.id] = return review.id
    
    def get_book_reviews(self, book_id: str) -> List[Review]:
        return [r for r in self.reviews.values() if r.book_id == book_id]
    
    # Users
    def add_user(self, user: User) -> str:
        self.users[user.id] = return user.id
    
    def get_user(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)
    
    # Loans
    def checkout(self, book_id: str, user_id: str) -> Optional[Loan]:
        book = self.books.get(book_id)
        user = self.users.get(user_id)
        
        if not book or not user:
            return None
        
        loan = Loan(
            id=f"loan_{book_id}_{user_id}",
            book_id=book_id,
            user_id=user_id
        )
        
        self.loans[loan.id] = loan
        user.checked_out.append(book_id)
        
        return loan
    
    def return_book(self, loan_id: str) -> bool:
        loan = self.loans.get(loan_id)
        if not loan:
            return False
        
        loan.returned = date.today()
        loan.status = BookStatus.Available
        
        user = self.users.get(loan.user_id)
        if user and loan.book_id in user.checked_out:
            user.checked_out.remove(loan.book_id)
        
        return True
    
    def get_user_loans(self, user_id: str) -> List[Loan]:
        return [l for l in self.loans.values() if l.user_id == user_id]
    
    # Statistics
    def stats(self) -> Dict:
        return {
            "total_books": len(self.books),
            "total_authors": len(self.authors),
            "total_reviews": len(self.reviews),
            "total_users": len(self.users),
            "active_loans": len([l for l in self.loans.values() if not l.returned])
        }


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("Book Database")
    print("=" * 50)
    
    db = BookDatabase()
    
    # Add authors
    authors = [
        ("a1", "George Orwell", "English writer, 1903-1950"),
        ("a2", "Jane Austen", "English novelist, 1775-1817"),
        ("a3", " Ernest Hemingway", "American writer, 1899-1961"),
    ]
    
    for aid, name, bio in authors:
        db.add_author(Author(id=aid, name=name, bio=bio))
    
    # Add books
    books = [
        Book(
            id="b1",
            title="1984",
            author_ids=["a1"],
            isbn="978-0451524935",
            publisher="Signet Classic",
            publish_date=date(1961, 1, 1),
            pages=328,
            format=BookFormat.Paperback,
            genres=[BookGenre.FICTION, BookGenre.SCIFI],
            rating=4.7,
            ratings_count=1000,
            description="Dystopian novel"
        ),
        Book(
            id="b2",
            title="Pride and Prejudice",
            author_ids=["a2"],
            isbn="978-0141439518",
            publisher=" Penguin Classics",
            publish_date=date(2002, 1, 1),
            pages=435,
            format=BookFormat.Paperback,
            genres=[BookGenre.FICTION, BookGenre.ROMANCE],
            rating=4.8,
            ratings_count=2000,
            description="Romantic novel"
        ),
    ]
    
    for book in books:
        db.add_book(book)
    
    # Search
    print("\nSearch '1984':")
    results = db.search_books("1984")
    for b in results:
        print(f"  {b.title}")
    
    print("\nTop rated:")
    top = db.get_top_rated()
    for b in top:
        print(f"  {b.title}: {b.rating}")
    
    print(f"\nStats:")
    stats = db.stats()
    print(f"  Books: {stats['total_books']}")
    print(f"  Authors: {stats['total_authors']}")


if __name__ == "__main__":
    main()


"""
Book Database Usage

    db = BookDatabase()
    
    # Add books
    db.add_book(Book(...))
    db.add_author(Author(...))
    
    # Search
    results = db.search_books("1984")
    results = db.get_books_by_genre(BookGenre.SCIFI)
    results = db.get_books_by_author(author_id)
    
    # Reviews
    db.add_review(Review(...))
    reviews = db.get_book_reviews(book_id)
    
    # Loans
    db.checkout(book_id, user_id)
    db.return_book(loan_id)
"""
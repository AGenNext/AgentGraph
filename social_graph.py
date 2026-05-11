"""
Social Graph - Network Analysis

Social graph for:
- Users and relationships
- Follows, friends, connections
- Influence metrics
- Network analysis

Reference:
- Twitter Developer: https://developer.twitter.com/
- Facebook Graph API: https://developers.facebook.com/
- LinkedIn API: https://developer.linkedin.com/

Data Sources:
- Twitter API (social graph, followers)
- Facebook API (friends)
- Instagram API (followers)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Set
from datetime import datetime
from enum import Enum
from collections import defaultdict


# =============================================================================
# RELATIONSHIP TYPES
# =============================================================================

class RelationshipType(Enum):
    """Types of social relationships"""
    FOLLOW = "follow"
    FRIEND = "friend"
    COLLEAGUE = "colleague"
    FAMILY = "family"
    MENTOR = "mentor"
    PARTNER = "partner"


class EdgeDirection(Enum):
    DIRECTED = "directed"
    UNDIRECTED = "undirected"


# =============================================================================
# NODES
# =============================================================================

@dataclass
class UserNode:
    """User node in social graph"""
    id: str
    name: str
    
    username: str = ""
    bio: str = ""
    
    followers_count: int = 0
    following_count: int = 0
    
    posts_count: int = 0
    
    verified: bool = False
    
    created_at: datetime = field(default_factory=datetime.now)
    
    last_active: Optional[datetime] = None
    
    def influence_score(self) -> float:
        """Calculate influence score"""
        return (self.followers_count * 1.0) + (self.posts_count * 0.1)


@dataclass
class PostNode:
    """Post node"""
    id: str
    user_id: str
    
    content: str = ""
    
    likes: int = 0
    shares: int = 0
    comments: int = 0
    
    created_at: datetime = field(default_factory=datetime.now)


# =============================================================================
# EDGES
# =============================================================================

@dataclass
class Relationship:
    """Relationship between users"""
    id: str
    
    from_user: str
    to_user: str
    
    relationship_type: RelationshipType = RelationshipType.FOLLOW
    
    direction: EdgeDirection = EdgeDirection.DIRECTED
    
    created_at: datetime = field(default_factory=datetime.now)
    
    metadata: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# SOCIAL GRAPH
# =============================================================================

class SocialGraph:
    """Social graph"""
    
    def __init__(self):
        # Nodes
        self.users: Dict[str, UserNode] = {}
        self.posts: Dict[str, PostNode] = {}
        
        # Edges
        # adjacency_list[user_id] = {follower_ids}
        self.followers: Dict[str, Set[str]] = defaultdict(set)
        self.following: Dict[str, Set[str]] = defaultdict(set)
        
        # Relationship edges
        self.relationships: Dict[str, Relationship] = {}
        
        # Metrics cached
        self._in_degree_cache: Dict[str, int] = {}
        self._out_degree_cache: Dict[str, int] = {}
    
    # Users
    def add_user(
        self,
        id: str,
        name: str,
        username: str = "",
        bio: str = ""
    ) -> UserNode:
        """Add user"""
        user = UserNode(
            id=id,
            name=name,
            username=username or name.lower().replace(" ", "_"),
            bio=bio
        )
        self.users[id] = user
        return user
    
    def get_user(self, user_id: str) -> Optional[UserNode]:
        """Get user"""
        return self.users.get(user_id)
    
    def remove_user(self, user_id: str) -> bool:
        """Remove user"""
        if user_id not in self.users:
            return False
        
        # Remove from followers/following
        self.followers.pop(user_id, None)
        self.following.pop(user_id, None)
        
        # Remove relationships
        for rel_id in list(self.relationships.keys()):
            rel = self.relationships[rel_id]
            if rel.from_user == user_id or rel.to_user == user_id:
                del self.relationships[rel_id]
        
        # Remove from other sets
        for users in self.followers.values():
            users.discard(user_id)
        for users in self.following.values():
            users.discard(user_id)
        
        del self.users[user_id]
        return True
    
    # Relationships
    def follow(self, from_user: str, to_user: str) -> bool:
        """Follow user"""
        if from_user == to_user:
            return False
        
        if from_user not in self.users or to_user not in self.users:
            return False
        
        self.following[from_user].add(to_user)
        self.followers[to_user].add(from_user)
        
        # Clear caches
        self._in_degree_cache.clear()
        self._out_degree_cache.clear()
        
        return True
    
    def unfollow(self, from_user: str, to_user: str) -> bool:
        """Unfollow user"""
        if to_user in self.following.get(from_user, set()):
            self.following[from_user].remove(to_user)
            self.followers[to_user].remove(from_user)
            return True
        return False
    
    def is_following(self, from_user: str, to_user: str) -> bool:
        """Check if following"""
        return to_user in self.following.get(from_user, set())
    
    def is_follower(self, from_user: str, to_user: str) -> bool:
        """Check if follower"""
        return from_user in self.followers.get(to_user, set())
    
    # Metrics
    def in_degree(self, user_id: str) -> int:
        """Get in-degree (followers)"""
        if user_id in self._in_degree_cache:
            return self._in_degree_cache[user_id]
        
        degree = len(self.followers.get(user_id, set()))
        self._in_degree_cache[user_id] = degree
        return degree
    
    def out_degree(self, user_id: str) -> int:
        """Get out-degree (following)"""
        if user_id in self._out_degree_cache:
            return self._out_degree_cache[user_id]
        
        degree = len(self.following.get(user_id, set()))
        self._out_degree_cache[user_id] = degree
        return degree
    
    def followers_list(self, user_id: str) -> List[UserNode]:
        """Get followers list"""
        follower_ids = self.followers.get(user_id, set())
        return [self.users[fid] for fid in follower_ids if fid in self.users]
    
    def following_list(self, user_id: str) -> List[UserNode]:
        """Get following list"""
        following_ids = self.following.get(user_id, set())
        return [self.users[fid] for fid in following_ids if fid in self.users]
    
    # Network analysis
    def common_followers(self, user1: str, user2: str) -> List[UserNode]:
        """Get mutual followers"""
        set1 = self.followers.get(user1, set())
        set2 = self.followers.get(user2, set())
        
        common = set1 & set2
        return [self.users[uid] for uid in common if uid in self.users]
    
    def common_following(self, user1: str, user2: str) -> List[UserNode]:
        """Get common following"""
        set1 = self.following.get(user1, set())
        set2 = self.following.get(user2, set())
        
        common = set1 & set2
        return [self.users[uid] for uid in common if uid in self.users]
    
    def get_influence_score(self, user_id: str) -> float:
        """Calculate influence score"""
        user = self.users.get(user_id)
        if not user:
            return 0.0
        
        followers = self.in_degree(user_id)
        following = self.out_degree(user_id)
        
        # Influence = followers / following ratio
        if following == 0:
            ratio = followers
        else:
            ratio = followers / following
        
        return user.influence_score() * ratio
    
    def get_top_influencers(self, limit: int = 10) -> List[UserNode]:
        """Get top influencers"""
        scores = []
        
        for user_id in self.users:
            score = self.get_influence_score(user_id)
            scores.append((user_id, score))
        
        scores.sort(key=lambda x: x[1], reverse=True)
        
        return [self.users[uid] for uid, _ in scores[:limit]]
    
    def suggest_follow(self, user_id: str, limit: int = 5) -> List[UserNode]:
        """Suggest users to follow"""
        user_following = self.following.get(user_id, set())
        
        suggestions = defaultdict(int)
        
        # For each person user follows
        for following_id in user_following:
            # Get who they follow
            for second_degree in self.following.get(following_id, set()):
                if second_degree != user_id and second_degree not in user_following:
                    suggestions[second_degree] += 1
        
        # Sort by common connections
        suggestions = sorted(suggestions.items(), key=lambda x: x[1], reverse=True)
        
        return [self.users[uid] for uid, _ in suggestions[:limit] if uid in self.users]
    
    # Statistics
    def total_users(self) -> int:
        return len(self.users)
    
    def total_relationships(self) -> int:
        return sum(len(f) for f in self.following.values())
    
    def avg_followers(self) -> float:
        if not self.users:
            return 0.0
        total = sum(len(f) for f in self.followers.values())
        return total / len(self.users)
    
    # Export
    def to_dict(self) -> Dict:
        return {
            "users": {uid: {
                "name": user.name,
                "username": user.username,
                "followers": self.in_degree(uid),
                "following": self.out_degree(uid)
            } for uid, user in self.users.items()},
            "total_users": self.total_users(),
            "total_relationships": self.total_relationships()
        }


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("Social Graph")
    print("=" * 50)
    
    # Create graph
    graph = SocialGraph()
    
    # Add users
    users = [
        ("u1", "Alice", "alice"),
        ("u2", "Bob", "bob"),
        ("u3", "Charlie", "charlie"),
        ("u4", "Diana", "diana"),
        ("u5", "Eve", "eve"),
    ]
    
    for uid, name, username in users:
        graph.add_user(uid, name, username)
    
    # Create relationships
    # Alice follows everyone
    graph.follow("u1", "u2")
    graph.follow("u1", "u3")
    graph.follow("u1", "u4")
    
    # Bob follows Alice
    graph.follow("u2", "u1")
    
    # Charlie follows everyone
    graph.follow("u3", "u1")
    graph.follow("u3", "u2")
    graph.follow("u3", "u4")
    graph.follow("u3", "u5")
    
    # Diana follows Alice and Bob
    graph.follow("u4", "u1")
    graph.follow("u4", "u2")
    
    # Eve follows Charlie
    graph.follow("u5", "u3")
    
    # Print stats
    print(f"\nStatistics:")
    print(f"  Total users: {graph.total_users()}")
    print(f"  Total relationships: {graph.total_relationships()}")
    print(f"  Avg followers: {graph.avg_followers():.1f}")
    
    # Show relationships
    print(f"\nAlice's followers:")
    followers = graph.followers_list("u1")
    for f in followers:
        print(f"  - {f.name}")
    
    print(f"\nAlice's following:")
    following = graph.following_list("u1")
    for f in following:
        print(f"  - {f.name}")
    
    # Common followers
    print(f"\nCommon followers of Charlie and Diana:")
    common = graph.common_followers("u3", "u4")
    for c in common:
        print(f"  - {c.name}")
    
    # Suggestions
    print(f"\nSuggestions for Alice:")
    suggestions = graph.suggest_follow("u1")
    for s in suggestions:
        print(f"  - {s.name}")
    
    # Top influencers
    print(f"\nTop influencers:")
    top = graph.get_top_influencers()
    for t in top:
        score = graph.get_influence_score(t.id)
        print(f"  - {t.name}: {score:.1f}")


if __name__ == "__main__":
    main()


"""
Social Graph Usage

    # Create graph
    graph = SocialGraph()
    
    # Add users
    graph.add_user("u1", "Alice", "alice")
    graph.add_user("u2", "Bob", "bob")
    
    # Follow
    graph.follow("u1", "u2")
    
    # Check
    graph.is_following("u1", "u2")  # True
    graph.is_follower("u2", "u1")  # True
    
    # Get lists
    followers = graph.followers_list("u1")
    following = graph.following_list("u1")
    
    # Analysis
    graph.common_followers("u1", "u2")
    graph.suggest_follow("u1")
    graph.get_top_influencers()
    graph.get_influence_score("u1")
"""
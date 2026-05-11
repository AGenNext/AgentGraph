"""
Code Repository Database

Version control system:
- Repositories
- Commits, Branches, Tags
- Pull requests
- Code search

Reference:
- GitHub/GitLab style
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import hashlib


# =============================================================================
# TYPES
# =============================================================================

class RepoStatus(Enum):
    Active = "Active"
    Archived = "Archived"
    Private = "Private"


class PRStatus(Enum):
    Open = "Open"
    Merged = "Merged"
    Closed = "Closed"
    Draft = "Draft"


class MergeStrategy(Enum):
    Merge_Commit = "merge_commit"
    Squash = "squash"
    Rebase = "rebase"


# =============================================================================
# ENTITIES
# =============================================================================

@dataclass
class Repository:
    """Repository"""
    id: str
    name: str
    owner: str
    
    description: str = ""
    
    default_branch: str = "main"
    
    status: RepoStatus = RepoStatus.Private
    
    language: str = ""  # Primary language
    
    stars: int = 0
    forks: int = 0
    watchers: int = 0
    
    open_issues: int = 0
    
    created_at: datetime = field(default_factory=datetime.now)
    
    updated_at: datetime = field(default_factory=datetime.now)
    
    license: str = ""
    
    topics: List[str] = field(default_factory=list)
    
    readme: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "owner": self.owner,
            "stars": self.stars,
            "language": self.language
        }


@dataclass
class Commit:
    """Commit"""
    id: str  # SHA
    
    message: str
    
    author: str  # user_id
    author_email: str = ""
    
    committer: str = ""
    
    branch: str = ""
    
    timestamp: datetime = field(default_factory=datetime.now)
    
    parent_ids: List[str] = field(default_factory=list)
    
    diff_size: int = 0
    
    files_changed: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "sha": self.id,
            "message": self.message[:50],
            "author": self.author,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class Branch:
    """Branch"""
    name: str
    repo_id: str
    
    head_commit: str = ""  # commit SHA
    
    is_default: bool = False
    
    is_protected: bool = False
    
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Tag:
    """Tag"""
    name: str
    repo_id: str
    
    commit_id: str
    
    message: str = ""
    
    created_at: datetime = field(default_factory=datetime.now)
    
    tagger: str = ""


@dataclass
class PullRequest:
    """Pull request"""
    id: str
    title: str
    
    repo_id: str
    author: str
    
    source_branch: str
    target_branch: str
    
    status: PRStatus = PRStatus.Open
    
    description: str = ""
    
    created_at: datetime = field(default_factory=datetime.now)
    
    merged_at: Optional[datetime] = None
    
    merge_strategy: MergeStrategy = MergeStrategy.Merge_Commit
    
    reviews: List[Dict] = field(default_factory=list)
    
    comments: int = 0
    
    commits: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status.value,
            "source": self.source_branch,
            "target": self.target_branch
        }


@dataclass
class Release:
    """Release"""
    id: str
    repo_id: str
    
    tag_name: str
    name: str = ""
    
    description: str = ""
    
    created_at: datetime = field(default_factory=datetime.now)
    
    author: str = ""
    
    draft: bool = False
    
    prerelease: bool = False
    
    assets: List[Dict] = field(default_factory=list)


# =============================================================================
# DATABASE
# =============================================================================

class CodeDatabase:
    """Code repository database"""
    
    def __init__(self):
        self.repositories: Dict[str, Repository] = {}
        self.commits: Dict[str, Commit] = {}
        self.branches: Dict[str, Branch] = {}
        self.tags: Dict[str, Tag] = {}
        self.pull_requests: Dict[str, PullRequest] = {}
        self.releases: Dict[str, Release] = {}
        
        # Indexes
        self.commits_by_repo: Dict[str, List[str]] = {}
        self.prs_by_repo: Dict[str, List[str]] = {}
    
    # Repositories
    def create_repo(
        self,
        name: str,
        owner: str,
        description: str = "",
        **kwargs
    ) -> Repository:
        repo = Repository(
            id=f"{owner}/{name}",
            name=name,
            owner=owner,
            description=description,
            **kwargs
        )
        self.repositories[repo.id] = repo
        return repo
    
    def get_repo(self, repo_id: str) -> Optional[Repository]:
        return self.repositories.get(repo_id)
    
    def search_repos(
        self,
        query: str = None,
        language: str = None,
        owner: str = None
    ) -> List[Repository]:
        results = list(self.repositories.values())
        
        if query:
            q = query.lower()
            results = [
                r for r in results
                if q in r.name.lower() or q in r.description.lower()
            ]
        
        if language:
            results = [r for r in results if r.language == language]
        
        if owner:
            results = [r for r in results if r.owner == owner]
        
        return results
    
    def get_user_repos(self, owner: str) -> List[Repository]:
        return [r for r in self.repositories.values() if r.owner == owner]
    
    def get_trending_repos(self, limit: int = 10) -> List[Repository]:
        return sorted(
            self.repositories.values(),
            key=lambda r: r.stars,
            reverse=True
        )[:limit]
    
    # Commits
    def add_commit(
        self,
        repo_id: str,
        message: str,
        author: str,
        parent_ids: List[str] = None,
        **kwargs
    ) -> Commit:
        # Generate SHA
        data = f"{message}{author}{datetime.now().isoformat()}"
        sha = hashlib.sha256(data.encode()).hexdigest()[:7]
        
        commit = Commit(
            id=sha,
            message=message,
            author=author,
            repo_id=repo_id,
            parent_ids=parent_ids or [],
            **kwargs
        )
        
        self.commits[sha] = commit
        
        # Index
        if repo_id not in self.commits_by_repo:
            self.commits_by_repo[repo_id] = []
        self.commits_by_repo[repo_id].append(sha)
        
        return commit
    
    def get_commit(self, sha: str) -> Optional[Commit]:
        return self.commits.get(sha)
    
    def get_repo_commits(
        self,
        repo_id: str,
        limit: int = 10
    ) -> List[Commit]:
        commit_shas = self.commits_by_repo.get(repo_id, [])
        
        commits = [self.commits[sha] for sha in commit_shas if sha in self.commits]
        
        return sorted(commits, key=lambda c: c.timestamp, reverse=True)[:limit]
    
    # Branches
    def create_branch(
        self,
        name: str,
        repo_id: str,
        commit_id: str = None,
        **kwargs
    ) -> Branch:
        branch = Branch(
            name=name,
            repo_id=repo_id,
            head_commit=commit_id or "",
            **kwargs
        )
        
        self.branches[f"{repo_id}/{name}"] = branch
        return branch
    
    def get_branch(self, repo_id: str, name: str) -> Optional[Branch]:
        return self.branches.get(f"{repo_id}/{name}")
    
    def get_repo_branches(self, repo_id: str) -> List[Branch]:
        prefix = f"{repo_id}/"
        return [
            b for key, b in self.branches.items()
            if key.startswith(prefix)
        ]
    
    # Pull requests
    def create_pr(
        self,
        title: str,
        repo_id: str,
        author: str,
        source_branch: str,
        target_branch: str,
        description: str = "",
        **kwargs
    ) -> PullRequest:
        pr = PullRequest(
            id=f"pr_{repo_id}_{source_branch}_{target_branch}",
            title=title,
            repo_id=repo_id,
            author=author,
            source_branch=source_branch,
            target_branch=target_branch,
            description=description,
            **kwargs
        )
        
        self.pull_requests[pr.id] = pr
        
        # Index
        if repo_id not in self.prs_by_repo:
            self.prs_by_repo[repo_id] = []
        self.prs_by_repo[repo_id].append(pr.id)
        
        return pr
    
    def get_pr(self, pr_id: str) -> Optional[PullRequest]:
        return self.pull_requests.get(pr_id)
    
    def get_repo_prs(
        self,
        repo_id: str,
        status: PRStatus = None
    ) -> List[PullRequest]:
        pr_ids = self.prs_by_repo.get(repo_id, [])
        
        prs = [self.prs[pid] for pid in pr_ids if pid in self.prs]
        
        if status:
            prs = [pr for pr in prs if pr.status == status]
        
        return prs
    
    def merge_pr(self, pr_id: str) -> bool:
        pr = self.pull_requests.get(pr_id)
        if not pr:
            return False
        
        pr.status = PRStatus.Merged
        pr.merged_at = datetime.now()
        
        return True
    
    # Releases
    def create_release(
        self,
        repo_id: str,
        tag_name: str,
        name: str = "",
        **kwargs
    ) -> Release:
        release = Release(
            id=f"release_{repo_id}_{tag_name}",
            repo_id=repo_id,
            tag_name=tag_name,
            name=name or tag_name,
            **kwargs
        )
        
        self.releases[release.id] = release
        return release
    
    def get_repo_releases(self, repo_id: str) -> List[Release]:
        return [r for r in self.releases.values() if r.repo_id == repo_id]
    
    # Statistics
    def stats(self) -> Dict:
        return {
            "total_repos": len(self.repositories),
            "total_commits": len(self.commits),
            "total_branches": len(self.branches),
            "total_prs": len(self.pull_requests),
            "total_releases": len(self.releases)
        }


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("Code Repository Database")
    print("=" * 50)
    
    db = CodeDatabase()
    
    # Create repo
    repo = db.create_repo(
        "agent-platform",
        "acme",
        description="AI Agent Platform",
        language="Python",
        stars=100
    )
    print(f"\nRepository: {repo.id}")
    print(f"  Language: {repo.language}")
    print(f"  Stars: {repo.stars}")
    
    # Add commits
    commit1 = db.add_commit(
        repo.id,
        "Initial commit",
        "alice",
        parent_ids=[]
    )
    commit2 = db.add_commit(
        repo.id,
        "Add agent functionality",
        "bob",
        parent_ids=[commit1.id]
    )
    print(f"\nCommits: {len([commit1, commit2])}")
    
    # Create branch
    branch = db.create_branch("feature", repo.id, commit2.id)
    print(f"\nBranch: {branch.name}")
    
    # Create PR
    pr = db.create_pr(
        "Add new feature",
        repo.id,
        "alice",
        "feature",
        "main",
        "Description of changes"
    )
    print(f"\nPR: {pr.title}")
    print(f"  Status: {pr.status.value}")
    
    # Get commits
    commits = db.get_repo_commits(repo.id)
    print(f"\nRepo commits: {len(commits)}")
    
    # Trending
    trending = db.get_trending_repos()
    print(f"\nTrending: {len(trending)} repos")
    
    print(f"\nStats:")
    stats = db.stats()
    print(f"  Repos: {stats['total_repos']}")
    print(f"  Commits: {stats['total_commits']}")


if __name__ == "__main__":
    main()


"""
Code Database Usage

    db = CodeDatabase()
    
    # Repositories
    repo = db.create_repo("name", "owner")
    repos = db.search_repos("query")
    repos = db.get_trending_repos()
    
    # Commits
    commit = db.add_commit(repo_id, "message", "author")
    commits = db.get_repo_commits(repo_id)
    
    # Branches
    branch = db.create_branch("name", repo_id)
    branches = db.get_repo_branches(repo_id)
    
    # Pull requests
    pr = db.create_pr("title", repo_id, "author", "source", "target")
    prs = db.get_repo_prs(repo_id)
    db.merge_pr(pr_id)
    
    # Releases
    release = db.create_release(repo_id, "tag")
    releases = db.get_repo_releases(repo_id)
"""
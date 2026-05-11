"""
Data Store - Stage-by-Stage Data Storage

Store data at every transformation stage:
- Stage storage
- Version snapshots
- Checkpoints
- Rollback support

Reference:
- Data versioning
- DVC-style storage
- Checkpoint patterns
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Callable
from datetime import datetime
from enum import Enum
import json
import hashlib
import secrets


# =============================================================================
# STAGE TYPES
# =============================================================================

class StageType(Enum):
    SOURCE = "source"
    TRANSFORM = "transform"
    VALIDATE = "validate"
    AGGREGATE = "aggregate"
    EXPORT = "export"
    CHECKPOINT = "checkpoint"


class StorageFormat(Enum):
    JSON = "json"
    PARQUET = "parquet"
    CSV = "csv"
    PICKLE = "pickle"
    MEMORY = "memory"


# =============================================================================
# DATA STAGE
# =============================================================================

@dataclass
class DataStage:
    """Single data stage"""
    id: str
    name: str
    
    stage_type: StageType = StageType.TRANSFORM
    
    # Data
    data: List[Dict] = field(default_factory=list)
    
    # Metadata
    row_count: int = 0
    size_bytes: int = 0
    
    # Hash for integrity
    data_hash: str = ""
    
    # Timing
    created_at: datetime = field(default_factory=datetime.now)
    
    # Parent stage
    parent_id: Optional[str] = None
    
    # Tags
    tags: List[str] = field(default_factory=list)
    
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def compute_hash(self) -> str:
        """Compute data hash"""
        if not self.data:
            return ""
        
        # Create hash from data
        data_str = json.dumps(self.data, sort_keys=True, default=str)
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]
    
    def to_dict(self, include_data: bool = False) -> Dict:
        """Export stage"""
        result = {
            "id": self.id,
            "name": self.name,
            "stage_type": self.stage_type.value,
            "row_count": self.row_count,
            "size_bytes": self.size_bytes,
            "data_hash": self.data_hash,
            "created_at": self.created_at.isoformat(),
            "parent_id": self.parent_id,
            "tags": self.tags,
            "metadata": self.metadata
        }
        
        if include_data:
            result["data"] = self.data
        
        return result


# =============================================================================
# DATA STORE
# =============================================================================

class DataStore:
    """Stage-by-stage data store"""
    
    def __init__(self, name: str = "store"):
        self.name = name
        
        # All stages indexed by ID
        self.stages: Dict[str, DataStage] = {}
        
        # Stage sequence (ordered)
        self.sequence: List[str] = []
        
        # Checkpoints
        self.checkpoints: Dict[str, str] = {}  # checkpoint_id -> stage_id
        
        # Latest stage references
        self.latest_by_type: Dict[StageType, str] = {}
        
        # Storage callbacks (for different formats)
        self.storage_handlers: Dict[StorageFormat, Callable] = {}
    
    # Create stage
    def create_stage(
        self,
        name: str,
        data: List[Dict],
        stage_type: StageType = StageType.TRANSFORM,
        parent_id: str = None,
        tags: List[str] = None,
        metadata: Dict = None
    ) -> DataStage:
        """Create and store a new stage"""
        
        # Generate ID
        stage_id = secrets.token_urlsafe(8)
        
        # Compute size and hash
        data_str = json.dumps(data, default=str)
        size_bytes = len(data_str)
        data_hash = hashlib.sha256(data_str.encode()).hexdigest()[:16]
        
        # Create stage
        stage = DataStage(
            id=stage_id,
            name=name,
            stage_type=stage_type,
            data=data,
            row_count=len(data),
            size_bytes=size_bytes,
            data_hash=data_hash,
            parent_id=parent_id,
            tags=tags or [],
            metadata=metadata or {}
        )
        
        # Compute hash if not computed
        if not stage.data_hash:
            stage.data_hash = stage.compute_hash()
        
        # Store
        self.stages[stage_id] = stage
        self.sequence.append(stage_id)
        
        # Update latest
        if stage.stage_type not in self.latest_by_type:
            self.latest_by_type[stage.stage_type] = []
        self.latest_by_type[stage_type] = stage_id
        
        return stage
    
    # Get stage
    def get_stage(self, stage_id: str) -> Optional[DataStage]:
        """Get stage by ID"""
        return self.stages.get(stage_id)
    
    def get_latest(self, stage_type: StageType = None) -> Optional[DataStage]:
        """Get latest stage"""
        if stage_type:
            stage_id = self.latest_by_type.get(stage_type)
        else:
            stage_id = self.sequence[-1] if self.sequence else None
        
        if stage_id:
            return self.stages.get(stage_id)
        return None
    
    # Checkpoints
    def create_checkpoint(
        self,
        checkpoint_name: str,
        stage_id: str = None
    ) -> str:
        """Create checkpoint"""
        
        if not stage_id:
            stage_id = self.sequence[-1] if self.sequence else None
        
        if not stage_id:
            return None
        
        checkpoint_id = secrets.token_urlsafe(8)
        
        self.checkpoints[checkpoint_name] = stage_id
        
        return checkpoint_id
    
    def restore_checkpoint(
        self,
        checkpoint_name: str
    ) -> Optional[DataStage]:
        """Restore from checkpoint"""
        
        stage_id = self.checkpoints.get(checkpoint_name)
        
        if stage_id:
            return self.stages.get(stage_id)
        return None
    
    def list_checkpoints(self) -> List[str]:
        """List checkpoint names"""
        return list(self.checkpoints.keys())
    
    # History
    def get_history(
        self,
        stage_type: StageType = None,
        limit: int = None
    ) -> List[DataStage]:
        """Get stage history"""
        
        if stage_type:
            stages = [
                self.stages[sid]
                for sid in self.sequence
                if sid in self.stages 
                and self.stages[sid].stage_type == stage_type
            ]
        else:
            stages = [
                self.stages[sid]
                for sid in self.sequence
                if sid in self.stages
            ]
        
        if limit:
            stages = stages[-limit:]
        
        return stages
    
    # Compare
    def compare_stages(
        self,
        stage_id1: str,
        stage_id2: str
    ) -> Dict:
        """Compare two stages"""
        
        stage1 = self.stages.get(stage_id1)
        stage2 = self.stages.get(stage_id2)
        
        if not stage1 or not stage2:
            return {"error": "Stage not found"}
        
        return {
            "stage1": {
                "id": stage1.id,
                "name": stage1.name,
                "row_count": stage1.row_count,
                "data_hash": stage1.data_hash
            },
            "stage2": {
                "id": stage2.id,
                "name": stage2.name,
                "row_count": stage2.row_count,
                "data_hash": stage2.data_hash
            },
            "row_count_diff": stage2.row_count - stage1.row_count,
            "hash_match": stage1.data_hash == stage2.data_hash
        }
    
    # Find changes
    def find_changes(
        self,
        from_stage_id: str,
        to_stage_id: str
    ) -> Dict:
        """Find changes between stages"""
        
        from_stage = self.stages.get(from_stage_id)
        to_stage = self.stages.get(to_stage_id)
        
        if not from_stage or not to_stage:
            return {"error": "Stage not found"}
        
        # Simple comparison
        from_ids = set(row.get("id", str(i)) for i, row in enumerate(from_stage.data))
        to_ids = set(row.get("id", str(i)) for i, row in enumerate(to_stage.data))
        
        added = to_ids - from_ids
        removed = from_ids - to_ids
        
        return {
            "added_count": len(added),
            "removed_count": len(removed),
            "net_change": len(to_ids) - len(from_ids)
        }
    
    # Export
    def export_stage(
        self,
        stage_id: str,
        format: StorageFormat = StorageFormat.JSON
    ) -> Any:
        """Export stage in format"""
        
        stage = self.stages.get(stage_id)
        if not stage:
            return None
        
        if format == StorageFormat.JSON:
            return stage.to_dict(include_data=True)
        
        # Other formats would use handlers
        return stage.data
    
    def export_all(
        self,
        format: StorageFormat = StorageFormat.JSON
    ) -> Dict:
        """Export all stages"""
        
        return {
            "name": self.name,
            "stages": [
                self.stages[sid].to_dict()
                for sid in self.sequence
                if sid in self.stages
            ],
            "checkpoints": self.checkpoints,
            "total_stages": len(self.stages),
            "total_rows": sum(s.row_count for s in self.stages.values())
        }
    
    # Statistics
    def stats(self) -> Dict:
        """Get statistics"""
        
        stages_by_type = {}
        for stage in self.stages.values():
            t = stage.stage_type.value
            if t not in stages_by_type:
                stages_by_type[t] = {"count": 0, "rows": 0, "bytes": 0}
            stages_by_type[t]["count"] += 1
            stages_by_type[t]["rows"] += stage.row_count
            stages_by_type[t]["bytes"] += stage.size_bytes
        
        return {
            "total_stages": len(self.stages),
            "total_rows": sum(s.row_count for s in self.stages.values()),
            "total_bytes": sum(s.size_bytes for s in self.stages.values()),
            "stages_by_type": stages_by_type,
            "checkpoints": len(self.checkpoints)
        }


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("Data Store - Stage by Stage")
    print("=" * 50)
    
    store = DataStore("sales_pipeline")
    
    # Stage 1: Raw data
    raw_data = [
        {"id": 1, "name": "Alice", "email": "alice@example.com", "sales": 100},
        {"id": 2, "name": "Bob", "email": "bob@example.com", "sales": 200},
        {"id": 3, "name": "Charlie", "email": None, "sales": 150},
    ]
    
    stage1 = store.create_stage(
        "raw_data",
        raw_data,
        stage_type=StageType.SOURCE,
        tags=["raw", "sales"]
    )
    print(f"\nStage 1: {stage1.name}")
    print(f"  Rows: {stage1.row_count}, Hash: {stage1.data_hash}")
    
    # Stage 2: Remove nulls
    clean_data = [
        r for r in raw_data if r.get("email")
    ]
    
    stage2 = store.create_stage(
        "clean_data",
        clean_data,
        stage_type=StageType.TRANSFORM,
        parent_id=stage1.id,
        tags=["cleaned"]
    )
    print(f"\nStage 2: {stage2.name}")
    print(f"  Rows: {stage2.row_count}, Parent: {stage2.parent_id}")
    
    # Stage 3: Add derived field
    enriched_data = [
        {**r, "sales_capped": min(r["sales"], 200)}
        for r in clean_data
    ]
    
    stage3 = store.create_stage(
        "enriched_data",
        enriched_data,
        stage_type=StageType.TRANSFORM,
        parent_id=stage2.id,
        tags=["enriched"]
    )
    print(f"\nStage 3: {stage3.name}")
    print(f"  Rows: {stage3.row_count}")
    
    # Stage 4: Aggregate
    aggregated = [
        {"total_sales": sum(r["sales"] for r in enriched_data)}
    ]
    
    stage4 = store.create_stage(
        "aggregated",
        aggregated,
        stage_type=StageType.AGGREGATE,
        parent_id=stage3.id,
        tags=["aggregated"]
    )
    print(f"\nStage 4: {stage4.name}")
    print(f"  Rows: {stage4.row_count}")
    
    # Checkpoint
    checkpoint = store.create_checkpoint("before_export", stage4.id)
    print(f"\nCheckpoint created: {checkpoint}")
    
    # Compare stages
    print(f"\nCompare stages 1->3:")
    comparison = store.compare_stages(stage1.id, stage3.id)
    print(f"  Row diff: {comparison['row_count_diff']}")
    print(f"  Hash match: {comparison['hash_match']}")
    
    # History
    print(f"\nHistory:")
    history = store.get_history(limit=5)
    for h in history:
        print(f"  {h.name}: {h.row_count} rows")
    
    # Stats
    print(f"\nStats:")
    stats = store.stats()
    print(f"  Total stages: {stats['total_stages']}")
    print(f"  Total rows: {stats['total_rows']}")
    
    # Export
    print(f"\nExport:")
    export = store.export_all()
    print(f"  Checkpoints: {export['checkpoints']}")


if __name__ == "__main__":
    main()


"""
Data Store Usage

    store = DataStore("pipeline")
    
    # Create stages
    stage1 = store.create_stage("raw", data, StageType.SOURCE)
    stage2 = store.create_stage("clean", data2, StageType.TRANSFORM, stage1.id)
    stage3 = store.create_stage("aggregated", data3, StageType.AGGREGATE, stage2.id)
    
    # Get stages
    stage = store.get_stage(id)
    latest = store.get_latest(StageType.TRANSFORM)
    
    # Checkpoints
    store.create_checkpoint("checkpoint_name")
    store.restore_checkpoint("checkpoint_name")
    
    # Compare
    store.compare_stages(id1, id2)
    
    # History
    store.get_history(limit=10)
    
    # Export
    store.export_all()
"""
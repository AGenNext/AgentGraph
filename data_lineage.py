"""
Data Lineage - Track Data Origin and Transformation

Data lineage for:
- Data sources
- Transformations
- Pipeline tracking
- Audit trail

Reference:
-- Data lineage standards
- Data governance
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Callable
from datetime import datetime
from enum import Enum
import hashlib
import secrets


# =============================================================================
# TYPES
# =============================================================================

class LineageType(Enum):
    SOURCE = "source"
    TRANSFORM = "transform"
    AGGREGATE = "aggregate"
    JOIN = "join"
    FILTER = "filter"
    DERIVE = "derive"


class DataState(Enum):
    CREATED = "created"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    DEPRECATED = "deprecated"


# =============================================================================
# NODES
# =============================================================================

@dataclass
class DataSource:
    """Data source node"""
    id: str
    name: str
    
    source_type: str = ""  # database, api, file, stream
    
    connection: Dict[str, str] = field(default_factory=dict)
    
    schema: Dict[str, str] = field(default_factory=dict)
    
    description: str = ""
    
    owner: str = ""
    
    created_at: datetime = field(default_factory=datetime.now)
    
    def connection_hash(self) -> str:
        """Hash of connection for identification"""
        conn_str = str(sorted(self.connection.items()))
        return hashlib.md5(conn_str.encode()).hexdigest()[:8]


@dataclass
class DataTransform:
    """Data transformation node"""
    id: str
    name: str
    
    transform_type: LineageType = LineageType.TRANSFORM
    
    code: str = ""
    
    input_schema: Dict[str, str] = field(default_factory=dict)
    output_schema: Dict[str, str] = field(default_factory=dict)
    
    description: str = ""
    
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Dataset:
    """Dataset node (result of transformation)"""
    id: str
    name: str
    
    lineage_type: LineageType
    
    state: DataState = DataState.CREATED
    
    row_count: int = 0
    
    size_bytes: int = 0
    
    created_at: datetime = field(default_factory=datetime.now)
    
    updated_at: Optional[datetime] = None
    
    metadata: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# LINEAGE GRAPH
# =============================================================================

class LineageGraph:
    """Data lineage graph"""
    
    def __init__(self):
        # Nodes
        self.sources: Dict[str, DataSource] = {}
        self.transformations: Dict[str, DataTransform] = {}
        self.datasets: Dict[str, Dataset] = {}
        
        # Edges (lineage)
        # upstream[downstream_id] = [upstream_ids]
        self.upstream: Dict[str, List[str]] = {}
        
        # downstream[upstream_id] = [downstream_ids]
        self.downstream: Dict[str, List[str]] = {}
        
        # Runs
        self.runs: Dict[str, Dict] = {}
    
    # Sources
    def add_source(
        self,
        id: str,
        name: str,
        source_type: str = "",
        **kwargs
    ) -> DataSource:
        """Add data source"""
        source = DataSource(
            id=id,
            name=name,
            source_type=source_type,
            **kwargs
        )
        self.sources[id] = source
        return source
    
    def get_source(self, source_id: str) -> Optional[DataSource]:
        """Get source"""
        return self.sources.get(source_id)
    
    # Transformations
    def add_transform(
        self,
        id: str,
        name: str,
        transform_type: LineageType = LineageType.TRANSFORM,
        **kwargs
    ) -> DataTransform:
        """Add transformation"""
        transform = DataTransform(
            id=id,
            name=name,
            transform_type=transform_type,
            **kwargs
        )
        self.transformations[id] = transform
        return transform
    
    def get_transform(self, transform_id: str) -> Optional[DataTransform]:
        """Get transformation"""
        return self.transformations.get(transform_id)
    
    # Datasets
    def add_dataset(
        self,
        id: str,
        name: str,
        lineage_type: LineageType = LineageType.SOURCE,
        **kwargs
    ) -> Dataset:
        """Add dataset"""
        dataset = Dataset(
            id=id,
            name=name,
            lineage_type=lineage_type,
            **kwargs
        )
        self.datasets[id] = dataset
        return dataset
    
    def get_dataset(self, dataset_id: str) -> Optional[Dataset]:
        """Get dataset"""
        return self.datasets.get(dataset_id)
    
    def update_dataset(self, dataset_id: str, **updates) -> bool:
        """Update dataset"""
        dataset = self.datasets.get(dataset_id)
        if not dataset:
            return False
        
        for key, value in updates.items():
            if hasattr(dataset, key):
                setattr(dataset, key, value)
        
        dataset.updated_at = datetime.now()
        return True
    
    # Lineage edges
    def add_lineage(
        self,
        upstream_id: str,
        downstream_id: str
    ) -> bool:
        """Add lineage edge"""
        # Validate both exist
        if (upstream_id not in self.sources and 
            upstream_id not in self.transformations and
            upstream_id not in self.datasets):
            return False
        
        if (downstream_id not in self.transformations and 
            downstream_id not in self.datasets):
            return False
        
        # Add upstream
        if downstream_id not in self.upstream:
            self.upstream[downstream_id] = []
        if upstream_id not in self.upstream[downstream_id]:
            self.upstream[downstream_id].append(upstream_id)
        
        # Add downstream
        if upstream_id not in self.downstream:
            self.downstream[upstream_id] = []
        if downstream_id not in self.downstream[upstream_id]:
            self.downstream[upstream_id].append(downstream_id)
        
        return True
    
    def get_upstream(self, node_id: str) -> List[str]:
        """Get upstream lineage"""
        return self.upstream.get(node_id, [])
    
    def get_downstream(self, node_id: str) -> List[str]:
        """Get downstream lineage"""
        return self.downstream.get(node_id, [])
    
    # Lineage paths
    def trace_upstream(self, start_id: str) -> List[str]:
        """Trace full upstream lineage"""
        visited = set()
        stack = [start_id]
        path = []
        
        while stack:
            node_id = stack.pop()
            
            if node_id in visited:
                continue
            
            visited.add(node_id)
            path.append(node_id)
            
            for upstream in self.get_upstream(node_id):
                if upstream not in visited:
                    stack.append(upstream)
        
        return path
    
    def trace_downstream(self, start_id: str) -> List[str]:
        """Trace full downstream lineage"""
        visited = set()
        stack = [start_id]
        path = []
        
        while stack:
            node_id = stack.pop()
            
            if node_id in visited:
                continue
            
            visited.add(node_id)
            path.append(node_id)
            
            for downstream in self.get_downstream(node_id):
                if downstream not in visited:
                    stack.append(downstream)
        
        return path
    
    # Runs
    def run_transform(
        self,
        transform_id: str,
        input_ids: List[str]
    ) -> Dict:
        """Run transformation"""
        transform = self.transformations.get(transform_id)
        if not transform:
            return {"error": "Transform not found"}
        
        # Create run
        run_id = secrets.token_urlsafe(8)
        
        self.runs[run_id] = {
            "id": run_id,
            "transform_id": transform_id,
            "input_ids": input_ids,
            "started_at": datetime.now(),
            "status": "running"
        }
        
        # Mark datasets as processing
        for iid in input_ids:
            self.update_dataset(iid, state=DataState.PROCESSING)
        
        # Simulate completion
        self.runs[run_id]["completed_at"] = datetime.now()
        self.runs[run_id]["status"] = "completed"
        
        return self.runs[run_id]
    
    def get_run(self, run_id: str) -> Optional[Dict]:
        """Get run"""
        return self.runs.get(run_id)
    
    def get_runs_for_transform(self, transform_id: str) -> List[Dict]:
        """Get all runs for transform"""
        return [
            r for r in self.runs.values()
            if r["transform_id"] == transform_id
        ]
    
    # Visualization
    def to_plantuml(self) -> str:
        """Generate PlantUML for visualization"""
        lines = ["@startuml", "title Data Lineage", ""]
        
        # Sources
        for source in self.sources.values():
            lines.append(f'card "{source.name}" as {source.id} {{}}[Source]")
        
        # Transforms
        for trans in self.transformations.values():
            lines.append(f'card "{trans.name}" as {trans.id} {{}}[Transform]')
        
        # Datasets
        for ds in self.datasets.values():
            lines.append(f'card "{ds.name}" as {ds.id} {{}}[Dataset]')
        
        lines.append("")
        
        # Edges
        for down_id, up_ids in self.upstream.items():
            for up_id in up_ids:
                lines.append(f"{up_id} --> {down_id}")
        
        lines.append("@enduml")
        
        return "\n".join(lines)
    
    def to_dict(self) -> Dict:
        """Export as dict"""
        return {
            "sources": {s.id: s.name for s in self.sources.values()},
            "transformations": {t.id: t.name for t in self.transformations.values()},
            "datasets": {d.id: d.name for d in self.datasets.values()},
            "lineage": {
                "upstream": self.upstream,
                "downstream": self.downstream
            }
        }


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("Data Lineage")
    print("=" * 50)
    
    graph = LineageGraph()
    
    # Add sources
    database = graph.add_source(
        "src1", "Sales Database", "surrealdb",
        connection={"host": "db.example.com", "port": "5432"},
        description="Main sales database"
    )
    
    api = graph.add_source(
        "src2", "Customer API", "rest",
        connection={"url": "https://api.example.com"},
        description="Customer data API"
    )
    
    # Add transformations
    clean = graph.add_transform(
        "t1", "Clean Data",
        transform_type=LineageType.TRANSFORM,
        description="Remove nulls and duplicates"
    )
    
    enrich = graph.add_transform(
        "t2", "Enrich Data",
        transform_type=LineageType.DERIVE,
        description="Add derived fields"
    )
    
    aggregate = graph.add_transform(
        "t3", "Aggregate Metrics",
        transform_type=LineageType.AGGREGATE,
        description="Calculate KPIs"
    )
    
    # Add datasets
    raw = graph.add_dataset("d1", "Raw Sales Data", LineageType.SOURCE)
    cleaned = graph.add_dataset("d2", "Clean Sales Data", LineageType.TRANSFORM)
    enriched = graph.add_dataset("d3", "Enriched Data", LineageType.DERIVE)
    metrics = graph.add_dataset("d4", "Sales Metrics", LineageType.AGGREGATE)
    
    # Add lineage
    graph.add_lineage("src1", "d1")  # Database -> Raw
    graph.add_lineage("d1", "t1")     # Raw -> Clean transform
    graph.add_lineage("t1", "d2")      # Clean transform -> Clean Data
    graph.add_lineage("src2", "t2")    # API -> Enrich transform
    graph.add_lineage("t2", "d3")     # Enrich transform -> Enriched Data
    graph.add_lineage("d2", "t3")     # Clean -> Aggregate transform
    graph.add_lineage("d3", "t3")      # Enriched -> Aggregate transform
    graph.add_lineage("t3", "d4")      # Aggregate transform -> Metrics
    
    # Trace
    print("\nUpstream of Metrics:")
    upstream = graph.trace_upstream("d4")
    for u in upstream:
        print(f"  <- {u}")
    
    print("\nDownstream of Sales Database:")
    downstream = graph.trace_downstream("src1")
    for d in downstream:
        print(f"  -> {d}")
    
    # Run transform
    print("\nRun transformation:")
    run = graph.run_transform("t1", ["d1"])
    print(f"  Run ID: {run['id']}")
    print(f"  Status: {run['status']}")
    
    # Export
    print("\nLineage graph:")
    lineage = graph.to_dict()
    print(f"  Sources: {len(lineage['sources'])}")
    print(f"  Transforms: {len(lineage['transformations'])}")
    print(f"  Datasets: {len(lineage['datasets'])}")


if __name__ == "__main__":
    main()


"""
Lineage Graph Usage

    graph = LineageGraph()
    
    # Add sources
    graph.add_source("src1", "Database", "surrealdb")
    graph.add_source("src2", "API", "rest")
    
    # Add transforms
    graph.add_transform("t1", "Clean")
    graph.add_transform("t2", "Enrich")
    
    # Add datasets
    graph.add_dataset("d1", "Raw")
    graph.add_dataset("d2", "Clean")
    
    # Add lineage
    graph.add_lineage("src1", "d1")
    graph.add_lineage("d1", "t1")
    graph.add_lineage("t1", "d2")
    
    # Trace
    graph.trace_upstream("d2")
    graph.trace_downstream("src1")
    
    # Run
    graph.run_transform("t1", ["d1"])
    
    # Export
    graph.to_dict()
    graph.to_plantuml()
"""

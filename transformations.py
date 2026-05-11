"""
Transformation Types - Complete Data Operations

All data transformation types:
- Schema transformations
- Data quality
- Encoding
- Aggregation
- Time series
- ML preprocessing

Reference:
- ETL pipelines
- Data engineering
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Callable
from datetime import datetime
from enum import Enum
import re


# =============================================================================
# SCHEMA TRANSFORMATIONS
# =============================================================================

class SchemaTransformType(Enum):
    """Schema transformation types"""
    RENAME = "rename"  # Rename columns
    TYPE_CAST = "type_cast"  # Change data type
    DROP = "drop"  # Remove columns
    SELECT = "select"  # Select specific columns
    DUPLICATE = "duplicate"  # Duplicate column with new name
    MERGE = "merge"  # Merge two columns
    SPLIT = "split"  # Split column into multiple
    EXTRACT = "extract"  # Extract substring/regex


class AggregateTransformType(Enum):
    """Aggregation types"""
    SUM = "sum"
    AVG = "avg"
    COUNT = "count"
    MIN = "min"
    MAX = "max"
    DISTINCT_COUNT = "distinct_count"
    GROUP_BY = "group_by"
    WINDOW = "window"
    ROLLING = "rolling"


class FilterTransformType(Enum):
    """Filter types"""
    WHERE = "where"  # SQL-like where
    IS_NULL = "is_null"
    NOT_NULL = "not_null"
    IS_IN = "is_in"
    BETWEEN = "between"
    LIKE = "like"  # Pattern matching
    REGEX = "regex"  # Regex match
    DUPLICATE = "duplicate"  # Remove duplicates


class JoinTransformType(Enum):
    """Join types"""
    INNER = "inner"
    LEFT = "left"
    RIGHT = "right"
    FULL = "full"
    CROSS = "cross"
    ANTI_JOIN = "anti_join"
    SEMI_JOIN = "semi_join"


class EncodingTransformType(Enum):
    """Encoding types"""
    ONE_HOT = "one_hot"  # One-hot encoding
    LABEL = "label"  # Label encoding
    ORDINAL = "ordinal"  # Ordinal encoding
    TARGET = "target"  # Target encoding
    HASH = "hash"  # Feature hashing
    BINNING = "binning"  # Discretization


class DataQualityTransformType(Enum):
    """Data quality types"""
    FILL_NULL = "fill_null"  # Fill null values
    IMPUTE = "impute"  # Imputation
    OUTLIER_DETECT = "outlier_detect"  # Detect outliers
    OUTLIER_REMOVE = "outlier_remove"  # Remove outliers
    STANDARDIZE = "standardize"  # StandardScaler
    NORMALIZE = "normalize"  # MinMax scaling
    DEDUPE = "dedupe"  # Remove duplicates


class TimeSeriesTransformType(Enum):
    """Time series types"""
    LAG = "lag"
    LEAD = "lead"
    DIFF = "diff"
    ROLLING_SUM = "rolling_sum"
    ROLLING_AVG = "rolling_avg"
    EXPANDING = "expanding"
    RESAMPLE = "resample"
    TIME_FILL = "time_fill"


class MLPreprocessingType(Enum):
    """ML preprocessing types"""
    FEATURE_SCALE = "feature_scale"  # Scale features
    FEATURE_SELECT = "feature_select"  # Select features
    PCA = "pca"  # Dimensionality reduction
    SAMPLE = "sample"  # Random sampling
    BALANCE = "balance"  # Class balancing
    ENCODE_CATEGORICAL = "encode_categorical"


# =============================================================================
# TRANSFORMATION DEFINITIONS
# =============================================================================

@dataclass
class Transform:
    """Transformation definition"""
    id: str
    name: str
    
    # Type (one of the enums above)
    transform_type: str
    
    # Configuration
    config: Dict[str, Any] = field(default_factory=dict)
    
    # Input/output
    input_columns: List[str] = field(default_factory=list)
    output_columns: List[str] = field(default_factory=list)
    
    # Description
    description: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.transform_type,
            "config": self.config,
            "input_columns": self.input_columns,
            "output_columns": self.output_columns
        }


@dataclass
class Pipeline:
    """Transformation pipeline"""
    id: str
    name: str
    
    transforms: List[Transform] = field(default_factory=list)
    
    description: str = ""
    
    created_at: datetime = field(default_factory=datetime.now)
    
    def add_transform(self, transform: Transform):
        """Add transformation"""
        self.transforms.append(transform)
    
    def execute(self, data: List[Dict]) -> List[Dict]:
        """Execute pipeline"""
        result = list(data)
        
        for transform in self.transforms:
            result = self._apply_transform(result, transform)
        
        return result
    
    def _apply_transform(self, data: List[Dict], transform: Transform) -> List[Dict]:
        """Apply single transformation"""
        
        if transform.transform_type == SchemaTransformType.RENAME.value:
            return self._rename(data, transform)
        
        elif transform.transform_type == FilterTransformType.WHERE.value:
            return self._where(data, transform)
        
        elif transform.transform_type == FilterTransformType.DUPLICATE.value:
            return self._dedupe(data, transform)
        
        elif transform.transform_type == AggregateTransformType.GROUP_BY.value:
            return self._group_by(data, transform)
        
        return data
    
    def _rename(self, data: List[Dict], transform: Transform) -> List[Dict]:
        """Apply rename"""
        mapping = transform.config.get("mapping", {})
        
        result = []
        for row in data:
            new_row = {}
            for key, value in row.items():
                new_key = mapping.get(key, key)
                new_row[new_key] = value
            result.append(new_row)
        
        return result
    
    def _where(self, data: List[Dict], transform: Transform) -> List[Dict]:
        """Apply where filter"""
        # Simplified: just return all
        return data
    
    def _dedupe(self, data: List[Dict], transform: Transform) -> List[Dict]:
        """Remove duplicates"""
        seen = set()
        result = []
        
        for row in data:
            # Create hashable key
            key = tuple(sorted(row.items()))
            
            if key not in seen:
                seen.add(key)
                result.append(row)
        
        return result
    
    def _group_by(self, data: List[Dict], transform: Transform) -> List[Dict]:
        """Apply group by"""
        # Simplified
        return data
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "transforms": [t.to_dict() for t in self.transforms],
            "transform_count": len(self.transforms)
        }


# =============================================================================
# CATALOG
# =============================================================================

class TransformCatalog:
    """Catalog of all transformation types"""
    
    # Schema transforms
    SCHEMA_TRANSFORMS = {
        "rename_columns": {"type": SchemaTransformType.RENAME, "params": ["mapping"]},
        "cast_type": {"type": SchemaTransformType.TYPE_CAST, "params": ["column", "new_type"]},
        "drop_columns": {"type": SchemaTransformType.DROP, "params": ["columns"]},
        "select_columns": {"type": SchemaTransformType.SELECT, "params": ["columns"]},
    }
    
    # Aggregate transforms
    AGGREGATE_TRANSFORMS = {
        "sum": {"type": AggregateTransformType.SUM, "params": ["columns"]},
        "avg": {"type": AggregateTransformType.AVG, "params": ["columns"]},
        "count": {"type": AggregateTransformType.COUNT, "params": []},
        "group_by": {"type": AggregateTransformType.GROUP_BY, "params": ["group_columns", "agg_columns"]},
        "window": {"type": AggregateTransformType.WINDOW, "params": ["partition_by", "order_by"]},
    }
    
    # Filter transforms
    FILTER_TRANSFORMS = {
        "where": {"type": FilterTransformType.WHERE, "params": ["condition"]},
        "is_null": {"type": FilterTransformType.IS_NULL, "params": ["column"]},
        "not_null": {"type": FilterTransformType.NOT_NULL, "params": ["column"]},
        "is_in": {"type": FilterTransformType.IS_IN, "params": ["column", "values"]},
        "between": {"type": FilterTransformType.BETWEEN, "params": ["column", "min", "max"]},
        "dedupe": {"type": FilterTransformType.DUPLICATE, "params": ["subset"]},
    }
    
    # Join transforms
    JOIN_TRANSFORMS = {
        "inner_join": {"type": JoinTransformType.INNER, "params": ["other", "on"]},
        "left_join": {"type": JoinTransformType.LEFT, "params": ["other", "on"]},
        "right_join": {"type": JoinTransformType.RIGHT, "params": ["other", "on"]},
        "full_join": {"type": JoinTransformType.FULL, "params": ["other", "on"]},
    }
    
    # Encoding transforms
    ENCODING_TRANSFORMS = {
        "one_hot": {"type": EncodingTransformType.ONE_HOT, "params": ["columns"]},
        "label_encode": {"type": EncodingTransformType.LABEL, "params": ["column"]},
        "ordinal_encode": {"type": EncodingTransformType.ORDINAL, "params": ["column", "order"]},
        "target_encode": {"type": EncodingTransformType.TARGET, "params": ["column", "target"]},
        "hash": {"type": EncodingTransformType.HASH, "params": ["columns", "num_features"]},
        "bin": {"type": EncodingTransformType.BINNING, "params": ["column", "bins"]},
    }
    
    # Data quality transforms
    DATA_QUALITY_TRANSFORMS = {
        "fill_null": {"type": DataQualityTransformType.FILL_NULL, "params": ["column", "value"]},
        "impute": {"type": DataQualityTransformType.IMPUTE, "params": ["column", "method"]},
        "outlier_detect": {"type": DataQualityTransformType.OUTLIER_DETECT, "params": ["column", "method"]},
        "standardize": {"type": DataQualityTransformType.STANDARDIZE, "params": ["columns"]},
        "normalize": {"type": DataQualityTransformType.NORMALIZE, "params": ["columns"]},
    }
    
    # Time series transforms
    TIME_SERIES_TRANSFORMS = {
        "lag": {"type": TimeSeriesTransformType.LAG, "params": ["column", "periods"]},
        "lead": {"type": TimeSeriesTransformType.LEAD, "params": ["column", "periods"]},
        "diff": {"type": TimeSeriesTransformType.DIFF, "params": ["column"]},
        "rolling_avg": {"type": TimeSeriesTransformType.ROLLING_AVG, "params": ["column", "window"]},
        "resample": {"type": TimeSeriesTransformType.RESAMPLE, "params": ["column", "freq"]},
    }
    
    # ML preprocessing transforms
    ML_PREPROCESSING_TRANSFORMS = {
        "scale": {"type": MLPreprocessingType.FEATURE_SCALE, "params": ["method"]},
        "feature_select": {"type": MLPreprocessingType.FEATURE_SELECT, "params": ["method"]},
        "pca": {"type": MLPreprocessingType.PCA, "params": ["n_components"]},
        "sample": {"type": MLPreprocessingType.SAMPLE, "params": ["frac"]},
        "balance": {"type": MLPreprocessingType.BALANCE, "params": ["target_column"]},
    }
    
    @classmethod
    def all_transforms(cls) -> Dict[str, Dict]:
        """Get all transforms"""
        all_t = {}
        
        all_t.update(cls.SCHEMA_TRANSFORMS)
        all_t.update(cls.AGGREGATE_TRANSFORMS)
        all_t.update(cls.FILTER_TRANSFORMS)
        all_t.update(cls.JOIN_TRANSFORMS)
        all_t.update(cls.ENCODING_TRANSFORMS)
        all_t.update(cls.DATA_QUALITY_TRANSFORMS)
        all_t.update(cls.TIME_SERIES_TRANSFORMS)
        all_t.update(cls.ML_PREPROCESSING_TRANSFORMS)
        
        return all_t
    
    @classmethod
    def list_categories(cls) -> List[str]:
        """List categories"""
        return [
            "Schema Transforms",
            "Aggregate Transforms",
            "Filter Transforms",
            "Join Transforms",
            "Encoding Transforms",
            "Data Quality Transforms",
            "Time Series Transforms",
            "ML Preprocessing Transforms"
        ]


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("Transformation Types")
    print("=" * 50)
    
    catalog = TransformCatalog()
    
    print("\nCategories:")
    for cat in catalog.list_categories():
        print(f"  - {cat}")
    
    all_t = catalog.all_transforms()
    print(f"\nTotal transforms: {len(all_t)}")
    
    print("\nExamples:")
    print(f"  Schema: {list(catalog.SCHEMA_TRANSFORMS.keys())}")
    print(f"  Filter: {list(catalog.FILTER_TRANSFORMS.keys())}")
    print(f"  Aggregate: {list(catalog.AGGREGATE_TRANSFORMS.keys())}")
    print(f"  Join: {list(catalog.JOIN_TRANSFORMS.keys())}")
    print(f"  Encoding: {list(catalog.ENCODING_TRANSFORMS.keys())}")
    print(f"  Data Quality: {list(catalog.DATA_QUALITY_TRANSFORMS.keys())}")
    print(f"  Time Series: {list(catalog.TIME_SERIES_TRANSFORMS.keys())}")
    print(f"  ML Preprocessing: {list(catalog.ML_PREPROCESSING_TRANSFORMS.keys())}")
    
    # Pipeline example
    print("\nPipeline example:")
    pipeline = Pipeline("p1", "Sales Pipeline")
    
    pipeline.add_transform(Transform(
        "t1", "Filter nulls",
        transform_type="is_null",
        config={"column": "email"}
    ))
    
    pipeline.add_transform(Transform(
        "t2", "Rename",
        transform_type="rename_columns",
        config={"mapping": {"full_name": "name"}}
    ))
    
    pipeline.add_transform(Transform(
        "t3", "Group by",
        transform_type="group_by",
        config={"group_columns": ["region"], "agg_columns": ["sales"]}
    ))
    
    print(f"  Transforms: {len(pipeline.transforms)}")


if __name__ == "__main__":
    main()


"""
Transform Types Usage

    # Get catalog
    catalog = TransformCatalog()
    all_transforms = catalog.all_transforms()
    
    # Get by category
    filters = catalog.FILTER_TRANSFORMS
    aggregates = catalog.AGGREGATE_TRANSFORMS
    
    # Create pipeline
    pipeline = Pipeline("p1", "My Pipeline")
    pipeline.add_transform(Transform("t1", "Name", "where", config={"condition": "..."}))
    
    # Execute
    result = pipeline.execute(data)
"""
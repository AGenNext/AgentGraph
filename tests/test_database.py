"""SurrealDB schema and configuration tests."""

from pathlib import Path


SCHEMA_PATH = Path(__file__).resolve().parents[1] / "surreal" / "schema" / "schemaorg-vocabulary.surql"


class TestSurrealSchema:
    """Test the canonical SurrealDB schema assets."""

    def test_schema_file_exists(self):
        assert SCHEMA_PATH.exists()
        assert SCHEMA_PATH.name == "schemaorg-vocabulary.surql"

    def test_schema_contains_table_definitions(self):
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        assert "DEFINE TABLE schema_term" in schema
        assert schema.count("DEFINE TABLE ") > 5

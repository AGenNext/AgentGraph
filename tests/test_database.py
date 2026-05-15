"""SurrealDB schema and configuration tests."""

from schema_org_orm import (
    count_define_statements,
    get_schema_path,
    load_schema_text,
    schema_exists,
)


class TestSurrealSchema:
    """Test the canonical SurrealDB schema assets."""

    def test_schema_file_exists(self):
        assert schema_exists()
        assert get_schema_path().name == "schema-org-surrealdb.surql"

    def test_schema_contains_table_definitions(self):
        schema = load_schema_text()
        assert "DEFINE TABLE thing" in schema
        assert count_define_statements() > 20

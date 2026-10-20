import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import database


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        database,
        "DATABASE_NAME",
        str(database_path)
    )

    database.create_table()
    return database

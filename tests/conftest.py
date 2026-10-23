"""Shared PostgreSQL test database fixture.

Tests use the dedicated job_tracker_test database, never the development database.
Create that database once and grant job_tracker_app access before running pytest.
"""
import os
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import database


@pytest.fixture
def test_database(monkeypatch):
    # Keep automated tests isolated from the development database.
    monkeypatch.setenv("DB_NAME", "job_tracker_test")

    # Each test starts with a clean applications table in the dedicated test DB.
    with database.get_db() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS applications CASCADE")

    database.create_table()
    return database

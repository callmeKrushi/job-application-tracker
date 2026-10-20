import sqlite3

import database


def test_create_table(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        database,
        "DATABASE_NAME",
        str(database_path)
    )

    database.create_table()

    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name = 'applications'
    """)

    table = cursor.fetchone()

    cursor.execute("""
        PRAGMA index_list(applications)
    """)

    indexes = cursor.fetchall()
    connection.close()

    assert table is not None
    assert any(
        index[1] == "idx_applications_status"
        for index in indexes
    )


def test_add_application(test_database):
    application_id = test_database.add_application(
        "Google",
        "Python Developer",
        "Hyderabad",
        "Full-time",
        "10 LPA",
        "https://example.com/job",
        "Python role",
        "Applied",
        "2026-10-02"
    )

    applications = test_database.get_applications()

    assert application_id == 1
    assert len(applications) == 1

    assert applications[0]["id"] == 1
    assert applications[0]["company"] == "Google"
    assert applications[0]["role"] == "Python Developer"
    assert applications[0]["location"] == "Hyderabad"
    assert applications[0]["job_type"] == "Full-time"
    assert applications[0]["salary"] == "10 LPA"
    assert applications[0]["job_url"] == "https://example.com/job"
    assert applications[0]["notes"] == "Python role"
    assert applications[0]["status"] == "Applied"
    assert applications[0]["date_applied"] == "2026-10-02"


def test_update_application_status(test_database):
    test_database.add_application(
        "Microsoft",
        "Data Analyst",
        "Hyderabad",
        "Full-time",
        "10 LPA",
        "https://example.com/job",
        "Data analyst role",
        "Applied",
        "2026-10-02"
    )

    applications = test_database.get_applications()
    application_id = applications[0]["id"]

    rows_updated = test_database.update_application_status(
        application_id,
        "Interview"
    )

    applications = test_database.get_applications()

    assert rows_updated == 1
    assert applications[0]["status"] == "Interview"


def test_delete_application(test_database):
    test_database.add_application(
        "Google",
        "Python Developer",
        "Hyderabad",
        "Full-time",
        "10 LPA",
        "https://example.com/job",
        "Python developer role",
        "Applied",
        "2026-10-02"
    )

    applications = test_database.get_applications()
    application_id = applications[0]["id"]

    rows_deleted = test_database.delete_application(application_id)

    applications = test_database.get_applications()

    assert rows_deleted == 1
    assert len(applications) == 0


def test_update_application_status_when_id_does_not_exist(
    test_database
):
    rows_updated = test_database.update_application_status(
        999,
        "Interview"
    )

    assert rows_updated == 0


def test_delete_application_when_id_does_not_exist(test_database):
    rows_deleted = test_database.delete_application(999)

    assert rows_deleted == 0


def test_migrate_database(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        database,
        "DATABASE_NAME",
        str(database_path)
    )

    # Create the old schema that needs migration.
    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                role TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)

        cursor.execute("""
            INSERT INTO applications (company, role, status)
            VALUES (?, ?, ?)
        """, ("Google", "Python Developer", "Applied"))

    database.migrate_database()

    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()

        cursor.execute("PRAGMA table_info(applications)")
        columns = cursor.fetchall()

        cursor.execute("SELECT * FROM applications")
        applications = cursor.fetchall()

    column_names = [column[1] for column in columns]

    assert column_names == [
        "id",
        "company",
        "role",
        "location",
        "job_type",
        "salary",
        "job_url",
        "notes",
        "status",
        "date_applied"
    ]

    assert len(applications) == 1
    assert applications[0][1] == "Google"
    assert applications[0][2] == "Python Developer"
    assert applications[0][8] == "Applied"


def test_get_db_rolls_back_on_error(test_database):
    try:
        with test_database.get_db() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO applications (
                    company,
                    role,
                    status,
                    date_applied
                )
                VALUES (?, ?, ?, ?)
            """, (
                "TestCompany",
                "TestRole",
                "Applied",
                "2026-10-11"
            ))

            raise ValueError("Simulated database failure")

    except ValueError as error:
        assert str(error) == "Simulated database failure"

    applications = test_database.get_applications()

    assert len(applications) == 0


def test_get_db_closes_connection_on_error(test_database):
    connection = None

    try:
        with test_database.get_db() as db_connection:
            connection = db_connection

            raise ValueError("Simulated error")

    except ValueError as error:
        assert str(error) == "Simulated error"

    assert connection is not None

    try:
        connection.execute("SELECT 1")
    except sqlite3.ProgrammingError as error:
        assert "closed" in str(error).lower()
    else:
        raise AssertionError("Connection should be closed")



def test_search_applications(test_database):
    test_database.add_application(
        "Google", "Python Developer", "Hyderabad", "Full-time",
        "10 LPA", "https://example.com/google", "Python role",
        "Applied", "2026-10-02"
    )

    test_database.add_application(
        "Microsoft", "Data Analyst", "Bengaluru", "Full-time",
        "12 LPA", "https://example.com/microsoft", "Data role",
        "Applied", "2026-10-03"
    )

    results = test_database.search_applications("Google")

    assert len(results) == 1
    assert results[0]["company"] == "Google"
    assert results[0]["role"] == "Python Developer"



def test_filter_applications(test_database):
    test_database.add_application(
        "Google", "Python Developer", "Hyderabad", "Full-time",
        "10 LPA", "https://example.com/google", "Python role",
        "Applied", "2026-10-02"
    )

    test_database.add_application(
        "Microsoft", "Data Analyst", "Bengaluru", "Full-time",
        "12 LPA", "https://example.com/microsoft", "Data role",
        "Interview", "2026-10-03"
    )

    results = test_database.filter_applications("Interview")

    assert len(results) == 1
    assert results[0]["company"] == "Microsoft"
    assert results[0]["status"] == "Interview"



def test_sort_applications(test_database):
    test_database.add_application(
        "Google", "Python Developer", "Hyderabad", "Full-time",
        "10 LPA", "https://example.com/google", "Python role",
        "Applied", "2026-10-02"
    )

    test_database.add_application(
        "Microsoft", "Data Analyst", "Bengaluru", "Full-time",
        "12 LPA", "https://example.com/microsoft", "Data role",
        "Applied", "2026-10-05"
    )

    test_database.add_application(
        "Amazon", "Backend Developer", "Chennai", "Full-time",
        "11 LPA", "https://example.com/amazon", "Backend role",
        "Applied", "2026-10-03"
    )

    results = test_database.sort_applications("desc")

    assert len(results) == 3
    assert results[0]["company"] == "Microsoft"
    assert results[1]["company"] == "Amazon"
    assert results[2]["company"] == "Google"



def test_search_applications_returns_empty_list_when_no_match(test_database):
    test_database.add_application(
        "Google", "Python Developer", "Hyderabad", "Full-time",
        "10 LPA", "https://example.com/google", "Python role",
        "Applied", "2026-10-02"
    )

    results = test_database.search_applications("NonexistentCompany")

    assert results == []


def test_search_applications_matches_partial_role(test_database):
    test_database.add_application(
        "Google", "Python Developer", "Hyderabad", "Full-time",
        "10 LPA", "https://example.com/google", "Python role",
        "Applied", "2026-10-02"
    )

    results = test_database.search_applications("Python")

    assert len(results) == 1
    assert results[0]["company"] == "Google"


def test_filter_applications_returns_empty_list_when_no_match(test_database):
    test_database.add_application(
        "Google", "Python Developer", "Hyderabad", "Full-time",
        "10 LPA", "https://example.com/google", "Python role",
        "Applied", "2026-10-02"
    )

    results = test_database.filter_applications("Rejected")

    assert results == []


def test_sort_applications_returns_empty_list_when_no_applications(test_database):
    results = test_database.sort_applications("desc")

    assert results == []

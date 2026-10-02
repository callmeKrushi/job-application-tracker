import database


def test_create_table(tmp_path):
    database_path = tmp_path / "test.db"

    database.DATABASE_NAME = str(database_path)

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

    connection.close()

    assert table is not None




def test_add_application(tmp_path):
    database_path = tmp_path / "test.db"

    database.DATABASE_NAME = str(database_path)

    database.create_table()

    application_id = database.add_application(
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

    applications = database.get_applications()

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

  



def test_update_application_status(tmp_path):
    database_path = tmp_path / "test.db"

    database.DATABASE_NAME = str(database_path)

    database.create_table()

    database.add_application(
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

    applications = database.get_applications()

    application_id = applications[0]["id"]

    rows_updated = database.update_application_status(
        application_id,
        "Interview"
    )

    applications = database.get_applications()

    assert rows_updated == 1
    assert applications[0]["status"] == "Interview"



def test_delete_application(tmp_path):
    database_path = tmp_path / "test.db"

    database.DATABASE_NAME = str(database_path)

    database.create_table()

    database.add_application(
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

    applications = database.get_applications()

    application_id = applications[0]["id"]

    rows_deleted = database.delete_application(application_id)

    applications = database.get_applications()

    assert rows_deleted == 1
    assert len(applications) == 0
  



def test_update_application_status_when_id_does_not_exist(tmp_path):
    database_path = tmp_path / "test.db"

    database.DATABASE_NAME = str(database_path)

    database.create_table()

    rows_updated = database.update_application_status(
        999,
        "Interview"
    )

    assert rows_updated == 0



def test_delete_application_when_id_does_not_exist(tmp_path):
    database_path = tmp_path / "test.db"

    database.DATABASE_NAME = str(database_path)

    database.create_table()

    rows_deleted = database.delete_application(999)

    assert rows_deleted == 0






def test_migrate_database(tmp_path):
    database_path = tmp_path / "test.db"

    database.DATABASE_NAME = str(database_path)

    connection = database.get_connection()
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

    connection.commit()
    connection.close()

    database.migrate_database()

    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("PRAGMA table_info(applications)")
    columns = cursor.fetchall()

    cursor.execute("SELECT * FROM applications")
    applications = cursor.fetchall()

    connection.close()

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



import sqlite3
from contextlib import contextmanager


DATABASE_NAME = "applications.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


@contextmanager
def get_db():
    connection = get_connection()

    try:
        yield connection
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def create_table():
    with get_db() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                role TEXT NOT NULL,
                location TEXT,
                job_type TEXT,
                salary TEXT,
                job_url TEXT,
                notes TEXT,
                status TEXT NOT NULL,
                date_applied TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_applications_status
            ON applications(status)
        """)


def add_application(
    company,
    role,
    location,
    job_type,
    salary,
    job_url,
    notes,
    status,
    date_applied
):
    with get_db() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO applications (
                company,
                role,
                location,
                job_type,
                salary,
                job_url,
                notes,
                status,
                date_applied
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            company,
            role,
            location,
            job_type,
            salary,
            job_url,
            notes,
            status,
            date_applied
        ))

        application_id = cursor.lastrowid

    return application_id




def get_applications():
    with get_db() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM applications
            ORDER BY id
        """)

        rows = cursor.fetchall()

    return [row_to_application(row) for row in rows]




def search_applications(search_term):
    with get_db() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM applications
            WHERE company LIKE ?
               OR role LIKE ?
            ORDER BY id
        """, (
            f"%{search_term}%",
            f"%{search_term}%"
        ))

        rows = cursor.fetchall()

    return [row_to_application(row) for row in rows]


def filter_applications(status):
    with get_db() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM applications
            WHERE status = ?
            ORDER BY id
        """, (status,))

        rows = cursor.fetchall()

    return [row_to_application(row) for row in rows]


def sort_applications(order):
    with get_db() as connection:
        cursor = connection.cursor()

        if order == "desc":
            cursor.execute("""
                SELECT *
                FROM applications
                ORDER BY date_applied DESC
            """)
        else:
            cursor.execute("""
                SELECT *
                FROM applications
                ORDER BY date_applied ASC
            """)

        rows = cursor.fetchall()

    return [row_to_application(row) for row in rows]


def update_application_status(application_id, new_status):
    with get_db() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE applications
            SET status = ?
            WHERE id = ?
        """, (new_status, application_id))

        rows_updated = cursor.rowcount

    return rows_updated


def delete_application(application_id):
    with get_db() as connection:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM applications WHERE id = ?",
            (application_id,)
        )

        rows_deleted = cursor.rowcount

    return rows_deleted


def update_application(
    application_id,
    company,
    role,
    location,
    job_type,
    salary,
    job_url,
    notes,
    status
):
    with get_db() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE applications
            SET
                company = ?,
                role = ?,
                location = ?,
                job_type = ?,
                salary = ?,
                job_url = ?,
                notes = ?,
                status = ?
            WHERE id = ?
        """, (
            company,
            role,
            location,
            job_type,
            salary,
            job_url,
            notes,
            status,
            application_id
        ))

        rows_updated = cursor.rowcount

    return rows_updated


def row_to_application(row):
    return {
        "id": row[0],
        "company": row[1],
        "role": row[2],
        "location": row[3],
        "job_type": row[4],
        "salary": row[5],
        "job_url": row[6],
        "notes": row[7],
        "status": row[8],
        "date_applied": row[9]
    }


def show_table_structure():
    with get_db() as connection:
        cursor = connection.cursor()

        cursor.execute("PRAGMA table_info(applications)")

        columns = cursor.fetchall()

    return columns


def migrate_database():
    with get_db() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            ALTER TABLE applications
            RENAME TO applications_old
        """)

        cursor.execute("""
            CREATE TABLE applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                role TEXT NOT NULL,
                location TEXT,
                job_type TEXT,
                salary TEXT,
                job_url TEXT,
                notes TEXT,
                status TEXT NOT NULL,
                date_applied TEXT NOT NULL
            )
        """)

        cursor.execute("""
            INSERT INTO applications (
                id,
                company,
                role,
                status,
                location,
                job_type,
                salary,
                job_url,
                notes,
                date_applied
            )
            SELECT
                id,
                company,
                role,
                status,
                '',
                '',
                '',
                '',
                '',
                DATE('now')
            FROM applications_old
        """)

        cursor.execute("DROP TABLE applications_old")

    print("Database migration completed successfully!")


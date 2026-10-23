
import sqlite3
import database


SQLITE_DATABASE = "applications.db"


def migrate_applications():
    # Step 1: Read records from SQLite without modifying the old database.
    with sqlite3.connect(SQLITE_DATABASE) as sqlite_connection:
        sqlite_connection.row_factory = sqlite3.Row

        rows = sqlite_connection.execute(
            """
            SELECT
                id,
                company,
                role,
                location,
                job_type,
                salary,
                job_url,
                notes,
                status,
                date_applied
            FROM applications
            ORDER BY id
            """
        ).fetchall()

    if not rows:
        print("No SQLite applications found to migrate.")
        return

    print(f"Found {len(rows)} applications in SQLite.")

    # Step 2: Import everything in one PostgreSQL transaction.
    with database.get_db() as pg_connection:
        with pg_connection.cursor() as cursor:

            # Check the expected starting state.
            cursor.execute("SELECT COUNT(*) FROM applications")
            existing_count = cursor.fetchone()[0]

            if existing_count != 1:
                raise RuntimeError(
                    "Migration stopped to avoid importing duplicates. "
                    f"Expected 1 existing PostgreSQL application, "
                    f"but found {existing_count}. "
                    "No records were imported."
                )

            # Step 3: Insert records without their SQLite IDs.
            # PostgreSQL will generate new IDs automatically.
            for row in rows:
                cursor.execute(
                    """
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
                    VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s
                    )
                    """,
                    (
                        row["company"],
                        row["role"],
                        row["location"] or None,
                        row["job_type"] or None,
                        row["salary"] or None,
                        row["job_url"] or None,
                        row["notes"] or None,
                        row["status"],
                        row["date_applied"],
                    ),
                )

    # Step 4: get_db() commits when the transaction succeeds.
    # If an insert fails, it rolls back the transaction.
    print(f"Successfully migrated {len(rows)} applications.")
    print("Your original SQLite database was not modified.")


if __name__ == "__main__":
    try:
        migrate_applications()
    except Exception as error:
        print(f"Migration failed: {error}")
        print("The PostgreSQL transaction was rolled back.")

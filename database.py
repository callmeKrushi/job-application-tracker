import sqlite3

DATABASE_NAME = "applications.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

    print("Applications table created successfully!")


def add_application(company, role, status):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO applications (company, role, status)
        VALUES (?, ?, ?)
    """, (company, role, status))

    connection.commit()
    connection.close()

    print("Application added successfully!")


def get_applications():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM applications")

    applications = cursor.fetchall()

    connection.close()

    return applications


if __name__ == "__main__":
    create_table()

    applications = get_applications()

    for application in applications:
        print(application)
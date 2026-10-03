# Job Application Tracker

A command-line Python application for managing and tracking job and internship applications.

The project is built as a learning project to practice Python, Git, GitHub, SQLite database management, modular programming, input validation, and automated testing.


## Project Evolution

This project is being developed incrementally, with each stage introducing new programming and software-engineering concepts.

### Development Journey

```text
CLI Application
      ↓
Basic CRUD Operations
      ↓
JSON Persistence
      ↓
Modular Architecture
      ↓
Input Validation & Normalization
      ↓
Automated Testing with Pytest
      ↓
Search • Filter • Sort • Edit
      ↓
SQLite Database Integration
      ↓
Database CRUD Layer
      ↓
Database Schema Migration
      ↓
47 Automated Tests Passing
      ↓
Current: SQLite-based CLI Application
```

### What I Learned at Each Stage

1. **CLI Application**
   Built the initial command-line application and learned how to structure the program flow.

2. **CRUD Operations**
   Implemented adding, viewing, updating, and deleting applications.

3. **JSON Persistence**
   Added persistent JSON storage so application data could survive between program executions.

4. **Modular Architecture**
   Separated responsibilities across multiple Python modules to make the project easier to maintain.

5. **Validation & Normalization**
   Added input validation and normalization for application fields such as status, job type, salary, and URLs.

6. **Automated Testing**
   Introduced pytest and built tests to verify application behavior and prevent regressions.

7. **Advanced Features**
   Added searching, filtering, sorting, application editing, and application dates.

8. **SQLite Migration**
   Replaced JSON persistence with SQLite and introduced relational database concepts.

9. **Database Layer**
   Created a dedicated database module for database connections and CRUD operations.

10. **Database Migration**
    Migrated the existing database schema and preserved existing application records.

11. **Current State**
    The project now uses SQLite as its persistence layer with a dedicated database architecture and 47 passing automated tests.


## Features

* Add a new job application
* View all applications
* Update application status
* Delete applications
* Edit existing applications
* Search applications by company or role
* Filter applications by status
* Sort applications by application date
* Persistent SQLite database storage
* Input validation and normalization
* Automated tests using pytest
* Modular project structure

## Application Statuses

The application supports statuses such as:

* Applied
* Interview
* Selected
* Rejected
* Withdrawn

## Application Information

Each application can contain:

* Company name
* Job role
* Location
* Job type
* Salary
* Job URL
* Notes
* Application status
* Application date

## Project Structure

```text
Job Application Tracker/

│
├── app.py
├── application_manager.py
├── database.py
├── applications.db
├── requirements.txt
├── README.md
├── .gitignore
│
└── tests/
    ├── conftest.py
    ├── test_application_manager.py
    ├── test_database.py
    ├── test_date_utils.py
    └── test_validation.py
```

## Technologies Used

* Python 3.11
* SQLite
* pytest
* Git
* GitHub

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/callmeKrushi/job-application-tracker.git
```

### 2. Navigate to the project

```bash
cd job-application-tracker
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python app.py
```

## Run Tests

Run all automated tests with:

```bash
pytest
```

The project currently contains tests for:

* Application creation
* Input normalization
* Application status updates
* Invalid application numbers
* Application deletion
* Application search
* Application filtering
* Application sorting
* Application editing
* Database CRUD operations
* Date utilities
* Input validation

All current tests are passing.

## Database

The project originally used JSON file storage for persistence.

The application has now been migrated to SQLite for database-based persistence.

The SQLite database contains an `applications` table with fields for:

* ID
* Company
* Role
* Location
* Job type
* Salary
* Job URL
* Notes
* Status
* Application date

Database operations are handled separately in `database.py`, keeping database logic separate from application-management logic.

## Git Workflow

This project follows a feature-based Git workflow.

Example:

```text
main

 ├── feature/add-application
 ├── feature/view-applications
 ├── feature/update-status
 ├── feature/delete-application
 ├── feature/search-applications
 ├── feature/sqlite-database
 └── refactor/project-structure
```

Features are developed on separate branches and merged into `main` through Pull Requests.

## Completed Improvements

The project has progressively added:

* Modular project structure
* JSON persistence
* Input validation
* Input normalization
* Application dates
* Application filtering
* Application sorting
* Application editing
* Expanded application fields
* SQLite database integration
* Database CRUD operations
* Database migration
* Automated database testing

## Future Improvements

Planned improvements include:

* PostgreSQL integration
* FastAPI backend
* REST API
* Pydantic data validation
* Web dashboard
* Application analytics
* Authentication
* Deployment
* AI-powered job application insights

## Learning Goals

This project is being developed progressively to practice:

* Python fundamentals
* Functions and modules
* File handling
* Error handling
* Input validation
* Automated testing
* Git
* GitHub
* Branching
* Pull Requests
* Clean project structure
* SQL
* SQLite
* Database design
* CRUD operations
* Backend development
* API development

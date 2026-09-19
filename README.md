# Job Application Tracker

A command-line Python application for managing and tracking job and internship applications.

The project is built as a learning project to practice Python, Git, GitHub, JSON storage, modular programming, and automated testing.

## Features

* Add a new job application
* View all applications
* Update application status
* Delete applications
* Search applications by company or role
* Persistent JSON data storage
* Automated tests using pytest
* Modular project structure

## Application Statuses

The application supports statuses such as:

* Applied
* Interview
* Selected
* Rejected
* Withdrawn

## Project Structure

```text
Job Application Tracker/
│
├── app.py
├── application_manager.py
├── storage.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── applications.json
│
└── tests/
    ├── conftest.py
    ├── test_application_manager.py
    └── test_storage.py
```

## Technologies Used

* Python 3.11
* JSON
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
* Application status updates
* Invalid application numbers
* Application deletion
* Application search
* JSON storage

## Git Workflow

This project follows a feature-based Git workflow.

Example:

```text
main
 │
 ├── feature/add-application
 ├── feature/view-applications
 ├── feature/update-status
 ├── feature/delete-application
 ├── feature/search-applications
 ├── feature/json-storage
 └── refactor/project-structure
```

Features are developed on separate branches and merged into `main` through Pull Requests.

## Future Improvements

Planned improvements include:

* SQLite database
* PostgreSQL integration
* Better input validation
* Application deadlines
* Application notes
* Filtering by status
* Sorting applications
* FastAPI backend
* Web dashboard
* Application analytics
* Authentication
* AI-powered job application insights

## Learning Goals

This project is being developed progressively to practice:

* Python fundamentals
* Functions and modules
* File handling
* JSON
* Error handling
* Automated testing
* Git
* GitHub
* Branching
* Pull Requests
* Clean project structure
* Backend development
* Databases

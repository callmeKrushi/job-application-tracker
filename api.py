
from datetime import date
from typing import Literal

from fastapi import FastAPI, HTTPException, Query, Response
from pydantic import BaseModel, Field, HttpUrl

import database


# --------------------------------------------------
# Application configuration
# --------------------------------------------------

app = FastAPI(
    title="Job Application Tracker API",
    description="REST API for managing job applications",
    version="1.0.0",
)


# --------------------------------------------------
# Allowed values
# --------------------------------------------------

JobType = Literal[
    "Full-time",
    "Part-time",
    "Internship",
    "Contract",
    "Freelance",
    "Temporary",
]

ApplicationStatus = Literal[
    "Applied",
    "Interview",
    "Selected",
    "Rejected",
    "Withdrawn",
]


# --------------------------------------------------
# Request models
# --------------------------------------------------

class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1, max_length=100)
    role: str = Field(min_length=1, max_length=100)

    location: str | None = None
    job_type: JobType | None = None
    salary: str | None = None
    job_url: HttpUrl | None = None
    notes: str | None = None

    status: ApplicationStatus = "Applied"
    date_applied: date = Field(default_factory=date.today)


class ApplicationUpdate(BaseModel):
    # All fields are optional for partial updates.
    company: str | None = Field(default=None, min_length=1, max_length=100)
    role: str | None = Field(default=None, min_length=1, max_length=100)

    location: str | None = None
    job_type: JobType | None = None
    salary: str | None = None
    job_url: HttpUrl | None = None
    notes: str | None = None
    status: ApplicationStatus | None = None


class StatusUpdate(BaseModel):
    status: ApplicationStatus


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def get_application_or_404(application_id: int):
    applications = database.get_applications()

    for application in applications:
        if application["id"] == application_id:
            return application

    raise HTTPException(
        status_code=404,
        detail=f"Application {application_id} not found",
    )


def clean_optional_text(value):
    if value is None:
        return ""

    return value.strip()


def handle_database_error():
    raise HTTPException(
        status_code=500,
        detail="A database operation failed",
    )


# --------------------------------------------------
# Home and health
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to the Job Application Tracker API"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# --------------------------------------------------
# READ: List and retrieve applications
# --------------------------------------------------

@app.get("/applications")
def list_applications(
    search: str | None = Query(default=None, min_length=1),
    status: ApplicationStatus | None = None,
    sort: Literal["asc", "desc"] = "desc",
):
    try:
        if search is not None:
            applications = database.search_applications(search.strip())
        elif status is not None:
            applications = database.filter_applications(status)
        else:
            applications = database.sort_applications(sort)

        # Apply status filtering after searching, if both were supplied.
        if search is not None and status is not None:
            applications = [
                application
                for application in applications
                if application["status"] == status
            ]

        return {
            "count": len(applications),
            "applications": applications,
        }

    except HTTPException:
        raise
    except Exception:
        handle_database_error()


@app.get("/applications/{application_id}")
def get_application(application_id: int):
    try:
        return get_application_or_404(application_id)
    except HTTPException:
        raise
    except Exception:
        handle_database_error()


# --------------------------------------------------
# CREATE: Add an application
# --------------------------------------------------

@app.post("/applications", status_code=201)
def create_application(application: ApplicationCreate):
    company = application.company.strip()
    role = application.role.strip()

    if not company or not role:
        raise HTTPException(
            status_code=422,
            detail="Company and role cannot be blank",
        )

    try:
        application_id = database.add_application(
            company,
            role,
            clean_optional_text(application.location),
            application.job_type or "",
            clean_optional_text(application.salary),
            str(application.job_url) if application.job_url else "",
            clean_optional_text(application.notes),
            application.status,
            application.date_applied.isoformat(),
        )

        return {
            "message": "Application created successfully",
            "id": application_id,
        }

    except Exception:
        handle_database_error()


# --------------------------------------------------
# UPDATE: Edit application details
# --------------------------------------------------

@app.patch("/applications/{application_id}")
def edit_application(
    application_id: int,
    changes: ApplicationUpdate,
):
    try:
        existing = get_application_or_404(application_id)

        updates = changes.model_dump(exclude_unset=True)

        if not updates:
            raise HTTPException(
                status_code=400,
                detail="Provide at least one field to update",
            )

        # Reject explicitly blank company or role values.
        for field in ("company", "role"):
            if field in updates:
                value = updates[field]

                if value is None or not value.strip():
                    raise HTTPException(
                        status_code=422,
                        detail=f"{field} cannot be blank",
                    )

                updates[field] = value.strip()

        # Keep unspecified values unchanged.
        company = updates.get("company", existing["company"])
        role = updates.get("role", existing["role"])
        location = updates.get("location", existing["location"])
        job_type = updates.get("job_type", existing["job_type"])
        salary = updates.get("salary", existing["salary"])
        job_url = updates.get("job_url", existing["job_url"])
        notes = updates.get("notes", existing["notes"])
        status = updates.get("status", existing["status"])

        if "job_url" in updates:
            job_url = (
                str(updates["job_url"])
                if updates["job_url"] is not None
                else ""
            )

        rows_updated = database.update_application(
            application_id,
            company,
            role,
            clean_optional_text(location),
            job_type or "",
            clean_optional_text(salary),
            clean_optional_text(job_url),
            clean_optional_text(notes),
            status,
        )

        if rows_updated == 0:
            raise HTTPException(
                status_code=404,
                detail=f"Application {application_id} not found",
            )

        return {
            "message": "Application updated successfully",
            "application": get_application_or_404(application_id),
        }

    except HTTPException:
        raise
    except Exception:
        handle_database_error()


# --------------------------------------------------
# UPDATE: Change only application status
# --------------------------------------------------

@app.patch("/applications/{application_id}/status")
def update_application_status(
    application_id: int,
    update: StatusUpdate,
):
    try:
        get_application_or_404(application_id)

        rows_updated = database.update_application_status(
            application_id,
            update.status,
        )

        if rows_updated == 0:
            raise HTTPException(
                status_code=404,
                detail=f"Application {application_id} not found",
            )

        return {
            "message": "Application status updated successfully",
            "id": application_id,
            "status": update.status,
        }

    except HTTPException:
        raise
    except Exception:
        handle_database_error()


# --------------------------------------------------
# DELETE: Remove an application
# --------------------------------------------------

@app.delete("/applications/{application_id}", status_code=204)
def delete_application(application_id: int):
    try:
        rows_deleted = database.delete_application(application_id)

        if rows_deleted == 0:
            raise HTTPException(
                status_code=404,
                detail=f"Application {application_id} not found",
            )

        return Response(status_code=204)

    except HTTPException:
        raise
    except Exception:
        handle_database_error()

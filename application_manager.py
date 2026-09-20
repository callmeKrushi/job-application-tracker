from storage import save_applications
from validation import (
    normalize_text,
    validate_text,
    validate_status,
    validate_salary,
    validate_job_type
)
from date_utils import get_current_date


def add_application(applications):
    company = input("Enter company name: ")
    role = input("Enter job role: ")
    location = input("Enter location (optional): ")

    job_type = input("Enter job type (optional): ")

    validated_job_type = validate_job_type(job_type)

    if validated_job_type is None:
        print(
            "Invalid job type. Choose Full-time, Part-time, "
            "Internship, Contract, Freelance, or Temporary."
        )
        return
    
    salary = input("Enter salary (optional): ")

    if not validate_salary(salary):
        print("Invalid salary. Please enter a valid salary.")
        return
    
    job_url = input("Enter job URL (optional): ")
    notes = input("Enter notes (optional): ")
    status = input(
        "Enter application status "
        "(Applied/Interview/Selected/Rejected/Withdrawn): "
    )

    if not validate_text(company):
        print("Company name cannot be empty.")
        return

    if not validate_text(role):
        print("Job role cannot be empty.")
        return

    company = normalize_text(company)
    role = normalize_text(role)

    validated_status = validate_status(status)

    if validated_status is None:
        print("Invalid application status.")
        return

    application = {
        "company": company,
        "role": role,
        "location": location.strip(),
        "job_type": validated_job_type,
        "salary": salary.strip(),
        "job_url": job_url.strip(),
        "notes": notes.strip(),
        "status": validated_status,
        "date_applied": get_current_date()
    }

    applications.append(application)
    save_applications(applications)

    print("Application added successfully!")

def display_application(application, index=None):
    if index is not None:
        print(f"\nApplication {index}")

    print(f"Company: {application['company']}")
    print(f"Role: {application['role']}")
    print(f"Location: {application['location']}")
    print(f"Job Type: {application['job_type']}")
    print(f"Salary: {application['salary']}")
    print(f"Job URL: {application['job_url']}")
    print(f"Notes: {application['notes']}")
    print(f"Status: {application['status']}")
    print(f"Date Applied: {application['date_applied']}")



def view_applications(applications):
    if not applications:
        print("\nNo applications found.")
        return

    print("\n--- Applications ---")

    for index, application in enumerate(applications, start=1):
        display_application(application, index)



def update_status(applications):
    if not applications:
        print("\nNo applications found.")
        return

    view_applications(applications)

    try:
        number = int(input("\nEnter application number: "))

        if number < 1 or number > len(applications):
            print("Invalid application number.")
            return

        new_status = input(
            "Enter new status (Applied/Interview/Selected/Rejected/Withdrawn): "
        )

        applications[number - 1]["status"] = new_status
        save_applications(applications)

        print("Application status updated successfully!")

    except ValueError:
        print("Please enter a valid number.")


def delete_application(applications):
    if not applications:
        print("\nNo applications found.")
        return

    view_applications(applications)

    try:
        number = int(input("\nEnter application number to delete: "))

        if number < 1 or number > len(applications):
            print("Invalid application number.")
            return

        deleted_application = applications.pop(number - 1)
        save_applications(applications)

        print(
            f"Application for {deleted_application['company']} "
            "deleted successfully!"
        )

    except ValueError:
        print("Please enter a valid number.")



def edit_application(applications):
    if not applications:
        print("\nNo applications found.")
        return

    view_applications(applications)

    try:
        number = int(input("\nEnter application number to edit: "))

        if number < 1 or number > len(applications):
            print("Invalid application number.")
            return

        application = applications[number - 1]

        company = input(
            f"Enter new company name [{application['company']}]: "
        ).strip()

        role = input(
            f"Enter new job role [{application['role']}]: "
        ).strip()

        location = input(
            f"Enter new location [{application['location']}]: "
        ).strip()

        job_type = input(
            f"Enter new job type [{application['job_type']}]: "
        ).strip()

        salary = input(
            f"Enter new salary [{application['salary']}]: "
        ).strip()

        job_url = input(
            f"Enter new job URL [{application['job_url']}]: "
        ).strip()

        notes = input(
            f"Enter new notes [{application['notes']}]: "
        ).strip()

        status = input(
            f"Enter new status [{application['status']}]: "
        ).strip()

        # Keep existing values if user presses Enter
        new_company = application["company"]
        new_role = application["role"]
        new_location = application["location"]
        new_job_type = application["job_type"]
        new_salary = application["salary"]
        new_job_url = application["job_url"]
        new_notes = application["notes"]
        new_status = application["status"]

        if company:
            new_company = normalize_text(company)

        if role:
            new_role = normalize_text(role)

        if location:
            new_location = location

        if job_type:
            new_job_type = job_type

        if salary:
            new_salary = salary

        if job_url:
            new_job_url = job_url

        if notes:
            new_notes = notes

        if status:
            validated_status = validate_status(status)

            if validated_status is None:
                print("Invalid application status.")
                return

            new_status = validated_status

        # Apply changes
        application["company"] = new_company
        application["role"] = new_role
        application["location"] = new_location
        application["job_type"] = new_job_type
        application["salary"] = new_salary
        application["job_url"] = new_job_url
        application["notes"] = new_notes
        application["status"] = new_status

        # Date Applied remains unchanged
        save_applications(applications)

        print("Application updated successfully!")

    except ValueError:
        print("Please enter a valid number.")



def search_applications(applications):
    if not applications:
        print("\nNo applications found.")
        return

    search_term = input("Enter company or role to search: ").strip().lower()

    found = False

    print("\n---------------------------------")
    print("      Search Results")
    print("---------------------------------")

    for index, application in enumerate(applications, start=1):
        if (
            search_term in application["company"].lower()
            or search_term in application["role"].lower()
        ):
            display_application(application, index)
            found = True

    if not found:
        print("\nNo matching applications found.")

    print("\n---------------------------------")

    

def filter_applications(applications):
    if not applications:
        print("\nNo applications found.")
        return

    status = input(
        "Enter status to filter "
        "(Applied/Interview/Selected/Rejected/Withdrawn): "
    )

    status = validate_status(status)

    if status is None:
        print("Invalid application status.")
        return

    found = False

    print("\n---------------------------------")
    print("     Filtered Applications")
    print("---------------------------------")

    for index, application in enumerate(applications, start=1):
        if application["status"] == status:
            display_application(application, index)
            found = True

    if not found:
        print(f"\nNo applications with status '{status}' found.")

    print("\n---------------------------------")



def sort_applications(applications):
    if not applications:
        print("\nNo applications found.")
        return

    print("\n1. Newest first")
    print("2. Oldest first")

    choice = input("Enter your choice: ")

    if choice == "1":
        sorted_applications = sorted(
            applications,
            key=lambda application: application["date_applied"],
            reverse=True
        )

    elif choice == "2":
        sorted_applications = sorted(
            applications,
            key=lambda application: application["date_applied"]
        )

    else:
        print("Invalid choice.")
        return

    print("\n---------------------------------")
    print("       Sorted Applications")
    print("---------------------------------")

    for index, application in enumerate(sorted_applications, start=1):
        display_application(application, index)

    print("\n---------------------------------")
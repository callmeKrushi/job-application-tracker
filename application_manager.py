from storage import save_applications
from validation import (
    normalize_text,
    validate_text,
    validate_status
)
from date_utils import get_current_date


def add_application(applications):
    company = input("Enter company name: ")

    if not validate_text(company):
        print("Company name cannot be empty.")
        return

    company = normalize_text(company)

    role = input("Enter job role: ")

    if not validate_text(role):
        print("Job role cannot be empty.")
        return

    role = normalize_text(role)

    status = input(
        "Enter application status (Applied/Interview/Selected/Rejected/Withdrawn): "
    )

    validated_status = validate_status(status)

    if validated_status is None:
        print("Invalid application status.")
        return

    application = {
        "company": company,
        "role": role,
        "status": validated_status,
        "date_applied": get_current_date()
    }

    applications.append(application)
    save_applications(applications)

    print("Application added successfully!")

def view_applications(applications):
    if not applications:
        print("\nNo applications found.")
        return

    print("\n---------------------------------")
    print("         Applications")
    print("---------------------------------")

    for index, application in enumerate(applications, start=1):
        print(f"\n{index}. {application['company']}")
        print(f"   Role: {application['role']}")
        print(f"   Status: {application['status']}")
        print(f"   Date Applied: {application['date_applied']}")

    print("\n---------------------------------")


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


def search_applications(applications):
    if not applications:
        print("\nNo applications found.")
        return

    search_term = input(
        "Enter company name or job role to search: "
    ).lower()

    found = False

    print("\n---------------------------------")
    print("       Search Results")
    print("---------------------------------")

    for index, application in enumerate(applications, start=1):
        company = application["company"].lower()
        role = application["role"].lower()

        if search_term in company or search_term in role:
            print(f"\n{index}. {application['company']}")
            print(f"   Role: {application['role']}")
            print(f"   Status: {application['status']}")

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
            print(f"\n{index}. {application['company']}")
            print(f"   Role: {application['role']}")
            print(f"   Status: {application['status']}")

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
        print(f"\n{index}. {application['company']}")
        print(f"   Role: {application['role']}")
        print(f"   Status: {application['status']}")
        print(f"   Date Applied: {application['date_applied']}")

    print("\n---------------------------------")
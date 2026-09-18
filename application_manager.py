from storage import save_applications


def add_application(applications):
    company = input("Enter company name: ")
    role = input("Enter job role: ")
    status = input("Enter application status: ")

    application = {
        "company": company,
        "role": role,
        "status": status
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
import json

FILE_NAME = "data/applications.json"

def load_applications():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_applications():
    with open(FILE_NAME, "w") as file:
        json.dump(applications, file, indent=4)


applications = load_applications()


def show_menu():
    print("\n=================================")
    print("     JOB APPLICATION TRACKER")
    print("=================================")
    print("1. Add Application")
    print("2. View Applications")
    print("3. Update Status")
    print("4. Delete Application")
    print("5. Search Applications")
    print("6. Exit")


def add_application():
    company = input("Enter company name: ")
    role = input("Enter job role: ")
    status = input("Enter application status: ")

    application = {
        "company": company,
        "role": role,
        "status": status
    }

    applications.append(application)

    save_applications()

    print("Application added successfully!")


def view_applications():
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

def update_status():
    if not applications:
        print("\nNo applications found.")
        return

    view_applications()

    try:
        number = int(input("\nEnter application number: "))

        if number < 1 or number > len(applications):
            print("Invalid application number.")
            return

        new_status = input(
            "Enter new status (Applied/Interview/Selected/Rejected/Withdrawn): "
        )

        applications[number - 1]["status"] = new_status

        save_applications()

        print("Application status updated successfully!")

    except ValueError:
        print("Please enter a valid number.")


def delete_application():
    if not applications:
        print("\nNo applications found.")
        return

    view_applications()

    try:
        number = int(input("\nEnter application number to delete: "))

        if number < 1 or number > len(applications):
            print("Invalid application number.")
            return

        deleted_application = applications.pop(number - 1)

        save_applications()

        print(
            f"Application for {deleted_application['company']} "
            "deleted successfully!"
        )

    except ValueError:
        print("Please enter a valid number.")


def search_applications():
    if not applications:
        print("\nNo applications found.")
        return

    search_term = input("Enter company name or job role to search: ").lower()

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




def main():
    running = True

    while running:
        show_menu()

        choice = input("Enter your choice: ")

        if choice == "1":
            add_application()

        elif choice == "2":
            view_applications()

        elif choice == "3":
            update_status()

        elif choice == "4":
            delete_application()

        elif choice == "5":
            search_applications()

        elif choice == "6":
            print("Thank you for using Job Application Tracker!")
            running = False

        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
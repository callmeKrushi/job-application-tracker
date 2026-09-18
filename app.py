applications = []


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
            print("Update Status selected")

        elif choice == "4":
            print("Delete Application selected")

        elif choice == "5":
            print("Search Applications selected")

        elif choice == "6":
            print("Thank you for using Job Application Tracker!")
            running = False

        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
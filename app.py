from storage import load_applications
from application_manager import (
    add_application,
    view_applications,
    update_status,
    delete_application,
    search_applications,
    filter_applications,
    sort_applications
)


def show_menu():
    print("\n=================================")
    print("     JOB APPLICATION TRACKER")
    print("=================================")
    print("1. Add Application")
    print("2. View Applications")
    print("3. Update Status")
    print("4. Delete Application")
    print("5. Search Applications")
    print("6. Filter Applications")
    print("7. Sort Applications")
    print("8. Exit")


def main():
    applications = load_applications()

    running = True

    while running:
        show_menu()

        choice = input("Enter your choice: ")

        if choice == "1":
            add_application(applications)

        elif choice == "2":
            view_applications(applications)

        elif choice == "3":
            update_status(applications)

        elif choice == "4":
            delete_application(applications)

        elif choice == "5":
            search_applications(applications)

        elif choice == "6":
            filter_applications(applications)

        elif choice == "7":
            sort_applications(applications)

        elif choice == "8":
            print("Thank you for using Job Application Tracker!")
            running = False

        else:
            print("Invalid choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
import database

from application_manager import (
    add_application,
    view_applications,
    update_status,
    delete_application,
    search_applications,
    filter_applications,
    sort_applications,
    edit_application
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
    print("8. Edit Application")
    print("9. Exit")


def main():

    database.create_table()
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
            filter_applications()

        elif choice == "7":
            sort_applications()

        elif choice == "8":
            edit_application()

        elif choice == "9":
            print("Thank you for using Job Application Tracker!")
            running = False

        else:
            print(
                "Invalid choice. "
                "Please enter a number from 1 to 9."
            )


if __name__ == "__main__":
    main()
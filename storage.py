import json

FILE_NAME = "data/applications.json"


def load_applications():
    try:
        with open(FILE_NAME, "r") as file:
            content = file.read().strip()

            if not content:
                return []

            applications = json.loads(content)

            if not isinstance(applications, list):
                print("Error: Applications data must be a list.")
                return []

            return applications

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print("Error: Applications file contains invalid JSON.")
        return []


def save_applications(applications):
    if not isinstance(applications, list):
        print("Error: Applications data must be a list.")
        return

    try:
        with open(FILE_NAME, "w") as file:
            json.dump(applications, file, indent=4)

    except OSError:
        print("Error: Could not save applications.")
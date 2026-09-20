import json

FILE_NAME = "data/applications.json"


def load_applications():
    try:
        with open(FILE_NAME, "r") as file:
            content = file.read().strip()

            if not content:
                return []

            return json.loads(content)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print("Error: Applications file contains invalid JSON.")
        return []


def save_applications(applications):
    with open(FILE_NAME, "w") as file:
        json.dump(applications, file, indent=4)
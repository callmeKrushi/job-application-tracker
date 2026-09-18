import json

FILE_NAME = "data/applications.json"


def load_applications():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_applications(applications):
    with open(FILE_NAME, "w") as file:
        json.dump(applications, file, indent=4)
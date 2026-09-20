VALID_STATUSES = [
    "Applied",
    "Interview",
    "Selected",
    "Rejected",
    "Withdrawn"
]


def normalize_text(value):
    return " ".join(value.strip().split()).title()


def validate_text(value):
    return bool(value.strip())


def validate_status(status):
    status = status.strip()

    for valid_status in VALID_STATUSES:
        if status.lower() == valid_status.lower():
            return valid_status

    return None


def validate_salary(salary):
    salary = salary.strip()

    # Salary is optional
    if not salary:
        return True

    # Salary must contain at least one digit
    if not any(character.isdigit() for character in salary):
        return False

    return True
from validation import validate_salary


def test_validate_salary_with_valid_lpa():
    assert validate_salary("12 LPA") is True


def test_validate_salary_with_valid_monthly_salary():
    assert validate_salary("50000 per month") is True


def test_validate_salary_with_empty_input():
    assert validate_salary("") is True


def test_validate_salary_with_invalid_text():
    assert validate_salary("abcxyz") is False


def test_validate_salary_with_special_characters():
    assert validate_salary("!!!") is False
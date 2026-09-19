from date_utils import get_current_date, validate_date


def test_validate_date():
    assert validate_date("2026-09-19") is True


def test_invalid_date():
    assert validate_date("19-09-2026") is False


def test_invalid_date_value():
    assert validate_date("2026-99-99") is False


def test_get_current_date():
    date = get_current_date()

    assert len(date) == 10
    assert date[4] == "-"
    assert date[7] == "-"
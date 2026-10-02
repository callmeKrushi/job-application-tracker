
import application_manager
import database


def setup_database(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        database,
        "DATABASE_NAME",
        str(database_path)
    )

    database.create_table()


def add_test_application(
    company,
    role,
    location,
    job_type,
    salary,
    job_url,
    notes,
    status,
    date_applied
):
    return database.add_application(
        company,
        role,
        location,
        job_type,
        salary,
        job_url,
        notes,
        status,
        date_applied
    )


def test_add_application(monkeypatch, tmp_path):
    setup_database(tmp_path, monkeypatch)

    inputs = iter([
        "Google",
        "Python Developer",
        "Hyderabad",
        "Full-time",
        "12 LPA",
        "https://example.com",
        "Referral",
        "Applied"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    application_manager.add_application()

    applications = database.get_applications()

    assert len(applications) == 1
    assert applications[0]["company"] == "Google"
    assert applications[0]["role"] == "Python Developer"
    assert applications[0]["location"] == "Hyderabad"
    assert applications[0]["job_type"] == "Full-time"
    assert applications[0]["salary"] == "12 LPA"
    assert applications[0]["job_url"] == "https://example.com"
    assert applications[0]["notes"] == "Referral"
    assert applications[0]["status"] == "Applied"


def test_add_application_normalizes_input(monkeypatch, tmp_path):
    setup_database(tmp_path, monkeypatch)

    inputs = iter([
        "   google   ",
        "   machine    learning   engineer   ",
        "",
        "",
        "",
        "",
        "",
        "   applied   "
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    application_manager.add_application()

    applications = database.get_applications()

    assert applications[0]["company"] == "Google"
    assert applications[0]["role"] == "Machine Learning Engineer"
    assert applications[0]["status"] == "Applied"


def test_update_status(monkeypatch, tmp_path):
    setup_database(tmp_path, monkeypatch)

    add_test_application(
        "Google",
        "Python Developer",
        "Hyderabad",
        "Full-time",
        "12 LPA",
        "https://example.com",
        "Referral",
        "Applied",
        "2026-09-19"
    )

    inputs = iter([
        "1",
        "Interview"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    application_manager.update_status()

    applications = database.get_applications()

    assert applications[0]["status"] == "Interview"


def test_update_status_invalid_number(monkeypatch, tmp_path):
    setup_database(tmp_path, monkeypatch)

    add_test_application(
        "Google",
        "Python Developer",
        "Hyderabad",
        "Full-time",
        "12 LPA",
        "https://example.com",
        "Referral",
        "Applied",
        "2026-09-19"
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "5"
    )

    application_manager.update_status()

    applications = database.get_applications()

    assert applications[0]["status"] == "Applied"


def test_delete_application(monkeypatch, tmp_path):
    setup_database(tmp_path, monkeypatch)

    add_test_application(
        "Google",
        "Python Developer",
        "Hyderabad",
        "Full-time",
        "12 LPA",
        "https://example.com",
        "Referral",
        "Applied",
        "2026-09-19"
    )

    add_test_application(
        "Microsoft",
        "Data Scientist",
        "Bangalore",
        "Full-time",
        "15 LPA",
        "https://microsoft.com/job",
        "Applied through referral",
        "Interview",
        "2026-09-19"
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "1"
    )

    application_manager.delete_application()

    applications = database.get_applications()

    assert len(applications) == 1
    assert applications[0]["company"] == "Microsoft"


def test_delete_application_invalid_number(monkeypatch, tmp_path):
    setup_database(tmp_path, monkeypatch)

    add_test_application(
        "Google",
        "Python Developer",
        "Hyderabad",
        "Full-time",
        "12 LPA",
        "https://example.com",
        "Referral",
        "Applied",
        "2026-09-19"
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "5"
    )

    application_manager.delete_application()

    applications = database.get_applications()

    assert len(applications) == 1
    assert applications[0]["company"] == "Google"


def test_search_applications(monkeypatch, capsys, tmp_path):
    setup_database(tmp_path, monkeypatch)

    add_test_application(
        "Google",
        "Python Developer",
        "Hyderabad",
        "Full-time",
        "12 LPA",
        "https://example.com",
        "Referral",
        "Applied",
        "2026-09-15"
    )

    add_test_application(
        "Microsoft",
        "Data Scientist",
        "Bangalore",
        "Full-time",
        "15 LPA",
        "https://microsoft.com/job",
        "Applied through referral",
        "Interview",
        "2026-09-15"
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "python"
    )

    application_manager.search_applications()

    output = capsys.readouterr().out

    assert "Google" in output
    assert "Python Developer" in output
    assert "Microsoft" not in output


def test_search_no_results(monkeypatch, capsys, tmp_path):
    setup_database(tmp_path, monkeypatch)

    add_test_application(
        "Google",
        "Python Developer",
        "Hyderabad",
        "Full-time",
        "12 LPA",
        "https://example.com",
        "Referral",
        "Applied",
        "2026-09-15"
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "Amazon"
    )

    application_manager.search_applications()

    output = capsys.readouterr().out

    assert "No matching applications found." in output


def test_filter_applications(monkeypatch, capsys, tmp_path):
    setup_database(tmp_path, monkeypatch)

    add_test_application(
        "Google",
        "Python Developer",
        "Hyderabad",
        "Full-time",
        "12 LPA",
        "https://example.com",
        "Referral",
        "Applied",
        "2026-09-15"
    )

    add_test_application(
        "Microsoft",
        "Data Scientist",
        "Bangalore",
        "Full-time",
        "15 LPA",
        "https://microsoft.com/job",
        "Applied through referral",
        "Interview",
        "2026-09-15"
    )

    add_test_application(
        "Amazon",
        "ML Engineer",
        "Hyderabad",
        "Full-time",
        "14 LPA",
        "https://amazon.com/job",
        "Applied online",
        "Applied",
        "2026-09-15"
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "applied"
    )

    application_manager.filter_applications()

    output = capsys.readouterr().out

    assert "Google" in output
    assert "Amazon" in output
    assert "Microsoft" not in output


def test_filter_applications_no_results(
    monkeypatch,
    capsys,
    tmp_path
):
    setup_database(tmp_path, monkeypatch)

    add_test_application(
        "Google",
        "Python Developer",
        "Hyderabad",
        "Full-time",
        "12 LPA",
        "https://example.com",
        "Referral",
        "Applied",
        "2026-09-15"
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "Selected"
    )

    application_manager.filter_applications()

    output = capsys.readouterr().out

    assert "No applications with status 'Selected' found." in output


def test_sort_applications_newest_first(
    monkeypatch,
    capsys,
    tmp_path
):
    setup_database(tmp_path, monkeypatch)

    add_test_application(
        "Google",
        "Python Developer",
        "Hyderabad",
        "Full-time",
        "12 LPA",
        "https://example.com",
        "Referral",
        "Applied",
        "2026-09-10"
    )

    add_test_application(
        "Microsoft",
        "Data Scientist",
        "Bangalore",
        "Full-time",
        "15 LPA",
        "https://microsoft.com/job",
        "Applied through referral",
        "Interview",
        "2026-09-18"
    )

    add_test_application(
        "Amazon",
        "ML Engineer",
        "Hyderabad",
        "Full-time",
        "14 LPA",
        "https://amazon.com/job",
        "Applied online",
        "Applied",
        "2026-09-15"
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "1"
    )

    application_manager.sort_applications()

    output = capsys.readouterr().out

    microsoft_position = output.index("Microsoft")
    amazon_position = output.index("Amazon")
    google_position = output.index("Google")

    assert microsoft_position < amazon_position
    assert amazon_position < google_position


def test_sort_applications_oldest_first(
    monkeypatch,
    capsys,
    tmp_path
):
    setup_database(tmp_path, monkeypatch)

    add_test_application(
        "Google",
        "Python Developer",
        "Hyderabad",
        "Full-time",
        "12 LPA",
        "https://example.com",
        "Referral",
        "Applied",
        "2026-09-10"
    )

    add_test_application(
        "Microsoft",
        "Data Scientist",
        "Bangalore",
        "Full-time",
        "15 LPA",
        "https://microsoft.com/job",
        "Applied through referral",
        "Interview",
        "2026-09-18"
    )

    add_test_application(
        "Amazon",
        "ML Engineer",
        "Hyderabad",
        "Full-time",
        "14 LPA",
        "https://amazon.com/job",
        "Applied online",
        "Applied",
        "2026-09-15"
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "2"
    )

    application_manager.sort_applications()

    output = capsys.readouterr().out

    google_position = output.index("Google")
    amazon_position = output.index("Amazon")
    microsoft_position = output.index("Microsoft")

    assert google_position < amazon_position
    assert amazon_position < microsoft_position


def test_edit_application(monkeypatch, tmp_path):
    setup_database(tmp_path, monkeypatch)

    add_test_application(
        "Google",
        "Software Engineer",
        "Hyderabad",
        "Full-time",
        "12 LPA",
        "https://example.com",
        "Referral",
        "Applied",
        "2026-09-19"
    )

    inputs = iter([
        "1",
        "Microsoft",
        "Data Scientist",
        "Bangalore",
        "Full-time",
        "15 LPA",
        "https://microsoft.com/job",
        "Referred by friend",
        "Interview"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    application_manager.edit_application()

    applications = database.get_applications()

    assert applications[0]["company"] == "Microsoft"
    assert applications[0]["role"] == "Data Scientist"
    assert applications[0]["location"] == "Bangalore"
    assert applications[0]["job_type"] == "Full-time"
    assert applications[0]["salary"] == "15 LPA"
    assert applications[0]["job_url"] == "https://microsoft.com/job"
    assert applications[0]["notes"] == "Referred by friend"
    assert applications[0]["status"] == "Interview"
    assert applications[0]["date_applied"] == "2026-09-19"


def test_edit_application_keep_existing_values(
    monkeypatch,
    tmp_path
):
    setup_database(tmp_path, monkeypatch)

    add_test_application(
        "Google",
        "Software Engineer",
        "Hyderabad",
        "Full-time",
        "12 LPA",
        "https://example.com",
        "Referral",
        "Applied",
        "2026-09-19"
    )

    inputs = iter([
        "1",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        ""
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    application_manager.edit_application()

    applications = database.get_applications()

    assert applications[0]["company"] == "Google"
    assert applications[0]["role"] == "Software Engineer"
    assert applications[0]["location"] == "Hyderabad"
    assert applications[0]["job_type"] == "Full-time"
    assert applications[0]["salary"] == "12 LPA"
    assert applications[0]["job_url"] == "https://example.com"
    assert applications[0]["notes"] == "Referral"
    assert applications[0]["status"] == "Applied"
    assert applications[0]["date_applied"] == "2026-09-19"


def test_edit_application_invalid_status(
    monkeypatch,
    tmp_path
):
    setup_database(tmp_path, monkeypatch)

    add_test_application(
        "Google",
        "Software Engineer",
        "Hyderabad",
        "Full-time",
        "12 LPA",
        "https://example.com",
        "Referral",
        "Applied",
        "2026-09-19"
    )

    inputs = iter([
        "1",
        "Microsoft",
        "Data Scientist",
        "Bangalore",
        "Full-time",
        "15 LPA",
        "https://microsoft.com/job",
        "New notes",
        "RandomStatus"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    application_manager.edit_application()

    applications = database.get_applications()

    assert applications[0]["company"] == "Google"
    assert applications[0]["role"] == "Software Engineer"
    assert applications[0]["location"] == "Hyderabad"
    assert applications[0]["status"] == "Applied"


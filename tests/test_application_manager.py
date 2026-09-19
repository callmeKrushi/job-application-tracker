import application_manager


def test_add_application(monkeypatch, tmp_path):
    applications = []

    inputs = iter([
        "Google",
        "Python Developer",
        "Applied"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    test_file = tmp_path / "applications.json"

    monkeypatch.setattr(
        application_manager,
        "save_applications",
        lambda applications: test_file.write_text(
            str(applications)
        )
    )

    application_manager.add_application(applications)

    assert len(applications) == 1
    assert applications[0]["company"] == "Google"
    assert applications[0]["role"] == "Python Developer"
    assert applications[0]["status"] == "Applied"
    assert "date_applied" in applications[0]


def test_update_status(monkeypatch):
    applications = [
        {
            "company": "Google",
            "role": "Python Developer",
            "status": "Applied",
            "date_applied": "2026-09-19"
        }
    ]

    inputs = iter([
        "1",
        "Interview"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    monkeypatch.setattr(
        "application_manager.save_applications",
        lambda applications: None
    )

    application_manager.update_status(applications)

    assert applications[0]["status"] == "Interview"


def test_update_status_invalid_number(monkeypatch):
    applications = [
        {
            "company": "Google",
            "role": "Python Developer",
            "status": "Applied",
            "date_applied": "2026-09-19"
        }
    ]

    inputs = iter(["5"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    application_manager.update_status(applications)

    assert applications[0]["status"] == "Applied"


def test_delete_application(monkeypatch):
    applications = [
        {
            "company": "Google",
            "role": "Python Developer",
            "status": "Applied",
            "date_applied": "2026-09-19"
        },
        {
            "company": "Microsoft",
            "role": "Data Scientist",
            "status": "Interview",
            "date_applied": "2026-09-19"
        }
    ]

    inputs = iter(["1"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    monkeypatch.setattr(
        "application_manager.save_applications",
        lambda applications: None
    )

    application_manager.delete_application(applications)

    assert len(applications) == 1
    assert applications[0]["company"] == "Microsoft"


def test_delete_application_invalid_number(monkeypatch):
    applications = [
        {
            "company": "Google",
            "role": "Python Developer",
            "status": "Applied",
            "date_applied": "2026-09-19"
        }
    ]

    inputs = iter(["5"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    application_manager.delete_application(applications)

    assert len(applications) == 1


def test_search_applications(monkeypatch, capsys):
    applications = [
        {
            "company": "Google",
            "role": "Python Developer",
            "status": "Applied"
        },
        {
            "company": "Microsoft",
            "role": "Data Scientist",
            "status": "Interview"
        }
    ]

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "python"
    )

    application_manager.search_applications(applications)

    output = capsys.readouterr().out

    assert "Google" in output
    assert "Python Developer" in output



def test_search_no_results(monkeypatch, capsys):
    applications = [
        {
            "company": "Google",
            "role": "Python Developer",
            "status": "Applied"
        }
    ]

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "Amazon"
    )

    application_manager.search_applications(applications)

    output = capsys.readouterr().out

    assert "No matching applications found." in output


def test_add_application_normalizes_input(monkeypatch):
    applications = []

    inputs = iter([
        "   google   ",
        "   machine    learning   engineer   ",
        "   applied   "
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    monkeypatch.setattr(
        "application_manager.save_applications",
        lambda applications: None
    )

    application_manager.add_application(applications)

    assert applications[0]["company"] == "Google"
    assert applications[0]["role"] == "Machine Learning Engineer"
    assert applications[0]["status"] == "Applied"
    assert "date_applied" in applications[0]


def test_filter_applications(monkeypatch, capsys):
    applications = [
        {
            "company": "Google",
            "role": "Python Developer",
            "status": "Applied"
        },
        {
            "company": "Microsoft",
            "role": "Data Scientist",
            "status": "Interview"
        },
        {
            "company": "Amazon",
            "role": "ML Engineer",
            "status": "Applied"
        }
    ]

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "applied"
    )

    application_manager.filter_applications(applications)

    output = capsys.readouterr().out

    assert "Google" in output
    assert "Amazon" in output
    assert "Microsoft" not in output


def test_filter_applications_no_results(monkeypatch, capsys):
    applications = [
        {
            "company": "Google",
            "role": "Python Developer",
            "status": "Applied"
        }
    ]

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "Selected"
    )

    application_manager.filter_applications(applications)

    output = capsys.readouterr().out

    assert "No applications with status 'Selected' found." in output

def test_sort_applications_newest_first(monkeypatch, capsys):
    applications = [
        {
            "company": "Google",
            "role": "Python Developer",
            "status": "Applied",
            "date_applied": "2026-09-10"
        },
        {
            "company": "Microsoft",
            "role": "Data Scientist",
            "status": "Interview",
            "date_applied": "2026-09-18"
        },
        {
            "company": "Amazon",
            "role": "ML Engineer",
            "status": "Applied",
            "date_applied": "2026-09-15"
        }
    ]

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "1"
    )

    application_manager.sort_applications(applications)

    output = capsys.readouterr().out

    microsoft_position = output.index("Microsoft")
    amazon_position = output.index("Amazon")
    google_position = output.index("Google")

    assert microsoft_position < amazon_position
    assert amazon_position < google_position

def test_sort_applications_oldest_first(monkeypatch, capsys):
    applications = [
        {
            "company": "Google",
            "role": "Python Developer",
            "status": "Applied",
            "date_applied": "2026-09-10"
        },
        {
            "company": "Microsoft",
            "role": "Data Scientist",
            "status": "Interview",
            "date_applied": "2026-09-18"
        },
        {
            "company": "Amazon",
            "role": "ML Engineer",
            "status": "Applied",
            "date_applied": "2026-09-15"
        }
    ]

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "2"
    )

    application_manager.sort_applications(applications)

    output = capsys.readouterr().out

    google_position = output.index("Google")
    amazon_position = output.index("Amazon")
    microsoft_position = output.index("Microsoft")

    assert google_position < amazon_position
    assert amazon_position < microsoft_position
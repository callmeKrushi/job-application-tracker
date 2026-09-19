import application_manager


def test_add_application(monkeypatch, tmp_path):
    applications = []

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
            "location": "Hyderabad",
            "job_type": "Full-time",
            "salary": "12 LPA",
            "job_url": "https://example.com",
            "notes": "Referral",
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
            "location": "Hyderabad",
            "job_type": "Full-time",
            "salary": "12 LPA",
            "job_url": "https://example.com",
            "notes": "Referral",
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
            "location": "Hyderabad",
            "job_type": "Full-time",
            "salary": "12 LPA",
            "job_url": "https://example.com",
            "notes": "Referral",
            "status": "Applied",
            "date_applied": "2026-09-19"
        },
        {
            "company": "Microsoft",
            "role": "Data Scientist",
            "location": "Bangalore",
            "job_type": "Full-time",
            "salary": "15 LPA",
            "job_url": "https://microsoft.com/job",
            "notes": "Applied through referral",
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
            "location": "Hyderabad",
            "job_type": "Full-time",
            "salary": "12 LPA",
            "job_url": "https://example.com",
            "notes": "Referral",
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
            "location": "Hyderabad",
            "job_type": "Full-time",
            "salary": "12 LPA",
            "job_url": "https://example.com",
            "notes": "Referral",
            "status": "Applied",
            "date_applied": "2026-09-15"
        },
        {
            "company": "Microsoft",
            "role": "Data Scientist",
            "location": "Bangalore",
            "job_type": "Full-time",
            "salary": "15 LPA",
            "job_url": "https://microsoft.com/job",
            "notes": "Applied through referral",
            "status": "Interview",
            "date_applied": "2026-09-15"
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
            "location": "Hyderabad",
            "job_type": "Full-time",
            "salary": "12 LPA",
            "job_url": "https://example.com",
            "notes": "Referral",
            "status": "Applied",
            "date_applied": "2026-09-15"
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
            "location": "Hyderabad",
            "job_type": "Full-time",
            "salary": "12 LPA",
            "job_url": "https://example.com",
            "notes": "Referral",
            "status": "Applied",
            "date_applied": "2026-09-15"
        },
        {
            "company": "Microsoft",
            "role": "Data Scientist",
            "location": "Bangalore",
            "job_type": "Full-time",
            "salary": "15 LPA",
            "job_url": "https://microsoft.com/job",
            "notes": "Applied through referral",
            "status": "Interview",
            "date_applied": "2026-09-15"
        },
        {
            "company": "Amazon",
            "role": "ML Engineer",
            "location": "Hyderabad",
            "job_type": "Full-time",
            "salary": "14 LPA",
            "job_url": "https://amazon.com/job",
            "notes": "Applied online",
            "status": "Applied",
            "date_applied": "2026-09-15"
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
            "location": "Hyderabad",
            "job_type": "Full-time",
            "salary": "12 LPA",
            "job_url": "https://example.com",
            "notes": "Referral",
            "status": "Applied",
            "date_applied": "2026-09-15"
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
            "location": "Hyderabad",
            "job_type": "Full-time",
            "salary": "12 LPA",
            "job_url": "https://example.com",
            "notes": "Referral",
            "status": "Applied",
            "date_applied": "2026-09-10"
        },
        {
            "company": "Microsoft",
            "role": "Data Scientist",
            "location": "Bangalore",
            "job_type": "Full-time",
            "salary": "15 LPA",
            "job_url": "https://microsoft.com/job",
            "notes": "Applied through referral",
            "status": "Interview",
            "date_applied": "2026-09-18"
        },
        {
            "company": "Amazon",
            "role": "ML Engineer",
            "location": "Hyderabad",
            "job_type": "Full-time",
            "salary": "14 LPA",
            "job_url": "https://amazon.com/job",
            "notes": "Applied online",
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
            "location": "Hyderabad",
            "job_type": "Full-time",
            "salary": "12 LPA",
            "job_url": "https://example.com",
            "notes": "Referral",
            "status": "Applied",
            "date_applied": "2026-09-10"
        },
        {
            "company": "Microsoft",
            "role": "Data Scientist",
            "location": "Bangalore",
            "job_type": "Full-time",
            "salary": "15 LPA",
            "job_url": "https://microsoft.com/job",
            "notes": "Applied through referral",
            "status": "Interview",
            "date_applied": "2026-09-18"
        },
        {
            "company": "Amazon",
            "role": "ML Engineer",
            "location": "Hyderabad",
            "job_type": "Full-time",
            "salary": "14 LPA",
            "job_url": "https://amazon.com/job",
            "notes": "Applied online",
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



def test_edit_application(monkeypatch):
    applications = [
        {
            "company": "Google",
            "role": "Software Engineer",
            "location": "Hyderabad",
            "job_type": "Full-time",
            "salary": "12 LPA",
            "job_url": "https://example.com",
            "notes": "Referral",
            "status": "Applied",
            "date_applied": "2026-09-19"
        }
    ]

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

    monkeypatch.setattr(
        "application_manager.save_applications",
        lambda applications: None
    )

    application_manager.edit_application(applications)

    assert applications[0]["company"] == "Microsoft"
    assert applications[0]["role"] == "Data Scientist"
    assert applications[0]["location"] == "Bangalore"
    assert applications[0]["job_type"] == "Full-time"
    assert applications[0]["salary"] == "15 LPA"
    assert applications[0]["job_url"] == "https://microsoft.com/job"
    assert applications[0]["notes"] == "Referred by friend"
    assert applications[0]["status"] == "Interview"
    assert applications[0]["date_applied"] == "2026-09-19"



def test_edit_application_keep_existing_values(monkeypatch):
    applications = [
        {
            "company": "Google",
            "role": "Software Engineer",
            "location": "Hyderabad",
            "job_type": "Full-time",
            "salary": "12 LPA",
            "job_url": "https://example.com",
            "notes": "Referral",
            "status": "Applied",
            "date_applied": "2026-09-19"
        }
    ]

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

    monkeypatch.setattr(
        "application_manager.save_applications",
        lambda applications: None
    )

    application_manager.edit_application(applications)

    assert applications[0]["company"] == "Google"
    assert applications[0]["role"] == "Software Engineer"
    assert applications[0]["location"] == "Hyderabad"
    assert applications[0]["job_type"] == "Full-time"
    assert applications[0]["salary"] == "12 LPA"
    assert applications[0]["job_url"] == "https://example.com"
    assert applications[0]["notes"] == "Referral"
    assert applications[0]["status"] == "Applied"
    assert applications[0]["date_applied"] == "2026-09-19"



def test_edit_application_invalid_status(monkeypatch):
    applications = [
        {
            "company": "Google",
            "role": "Software Engineer",
            "location": "Hyderabad",
            "job_type": "Full-time",
            "salary": "12 LPA",
            "job_url": "https://example.com",
            "notes": "Referral",
            "status": "Applied",
            "date_applied": "2026-09-19"
        }
    ]

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

    monkeypatch.setattr(
        "application_manager.save_applications",
        lambda applications: None
    )

    application_manager.edit_application(applications)

    assert applications[0]["company"] == "Google"
    assert applications[0]["role"] == "Software Engineer"
    assert applications[0]["location"] == "Hyderabad"
    assert applications[0]["status"] == "Applied"
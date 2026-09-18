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
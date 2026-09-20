from storage import load_applications, save_applications


def test_save_and_load_applications(tmp_path):
    file_path = tmp_path / "applications.json"

    applications = [
        {
            "company": "Google",
            "role": "Python Developer",
            "status": "Applied"
        }
    ]

    import storage
    storage.FILE_NAME = str(file_path)

    save_applications(applications)

    loaded_applications = load_applications()

    assert loaded_applications == applications


def test_load_applications_when_file_does_not_exist(tmp_path):
    import storage

    file_path = tmp_path / "missing.json"
    storage.FILE_NAME = str(file_path)

    applications = load_applications()

    assert applications == []


def test_load_applications_when_file_is_empty(tmp_path):
    import storage

    file_path = tmp_path / "empty.json"
    file_path.write_text("")

    storage.FILE_NAME = str(file_path)

    applications = load_applications()

    assert applications == []


def test_load_applications_when_json_is_invalid(tmp_path, capsys):
    import storage

    file_path = tmp_path / "invalid.json"
    file_path.write_text('{"company": "Google"')

    storage.FILE_NAME = str(file_path)

    applications = load_applications()

    captured = capsys.readouterr()

    assert applications == []
    assert "invalid JSON" in captured.out
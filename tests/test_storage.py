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


def test_load_applications_when_json_is_not_a_list(tmp_path, capsys):
    import storage

    file_path = tmp_path / "invalid_structure.json"
    file_path.write_text('{"company": "Google"}')

    storage.FILE_NAME = str(file_path)

    applications = load_applications()

    captured = capsys.readouterr()

    assert applications == []
    assert "must be a list" in captured.out


def test_save_applications_when_file_cannot_be_written(tmp_path, capsys):
    import storage

    file_path = tmp_path / "missing_folder" / "applications.json"
    storage.FILE_NAME = str(file_path)

    save_applications([])

    captured = capsys.readouterr()

    assert "Could not save applications" in captured.out


def test_save_applications_when_data_is_not_a_list(tmp_path, capsys):
    import storage

    file_path = tmp_path / "applications.json"
    storage.FILE_NAME = str(file_path)

    save_applications({"company": "Google"})

    captured = capsys.readouterr()

    assert "must be a list" in captured.out
    assert not file_path.exists()
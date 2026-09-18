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
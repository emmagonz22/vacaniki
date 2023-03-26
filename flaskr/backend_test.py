from flaskr.backend import Backend
from unittest.mock import Mock, MagicMock, patch, create_autospec, mock_open
import pytest
from io import BytesIO
# TODO(Project 1): Write tests for Backend methods.


def test_sign_in_success():

    mock_storage = MagicMock()
    backend = Backend(mock_storage)
    #Return value of exist to True
    mock_storage.bucket.return_value.bucket.blob.return_value.blob.exists.return_value = True
    #888e54607077255491385154008887117a71e5627cca1c6df3e8c0e110eb6247196a281ed0cf335690de59467cd1ce305b9fc23639ac72eba9a106d179f2c900 is the hash of testpassword
    mock_storage.bucket.return_value.blob.return_value.open.return_value.__enter__.return_value.read.return_value = "888e54607077255491385154008887117a71e5627cca1c6df3e8c0e110eb6247196a281ed0cf335690de59467cd1ce305b9fc23639ac72eba9a106d179f2c900"

    assert backend.sign_in("testuser", "testpassword") == True


def test_sign_in_user_not_exist():

    mock_storage = MagicMock()
    backend = Backend(mock_storage)

    mock_storage.bucket.return_value.blob.return_value.exists.return_value = False
    #888e54607077255491385154008887117a71e5627cca1c6df3e8c0e110eb6247196a281ed0cf335690de59467cd1ce305b9fc23639ac72eba9a106d179f2c900 is the hash of testpassword
    mock_storage.bucket.return_value.blob.return_value.open.return_value.__enter__.return_value.read.return_value = "888e54607077255491385154008887117a71e5627cca1c6df3e8c0e110eb6247196a281ed0cf335690de59467cd1ce305b9fc23639ac72eba9a106d179f2c900"

    assert backend.sign_in("test_user", "test_password") == False


def test_sign_in_incorrect_password():
    mock_storage = MagicMock()
    backend = Backend(mock_storage)

    mock_storage.bucket.return_value.blob.return_value.exists.return_value = True
    mock_storage.bucket.return_value.bucket.blob.return_value.blob.exists.return_value = True
    #888e54607077255491385154008887117a71e5627cca1c6df3e8c0e110eb6247196a281ed0cf335690de59467cd1ce305b9fc23639ac72eba9a106d179f2c900 is the hash of testpassword
    mock_storage.bucket.return_value.blob.return_value.open.return_value.__enter__.return_value.read.return_value = "888e54607077255491385154008887117a71e5627cca1c6df3e8c0e110eb6247196a281ed0cf335690de59467cd1ce305b9fc23639ac72eba9a106d179f2c900"

    assert backend.sign_in("test_user", "test_password") == False


def test_sign_up_sucess():
    mock_storage = MagicMock()
    backend = Backend(mock_storage)

    mock_storage.bucket.return_value.blob.return_value.exists.return_value = False

    assert backend.sign_up("test_user", "test_password") == True


def test_sign_up_user_exist_failure():
    mock_storage = MagicMock()
    backend = Backend(mock_storage)

    mock_storage.bucket.return_value.blob.return_value.exists.return_value = True
    assert backend.sign_up("test_user",
                           "test_password") == False  #User already exist


def test_get_wiki_success():
    mock_storage = MagicMock()
    backend = Backend(mock_storage)

    mock_storage.bucket.return_value.blob.return_value.open.return_value.__enter__.return_value.read.return_value = "wiki_test.html"
    assert backend.get_wiki_page("wiki_test.html") == "wiki_test.html"


def test_get_wiki_failure():
    mock_storage = MagicMock()
    backend = Backend(mock_storage)

    mock_storage = MagicMock()
    backend = Backend(mock_storage)

    mock_storage.bucket.return_value.blob.return_value.open.return_value.__enter__.return_value.read.return_value = None
    assert backend.get_wiki_page("wiki_test.html") == None


def test_get_all_page_names_success():
    mock_storage = MagicMock()
    backend = Backend(mock_storage)

    class mock_blob:

        def __init__(self, name, content_type):
            self.name = name
            self.content_type = content_type

    mock_storage.list_blobs.return_value = [
        mock_blob("wiki_test.html", "text/html"),
        mock_blob("wiki_test_2.html", "text/html"),
        mock_blob("style.css", "text/css")
    ]
    assert ["wiki_test.html",
            "wiki_test_2.html"] == backend.get_all_page_names()


def test_get_all_page_names_empty():
    mock_storage = MagicMock()
    backend = Backend(mock_storage)

    class mock_blob:

        def __init__(self, name, content_type):
            self.name = name
            self.content_type = content_type

    mock_storage.list_blobs.return_value = [
        mock_blob("script1.js", "text/js"),
        mock_blob("script2.js", "text/js"),
        mock_blob("style.css", "text/css")
    ]
    assert [] == backend.get_all_page_names()


def test_upload():
    mock_storage = MagicMock()
    backend = Backend(mock_storage)

    bucket = backend.bucket_content
    blob = bucket.blob("TestBlob")
    blob.upload_from_file("content")

    assert blob.exists("TestBlob")


def test_get_image_failure():
    # Create a mock GCS bucket and blob
    storage_client = MagicMock()
    # Create an instance of the class with the mock storage
    backend = Backend(storage_client)
    blob_mock = MagicMock()
    blob_mock.download_as_bytes.return_value = b"Image not Found"
    backend.bucket_content.get_blob.return_value = blob_mock
    blob_mock.exists.return_value = True

    # Call the get_image method with a mock blob name and BytesIO class
    result = backend.get_image("mock_blob_name", bytes_io=BytesIO)
    # Verify that the result is a bytes_io object containing the mock image data
    assert isinstance(result, BytesIO)

    # Verify that the byte content of the returned BytesIO object matches the expected byte content
    assert result.getvalue() == b"Image not Found"


def test_get_image_success():
    # Create a mock GCS bucket and blob
    storage_client = MagicMock()
    # Create an instance of the class with the mock storage
    backend = Backend(storage_client)
    blob_mock = MagicMock()
    blob_mock.download_as_bytes.return_value = b"image_data"
    backend.bucket_content.get_blob.return_value = blob_mock
    blob_mock.exists.return_value = True

    # Call the get_image method with a mock blob name and BytesIO class
    result = backend.get_image("mock_blob_name", bytes_io=BytesIO)
    # Verify that the result is a bytes_io object containing the mock image data
    assert isinstance(result, BytesIO)

    # Verify that the byte content of the returned BytesIO object matches the expected byte content
    assert result.getvalue() == b"image_data"

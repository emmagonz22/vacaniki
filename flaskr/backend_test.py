from flaskr.backend import Backend
from unittest.mock import MagicMock, patch, create_autospec, mock_open
import pytest
# TODO(Project 1): Write tests for Backend methods.

#@patch("flaskr.backend.open", new_callable=mock_open, read_data="testpassword")
def test_sign_in_success():
   
    mock_storage = MagicMock()
    backend = Backend(mock_storage)
    #Return value of exist to True
    mock_storage.bucket.return_value.bucket.blob.return_value.blob.exists.return_value = True
    #888e54607077255491385154008887117a71e5627cca1c6df3e8c0e110eb6247196a281ed0cf335690de59467cd1ce305b9fc23639ac72eba9a106d179f2c900 is the hash of testpassword
    mock_storage.bucket.return_value.blob.return_value.open.return_value.__enter__.return_value.read.return_value = "888e54607077255491385154008887117a71e5627cca1c6df3e8c0e110eb6247196a281ed0cf335690de59467cd1ce305b9fc23639ac72eba9a106d179f2c900"

    assert backend.sign_in("testuser","testpassword") == True

        

def test_sign_in_user_not_exist():

    mock_storage = MagicMock()
    backend = Backend(mock_storage)
 
    mock_storage.bucket.return_value.blob.return_value.exists.return_value = False
    #888e54607077255491385154008887117a71e5627cca1c6df3e8c0e110eb6247196a281ed0cf335690de59467cd1ce305b9fc23639ac72eba9a106d179f2c900 is the hash of testpassword
    mock_storage.bucket.return_value.blob.return_value.open.return_value.__enter__.return_value.read.return_value = "888e54607077255491385154008887117a71e5627cca1c6df3e8c0e110eb6247196a281ed0cf335690de59467cd1ce305b9fc23639ac72eba9a106d179f2c900"

    assert backend.sign_in("test_user","test_password") == False

def test_sign_in_incorrect_password():
    mock_storage = MagicMock()
    backend = Backend(mock_storage)
  
    mock_storage.bucket.return_value.blob.return_value.exists.return_value = True
    mock_storage.bucket.return_value.bucket.blob.return_value.blob.exists.return_value = True
    #888e54607077255491385154008887117a71e5627cca1c6df3e8c0e110eb6247196a281ed0cf335690de59467cd1ce305b9fc23639ac72eba9a106d179f2c900 is the hash of testpassword
    mock_storage.bucket.return_value.blob.return_value.open.return_value.__enter__.return_value.read.return_value = "888e54607077255491385154008887117a71e5627cca1c6df3e8c0e110eb6247196a281ed0cf335690de59467cd1ce305b9fc23639ac72eba9a106d179f2c900"

    assert backend.sign_in("test_user","test_password") == False


def test_sign_up_sucess():
    mock_storage = MagicMock()
    backend = Backend(mock_storage)
 
    mock_storage.bucket.return_value.blob.return_value.exists.return_value = False

    assert backend.sign_up("test_user","test_password") == True

def test_sign_up_user_exist_failure():
    mock_storage = MagicMock()
    backend = Backend(mock_storage)
    
    mock_storage.bucket.return_value.blob.return_value.exists.return_value = True
    assert backend.sign_up("test_user","test_password") == False  #User already exist

def test_get_wiki_success():
    mock_storage = MagicMock()
    backend = Backend(mock_storage)
    
    mock_storage.bucket.return_value.blob.return_value.exists.return_value = True
    mock_storage.bucket.return_value.blob.return_value.download_to_filename.return_value = "File Downloaded"

    assert backend.get_wiki_page("wiki_test.html")[3] == "wiki_test.html"

def test_get_wiki_failure():
    mock_storage = MagicMock()
    backend = Backend(mock_storage)
    
    mock_storage.bucket.return_value.blob.return_value.exists.return_value = False
    mock_storage.bucket.return_value.blob.return_value.download_to_filename.return_value = "File Downloaded"

    assert backend.get_wiki_page("wiki_test.html") is None

def test_get_all_page_names_success():
    mock_storage = MagicMock()
    backend = Backend(mock_storage)
    class blob:
        def __init__(self, name, content_type):
            self.name = name
            self.content_type = content_type
    mock_storage.list_blobs.return_value = [blob("wiki_test.html", "text/html"), blob("wiki_test_2.html", "text/html"), blob("style.css", "text/css")]
    return ["wiki_test.html", "wiki_test_2.html"] == backend.get_all_page_names()

def test_get_all_page_names_empty():
    mock_storage = MagicMock()
    backend = Backend(mock_storage)
    class blob:
        def __init__(self, name, content_type):
            self.name = name
            self.content_type = content_type
    mock_storage.list_blobs.return_value = [blob("script1.js", "text/js"), blob("script2.js", "text/js"), blob("style.css", "text/css")]
    return [] == backend.get_all_page_names()

"""
@patch("flaskr.backend.storage.Client")
def test_upload(client):

    # assert bucket was called with the passed string
    bucket = client().get_bucket
    bucket.assert_called_with("wikiviewer-content")

    # assert blob and upload were called with expected params
    blob = bucket().blob
    blob.assert_called_with("report")
    blob().upload_from_string.assert_called_with("")
"""
def get_image_success():
    pass

def get_image_failure():

    assert None


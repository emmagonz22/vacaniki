from flaskr import create_app
from io import BytesIO


import pytest
from unittest.mock import patch

# See https://flask.palletsprojects.com/en/2.2.x/testing/ 
# for more info on testing
@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# TODO(Checkpoint (groups of 4 only) Requirement 4): Change test to
# match the changes made in the other Checkpoint Requirements.
def test_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Hello, World!\n" in resp.data

def test_homepage(client):
   resp = client.get("/")
   assert resp.status_code == 200
   assert b"Vacationiki - One stop shop for the greatest vacation sites!\n" in resp.data
 
def test_about_page(client):
   resp = client.get("/about")
   assert resp.status_code == 200
   assert b"About This Wiki\n" in resp.data
 
def test_all_pages(client):
   with patch("flaskr.backend.Backend.get_all_page_names", return_value=["Canada.txt", "California.txt"]):
       resp = client.get("/pages")
       assert resp.status_code == 200
       assert b"Vactionwiki Pages\n" in resp.data
 
@patch("flaskr.backend.Backend.get_wiki_page", return_value=b"test.")
def test_get_page(mock_get_wiki_page, client):
   name = "california"
   resp = client.get("/pages/california")
   assert resp.status_code == 200
   assert b"test." in resp.data
   mock_get_wiki_page.assert_called_once_with(name)
 
@patch("flaskr.backend.Backend.get_image", return_value=BytesIO())
def test_get_image(mock_get_image, client):
   image_name = "img"
   resp = client.get("/images/img")
   assert resp.status_code == 200
   mock_get_image.assert_called_once_with(image_name)

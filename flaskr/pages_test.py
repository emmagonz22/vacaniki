from flaskr import create_app

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

def test_signup_page(client):
    with patch('flaskr.backend.Backend.sign_up') as mock_sign_up:
        # Successful signup
        mock_sign_up.return_value = True
        data = {'username': 'Cesar', 'password': '123'}
        resp = client.post("/signup/", data=data, follow_redirects=True)
        assert resp.status_code == 200
        assert b'Signed up successfully!' in resp.data

        # Unsuccessful signup
        mock_sign_up.return_value = False
        data = {'username': 'Cesar', 'password': '123'}
        resp = client.post("/signup/", data=data, follow_redirects=True)
        assert resp.status_code == 200
        assert b'Account already exist!' in resp.data

def test_login_page(client):
    with patch('flaskr.backend.Backend.sign_in') as mock_login:
        # Successful Login
        mock_login.return_value = True
        data = {'username': 'cooldude2006', 'password': '12345'}
        resp = client.post("/login/", data=data, follow_redirects=True)
        assert resp.status_code == 200
        assert b'Logged in successfully.' in resp.data

        # Unsuccessful Login 
        mock_login.return_value = False
        data = {'username': 'cooldude2006', 'password': '12345'}
        resp = client.post("/login/", data=data, follow_redirects=True)
        assert resp.status_code == 200
        assert b'Wrong username or password. Please Try Again.' in resp.data

def test_logout(client):
    with patch('flask_login.current_user', create=True) as mock_user:
        mock_user.is_authenticated = True
        resp = client.get("/logout/", follow_redirects=True)
        assert resp.status_code == 200
        assert b'Logged out' in resp.data

def test_upload(client):
    with patch('flaskr.backend.Backend.upload'):
        # No File Input
        data = {'wikiname': '', 'filename': ''}
        resp = client.post("/upload/", data=data, follow_redirects=True)
        assert resp.status_code == 200
        assert b'No File Input' in resp.data

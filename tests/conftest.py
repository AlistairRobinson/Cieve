import os
import pytest
from flaskr import create_app

# This is the test config. It contains the application definition as well as class definitions for each individual test.

# Defines the testing application
@pytest.fixture 
def app():

    app = create_app({
        'TESTING': True
    })

    yield app

# Allows the creation of a test client
@pytest.fixture
def client(app):
    return app.test_client()

# Allows the creation of a test client runner
@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# Encapsulates functions used to test authentication
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login_cli(self, username='test', password='test'):
        return self._client.post(
            '/auth/cli/login',
            data={'username': username, 'password': password}
        )

    def login_apl(self, username='test', password='test'):
        return self._client.post(
            '/auth/apl/login',
            data={'username': username, 'password': password}
        )

    def register(self, username='test', password='test'):
        return self._client.post(
            '/auth/apl/register',
            data={'username': username, 'password': password}
        ) 

    def logout(self):
        return self._client.get('/auth/logout')

# Returns an authentication test object
@pytest.fixture
def auth(client):
    return AuthActions(client)
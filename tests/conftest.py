import os
import pytest
from flaskr import create_app

@pytest.fixture
def app():

    app = create_app({
        'TESTING': True
    })

    yield app

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

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


@pytest.fixture
def auth(client):
    return AuthActions(client)
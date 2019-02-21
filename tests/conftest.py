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
            '/cli/auth/login',
            data={'username': username, 'password': password}
        )

    def login_apl(self, username='test', password='test'):
        return self._client.post(
            'apl/auth/login',
            data={'username': username, 'password': password}
        )

    def register(self, username='test', password='test'):
        return self._client.post(
            'apl/auth/register',
            data={'username': username, 'password': password}
        ) 

    def logout(self):
        return self._client.get('/auth/logout')

# Returns an authentication test object
@pytest.fixture
def auth(client):
    return AuthActions(client)

# Encapsulates functions used to test jobs and applications
class JobActions(object):
    def __init__(self, client):
        self._client = client

    def post_vacancy(self, data):
        return self._client.post(
            'path/to/post/vacancy', # TODO
            data
        )
    
    def apply_to_vacancy(self, data):
        return self._client.post(
            'path/to/vacancy/application', # TODO
            data
        )

    def retrieve_application(self, data):
        return self._client.post(
            'path/to/application/retrival', # TODO
            data
        )

    def get_vacancies(self, data):
        return self._client.post(
            'path/to/vacancy/retrival', # TODO
            data
        )

# Returns a job test object
@pytest.fixture
def jobs(client):
    return JobActions(client)